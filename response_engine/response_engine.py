def generate_security_response(
    security_decision,
    attack_type,
    verification_result
):
    """Return a simulation-only response based on existing verification results."""
    decision_status = security_decision.get("status")
    reason = security_decision.get("primary_reason", "Verification rejected")
    response = {
        "status": "LEGITIMATE" if decision_status == "LEGITIMATE" else "THREAT",
        "action": "VERIFICATION REJECTED",
        "action_type": "BLOCK",
        "action_detail": "Verification failed; the session was not accepted.",
        "reason": reason,
        "session_allowed": False,
        "session_status": "BLOCKED",
        "communication_compromised": False,
        "fresh_verification_required": False,
        "mark_signature_used": bool(verification_result.get("replay_detected", False))
    }

    if decision_status == "LEGITIMATE":
        response.update({
            "action": "SESSION ACCEPTED",
            "action_type": "ALLOW",
            "action_detail": "Verification allowed; the session may continue.",
            "session_allowed": True,
            "session_status": "ACTIVE"
        })
    elif (
        attack_type == "Forgery"
        and verification_result.get("signature_integrity") is False
    ):
        response.update({
            "action": "SIGNATURE REJECTED",
            "action_detail": "Forged signature rejected; the session was not accepted."
        })
    elif (
        attack_type == "Impersonation"
        and verification_result.get("identity_verified") is False
    ):
        response.update({
            "action": "IDENTITY VERIFICATION FAILED",
            "action_detail": "Authentication rejected; the session was not accepted."
        })
    elif (
        attack_type == "Replay"
        and verification_result.get("replay_detected", False)
    ):
        response.update({
            "action": "REPLAY BLOCKED",
            "action_detail": "Previously used signature/session rejected."
        })
    elif (
        attack_type == "Quantum Channel Manipulation"
        and verification_result.get("channel_integrity") is False
    ):
        response.update({
            "action": "CHANNEL INTEGRITY FAILURE",
            "action_detail": "Transmission rejected; a fresh verification is required.",
            "communication_compromised": True,
            "fresh_verification_required": True,
            "session_status": "FRESH VERIFICATION REQUIRED"
        })

    return response