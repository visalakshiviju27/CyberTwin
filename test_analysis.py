from app.services.analysis_engine import analyze

def test_otp_urgency_triggers_warning():
    result = analyze("Not sure", "Urgent scholarship: share your OTP immediately to receive funds")
    assert result["risk"] == "High concern — take protective steps"
    assert any("Credential" in f["title"] for f in result["findings"])
    assert any("Urgency" in f["title"] for f in result["findings"])

def test_money_and_link_gives_verification_guidance():
    result = analyze("Online scam / phishing", "Please transfer payment now at https://example.invalid")
    assert result["risk"] in {"Suspicious — verify first", "High concern — take protective steps"}
    assert any("Payment" in f["title"] for f in result["findings"])
    assert any("URL" in f["title"] for f in result["findings"])
    assert any("Verify" in action or "verify" in action for action in result["actions"])

def test_impersonation_category_detected():
    result = analyze("Fake account / impersonation", "Someone copied my photo")
    assert any("impersonation" in f["title"].lower() for f in result["findings"])

def test_bullying_recommends_support():
    result = analyze("Cyberbullying / harassment", "Repeated humiliating threats in a group chat")
    assert any("Harassment" in f["title"] for f in result["findings"])
    assert any("trusted support" in action.lower() for action in result["actions"])

def test_unknown_short_text_is_rejected_by_api_schema():
    from pydantic import ValidationError
    from app.main import AnalyzeRequest
    try:
        AnalyzeRequest(text="hi")
        assert False, "Expected validation failure"
    except ValidationError:
        assert True
