# Response Engine

This module maps the existing security decision and attack-specific verification
results to a controlled, simulation-only response. It does not interact with
networks, devices, or external security controls.

`generate_security_response(security_decision, attack_type, verification_result)`
returns the response action, whether the session is allowed, the session status,
and channel/replay handling flags. The UI applies those flags to its existing
session state and audit event history.

The module uses only the Python standard library; project dependencies remain in
the repository-level `requirements.txt`.