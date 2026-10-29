"""Lab 17: public FRED/ALFRED downloads, with no API key."""
from datetime import date, datetime, timezone
from io import StringIO
import re
import subprocess
from urllib.parse import urlencode

import pandas as pd
import streamlit as st


SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}


def validate_id(series_id):
    series_id = series_id.strip().upper()
    if not re.fullmatch(r"[A-Z0-9_]+", series_id):
        raise ValueError("Enter a FRED series ID using letters, numbers or underscores.")
    return series_id


def read_csv_url(url):
    """One HTTP request; retain missing observations as NaN, never zero."""
    response = subprocess.run(
        ["curl", "-L", "--fail", "--silent", "--show-error", "--max-time", "30", url],
        capture_output=True, timeout=35, check=False,
    )
    if response.returncode:
        raise ValueError(response.stderr.decode("utf-8", errors="replace").strip())
    raw = response.stdout.decode("utf-8-sig")
    frame = pd.read_csv(StringIO(raw), na_values=["."])
    if len(frame.columns) != 2 or frame.columns[0].lower() not in ("date", "observation_date"):
        raise ValueError("The server did not return the expected two-column FRED CSV.")
    frame.columns = ["Date", "Value"]  # ALFRED's value heading includes its vintage.
    frame["Date"] = pd.to_datetime(frame["Date"], errors="raise")
    frame["Value"] = pd.to_numeric(frame["Value"], errors="raise")
    if frame["Date"].duplicated().any():
        raise ValueError("Duplicate observation dates in source data.")
    frame = frame.set_index("Date").sort_index()
    frame.attrs = {"url": url, "downloaded_utc": datetime.now(timezone.utc).isoformat(), "raw_csv": raw}
    return frame


@st.cache_data(ttl=3600, show_spinner=False)
def download_current(series_id, download_day):
    """download_day participates in the cache key, so yesterday is not today."""
    series_id = validate_id(series_id)
    return read_csv_url("https://fred.stlouisfed.org/graph/fredgraph.csv?" + urlencode({"id": series_id}))


@st.cache_data(ttl=3600, show_spinner=False)
def download_vintage(series_id, as_of, download_day):
    """Ask ALFRED for its historical snapshot, not today's data cut by date."""
    series_id = validate_id(series_id)
    as_of = date.fromisoformat(str(as_of))
    if as_of > download_day:
        raise ValueError("The as-known date cannot be in the future.")
    params = {"id": series_id, "vintage_date": as_of.isoformat()}
    url = "https://alfred.stlouisfed.org/graph/alfredgraph.csv?" + urlencode(params)
    frame = read_csv_url(url)
    return frame.loc[frame.index <= pd.Timestamp(as_of)].copy()


def compare_series(series_id, current, vintage):
    """Counts use all downloaded history; chart start does not change the audit."""
    now = current["Value"].dropna()
    then = vintage["Value"].dropna()
    common = pd.concat([then.rename("Then"), now.rename("Now")], axis=1).dropna()
    revised = int(((common["Then"] - common["Now"]).abs() > 1e-9).sum())
    last_then = then.index[-1] if len(then) else None
    last_now = now.index[-1] if len(now) else None
    return {
        "Series": f"https://fred.stlouisfed.org/series/{series_id}",
        "Last measured — as known": last_then.strftime("%Y-%m-%d") if last_then is not None else None,
        "Value — as known": float(then.iloc[-1]) if len(then) else None,
        "Last measured — today": last_now.strftime("%Y-%m-%d") if last_now is not None else None,
        "Value — today": float(now.iloc[-1]) if len(now) else None,
        "Later observations": int((now.index > last_then).sum()) if last_then is not None else None,
        "Revised observations": revised,
    }


def main():
    st.set_page_config(page_title="Point-in-Time Rates Audit", layout="wide")
    today = date.today()
    st.title("Point-in-Time Rates Audit")
    st.caption(
        f"Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today ({today}); "
        "built with AI help, a learning demonstration, not investment advice."
    )
    selected = st.sidebar.multiselect("Series", list(SERIES), default=list(SERIES),
                                     format_func=lambda key: f"{key} — {SERIES[key]}")
    extra = st.sidebar.text_input("Add another FRED series ID", placeholder="CPIAUCSL or PAYEMS")
    start = st.sidebar.date_input("Start date", date(2020, 1, 1), min_value=date(1776, 1, 1), max_value=today)
    as_of = st.sidebar.date_input("As known on", today, min_value=date(1776, 1, 1), max_value=today)
    if extra.strip():
        selected = list(dict.fromkeys(selected + [extra.strip().upper()]))
    st.sidebar.caption("The start date controls charts only. Audit counts use the full downloaded history.")
    rows = []
    for series_id in selected:
        st.subheader(f"{series_id} — {SERIES.get(series_id, 'Additional series')}")
        try:
            current = download_current(series_id, today)
            vintage = download_vintage(series_id, as_of, today)
            row = compare_series(series_id, current, vintage)
            rows.append(row)
            chart = current.loc[current.index >= pd.Timestamp(start)]
            if chart["Value"].notna().any():
                st.line_chart(chart, y="Value", x_label="Observation date", y_label="Source units")
            else:
                st.info("No current observations in the selected chart window.")
            last = row["Last measured — as known"] or "No nonmissing observations available"
            st.caption(f"Last date measured in the data known on {as_of}: {last}")
            if row["Last measured — as known"] is None:
                st.info("ALFRED returned no usable observations for this vintage; no current-data fallback was used.")
            with st.expander("Sources and download timestamps"):
                st.markdown(f"[FRED page](https://fred.stlouisfed.org/series/{series_id}) · "
                            f"[Current CSV]({current.attrs['url']}) · [Vintage CSV]({vintage.attrs['url']})")
                st.write({"Current download (UTC)": current.attrs["downloaded_utc"],
                          "Vintage download (UTC)": vintage.attrs["downloaded_utc"]})
        except Exception as exc:
            st.error(f"{series_id}: {type(exc).__name__}: {exc}")
    st.subheader("As-known comparison")
    if rows:
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch", column_config={
            "Series": st.column_config.LinkColumn("Series", display_text=r"https://fred\.stlouisfed\.org/series/(.*)"),
        })
        st.caption("Dates identify periods measured, not publication dates. Monthly observations are labeled "
                   "by the first day of the month. Later = nonmissing current observations after the last "
                   "known observation. Revised = differing nonmissing values on shared dates (tolerance 1e-9). "
                   "Source units vary: the default rates are percent; PAYEMS is thousands; CPIAUCSL is an index.")
    elif not selected:
        st.info("Select a series or enter a FRED series ID.")


if __name__ == "__main__":
    main()
