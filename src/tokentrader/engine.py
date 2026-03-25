from __future__ import annotations

from uuid import uuid4
from .models import ExecuteResponse, QuoteItem, QuoteResponse, QualityTier, SupplyOffer, TaskOrder

DEFAULT_OFFERS: list[SupplyOffer] = [
    SupplyOffer("provider_a", "cheap-llm-v1", 0.08, 0.55, 0.90, 900, 2_000_000),
    SupplyOffer("provider_b", "balanced-llm-v2", 0.45, 0.78, 0.93, 1300, 600_000),
    SupplyOffer("provider_c", "premium-llm-x", 1.20, 0.93, 0.97, 1800, 200_000),
]


def _quality_target(tier: QualityTier) -> float:
    if tier == QualityTier.ECONOMY:
        return 0.45
    if tier == QualityTier.BALANCED:
        return 0.70
    return 0.88


def _normalized_latency(avg_latency_ms: int, max_latency_ms: int) -> float:
    if avg_latency_ms <= max_latency_ms:
        return 1.0
    overflow = (avg_latency_ms - max_latency_ms) / max_latency_ms
    return max(0.0, 1.0 - overflow)


def _estimate_cost(order: TaskOrder, offer: SupplyOffer) -> float:
    return round((order.prompt_tokens / 1000) * offer.price_per_1k_tokens, 6)


def offer_score(order: TaskOrder, offer: SupplyOffer) -> float:
    cost = _estimate_cost(order, offer)
    if cost > order.budget_credits:
        return -1.0
    if order.prompt_tokens > offer.available_tokens:
        return -1.0

    target = _quality_target(order.quality_tier)
    quality_fit = max(0.0, 1 - abs(offer.quality_score - target))
    latency_fit = _normalized_latency(offer.avg_latency_ms, order.max_latency_ms)
    price_fit = max(0.0, 1 - (cost / order.budget_credits))

    w_price, w_quality, w_latency, w_reliability = 0.35, 0.30, 0.20, 0.15
    final = (
        w_price * price_fit
        + w_quality * quality_fit
        + w_latency * latency_fit
        + w_reliability * offer.reliability_score
    )
    return round(final, 6)


def build_quote(order: TaskOrder, offers: list[SupplyOffer] | None = None) -> QuoteResponse:
    offers = offers or DEFAULT_OFFERS
    ranked: list[QuoteItem] = []
    for offer in offers:
        score = offer_score(order, offer)
        if score <= 0:
            continue
        ranked.append(
            QuoteItem(
                provider=offer.provider,
                model=offer.model,
                estimated_cost_credits=_estimate_cost(order, offer),
                score=score,
            )
        )
    ranked.sort(key=lambda i: i.score, reverse=True)
    return QuoteResponse(order=order, candidates=ranked)


def execute(order: TaskOrder, provider: str, model: str, offers: list[SupplyOffer] | None = None) -> ExecuteResponse:
    offers = offers or DEFAULT_OFFERS
    matched = next((o for o in offers if o.provider == provider and o.model == model), None)
    if not matched:
        return ExecuteResponse(False, str(uuid4()), 0.0, "selected route not found")

    score = offer_score(order, matched)
    if score <= 0:
        return ExecuteResponse(False, str(uuid4()), 0.0, "route rejected due to budget/capacity/sla constraints")

    return ExecuteResponse(True, str(uuid4()), _estimate_cost(order, matched), "task accepted and executed in simulation mode")
