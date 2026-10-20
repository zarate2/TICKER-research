# Lab 14 — Submission Guide

Start with [Submission.md](Submission.md). It contains the written lab response, results, verification summary, diversification calculation, reflection draft, fund choices and price sources.

## What to deliver

The assignment requests GitHub links to the Markdown, Python and any supporting files. Upload the **whole Lab 14 folder**, preserving its layout, then use these main links for checkout:

| File | What it delivers |
|---|---|
| [Submission.md](Submission.md) | Main written submission, including Thursday's fund preparation |
| [portfolio.py](portfolio.py) | Required standalone risk engine and three baseline portfolios |
| [mandate.py](mandate.py) | Lab 13 checker extended with benchmark candidate E |
| [prices.csv](prices.csv) | Five years of monthly adjusted prices for BIL, IEF, LQD and VT |
| [outputs/Verification.txt](outputs/Verification.txt) | Evidence of known-answer checks, bad-correlation rejection, candidate E and price validation |

`portfolio.py`, `mandate.py` and `prices.csv` keep the exact names requested by the assignment. This guide is for navigating and uploading the work; the written answers are in Submission.md.

## Run the lab

Open a terminal in `Lab 14` and run:

```sh
python3 portfolio.py
python3 mandate.py
python3 support/check_results.py
```

The first two commands print the portfolio results and mandate verdicts. The third runs eight tests, performs the required correlation changes in temporary copies, checks the saved price data, and refreshes the files in `outputs/`. These commands use only Python's standard library and do not require internet access.

To download the same historical price window again:

```sh
python3 support/fetch_prices.py
python3 support/check_results.py
```

Downloading requires internet access and replaces `prices.csv` and the price-source records. Yahoo may revise historical adjustments. The saved window is September 2021–September 2026: 61 price levels supporting 60 monthly returns.

## Folder layout

```text
Lab 14/
  README.md                 Submission guide
  Submission.md             Main written deliverable
  portfolio.py              Required risk engine
  mandate.py                Required mandate checker
  prices.csv                Required historical prices
  outputs/                  Saved results and verification
    Portfolio.txt
    Mandate.txt
    Results.json
    Verification.txt
  support/                  Rerun, test and download scripts
    check_results.py
    test_portfolio.py
    fetch_prices.py
  sources/                  Assignment and retained price evidence
    Assignment.md
    Prices.json
    yahoo/                  Original responses for the four funds
```

## Before checkout

- Answer the personal code quiz in Submission.md.
- Complete the no-AI code explanation and partner swap, then record the actual exchange.
- Review the reflection draft and discuss your reasoning with your partner.
- Upload the folder to your course GitHub repository and paste the individual file links into checkout.

The calculations and local verification are complete. Personal participation and GitHub submission remain pending. ELV is retained as the company reference; this lab's required portfolios and price dataset use funds.
