def send_confirmation(email: str, widget_title: str):
    if not email:
        return
    # Fake/local: log instead of real SMTP. Swap for Mailpit later if desired.
    print(f"[EMAIL] Confirmation to {email} for widget '{widget_title}'")
    # Simulate a controllable failure point for demo/testing:
    import os
    if os.getenv("FORCE_EMAIL_FAILURE") == "true":
        raise RuntimeError("SMTP down")