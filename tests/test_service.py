from pathlib import Path
from tokentrader.service import TokenTraderService

def test_register_login_and_quote_flow(tmp_path: Path) -> None:
    service = TokenTraderService(db_path=str(tmp_path / "test.db"))
    user = service.register_user("alice@example.com", "passw0rd!", "Alice")
    assert user["email"] == "alice@example.com"
    auth = service.login("alice@example.com", "passw0rd!")
    assert auth["token"]
    quote = service.build_quote_for_user(
        token=auth["token"],
        payload={"task_type": "analysis", "prompt_tokens": 1200, "max_latency_ms": 1500, "budget_credits": 1.0, "quality_tier": "balanced"},
    )
    assert quote["candidates"]

def test_register_duplicate_email(tmp_path: Path) -> None:
    service = TokenTraderService(db_path=str(tmp_path / "dup.db"))
    service.register_user("bob@example.com", "passw0rd!", "Bob")
    try:
        service.register_user("bob@example.com", "passw0rd!", "Bobby")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "已注册" in str(exc)
