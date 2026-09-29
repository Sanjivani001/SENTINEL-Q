def calculate_deviation(expected, observed):
    """Calculate absolute probability deviation."""
    return abs(observed - expected)


def check_threshold(deviation, threshold):
    """Check whether statistical deviation exceeds threshold."""
    return deviation > threshold


def detect_attack(
    expected,
    observed,
    threshold,
    attack_data=None
):
    """
    Combine statistical analysis with security-event checks.
    """

    deviation = calculate_deviation(
        expected,
        observed
    )

    threshold_exceeded = check_threshold(
        deviation,
        threshold
    )

    reasons = []

    # -----------------------------------------
    # Statistical anomaly
    # -----------------------------------------

    if threshold_exceeded:
        reasons.append(
            "Measurement deviation exceeded threshold"
        )

    # -----------------------------------------
    # Attack-specific checks
    # -----------------------------------------

    attack_type = "Normal"

    if attack_data:

        attack_type = attack_data.get(
            "attack",
            "Normal"
        )

        if attack_data.get("replayed", False):

            reasons.append(
                "Previously used signature/session detected"
            )

        if attack_data.get("channel_modified", False):

            reasons.append(
                "Quantum channel modification detected"
            )

        if attack_type == "Forgery":

            reasons.append(
                "Signature integrity verification failed"
            )

        if attack_type == "Impersonation":

            reasons.append(
                "Identity verification mismatch detected"
            )

    # -----------------------------------------
    # Final decision
    # -----------------------------------------

    attack_detected = len(reasons) > 0

    if attack_detected:

        status = "ATTACK DETECTED"

    else:

        status = "LEGITIMATE"

    return {
        "expected": expected,
        "observed": observed,
        "deviation": deviation,
        "threshold": threshold,
        "threshold_exceeded": threshold_exceeded,
        "attack_type": attack_type,
        "attack_detected": attack_detected,
        "status": status,
        "reasons": reasons
    }


def calculate_metrics(results):
    """
    Calculate basic detection metrics.

    Each result should contain:

        actual_attack
        detected_attack
    """

    total = len(results)

    normal_tests = 0
    attack_tests = 0
    detected_attacks = 0
    missed_attacks = 0
    false_alarms = 0

    for result in results:

        actual_attack = result.get(
            "actual_attack",
            False
        )

        detected_attack = result.get(
            "detected_attack",
            False
        )

        if actual_attack:

            attack_tests += 1

            if detected_attack:

                detected_attacks += 1

            else:

                missed_attacks += 1

        else:

            normal_tests += 1

            if detected_attack:

                false_alarms += 1

    detection_rate = (
        detected_attacks / attack_tests
        if attack_tests > 0
        else 0
    )

    false_positive_rate = (
        false_alarms / normal_tests
        if normal_tests > 0
        else 0
    )

    return {
        "total_tests": total,
        "normal_tests": normal_tests,
        "attack_tests": attack_tests,
        "detected_attacks": detected_attacks,
        "missed_attacks": missed_attacks,
        "false_alarms": false_alarms,
        "detection_rate": detection_rate,
        "false_positive_rate": false_positive_rate
    }