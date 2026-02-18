# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an early-stage Python data analysis project exploring 10-K financial data for Apple, Microsoft, and Tesla. The goal is to build chatbot-like query capabilities over financial statement data.

## Running the Project

Open `Untitled-1.ipynb` in Jupyter Notebook or JupyterLab:

```bash
jupyter notebook Untitled-1.ipynb
# or
jupyter lab
```

There is no package manager file yet. Install dependencies manually:

```bash
pip install pandas jupyter
```

## Data

`Data/10-K_Extract__MSFT_TSLA_AAPL_.csv` contains annual 10-K financial data for AAPL, MSFT, and TSLA with columns: `Company`, `Fiscal Year`, `Total Revenue`, `Net Income`, `Total Assets`, `Total Liabilities`, `CFO`. Note that `Total Assets` and `Total Liabilities` are missing for the oldest year of each company (2022 for Apple/Tesla, 2023 for Microsoft).

## Current State

The notebook (`Untitled-1.ipynb`) currently only imports pandas. The chatbot/analysis logic has not yet been implemented.
