"""
Financial Analysis Chatbot
--------------------------
Answers predefined queries about Apple, Microsoft, and Tesla
using 10-K financial data loaded from the CSV in the Data/ folder.

Usage (CLI):
    python chatbot.py

Usage (programmatic):
    from chatbot import simple_chatbot
    print(simple_chatbot("What is the total revenue for Apple?"))
"""

import pandas as pd

# ── Load and prepare data ─────────────────────────────────────────────────────

df = pd.read_csv("Data/10-K_Extract__MSFT_TSLA_AAPL_.csv")
df = df.sort_values(["Company", "Fiscal Year"]).reset_index(drop=True)

# ── Constants ─────────────────────────────────────────────────────────────────

# Maps lowercase keywords → canonical company name
COMPANY_ALIASES = {
    "apple": "Apple",     "aapl": "Apple",
    "microsoft": "Microsoft", "msft": "Microsoft",
    "tesla": "Tesla",     "tsla": "Tesla",
}

PREDEFINED_QUERIES = [
    "What is the total revenue for Apple?",
    "What is the total revenue for Microsoft?",
    "What is the total revenue for Tesla?",
    "How has net income changed for Apple?",
    "How has net income changed for Microsoft?",
    "How has net income changed for Tesla?",
    "Which company has the highest revenue?",
    "What is the cash flow from operations for Apple?",
    "What is the cash flow from operations for Microsoft?",
    "What is the cash flow from operations for Tesla?",
    "What are the total assets for Apple?",
    "What are the total assets for Microsoft?",
    "What are the total assets for Tesla?",
]

FALLBACK = (
    "Sorry, I can only respond to predefined queries. Try asking:\n"
    "  - 'What is the total revenue for Apple?'\n"
    "  - 'How has net income changed for Microsoft?'\n"
    "  - 'Which company has the highest revenue?'\n"
    "  - 'What is the cash flow from operations for Tesla?'\n"
    "  - 'What are the total assets for Apple?'"
)

# ── Internal helpers ──────────────────────────────────────────────────────────

def _latest_row(company: str):
    """Return the most recent row for a company."""
    return (
        df[df["Company"] == company]
        .sort_values("Fiscal Year")
        .iloc[-1]
    )

def _prev_row(company: str):
    """Return the second-most-recent row for a company."""
    return (
        df[df["Company"] == company]
        .sort_values("Fiscal Year")
        .iloc[-2]
    )

def _detect_company(query_lower: str):
    """Return the canonical company name found in the query, or None."""
    for alias, name in COMPANY_ALIASES.items():
        if alias in query_lower:
            return name
    return None

# ── Core chatbot function ─────────────────────────────────────────────────────

def simple_chatbot(user_query: str) -> str:
    """
    Match *user_query* against predefined financial query patterns and return
    a data-driven response.  Returns a fallback message for unrecognised input.
    """
    if not user_query or not user_query.strip():
        return FALLBACK

    q = user_query.lower().strip()
    company = _detect_company(q)

    # ── R1a: Total revenue ────────────────────────────────────────────────────
    if "revenue" in q and "highest" not in q and company:
        row = _latest_row(company)
        return (
            f"{company}'s total revenue in FY{int(row['Fiscal Year'])} "
            f"was ${row['Total Revenue']:,.0f}M."
        )

    # ── R1b: Net income change ────────────────────────────────────────────────
    if "net income" in q and company:
        latest = _latest_row(company)
        prev    = _prev_row(company)
        change  = latest["Net Income"] - prev["Net Income"]
        pct     = (change / prev["Net Income"]) * 100
        direction = "increased" if change >= 0 else "decreased"
        return (
            f"{company}'s net income {direction} by ${abs(change):,.0f}M "
            f"({abs(pct):.1f}%) from FY{int(prev['Fiscal Year'])} "
            f"to FY{int(latest['Fiscal Year'])}."
        )

    # ── R1c: Highest revenue across companies ─────────────────────────────────
    if "highest" in q and "revenue" in q:
        latest_each = (
            df.sort_values("Fiscal Year")
            .groupby("Company")
            .last()
            .reset_index()
        )
        top = latest_each.loc[latest_each["Total Revenue"].idxmax()]
        return (
            f"{top['Company']} has the highest revenue at "
            f"${top['Total Revenue']:,.0f}M in FY{int(top['Fiscal Year'])}."
        )

    # ── R1d: Cash flow from operations ────────────────────────────────────────
    if ("cash flow" in q or "cfo" in q or "operating" in q) and company:
        row = _latest_row(company)
        return (
            f"{company}'s cash flow from operations in FY{int(row['Fiscal Year'])} "
            f"was ${row['CFO']:,.0f}M."
        )

    # ── R1e: Total assets ─────────────────────────────────────────────────────
    if "assets" in q and company:
        row = _latest_row(company)
        if pd.isna(row["Total Assets"]):
            return (
                f"Total assets data for {company} in "
                f"FY{int(row['Fiscal Year'])} is not available."
            )
        return (
            f"{company}'s total assets in FY{int(row['Fiscal Year'])} "
            f"were ${row['Total Assets']:,.0f}M."
        )

    return FALLBACK

# ── CLI entry point ───────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  Financial Analysis Chatbot")
    print("  Data: Apple, Microsoft, Tesla  |  10-K Filings")
    print("=" * 55)
    print("Type 'help' to list queries, or 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if user_input.lower() == "help":
            print("\nSupported queries:")
            for query in PREDEFINED_QUERIES:
                print(f"  - {query}")
            print()
            continue

        print(f"Bot: {simple_chatbot(user_input)}\n")


if __name__ == "__main__":
    main()
