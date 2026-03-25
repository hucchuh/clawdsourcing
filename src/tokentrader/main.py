from __future__ import annotations
import json
from dataclasses import asdict
from .engine import build_quote, execute
from .models import QualityTier, TaskOrder

def demo() -> dict:
    order = TaskOrder("code_generation", 1500, 1600, 1.0, QualityTier.BALANCED)
    quote = build_quote(order)
    first = quote.candidates[0] if quote.candidates else None
    execution = execute(order, first.provider, first.model) if first else {"accepted": False, "message": "no candidates"}
    return {
        "order": asdict(order),
        "candidates": [asdict(c) for c in quote.candidates],
        "execution": asdict(execution) if hasattr(execution, "accepted") else execution,
    }

if __name__ == "__main__":
    print(json.dumps(demo(), ensure_ascii=False, indent=2))
