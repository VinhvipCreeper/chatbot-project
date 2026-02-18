# Financial Analysis Chatbot

A Python chatbot that answers predefined financial queries about Apple, Microsoft, and Tesla using data extracted from their 10-K SEC filings.

---

## Overview

This project was built in two parts:

1. **Data Analysis** (`Untitled-1.ipynb`) — loads 10-K financial data and computes year-over-year growth for revenue, net income, total assets, total liabilities, and cash flow from operations across three fiscal years per company.

2. **Chatbot** (`chatbot.py`) — a command-line chatbot that answers five types of financial queries using the same dataset.

---

## Setup

**Requirements:** Python 3.8+

Install the only dependency:

```bash
pip install pandas
```

---

## Running the Chatbot

> **To start the chatbot, open `running_chatbot.py`.**

```bash
python running_chatbot.py
```

This will automatically open a new terminal window with the chatbot ready to use. You do not need to open a terminal manually.

Once the terminal opens, you will see:

```
=======================================================
  Financial Analysis Chatbot
  Data: Apple, Microsoft, Tesla  |  10-K Filings
=======================================================
Type 'help' to list queries, or 'quit' to exit.

You:
```

Type your question and press Enter. Type `help` to see all supported queries, or `quit` to exit.

---

## Supported Queries

The chatbot recognises five query types. You can use any casing and refer to companies by name or ticker symbol (`AAPL`, `MSFT`, `TSLA`).

### 1. Total Revenue
> What is the total revenue for **[Company]**?

```
You: What is the total revenue for Apple?
Bot: Apple's total revenue in FY2024 was $391,035M.
```

### 2. Net Income Change
> How has net income changed for **[Company]**?

```
You: How has net income changed for Tesla?
Bot: Tesla's net income decreased by $7,845M (52.3%) from FY2023 to FY2024.
```

### 3. Highest Revenue Company
> Which company has the highest revenue?

```
You: Which company has the highest revenue?
Bot: Apple has the highest revenue at $391,035M in FY2024.
```

### 4. Cash Flow from Operations
> What is the cash flow from operations for **[Company]**?

```
You: What is the cash flow from operations for Microsoft?
Bot: Microsoft's cash flow from operations in FY2025 was $136,162M.
```

### 5. Total Assets
> What are the total assets for **[Company]**?

```
You: What are the total assets for Tesla?
Bot: Tesla's total assets in FY2024 were $122,070M.
```

---

## Query Tips

- **Case-insensitive:** `APPLE`, `apple`, and `Apple` all work.
- **Ticker symbols:** `AAPL`, `MSFT`, and `TSLA` are recognised.
- **Partial phrasing:** `"of"` and `"for"` are both fine — the chatbot matches on keywords, not exact phrasing.
- **Unknown queries** return a friendly fallback with suggestions rather than an error.

---

## Running the Tests

```bash
python test_chatbot.py       # no external dependencies needed
# or
python -m pytest test_chatbot.py -v
```

Expected output:

```
  PASS  TestTotalRevenue.test_apple_revenue_handled
  PASS  TestTotalRevenue.test_microsoft_revenue_handled
  ...
Results: 30 passed, 0 failed
```

The test suite covers all five query types, fallback behaviour, case-insensitive matching, ticker aliases, and that no exception is ever raised for unexpected input.

---

## Data

`Data/10-K_Extract__MSFT_TSLA_AAPL_.csv` — manually extracted from SEC EDGAR 10-K filings.

| Column | Description |
|---|---|
| Company | Apple, Microsoft, or Tesla |
| Fiscal Year | FY2022–FY2025 (varies by company) |
| Total Revenue | Annual revenue in $M |
| Net Income | Annual net income in $M |
| Total Assets | Total assets in $M |
| Total Liabilities | Total liabilities in $M |
| CFO | Cash flow from operations in $M |

> Note: Total Assets and Total Liabilities are missing for the oldest year of each company (2022 for Apple/Tesla, 2023 for Microsoft).

---

## CI

Every push to `main` triggers a GitHub Actions workflow (`.github/workflows/test.yml`) that installs dependencies and runs the full test suite on Python 3.11.

[![Run Chatbot Tests](https://github.com/VinhvipCreeper/chatbot-project/actions/workflows/test.yml/badge.svg)](https://github.com/VinhvipCreeper/chatbot-project/actions/workflows/test.yml)

---

## Project Structure

```
chatbot-project/
├── Data/
│   └── 10-K_Extract__MSFT_TSLA_AAPL_.csv
├── .github/
│   └── workflows/
│       └── test.yml
├── chatbot.py          # Chatbot logic and CLI
├── running_chatbot.py  # Opens a new terminal and launches the chatbot
├── test_chatbot.py     # 30-test suite
├── Untitled-1.ipynb    # Data analysis notebook
└── README.md
```
