# SENTINEL-Q: SIH26141 Final Presentation Package

## 1. Repository Review

### What is actually implemented

- `main.py` launches the Streamlit application in `ui/ui.py`.
- `quantum_engine/quantum_engine.py` uses Qiskit and Qiskit Aer `AerSimulator`. It maps a message through SHA-256's first eight hexadecimal digits to a rotation angle, prepares an `Ry(angle)|0>` state, builds a teleportation circuit with a Bell pair, performs measurements and conditional Pauli corrections, and returns simulator counts and probabilities. The default run uses 1,024 shots.
- The expected probability of the recovered qubit is calculated analytically from the rotation angle. The observed probability is calculated from simulator counts. The UI uses the `|0>` values for its deviation analysis.
- `attack_engine/attack_engine.py` produces controlled scenario records for Normal, Forgery, Impersonation, Replay, and Quantum Channel Manipulation. These are simulated flags and fields, not attacks on a real network.
- `detection_engine/detection_engine.py` calculates absolute deviation, compares it to a threshold, and returns reasons for anomaly and scenario flags. It also defines a metrics helper, but the UI does not run an evaluation dataset or present its metrics.
- `ui/ui.py` orchestrates the modules. It interprets scenario fields into the displayed signature, identity, replay, and channel checks, combines those checks with the detection result, and presents the final status. The threshold is currently assigned as `0.15` in the UI; it is a prototype parameter, not a calibrated or universal standard.
- `response_engine/response_engine.py` maps the decision into simulated allow/block actions and session-status text. It does not control a real connection or security device.
- Streamlit session state maintains the event list and accepted/used signature IDs for the current app session. Clearing the event log does not clear replay bookkeeping.
- The UI uses Plotly to visualize the actual measurement counts. The quick-action buttons invoke the same existing scenario path as the main verification button.

### Important boundaries for presentation claims

- The displayed “Quantum Signature” is a message-derived simulated quantum state. It is not a cryptographic signature or a complete Quantum Digital Signature (QDS) protocol. SHA-256 is used in the message-to-angle mapping and prototype ID generation; this does not make the prototype cryptographically secure.
- The controlled Forgery scenario creates a forged hash field and a `modified` marker. The UI treats that marker as failed signature integrity; it does not perform a standards-based cryptographic signature verification.
- Impersonation uses controlled claimed/actual identity fields. There is no user authentication system.
- Replay is detected using accepted/used IDs held in the current Streamlit session. This is useful for the demo but is not persistent storage across app restarts or separate sessions.
- Quantum Channel Manipulation sets a controlled `channel_modified` flag. The current path does not alter a physical channel, network traffic, circuit, or the simulator's measurement counts for that scenario. Describe it as a simulated channel-integrity event.
- `detect_attack` owns deviation/threshold calculation and returns attack reasons based on flags. Some scenario-specific verification booleans and the combined final status are constructed in the Streamlit UI. Describe the real division of responsibility accurately.
- The threshold value is fixed in the current UI code, not user-adjustable through the dashboard. It has not been scientifically calibrated.
- `calculate_metrics` exists as a helper but is not connected to a labeled validation dataset or the displayed demo outcomes. Do not claim a measured detection rate, false-positive rate, or accuracy.
- The requirements list includes NumPy, SciPy, and pandas, but the inspected engine/UI path uses Qiskit/Aer, Streamlit, Plotly, and Python standard-library modules; do not imply those numerical packages drive the current detection flow.
- The repository has no official SIH slide template, no project screenshot/result artifact, an empty root `README.md`, and only `.gitkeep` in `tests/`. The exact official SIH26141 problem-statement wording was not present locally. Use the wording from the official SIH portal/template if available; the problem framing below is a paraphrase, not a quotation.

## 2. Architecture and Workflow

### Architecture diagram description

Draw six boxes left-to-right, with the UI above them and session/audit state below:

```text
User Message + Scenario
          |
          v
Streamlit UI / Orchestrator
  |             |              |
  v             v              v
Quantum       Attack         Detection
Engine        Engine         Engine
(Qiskit Aer)  (controlled)   (statistics + reasons)
  \             |              /
   \------------+-------------/
                v
       UI decision composition
                |
          Response Engine
       (simulated allow/block)
                |
                v
      Session State + Event Log
```

Label the quantum engine “local simulator” and the attack engine “controlled scenario data.” Show that the Streamlit UI passes values among modules and combines outputs. Do not imply that Qiskit communicates with a remote quantum device or that the response engine blocks real network traffic.

### Workflow diagram description

```text
User message
  -> message-derived state preparation
  -> Bell pair prepared in the circuit
  -> teleportation circuit and conditional Pauli corrections
  -> selected controlled scenario produces attack fields
  -> Aer simulator measurement counts
  -> expected/observed |0> probability and absolute deviation
  -> threshold check AND scenario-specific checks
  -> UI composes final decision and explanation
  -> simulated response and session event history
```

Key line to say aloud: “Measurement analysis and attack verification are separate inputs to the final decision.”

## 3. Final Slide-by-Slide Content

Use these 22 slides as a full-length option. If the official SIH template limits slide count, merge slides 3–5, 8–9, 10–12, and 17–19. Keep the official template's required order when one is supplied.

### Slide 1 — SENTINEL-Q

**Purpose:** Introduce project, team, and SIH identifier.

**Exact slide text:**
- SENTINEL-Q
- Quantum-Inspired Cyber Threat Detection & Prevention
- SIH26141 | SIH 2026
- Team name and member names
- Controlled quantum-security prototype

**Visual:** Actual dashboard screenshot cropped to show the title and pipeline, or a restrained circuit motif built from simple lines/icons.

**Presenter says:** “We are presenting SENTINEL-Q, a controlled prototype that combines quantum-circuit simulation with scenario-specific security verification.”

**Do not claim:** Real quantum hardware, production QDS, or AI-based detection.

### Slide 2 — Problem Statement

**Purpose:** State the challenge without misquoting the SIH prompt.

**Exact slide text:**
- SIH Problem Statement: SIH26141
- Reliable verification must consider forgery, impersonation, replay, and channel-integrity events.
- A single measurement signal may not describe every security failure.
- *(Insert the exact official problem-statement wording from the SIH portal/template.)*

**Visual:** Threat-to-verification diagram: message/session -> threat cases -> verification decision.

**Presenter says:** “Our framing is that verification should examine both measurement behavior and protocol-specific evidence. The first line on the final slide should use the organizer's exact wording.”

**Do not claim:** That the paraphrase is the official SIH text, or that this prototype secures deployed communications.

### Slide 3 — Existing Challenge

**Purpose:** Explain why the demonstration evaluates more than one signal.

**Exact slide text:**
- Measurement deviation can indicate statistical change.
- Replay can reuse a previously accepted session without requiring a large measurement deviation.
- Forgery, identity mismatch, and channel flags need their own checks.
- One result must combine these paths transparently.

**Visual:** Two lanes: “Measurement path” and “Security verification path,” joining at “Decision.”

**Presenter says:** “A normal-looking measurement is not proof that the requested operation is legitimate; the replay example makes this distinction visible.”

**Do not claim:** That sophisticated real-world attacks have been comprehensively modeled.

### Slide 4 — Proposed Solution

**Purpose:** Describe the actual prototype in one view.

**Exact slide text:**
- Qiskit Aer quantum-circuit simulation
- Controlled security scenarios
- Probability deviation against a prototype threshold
- Scenario-specific verification and explainable reason
- Streamlit dashboard and session event history

**Visual:** Five connected module blocks matching the repository.

**Presenter says:** “The prototype makes the processing and decision path inspectable in one dashboard.”

**Do not claim:** Automated prevention on a real network; response actions are simulated UI/session outcomes.

### Slide 5 — Innovation / Key Idea

**Purpose:** Present the defensible contribution as an integration/demo idea, not an unsupported novelty claim.

**Exact slide text:**
- Demonstrates Bell-pair preparation and teleportation in a simulator.
- Runs controlled attack scenarios through one workflow.
- Keeps statistical anomaly and protocol verification separate.
- Shows a reason for each final decision.

**Visual:** “Measurement evidence + verification evidence -> decision” equation.

**Presenter says:** “The key design idea is the separation of statistical measurement analysis from attack-specific checks, then showing how both inform the final decision.”

**Do not claim:** First-of-its-kind, quantum-secure by proof, or superior to classical systems.

### Slide 6 — System Architecture

**Purpose:** Show module ownership and integration.

**Exact slide text:**
- Quantum Engine: circuit construction, Aer execution, counts/probabilities
- Attack Engine: controlled scenario data
- Detection Engine: deviation, threshold, attack reasons
- Streamlit UI: maps checks and composes the displayed decision
- Response Engine: simulated response text/state

**Visual:** Use the architecture diagram above; annotate the UI as orchestrator.

**Presenter says:** “The engines are separate Python modules. The UI passes their outputs together and maintains session-scoped history.”

**Do not claim:** That the detection module alone performs every verification comparison or final status composition.

### Slide 7 — Complete Workflow

**Purpose:** Walk through the ordered path.

**Exact slide text:**
- Message -> quantum processing -> Bell state -> teleportation
- Scenario -> measurement -> statistical analysis
- Attack-specific verification -> security decision -> event history

**Visual:** Nine-stage horizontal pipeline; use the actual UI pipeline screenshot.

**Presenter says:** “Each run starts with a user message and selected scenario, then follows the same ordered path to an explainable session decision.”

**Do not claim:** That the selected scenario hardcodes the final status; the UI calls the existing attack and detection paths.

### Slide 8 — Quantum Processing Layer

**Purpose:** Explain what the simulator computes.

**Exact slide text:**
- Message digest prefix maps to a rotation angle.
- State preparation: `Ry(angle)|0>`.
- Qiskit Aer executes the circuit locally.
- Default simulator run: 1,024 shots.
- Counts produce observed probabilities.

**Visual:** Screenshot of the live Quantum Evidence panel with one real run's quantum state and counts.

**Presenter says:** “The message is mapped deterministically to a rotation parameter; Aer runs the circuit and returns counts. Those counts, not invented values, feed the displayed observed probability.”

**Do not claim:** The message-to-angle mapping is encryption, a cryptographic hash signature, or a complete QDS protocol.

### Slide 9 — Bell State & Teleportation

**Purpose:** Explain the circuit concepts simply.

**Exact slide text:**
- Hadamard + CNOT prepare an entangled Bell pair.
- Bell-basis measurement yields classical outcomes.
- Conditional X and Z Pauli corrections are applied.
- The recovered qubit is measured in the simulator.

**Visual:** Three-qubit circuit sketch matching `create_teleportation_circuit`.

**Presenter says:** “The circuit prepares an input state and a Bell pair, performs the teleportation operations, applies corrections conditioned on measured classical bits, and measures the recovered qubit.”

**Do not claim:** Teleportation sends matter, uses a real quantum link, or independently detects cyberattacks.

### Slide 10 — Controlled Attack Simulation

**Purpose:** Make clear how each attack enters this prototype.

**Exact slide text:**
- Forgery: controlled modified marker and forged-hash field.
- Impersonation: controlled claimed/actual identity mismatch.
- Replay: reuse check against accepted/used IDs in this app session.
- Channel manipulation: controlled channel-modified flag.

**Visual:** Four attack cards feeding the existing verification workflow.

**Presenter says:** “These scenarios inject controlled data into the pipeline; no external traffic or user identity system is involved.”

**Do not claim:** Real adversary emulation, a real identity provider, or actual channel tampering.

### Slide 11 — Detection & Statistical Analysis

**Purpose:** Define the measurement path and its boundary.

**Exact slide text:**
- Expected probability: analytical `P(0)` for the prepared state.
- Observed probability: simulator count-derived `P(0)`.
- Deviation: `|Observed - Expected|`.
- Measurement anomaly when deviation `> 0.15`.
- `0.15` is the current prototype setting, not a universal threshold.

**Visual:** Display expected, observed, deviation, and threshold from a live run. Do not fill in made-up values.

**Presenter says:** “The comparison is absolute probability deviation. The current threshold is a prototype setting in the UI and has not been calibrated against a real deployment dataset.”

**Do not claim:** Universal QDS threshold, calibrated operating point, or measured accuracy.

### Slide 12 — Security Verification Layer

**Purpose:** Explain the checks and their implementation ownership.

**Exact slide text:**
- Forgery: UI maps the scenario's `modified` flag to signature-integrity failure.
- Impersonation: UI compares controlled claimed/actual identity fields.
- Replay: UI checks the replay ID against session-used IDs.
- Channel: UI maps the controlled channel flag to channel-integrity failure.

**Visual:** Scenario-specific check table with only relevant check highlighted.

**Presenter says:** “The detection module returns statistical and attack-flag reasons; the UI derives the displayed checks and combines them into the final result.”

**Do not claim:** Standards-based signature verification, real authentication, persistent replay storage, or an altered quantum channel.

### Slide 13 — Dashboard

**Purpose:** Show how judges can inspect the run.

**Exact slide text:**
- Ordered pipeline and scenario selection
- Quantum state, Bell state, teleportation status
- Simulator counts and Plotly measurement visualization
- Separate analysis, verification, and final decision
- Session event history and counters

**Visual:** Actual screenshot from the running app. Capture it from the current UI; no repository screenshot is supplied.

**Presenter says:** “The dashboard exposes the evidence and the reason, rather than presenting an unexplained threat label.”

**Do not claim:** Global monitoring, persistent audit storage, or real-time network telemetry.

### Slide 14 — Five Security Scenarios

**Purpose:** Summarize the controlled test cases.

**Exact slide text:**
- Normal baseline
- Forgery
- Impersonation
- Replay
- Quantum Channel Manipulation
- Each uses the same processing and decision workflow.

**Visual:** Five-column scenario-to-check map.

**Presenter says:** “Each scenario activates a different controlled verification condition, and the final decision is shown with its primary reason.”

**Do not claim:** These five cases exhaust all attacks.

### Slide 15 — Results & Validation

**Purpose:** Present actual tested outcomes without inventing quantitative performance.

**Exact slide text:**
- All five controlled UI scenarios exercised.
- In the tested runs, measurement anomaly: No.
- Normal passed; each attack scenario failed its corresponding check.
- Replay reuse detected after a Normal run; clearing the event log preserved replay state.

**Visual:** Use the results table in Section 5. Optionally show an actual event-log screenshot.

**Presenter says:** “These are scenario outcomes, not a statistical benchmark. The demonstration shows why measurement anomaly and attack verification must be reported separately.”

**Do not claim:** Accuracy, false-positive rate, throughput, or a statistically representative evaluation.

### Slide 16 — Technology Stack

**Purpose:** Name only the technologies and roles supported by code.

**Exact slide text:**
- Python
- Qiskit + Qiskit Aer simulator
- Streamlit + Plotly
- Git/GitHub and VS Code for development
- NumPy/SciPy/pandas appear in requirements but are not used in the inspected live path

**Visual:** Clean icon row with role labels.

**Presenter says:** “The quantum circuit is executed by the local Aer simulator; Streamlit renders the workflow and Plotly charts returned counts.”

**Do not claim:** Cloud services, external APIs, or a deployed quantum backend.

### Slide 17 — Advantages

**Purpose:** Summarize demonstrable prototype strengths.

**Exact slide text:**
- Modular Python engines
- Repeatable controlled scenarios
- Engine-derived measurement counts/probabilities
- Separate statistical and scenario-specific evidence
- Human-readable primary reason and event history

**Visual:** Five short proof points, each linked to a code/UI surface.

**Presenter says:** “The value at this stage is an inspectable educational prototype that makes its scenario assumptions and decision reason visible.”

**Do not claim:** Production readiness, cryptographic assurance, or security guarantees.

### Slide 18 — Limitations

**Purpose:** Demonstrate technical maturity and honest scope.

**Exact slide text:**
- Local simulator, not quantum hardware
- Controlled attack flags, not real traffic attacks
- Prototype threshold not calibrated
- No real identity/authentication service
- Replay state is session-scoped
- Not a production cryptographic/QDS implementation

**Visual:** “Prototype boundary” box around the implemented system.

**Presenter says:** “These limits define what this prototype demonstrates and what would need rigorous engineering before deployment.”

**Do not claim:** The limitations have already been solved.

### Slide 19 — Future Scope

**Purpose:** Suggest realistic next research steps.

**Exact slide text:**
- Calibrate statistical thresholds with defined experiments.
- Add a standards-reviewed cryptographic/QDS layer if required by the application.
- Integrate a real communication-channel test harness.
- Evaluate more attack cases and session persistence requirements.
- Explore hardware execution only when access and protocol design justify it.

**Visual:** Staged roadmap: validation -> integration -> hardware research.

**Presenter says:** “These are future directions, not current capabilities. Each would require a separate design and evaluation.”

**Do not claim:** A roadmap item is implemented or guaranteed.

### Slide 20 — Conclusion

**Purpose:** Reinforce the project message.

**Exact slide text:**
- Quantum simulation provides measured circuit output.
- Statistical analysis evaluates probability deviation.
- Scenario-specific verification can detect a threat even with no measurement anomaly.
- The final decision includes an explainable reason.

**Visual:** Measurement evidence + verification evidence -> security decision.

**Presenter says:** “SENTINEL-Q demonstrates a combined, explainable decision path in a controlled simulation.”

**Do not claim:** Quantum processing alone detects every attack.

### Slide 21 — Live Demo

**Purpose:** Invite judges to observe the real application.

**Exact slide text:**
- Normal baseline -> accepted session
- Run one or two attacks -> inspect corresponding failed check
- Replay -> show reuse of the accepted session
- Compare measurement status with final decision

**Visual:** Actual app URL/QR only if the demo network permits access; otherwise launch locally.

**Presenter says:** “We will keep the message fixed, establish a Normal accepted session, and then run the controlled scenarios through the same workflow.”

**Do not claim:** The URL is publicly reachable or the app is deployed in the cloud.

### Slide 22 — Thank You / Q&A

**Purpose:** End with the main technical takeaway.

**Exact slide text:**
- Thank you
- Questions?
- “Measurement evidence and security verification are separate inputs to one explainable decision.”

**Visual:** Minimal project title and actual circuit/dashboard image.

**Presenter says:** “Thank you. We welcome questions about the simulator, controlled scenarios, threshold assumptions, and the prototype's boundaries.”

**Do not claim:** Anything beyond the demonstrated scope.

## 4. Judge-Friendly Quantum Explanation

### 20-second version

“A qubit is represented by a quantum state. Our simulator prepares a message-dependent state, creates an entangled Bell pair, runs the teleportation circuit and conditional corrections, then measures the recovered qubit. Qiskit Aer returns counts from which we calculate the observed probability. This is a local simulation, not quantum hardware.”

### 1-minute version

“We convert the message into a deterministic rotation angle and prepare `Ry(angle)|0>`. In the three-qubit circuit, a Hadamard and CNOT prepare an entangled Bell pair. The input and one half of the pair undergo the Bell-measurement operations. The two classical measurement bits control X and Z corrections on the destination qubit. Aer simulates the circuit for 1,024 shots by default and returns three-bit counts. We read the recovered qubit's bit to calculate observed `P(0)` and `P(1)`, then compare observed `P(0)` with the analytical expected value. All of this is a circuit simulation; the message mapping is not a cryptographic signature.”

### Technical explanation for a quantum-aware judge

- `message_to_angle` computes SHA-256 over the UTF-8 message, interprets the first eight hex digits as an integer, and divides by `0xFFFFFFFF`; the result is used as the `Ry` angle.
- The circuit contains three qubits and three classical bits. It prepares qubit 0 with `Ry(angle)`, prepares qubits 1 and 2 with `H(1)` and `CX(1,2)`, applies the Bell-measurement operations `CX(0,1)` and `H(0)`, and measures qubits 0 and 1 into classical bits 0 and 1.
- Conditional corrections apply X to qubit 2 when classical bit 1 is 1, and Z when classical bit 0 is 1. Qubit 2 is then measured into classical bit 2.
- Aer returns counts. In the displayed count strings, the code reads `state[0]` as the recovered qubit bit. It computes expected `P(0) = cos(angle/2)^2`, observed `P(0) = zero_count/total`, and absolute deviation.
- The engine has a separate `create_bell_pair()` helper, but the live teleportation circuit prepares its Bell pair directly; do not imply that this helper is called by the main simulation function.
- Avoid calling this protocol a QDS implementation. A quantum circuit demonstration is not, by itself, proof of signature authenticity or security.

## 5. Attack Explanations

### Normal baseline

- **Meaning:** No controlled attack condition is selected.
- **Simulation:** Attack engine returns unmodified/non-replayed fields.
- **Indicator:** The UI's relevant baseline checks pass; the accepted ID is retained when the security response allows the session.
- **Detection path:** Detection engine evaluates measurement deviation and the Normal attack record.
- **Decision:** LEGITIMATE when neither the detection result nor UI-derived verification checks indicate a threat. In the validated run, reason: “All verification checks passed.”

### Forgery

- **Meaning:** A controlled signature-integrity failure case.
- **Simulation:** Attack engine creates a `_FORGED` hash field and returns `modified=True`.
- **Indicator:** UI maps `modified=True` for Forgery to `signature_integrity=False`.
- **Detection path:** Detection engine recognizes the Forgery scenario and returns its reason; the UI also includes failed signature integrity in its combined decision.
- **Decision:** SECURITY THREAT DETECTED. Reason: “Signature integrity verification failed.”
- **Caveat:** This does not compare a real public-key signature or validate a deployed QDS protocol.

### Impersonation

- **Meaning:** A controlled identity-mismatch case.
- **Simulation:** Attack engine supplies `claimed_identity="AUTHORIZED_USER"` and `actual_identity="UNKNOWN_USER"`.
- **Indicator:** UI compares those values and marks identity verification false.
- **Detection path:** Detection engine adds the Impersonation reason; UI includes the failed identity check in its decision.
- **Decision:** SECURITY THREAT DETECTED. Reason: “Identity verification mismatch detected.”
- **Caveat:** There is no real identity provider or authentication flow.

### Replay

- **Meaning:** Reuse of an accepted signature/session ID.
- **Simulation:** UI keeps `last_accepted_signature_id` and `used_signature_ids` in Streamlit session state. After a Normal run, Replay reuses the accepted ID and tests membership in the used-ID set.
- **Indicator:** `replayed=True` when that ID is already used.
- **Detection path:** Detection engine includes the replay reason; the UI marks Replay Status failed and the decision threat.
- **Decision:** SECURITY THREAT DETECTED. Reason: “Previously used signature/session detected.”
- **Caveat:** Run Normal first. IDs and replay state are session-scoped and are not durable across app restarts.

### Quantum Channel Manipulation

- **Meaning:** A controlled channel-integrity failure case.
- **Simulation:** Attack engine returns `channel_modified=True`.
- **Indicator:** UI maps the flag to `channel_integrity=False`.
- **Detection path:** Detection engine returns the channel-modification reason; UI includes the failed channel check in its combined decision.
- **Decision:** SECURITY THREAT DETECTED. Reason: “Quantum channel modification detected.”
- **Caveat:** The flag does not modify an actual network/quantum channel or current simulator counts.

## 6. Detection Explanation

- **Expected Probability:** Analytical probability of measuring zero for the prepared `Ry(angle)|0>` state.
- **Observed Probability:** Frequency of zero for the recovered-qubit bit across simulator shots.
- **Deviation:** `|Observed - Expected|`.
- **Threshold:** Current UI value is `0.15`. It is fixed in this prototype path and is not a universal QDS threshold.
- **Measurement Anomaly:** `deviation > threshold`.
- **Attack Verification:** Separate scenario checks for modified signature marker, identity mismatch, reused session ID, or channel-modified flag.
- **Final Security Decision:** Threat if the detection engine reports an attack or the UI-derived verification booleans fail; otherwise legitimate.

Use this exact explanation when a judge sees normal measurement and threat status:

> “The measured probability stayed within this prototype threshold, so the measurement path reports no anomaly. The independent replay check found that the accepted session ID was reused, so the combined security decision is still a threat. A normal measurement alone does not establish a legitimate session.”

## 7. Results Table

These are the actual qualitative outcomes from the latest validated controlled scenario run. No probability values are included because they vary with the run and are not needed to state the tested behavior.

| Scenario | Measurement anomaly | Verification | Final decision | Primary reason |
|---|---|---|---|---|
| Normal | No | Passed | LEGITIMATE | All verification checks passed |
| Forgery | No | Failed | SECURITY THREAT DETECTED | Signature integrity verification failed |
| Impersonation | No | Failed | SECURITY THREAT DETECTED | Identity verification mismatch detected |
| Replay | No | Failed | SECURITY THREAT DETECTED | Previously used signature/session detected |
| Quantum Channel Manipulation | No | Failed | SECURITY THREAT DETECTED | Quantum channel modification detected |

**Result caveat:** “No measurement anomaly” describes the validated runs only. It is not a guarantee for every message/run. Aer measurements are sampled; the actual probabilities/counts should be read from the current live run. No accuracy, detection-rate, false-positive-rate, or speed benchmark has been established.

## 8. Live Demo Plan (3–5 Minutes)

### Before judges arrive

- Start the app with `python main.py` or `python -m streamlit run ui/ui.py`.
- Open the local page and keep one Streamlit session for the full demo.
- Use one fixed message: `SIH Security Test`.
- Do not clear the event history before demonstrating Replay.
- Ensure a Normal run succeeds before pressing Replay; replay depends on an accepted ID.
- Use the five quick-action buttons only after entering the message. They run the same engine path as the main button.

### Exact presenter script

**0:00–0:20 — Set context**

“First, I will show a baseline verification, then controlled attack cases. The quantum circuit is simulated locally. We report its measurement analysis separately from attack-specific verification.”

**0:20–1:10 — Normal baseline**

- Enter `SIH Security Test`.
- Click **NORMAL TEST**.
- Point to the nine completed processing stages.
- Show Quantum State, Bell State, Completed teleportation, simulator measurement counts, and probabilities.
- Show expected/observed probability, deviation, and the configured threshold.
- Show Attack Verification passed, Detection Summary, LEGITIMATE SIGNATURE VERIFIED, and the accepted session/event.

Say: “This Normal result establishes the session ID that the Replay scenario can reuse.”

**1:10–1:40 — Forgery**

- Click **FORGERY TEST** without changing the message.
- Point to Signature Integrity failure and the primary reason.

Say: “The controlled forgery marker fails the prototype's signature-integrity check. This is a simulation flag, not production cryptographic signature verification.”

**1:40–2:10 — Impersonation**

- Click **IMPERSONATION TEST**.
- Point to the identity mismatch and decision.

Say: “The scenario supplies controlled claimed and actual identities; their mismatch causes the verification failure.”

**2:10–2:40 — Replay**

- Click **REPLAY TEST**.
- Point to the reused ID and event history.
- Emphasize that Measurement Anomaly may say No while Attack Verification says Failed.

Say: “Replay reuses the accepted ID from our Normal run. The measurement result can remain within threshold, but the reused session is still a security threat.”

**2:40–3:10 — Channel manipulation**

- Click **CHANNEL ATTACK TEST**.
- Point to Channel Integrity failure and primary reason.

Say: “This controlled scenario sets the channel-modified flag; the prototype does not alter a real channel or quantum hardware.”

**3:10–3:40 — Wrap**

- Show event history and counters.
- Restate: “Measurement analysis and attack verification are separate inputs to one explainable security decision.”

For a shorter slot, show Normal and Replay only, then explain the other three using the results table.

## 9. Presentation Scripts

### A. 30-second opening

“Good morning. We are presenting SENTINEL-Q for SIH26141: a controlled quantum-security prototype. It uses Qiskit Aer to simulate a message-dependent state, Bell-pair preparation, teleportation, corrections, and measurement. We then combine measurement-deviation analysis with controlled checks for forgery, impersonation, replay, and channel-integrity events. The key point is that a normal measurement does not automatically mean a legitimate session. This is a simulator-based prototype, not a production QDS system.”

### B. 1-minute problem explanation

“Security verification may face different kinds of failure. A forged message, an identity mismatch, a reused session, or a channel-integrity event does not necessarily appear as a large change in one measurement statistic. If a system only watches one signal, it can miss the meaning of protocol-level evidence. Our project uses a controlled environment to demonstrate two distinct paths: probability deviation and scenario-specific verification. We are not claiming that these five cases cover every attack. They let us explain why each check exists and how its result contributes to a final decision. For the final presentation, we will use the exact SIH26141 statement from the official portal.”

### C. 1-minute solution explanation

“SENTINEL-Q accepts a message and scenario, prepares a message-derived state, and runs a three-qubit teleportation circuit through Qiskit Aer. The simulator returns measurement counts; the app derives observed probabilities and deviation from an analytical expected probability. In parallel, the attack engine supplies controlled scenario fields. The detection module evaluates deviation and attack flags, while the UI maps scenario-specific checks and composes the displayed final status. The response engine provides a simulation-only allow/block result, and the session event list records the run. The dashboard exposes the reason, not just a label.”

### D. 1-minute architecture explanation

“The Streamlit UI is the orchestrator. It calls the quantum engine for state/circuit output, calls the attack engine for the selected controlled scenario, and passes the expected probability, observed probability, threshold, and attack record into the detection engine. The UI derives the displayed integrity checks and combines them with the detection result. The response engine maps that decision to simulated session text. Streamlit session state stores used IDs, the last accepted ID, and the event history. This state is local to the current app session; clearing the event log does not clear replay bookkeeping.”

### E. 2-minute technical explanation

“The quantum engine computes a deterministic angle from the first eight hexadecimal characters of the message's SHA-256 digest. It prepares qubit zero using an Ry rotation. It prepares a Bell pair with a Hadamard and CNOT, entangles the input and Bell pair for Bell measurement, and measures two classical bits. Those bits conditionally apply X and Z corrections to the destination qubit, which is then measured. Qiskit Aer executes the circuit locally, 1,024 shots by default. The expected P-zero comes from the rotation-angle formula; observed P-zero comes from counts.

“The detection module calculates absolute deviation and checks whether it exceeds 0.15. That value is a prototype setting in the UI, not a calibrated standard. The attack engine creates controlled records. For example, Replay reuses a previously accepted ID; the UI checks that ID against the session's used-ID set. Forgery and channel manipulation use explicit flags, while impersonation supplies controlled identity values. The UI combines the measurement result with those checks. Therefore, Replay can produce no measurement anomaly and still produce a threat decision. The implementation demonstrates this decision structure; it does not provide a cryptographic QDS implementation, real identity service, real channel attack, or production enforcement.”

### F. 3–5-minute live demo

Use the exact timed sequence in Section 8. Keep the message fixed, establish Normal first, and narrate the distinct measurement and verification results on Replay.

### G. Results explanation

“In our latest controlled runs, Normal passed and each attack scenario produced its expected scenario-specific failed check and reason. The tested runs showed no measurement anomaly. That is not a failed test: Replay demonstrates that a protocol verification can detect reuse even while measured probability remains within threshold. These are functional scenario checks, not a statistically representative performance evaluation.”

### H. Innovation explanation

“Our key idea is to place quantum-circuit simulation, controlled attack cases, probability analysis, and protocol-specific checks in one inspectable workflow. The important design choice is to keep measurement anomaly separate from attack verification. That makes the decision explainable and avoids implying that one statistic represents every security condition. We make no AI/ML claim and do not claim cryptographic novelty.”

### I. Limitations

“This is a controlled simulator prototype. It has no real quantum hardware, deployed communication channel, identity provider, or production cryptographic signature verification. Attack cases are flags and controlled fields. The threshold is a fixed prototype value, and we have not calibrated it or measured false-positive/false-negative rates. Replay state is session-scoped. We state these limits so the demonstration is understood correctly.”

### J. Future scope

“Next steps would begin with a formal threat model and requirements. We could calibrate the statistical threshold using designed experiments, integrate a real channel test harness, define durable replay-state requirements, add a standards-reviewed cryptographic identity/signature layer if required, and expand controlled attack cases. Quantum hardware integration would be an experimental extension, not a drop-in production guarantee. AI/ML is not assumed as a future requirement.”

### K. Final closing statement

“SENTINEL-Q demonstrates how quantum-circuit measurement evidence and scenario-specific security verification can be evaluated separately and combined into one explainable decision. Our results show that a measurement within threshold can still accompany a detected replay. The current system is a controlled, local simulation, and our next work is rigorous calibration and integration. Thank you; we welcome your questions.”

## 10. Member-Wise Speaking Allocation

### Member 1 — Team Lead / System Integration

- **Say:** Opening, architecture hand-off, explanation of module integration, and closing.
- **Demonstrate:** Run order, Normal baseline first, Replay dependency, final dashboard/event history.
- **Prepare for:** Why the UI composes the decision; session-state lifecycle; how to reproduce the demo; what is/is not integrated.

### Member 2 — Quantum Engine

- **Say:** Message-to-angle mapping, qubit state, Bell pair, teleportation, corrections, measurement and Aer counts.
- **Demonstrate:** Quantum State, Bell State, teleportation status, measurement counts/probabilities, circuit drawing if separately prepared.
- **Prepare for:** Qubit/superposition, H/CNOT, Bell measurement, conditional X/Z, simulator versus hardware, why this is not a QDS signature.

### Member 3 — Attack Engine

- **Say:** What each controlled scenario represents and exactly which fields/flags are injected.
- **Demonstrate:** Forgery, Impersonation, Replay, and Channel Attack quick actions.
- **Prepare for:** Why attacks are controlled; why channel manipulation does not alter the circuit; what would be required for realistic attack emulation.

### Member 4 — Detection Engine

- **Say:** Expected/observed probability, absolute deviation, threshold comparison, attack reasons, and combined decision distinction.
- **Demonstrate:** Measurement Analysis beside Attack Verification and Detection Summary.
- **Prepare for:** Why 0.15; anomaly versus verification; false positives/negatives; unused metrics helper; lack of calibration dataset.

### Member 5 — UI / Dashboard

- **Say:** Dashboard navigation, Plotly counts, quick actions, decision explanation, and event history.
- **Demonstrate:** One complete run and where to find all evidence; do not clear event log before Replay.
- **Prepare for:** Streamlit session state, browser/local launch, count visualization, current-session-only counters and history.

### Member 6 — Research / PPT

- **Say:** Problem framing, innovation statement, results caveat, limitations, and future scope.
- **Demonstrate:** Results table and claim-audit slide.
- **Prepare for:** Exact official problem statement wording; evidence behind every claim; why no AI/ML; prototype versus production scope.

## 11. Likely Judge Questions and Concise Answers

1. **What problem does SENTINEL-Q address?**  
   It demonstrates controlled security verification for forgery, impersonation, replay, and channel-integrity scenarios alongside quantum-circuit measurement analysis. Use the official SIH26141 wording when quoting the problem statement.

2. **What is the main idea?**  
   Keep measurement anomaly analysis separate from attack-specific verification, then show how both inform an explainable decision.

3. **Is this real quantum hardware?**  
   No. Qiskit Aer simulates the circuit locally.

4. **Is this a real Quantum Digital Signature system?**  
   No. The UI calls the message-derived simulated state a Quantum Signature, but this prototype does not implement or prove a cryptographic QDS protocol.

5. **Why use a Bell state?**  
   The teleportation circuit needs an entangled Bell pair as a resource. Here it demonstrates the circuit workflow; it is not by itself an attack detector.

6. **Why demonstrate quantum teleportation?**  
   It is part of the project's quantum-processing demonstration. It does not mean matter is transported or that a real communication link is used.

7. **What does the Hadamard gate do here?**  
   It creates a superposition on one qubit as part of Bell-pair preparation and is also applied in the Bell-measurement sequence.

8. **What does CNOT do?**  
   It entangles the Bell-pair qubits and later couples the input with one Bell qubit for the teleportation measurement operations.

9. **What is a qubit?**  
   A quantum two-level system represented by amplitudes for basis states zero and one. In this project it is represented and executed in a simulator.

10. **What is superposition?**  
    A state can have amplitudes for both basis outcomes before measurement. The simulator samples outcomes according to the circuit state.

11. **What is Bell-state measurement?**  
    The circuit applies CNOT and Hadamard operations, then measures two qubits to obtain classical bits used for conditional corrections.

12. **What are Pauli corrections?**  
    Conditional X and Z operations applied to the destination qubit based on the measured classical bits.

13. **How is the message encoded?**  
    The engine hashes the message with SHA-256, takes the first eight hexadecimal digits, maps them to a rotation angle, and prepares an Ry-rotated state. This is prototype state preparation, not secure message signing.

14. **How many shots are run?**  
    The current engine defaults to 1,024 simulator shots.

15. **Where do the probabilities come from?**  
    Expected P-zero is calculated from the rotation angle; observed probabilities are derived from Qiskit Aer measurement counts.

16. **How do you detect forgery?**  
    The controlled Forgery scenario sets a `modified` flag and generates a forged-hash field. The UI maps the flag to signature-integrity failure. It is not a real cryptographic signature comparison.

17. **How do you detect impersonation?**  
    The scenario supplies fixed claimed/actual identity values that differ; the UI compares them and marks identity verification failed. No real identity service is present.

18. **How do you detect replay?**  
    After a Normal session is accepted, the UI reuses its signature/session ID for Replay and checks it against IDs already used in the current Streamlit session.

19. **Does replay work if you press Replay first?**  
    The intended demonstration is to run Normal first. Replay detection depends on an accepted/used session ID in the current app session.

20. **Does clearing the event log clear replay state?**  
    No. Clearing removes the event list only; accepted and used IDs remain in session state.

21. **How is channel manipulation simulated?**  
    The attack engine sets a controlled channel-modified flag. The UI treats that as a failed channel-integrity check. It does not tamper with a real channel or alter the measured circuit counts.

22. **What is the deviation formula?**  
    `|Observed Probability - Expected Probability|`.

23. **What happens when deviation exceeds the threshold?**  
    The measurement path reports an anomaly. The final decision also considers scenario-specific verification.

24. **What if the measurement looks normal but Replay fails?**  
    The final status is still a threat because attack verification is independent of measurement anomaly. This is a central demonstration case.

25. **Why is the threshold 0.15?**  
    It is the current prototype value in the UI. It is not universal or scientifically calibrated; future work would define experiments and calibrate it.

26. **Can users configure the threshold in the dashboard?**  
    Not in the current UI. The value is assigned in the code as a prototype parameter.

27. **What are false positives and false negatives?**  
    A false positive is a legitimate case flagged as a threat; a false negative is an attack case not flagged. This prototype has not measured their rates on a representative labeled dataset.

28. **What detection rate does the system achieve?**  
    We do not claim one. A metrics helper exists, but it is not run against a defined evaluation dataset in the current demo.

29. **Does the attack change the observed probability?**  
    In the current validated scenarios, observed probability comes from the quantum engine. The channel scenario sets a flag; it does not currently alter the circuit counts.

30. **Is the security response enforced on a real connection?**  
    No. The response engine returns simulation-only allow/block and session-status information for the UI.

31. **How is replay state stored?**  
    In Streamlit session state as accepted and used signature/session IDs. It is not durable storage across app restarts.

32. **Can this scale to production?**  
    Scaling has not been evaluated. Production use would require a threat model, secure identity/signature protocol, durable state, channel integration, calibration, and performance/security testing.

33. **Why Qiskit?**  
    The project already uses Qiskit to define quantum circuits and Qiskit Aer to execute them in a local simulator.

34. **Why Python and Streamlit?**  
    Python supports the existing Qiskit modules; Streamlit provides a compact interactive dashboard that connects those modules for the prototype.

35. **How do the modules communicate?**  
    The Streamlit UI imports and calls each Python module, passes returned dictionaries to the next step, and combines outputs for display and session state.

36. **Where is AI/ML?**  
    “AI/ML is not required by our problem statement. Our prototype focuses on quantum simulation, statistical measurement analysis and security verification. We intentionally did not introduce AI/ML where it was not necessary.”

37. **Why are NumPy, SciPy, and pandas listed?**  
    They are declared in `requirements.txt`, but the inspected runtime path does not use them directly. They should not be presented as active components of the current detection flow.

38. **What is the strongest result you can defend?**  
    In the tested controlled scenarios, each attack case produced its expected verification reason, and Replay was detected after Normal established an accepted session. This is functional scenario validation, not a performance benchmark.

## 12. Honest Limitations

- Qiskit Aer simulation, not execution on real quantum hardware.
- State preparation is a deterministic message-to-angle mapping, not a cryptographic signature scheme.
- Forgery, impersonation, replay, and channel cases are controlled scenario data, not attacks against live infrastructure.
- The channel case sets a flag and does not modify the simulator circuit/counts.
- The prototype threshold is fixed in the UI and has no documented calibration study.
- No representative labeled evaluation dataset or reported detection metrics.
- No real user identity provider, network integration, durable database, or production response enforcement.
- Replay bookkeeping is session-scoped.
- The supported scenario set is limited and does not claim comprehensive threat coverage.

Frame these as prototype boundaries and validation work, not as capabilities already delivered.

## 13. Future Scope

1. Define an explicit threat model and exact security protocol requirements.
2. Design controlled statistical experiments and calibrate the prototype threshold; report sample sizes and uncertainty.
3. If required, integrate a standards-reviewed signature/authentication protocol and test key/session lifecycle.
4. Build a channel test harness that demonstrably modifies channel/circuit inputs and records the resulting evidence.
5. Define whether replay state must persist across users/restarts; then select a suitable secure persistence design.
6. Expand attack scenarios and evaluate false positives/false negatives using labeled test cases.
7. Benchmark runtime and simulator shot tradeoffs before making performance claims.
8. Explore real quantum hardware as a separate research experiment when access and circuit compatibility are available.
9. Consider secure communication-platform integration only after protocol and deployment reviews.
10. Do not add AI/ML unless a future requirement and measurable use case justify it.

## 14. PPT Design Guidance

- Use a dark charcoal/navy background with restrained cyan for quantum evidence, green for legitimate outcomes, and red/orange for threats.
- Use one font family with two weights; keep titles and body text consistent.
- Keep visible copy to short phrases. Put caveats in speaker notes or a compact prototype-boundary footer.
- Use actual screenshots from the running dashboard and actual simulator results. Do not fabricate chart values or screenshots.
- Use simple circuit symbols and arrows rather than decorative AI/cyber stock art.
- Keep the architecture diagram, nine-stage workflow, result table, and one real Replay screenshot as the visual anchors.
- Use minimal transitions; no pulsing/glowing effects or dense animations.
- Add a small footer: `SIH26141 | Controlled simulator prototype | No real quantum hardware`.
- Obtain the official SIH slide template and exact problem statement before final export. No official template or statement file was present in this repository.

## 15. Claim Audit

| Claim | Classification | Approved wording / boundary |
|---|---|---|
| Qiskit circuit is executed by Qiskit Aer | IMPLEMENTED / DEMONSTRATED | “A local Aer simulation executes the circuit.” |
| A message-dependent Ry state is prepared | IMPLEMENTED / SIMULATED | “A deterministic message mapping selects an Ry angle in simulation.” |
| Bell-pair operations and teleportation steps exist in the circuit | IMPLEMENTED / SIMULATED | Describe circuit operations; do not imply a real quantum link. |
| Counts and observed probabilities come from simulator output | IMPLEMENTED / DEMONSTRATED | Use the current run's counts and values. |
| Expected P-zero and deviation are calculated | IMPLEMENTED | State the formula and current configured threshold. |
| Threshold 0.15 is universal or calibrated | NOT SUPPORTED | Call it the current prototype parameter only. |
| Controlled Forgery scenario produces signature-integrity failure | SIMULATED / DEMONSTRATED | Explain that the UI maps a controlled `modified` flag; no real signature verification. |
| Controlled Impersonation scenario produces identity mismatch | SIMULATED / DEMONSTRATED | Fixed scenario identity fields; no real authentication provider. |
| Replay of accepted ID is detected within the session | IMPLEMENTED / DEMONSTRATED | Run Normal first; state is session-scoped. |
| Channel-manipulation attack alters channel or quantum counts | NOT SUPPORTED | Current implementation sets a controlled flag only. |
| Final reason is shown for the current decision | IMPLEMENTED / DEMONSTRATED | Quote the reason returned/derived by the existing workflow. |
| Security response blocks actual network traffic | NOT SUPPORTED | Response is simulation-only UI/session state. |
| Production-grade QDS or cryptographic guarantee | NOT SUPPORTED | Explicitly state this prototype does not implement/prove it. |
| Accuracy/detection rate/false-positive rate | NOT SUPPORTED | No evaluation dataset or computed demo metrics. |
| Real quantum hardware integration | FUTURE SCOPE | Not part of current execution. |
| Expanded threats, threshold calibration, real channel integration | FUTURE SCOPE | Present only as proposed work. |
| AI/ML detection | NOT SUPPORTED / NOT USED | State plainly that AI/ML is not used or required. |
| Project has a live polished dashboard | IMPLEMENTED / DEMONSTRATED | Show the actual running Streamlit UI, not a mockup. |

## 16. Final Checklist Before SIH Presentation

### Content and claims

- [ ] Paste the exact official SIH26141 problem statement and follow the official slide template if required.
- [ ] Add team name, member names, institute, and any required SIH identifiers.
- [ ] Keep “simulator,” “controlled scenario,” and “prototype threshold” visible where relevant.
- [ ] Do not label this a real QDS implementation, production quantum security, or an AI system.
- [ ] Do not add invented probability values, performance percentages, or global event counts.
- [ ] Present channel manipulation as a controlled flag, not a real altered channel.

### Demo preparation

- [ ] Launch using the intended Python environment and confirm the Streamlit page loads.
- [ ] Enter the fixed demo message before using quick actions.
- [ ] Run Normal first and confirm the legitimate result.
- [ ] Run Replay in the same app session and show the previously accepted ID is reused.
- [ ] Show that Replay can be a threat while Measurement Anomaly is No.
- [ ] Demonstrate Forgery, Impersonation, and Channel Manipulation with their exact reasons.
- [ ] Keep event history until after Replay; Clear Event Log does not clear replay state.
- [ ] Capture actual screenshots only after fresh runs; ensure visible values come from that run.
- [ ] Have a backup spoken explanation if venue connectivity/browser presentation fails.

### Team readiness

- [ ] Each member knows their hand-off line and one technical boundary.
- [ ] Member 2 can explain the circuit gates and simulator.
- [ ] Member 3 can explain the flags and scenario limitations.
- [ ] Member 4 can explain `|Observed - Expected|`, threshold, and two-path decision.
- [ ] Member 1 can explain session state and repeat the Replay demonstration.
- [ ] Member 6 can distinguish tested behavior from future scope and quote the official challenge accurately.
- [ ] Rehearse within the allotted presentation time and reserve time for judge questions.
