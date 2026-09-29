import hashlib
import time


def simulate_normal(message, signature_id):
    """
    Normal legitimate verification scenario.
    """

    return {
        "attack": "Normal",
        "modified": False,
        "message": message,
        "signature_id": signature_id,
        "replayed": False,
        "channel_modified": False
    }


def simulate_forgery(message, signature_id):
    """
    Controlled forgery simulation.

    The message/signature relationship is deliberately
    changed to simulate an invalid signature.
    """

    forged_signature = hashlib.sha256(
        (message + "_FORGED").encode("utf-8")
    ).hexdigest()

    return {
        "attack": "Forgery",
        "modified": True,
        "message": message,
        "signature_id": signature_id,
        "forged_signature": forged_signature,
        "replayed": False,
        "channel_modified": False
    }


def simulate_impersonation(message, signature_id):
    """
    Controlled impersonation simulation.

    A different identity is associated with the
    submitted signature.
    """

    return {
        "attack": "Impersonation",
        "modified": True,
        "message": message,
        "signature_id": signature_id,
        "claimed_identity": "AUTHORIZED_USER",
        "actual_identity": "UNKNOWN_USER",
        "replayed": False,
        "channel_modified": False
    }


def simulate_replay(message, signature_id):
    """
    Controlled replay simulation.

    The same signature/session identifier is reused.
    """

    return {
        "attack": "Replay",
        "modified": False,
        "message": message,
        "signature_id": signature_id,
        "replayed": True,
        "channel_modified": False
    }


def simulate_channel_attack(message, signature_id):
    """
    Controlled quantum-channel manipulation simulation.

    The channel is marked as modified so that the
    quantum measurement statistics can be altered
    in the detection stage.
    """

    return {
        "attack": "Quantum Channel Manipulation",
        "modified": True,
        "message": message,
        "signature_id": signature_id,
        "replayed": False,
        "channel_modified": True
    }


def generate_signature_id(message):
    """
    Generate a deterministic identifier for the
    prototype signature/session.
    """

    timestamp = str(int(time.time()))

    return hashlib.sha256(
        (message + timestamp).encode("utf-8")
    ).hexdigest()[:16]