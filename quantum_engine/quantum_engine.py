import hashlib
import math

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def message_to_angle(message):
    """
    Convert a message into a deterministic angle.

    This is a prototype encoding mechanism.
    It is NOT a cryptographic hash or QDS signature by itself.
    """

    digest = hashlib.sha256(
        message.encode("utf-8")
    ).hexdigest()

    value = int(digest[:8], 16)

    angle = (value / 0xFFFFFFFF)

    return angle


def create_bell_pair():
    """
    Create a Bell pair using:

    H on qubit 1
    CNOT between qubit 1 and qubit 2
    """

    circuit = QuantumCircuit(2)

    circuit.h(0)
    circuit.cx(0, 1)

    return circuit


def create_teleportation_circuit(angle):
    """
    Create a 3-qubit quantum teleportation circuit.

    Qubit 0:
        Unknown state |ψ>

    Qubit 1 and Qubit 2:
        Bell pair

    The unknown state is teleported from
    qubit 0 to qubit 2.
    """

    circuit = QuantumCircuit(3, 3)

    # ---------------------------------------------
    # STEP 1: Prepare unknown state |ψ>
    # ---------------------------------------------

    circuit.ry(angle, 0)

    # ---------------------------------------------
    # STEP 2: Create Bell pair
    # ---------------------------------------------

    circuit.h(1)
    circuit.cx(1, 2)

    # ---------------------------------------------
    # STEP 3: Bell measurement
    # ---------------------------------------------

    circuit.cx(0, 1)
    circuit.h(0)

    circuit.measure(0, 0)
    circuit.measure(1, 1)

    # ---------------------------------------------
    # STEP 4: Pauli corrections
    # ---------------------------------------------

    with circuit.if_test((circuit.clbits[1], 1)):
        circuit.x(2)

    with circuit.if_test((circuit.clbits[0], 1)):
            circuit.z(2)

    # ---------------------------------------------
    # STEP 5: Measure recovered state
    # ---------------------------------------------

    circuit.measure(2, 2)

    return circuit


def run_quantum_simulation(message, shots=1024):
    """
    Run the complete quantum simulation.
    """

    angle = message_to_angle(message)

    # Theoretical probabilities for |ψ⟩ = Ry(angle)|0⟩
    expected_probability_zero = math.cos(angle / 2) ** 2
    expected_probability_one = math.sin(angle / 2) ** 2

    circuit = create_teleportation_circuit(angle)

    simulator = AerSimulator()

    compiled_circuit = transpile(
        circuit,
        simulator
    )

    result = simulator.run(
        compiled_circuit,
        shots=shots
    ).result()

    counts = result.get_counts()

    total = sum(counts.values())

    zero_count = 0
    one_count = 0

    for state, count in counts.items():

        # Last classical bit corresponds to
        # the recovered qubit measurement.

        recovered_bit = state[0]

        if recovered_bit == "0":
            zero_count += count
        else:
            one_count += count

    probability_zero = zero_count / total
    probability_one = one_count / total

    return {
        "message": message,
        "angle": angle,
        "shots": shots,
        "counts": counts,
        "expected_probability_zero": expected_probability_zero,
        "expected_probability_one": expected_probability_one,
        "probability_zero": probability_zero,
        "probability_one": probability_one,
        "deviation_zero": abs(
            probability_zero - expected_probability_zero
        ),
        "deviation_one": abs(
            probability_one - expected_probability_one
        )
    }


def generate_quantum_signature(message):

    result = run_quantum_simulation(message)

    return {
        "message": message,
        "quantum_state": f"|ψ⟩ = Ry({result['angle']:.4f})|0⟩",
        "bell_state": "Φ+ = (|00⟩ + |11⟩) / √2",
        "teleportation": "Completed",
        "measurement": result["counts"],
        "expected_probability_zero": result["expected_probability_zero"],
        "expected_probability_one": result["expected_probability_one"],
        "probability_zero": result["probability_zero"],
        "probability_one": result["probability_one"],
        "deviation_zero": result["deviation_zero"],
        "deviation_one": result["deviation_one"]
    }