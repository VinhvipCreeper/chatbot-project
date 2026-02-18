"""
Tests for simple_chatbot() in chatbot.py.

Run with:  python -m pytest test_chatbot.py -v
           python test_chatbot.py          (no pytest required)

Requirements tested
-------------------
R1  Five predefined query types are handled:
      R1a  Total revenue query (per company)
      R1b  Net income change query (per company)
      R1c  Highest-revenue company query
      R1d  Cash flow from operations query (per company)
      R1e  Total assets query (per company)
R2  Responses contain real data values (not template placeholders).
R3  Unknown / off-topic queries return a fallback message, not an error.
R4  Matching is case-insensitive (user may type in any casing).
R5  All three companies (Apple, Microsoft, Tesla) are supported.
R6  Responses mention the company name that was asked about.
R7  Responses contain a dollar amount (numeric data).
"""

import sys
import re

# ── import the module under test ──────────────────────────────────────────────
try:
    from chatbot import simple_chatbot
except ImportError:
    print("ERROR: chatbot.py not found. Implement it first, then re-run tests.")
    sys.exit(1)


# ── helpers ───────────────────────────────────────────────────────────────────

def has_number(text: str) -> bool:
    """Return True if text contains at least one digit sequence."""
    return bool(re.search(r"\d+", text))


def is_fallback(text: str) -> bool:
    """Return True if the response looks like the fallback / 'I don't know' reply."""
    fallback_markers = ["sorry", "only", "predefined", "cannot", "can't", "don't know"]
    lower = text.lower()
    return any(m in lower for m in fallback_markers)


# ── R1a: Total Revenue ────────────────────────────────────────────────────────

class TestTotalRevenue:
    QUERIES = {
        "Apple":     "What is the total revenue for Apple?",
        "Microsoft": "What is the total revenue for Microsoft?",
        "Tesla":     "What is the total revenue for Tesla?",
    }

    def test_apple_revenue_handled(self):
        resp = simple_chatbot(self.QUERIES["Apple"])
        assert not is_fallback(resp), f"Fallback returned for Apple revenue: {resp}"

    def test_microsoft_revenue_handled(self):
        resp = simple_chatbot(self.QUERIES["Microsoft"])
        assert not is_fallback(resp), f"Fallback returned for Microsoft revenue: {resp}"

    def test_tesla_revenue_handled(self):
        resp = simple_chatbot(self.QUERIES["Tesla"])
        assert not is_fallback(resp), f"Fallback returned for Tesla revenue: {resp}"

    def test_response_contains_number(self):
        for company, q in self.QUERIES.items():
            resp = simple_chatbot(q)
            assert has_number(resp), f"No numeric value in {company} revenue response: {resp}"

    def test_response_mentions_company(self):
        for company, q in self.QUERIES.items():
            resp = simple_chatbot(q)
            assert company.lower() in resp.lower(), \
                f"Company name '{company}' missing from response: {resp}"


# ── R1b: Net Income Change ────────────────────────────────────────────────────

class TestNetIncomeChange:
    QUERIES = {
        "Apple":     "How has net income changed for Apple?",
        "Microsoft": "How has net income changed for Microsoft?",
        "Tesla":     "How has net income changed for Tesla?",
    }

    def test_apple_net_income_change_handled(self):
        resp = simple_chatbot(self.QUERIES["Apple"])
        assert not is_fallback(resp), f"Fallback for Apple net income: {resp}"

    def test_microsoft_net_income_change_handled(self):
        resp = simple_chatbot(self.QUERIES["Microsoft"])
        assert not is_fallback(resp), f"Fallback for Microsoft net income: {resp}"

    def test_tesla_net_income_change_handled(self):
        resp = simple_chatbot(self.QUERIES["Tesla"])
        assert not is_fallback(resp), f"Fallback for Tesla net income: {resp}"

    def test_response_indicates_direction(self):
        """Response must say 'increased' or 'decreased' (or equivalent)."""
        direction_words = {"increased", "decreased", "grew", "fell", "dropped", "rose", "up", "down"}
        for company, q in self.QUERIES.items():
            resp = simple_chatbot(q)
            words = set(resp.lower().split())
            assert words & direction_words, \
                f"No direction word in {company} net income response: {resp}"

    def test_response_contains_number(self):
        for company, q in self.QUERIES.items():
            resp = simple_chatbot(q)
            assert has_number(resp), f"No numeric value in {company} net income response: {resp}"


# ── R1c: Highest Revenue Company ──────────────────────────────────────────────

class TestHighestRevenue:
    QUERY = "Which company has the highest revenue?"

    def test_highest_revenue_handled(self):
        resp = simple_chatbot(self.QUERY)
        assert not is_fallback(resp), f"Fallback for highest revenue query: {resp}"

    def test_response_contains_company_name(self):
        resp = simple_chatbot(self.QUERY)
        companies = {"apple", "microsoft", "tesla"}
        assert any(c in resp.lower() for c in companies), \
            f"No company name in highest-revenue response: {resp}"

    def test_response_contains_number(self):
        resp = simple_chatbot(self.QUERY)
        assert has_number(resp), f"No numeric value in highest-revenue response: {resp}"

    def test_correct_winner(self):
        """Apple has the highest latest-year revenue ($391,035M in FY2024),
        which exceeds Microsoft's $281,724M in FY2025."""
        resp = simple_chatbot(self.QUERY)
        assert "apple" in resp.lower(), \
            f"Expected Apple as highest-revenue company, got: {resp}"


# ── R1d: Cash Flow from Operations ───────────────────────────────────────────

class TestCashFlow:
    QUERIES = {
        "Apple":     "What is the cash flow from operations for Apple?",
        "Microsoft": "What is the cash flow from operations for Microsoft?",
        "Tesla":     "What is the cash flow from operations for Tesla?",
    }

    def test_apple_cfo_handled(self):
        resp = simple_chatbot(self.QUERIES["Apple"])
        assert not is_fallback(resp), f"Fallback for Apple CFO: {resp}"

    def test_microsoft_cfo_handled(self):
        resp = simple_chatbot(self.QUERIES["Microsoft"])
        assert not is_fallback(resp), f"Fallback for Microsoft CFO: {resp}"

    def test_tesla_cfo_handled(self):
        resp = simple_chatbot(self.QUERIES["Tesla"])
        assert not is_fallback(resp), f"Fallback for Tesla CFO: {resp}"

    def test_response_contains_number(self):
        for company, q in self.QUERIES.items():
            resp = simple_chatbot(q)
            assert has_number(resp), f"No numeric value in {company} CFO response: {resp}"

    def test_response_mentions_company(self):
        for company, q in self.QUERIES.items():
            resp = simple_chatbot(q)
            assert company.lower() in resp.lower(), \
                f"Company name '{company}' missing from CFO response: {resp}"


# ── R1e: Total Assets ─────────────────────────────────────────────────────────

class TestTotalAssets:
    QUERIES = {
        "Apple":     "What are the total assets for Apple?",
        "Microsoft": "What are the total assets for Microsoft?",
        "Tesla":     "What are the total assets for Tesla?",
    }

    def test_apple_assets_handled(self):
        resp = simple_chatbot(self.QUERIES["Apple"])
        assert not is_fallback(resp), f"Fallback for Apple assets: {resp}"

    def test_microsoft_assets_handled(self):
        resp = simple_chatbot(self.QUERIES["Microsoft"])
        assert not is_fallback(resp), f"Fallback for Microsoft assets: {resp}"

    def test_tesla_assets_handled(self):
        resp = simple_chatbot(self.QUERIES["Tesla"])
        assert not is_fallback(resp), f"Fallback for Tesla assets: {resp}"

    def test_response_contains_number(self):
        for company, q in self.QUERIES.items():
            resp = simple_chatbot(q)
            assert has_number(resp), f"No numeric value in {company} assets response: {resp}"


# ── R3: Fallback for unknown queries ──────────────────────────────────────────

class TestFallback:
    UNKNOWN_QUERIES = [
        "What is the weather today?",
        "Tell me a joke.",
        "Who is the CEO?",
        "",
        "aasdkjhaksjdh",
    ]

    def test_unknown_queries_return_fallback(self):
        for q in self.UNKNOWN_QUERIES:
            resp = simple_chatbot(q)
            assert is_fallback(resp), \
                f"Expected fallback for unknown query '{q}', got: {resp}"

    def test_fallback_does_not_raise(self):
        """Chatbot must never raise an exception, even for garbage input."""
        for q in self.UNKNOWN_QUERIES:
            try:
                simple_chatbot(q)
            except Exception as e:
                raise AssertionError(f"Exception raised for input '{q}': {e}")


# ── R4: Case-insensitive matching ─────────────────────────────────────────────

class TestCaseInsensitive:
    def test_all_lowercase(self):
        resp = simple_chatbot("what is the total revenue for apple?")
        assert not is_fallback(resp), f"Lowercase query not handled: {resp}"

    def test_all_uppercase(self):
        resp = simple_chatbot("WHAT IS THE TOTAL REVENUE FOR APPLE?")
        assert not is_fallback(resp), f"Uppercase query not handled: {resp}"

    def test_mixed_case(self):
        resp = simple_chatbot("wHaT Is ThE ToTaL ReVeNuE FoR ApPlE?")
        assert not is_fallback(resp), f"Mixed-case query not handled: {resp}"

    def test_ticker_symbol(self):
        """Ticker aliases (AAPL, MSFT, TSLA) should resolve to the right company."""
        resp = simple_chatbot("What is the total revenue for MSFT?")
        assert not is_fallback(resp), f"Ticker alias MSFT not handled: {resp}"
        assert "microsoft" in resp.lower(), f"Response doesn't mention Microsoft: {resp}"


# ── R5 + R6: All companies supported, name in response ───────────────────────

class TestCompanyCoverage:
    def test_all_companies_revenue(self):
        for company in ["Apple", "Microsoft", "Tesla"]:
            resp = simple_chatbot(f"What is the total revenue for {company}?")
            assert not is_fallback(resp), f"{company} not supported"
            assert company.lower() in resp.lower(), f"{company} missing from response"


# ── standalone runner (no pytest needed) ─────────────────────────────────────

if __name__ == "__main__":
    import traceback

    test_classes = [
        TestTotalRevenue,
        TestNetIncomeChange,
        TestHighestRevenue,
        TestCashFlow,
        TestTotalAssets,
        TestFallback,
        TestCaseInsensitive,
        TestCompanyCoverage,
    ]

    passed = 0
    failed = 0
    errors = []

    for cls in test_classes:
        instance = cls()
        methods = [m for m in dir(instance) if m.startswith("test_")]
        for method in methods:
            test_name = f"{cls.__name__}.{method}"
            try:
                getattr(instance, method)()
                print(f"  PASS  {test_name}")
                passed += 1
            except AssertionError as e:
                print(f"  FAIL  {test_name}: {e}")
                failed += 1
                errors.append((test_name, str(e)))
            except Exception as e:
                print(f"  ERROR {test_name}: {e}")
                failed += 1
                errors.append((test_name, traceback.format_exc()))

    print(f"\n{'='*55}")
    print(f"Results: {passed} passed, {failed} failed")
    if errors:
        print("\nFailed tests:")
        for name, msg in errors:
            print(f"  - {name}: {msg}")
    sys.exit(0 if failed == 0 else 1)
