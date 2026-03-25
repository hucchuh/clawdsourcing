from tokentrader.engine import build_quote, execute
from tokentrader.models import QualityTier, TaskOrder

def test_quote_ranks_candidates() -> None:
    order = TaskOrder("analysis", 1200, 1600, 1.0, QualityTier.BALANCED)
    quote = build_quote(order)
    assert quote.candidates
    assert quote.candidates[0].score >= quote.candidates[-1].score

def test_execute_rejects_when_budget_too_low() -> None:
    order = TaskOrder("reasoning", 6000, 1500, 0.05, QualityTier.PREMIUM)
    result = execute(order, provider="provider_c", model="premium-llm-x")
    assert result.accepted is False
    assert "rejected" in result.message
