from datetime import datetime
from html import escape

import streamlit as st
import plotly.graph_objects as go

from quantum_engine.quantum_engine import (
    generate_quantum_signature
)

from attack_engine.attack_engine import (
    generate_signature_id,
    simulate_normal,
    simulate_forgery,
    simulate_impersonation,
    simulate_replay,
    simulate_channel_attack
)

from detection_engine.detection_engine import (
    detect_attack
)
from response_engine.response_engine import (
    generate_security_response
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SENTINEL-Q | Quantum Cyber Threat Detection",
    page_icon="🔐",
    layout="wide"
)

st.session_state.setdefault("security_event_log", [])
pending_demo_scenario = st.session_state.pop("pending_demo_scenario", None)
if pending_demo_scenario is not None:
    st.session_state["attack_type_selector"] = pending_demo_scenario

st.markdown(
    """
    <style>
    :root {
        color-scheme: dark;
        --bg: #07131d;
        --bg-alt: #0a1a28;
        --panel: rgba(12, 25, 36, 0.93);
        --panel-strong: rgba(8, 17, 27, 0.98);
        --panel-soft: rgba(15, 34, 48, 0.8);
        --line: rgba(118, 167, 188, 0.17);
        --line-strong: rgba(88, 214, 234, 0.36);
        --text: #edf6fd;
        --muted: #a3b9c9;
        --cyan: #59d6ef;
        --blue: #5ea6ff;
        --green: #70e0b7;
        --green-strong: #3bd39a;
        --red: #ff7a86;
        --orange: #ffb968;
    }
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(18, 99, 124, 0.22), transparent 24%),
            radial-gradient(circle at 90% 12%, rgba(39, 77, 120, 0.18), transparent 22%),
            linear-gradient(180deg, #08131b 0%, #050b11 100%);
        color: var(--text);
        font-family: "Segoe UI", "Inter", sans-serif;
    }
    [data-testid="stHeader"] {
        background: rgba(5, 12, 18, 0.8);
        backdrop-filter: blur(6px);
    }
    .block-container {
        max-width: 1520px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
    }
    h1, h2, h3, h4 {
        color: var(--text);
        font-family: "Segoe UI", "Inter", sans-serif;
    }
    h1 {
        font-size: 2.7rem;
        line-height: 1.1;
        font-weight: 800;
        margin-bottom: 0.2rem;
        letter-spacing: -0.04em;
    }
    .hero-shell {
        border: 1px solid var(--line);
        border-radius: 14px;
        background: linear-gradient(145deg, rgba(12, 26, 35, 0.94), rgba(7, 17, 25, 0.94));
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.22);
        padding: 1.25rem 1.4rem 1rem;
    }
    .hero-kicker {
        color: var(--cyan);
        font-size: 0.71rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin: 0 0 0.6rem;
    }
    .prototype-note {
        color: var(--muted);
        font-size: 0.76rem;
        margin-top: 0.1rem;
    }
    .header-indicators {
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
        margin-top: 0.2rem;
    }
    .header-indicator {
        border-radius: 8px;
        border: 1px solid var(--line);
        background: rgba(10, 22, 30, 0.9);
        color: #d3eaf6;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        padding: 0.55rem 0.75rem;
        text-transform: uppercase;
    }
    .header-indicator.online {
        border-color: rgba(59, 211, 154, 0.34);
        color: #7ce5b8;
    }
    .header-indicator.quantum {
        border-color: rgba(89, 214, 239, 0.3);
        color: var(--cyan);
    }
    .eyebrow {
        color: var(--cyan);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.7rem;
    }
    .overview-panel {
        border: 1px solid var(--line);
        border-radius: 12px;
        background: linear-gradient(145deg, rgba(13, 26, 35, 0.94), rgba(8, 16, 24, 0.96));
        padding: 1rem 1rem 0.8rem;
        box-shadow: 0 14px 28px rgba(0,0,0,0.12);
    }
    .pipeline-track {
        display: grid;
        grid-template-columns: repeat(9, minmax(0, 1fr));
        gap: 0.5rem;
    }
    .pipeline-node {
        position: relative;
        min-height: 78px;
        padding: 0.72rem 0.55rem 0.6rem;
        border-radius: 8px;
        border: 1px solid rgba(89, 214, 239, 0.16);
        background: linear-gradient(180deg, rgba(11, 30, 41, 0.9), rgba(8, 18, 29, 0.9));
        color: #d8edf7;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
    }
    .pipeline-node:not(:last-child)::after {
        content: "→";
        position: absolute;
        right: -0.42rem;
        top: 50%;
        transform: translate(50%, -50%);
        color: var(--cyan);
        font-weight: 700;
        font-size: 0.9rem;
    }
    .pipeline-index {
        display: block;
        color: var(--cyan);
        font-size: 0.6rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        margin-bottom: 0.35rem;
    }
    .pipeline-label {
        display: block;
        font-size: 0.68rem;
        font-weight: 700;
        line-height: 1.35;
    }
    .pipeline-detail {
        display: block;
        color: #91aaba;
        font-size: 0.61rem;
        line-height: 1.35;
        margin-top: 0.28rem;
    }
    .detection-paths {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.7rem;
        margin-top: 0.9rem;
    }
    .detection-path {
        border-left: 2px solid rgba(89, 214, 239, 0.5);
        border-radius: 0 7px 7px 0;
        background: rgba(7, 17, 24, 0.72);
        color: #a8bac8;
        font-size: 0.76rem;
        line-height: 1.55;
        padding: 0.7rem 0.8rem;
    }
    .detection-path strong {
        display: block;
        font-size: 0.67rem;
        letter-spacing: 0.08em;
        color: #d2ecf9;
        margin-bottom: 0.2rem;
        text-transform: uppercase;
    }
    [data-testid="stMetric"] {
        min-height: 104px;
        background: linear-gradient(145deg, rgba(15, 31, 45, 0.94), rgba(8, 18, 27, 0.96));
        border: 1px solid var(--line);
        border-radius: 10px;
        padding: 0.9rem 0.95rem;
        box-shadow: 0 10px 26px rgba(0,0,0,0.08);
    }
    [data-testid="stMetricLabel"] {
        color: #9bb4c3;
        font-size: 0.71rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    [data-testid="stMetricValue"] {
        color: #eaf9ff;
        font-weight: 700;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(145deg, rgba(11, 24, 35, 0.96), rgba(7, 18, 28, 0.96));
        border: 1px solid var(--line);
        border-radius: 12px;
        box-shadow: 0 18px 40px rgba(0,0,0,0.14);
    }
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background: rgba(9, 18, 28, 0.96);
        border: 1px solid rgba(105, 164, 182, 0.32);
        color: var(--text);
    }
    .stButton > button[kind="primary"] {
        min-height: 3.1rem;
        border: 1px solid rgba(89, 214, 239, 0.42);
        background: linear-gradient(90deg, #0d7b92 0%, #196cb0 100%);
        color: #f0fdff;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        box-shadow: 0 15px 28px rgba(22, 118, 145, 0.18);
    }
    .stButton > button[kind="primary"]:hover {
        border-color: rgba(136, 234, 248, 0.8);
        background: linear-gradient(90deg, #0e8ba5 0%, #1d7cc2 100%);
    }
    .scenario-list {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 0.2rem 0 0.8rem;
    }
    .scenario-tag {
        border: 1px solid rgba(119, 163, 189, 0.22);
        background: rgba(12, 28, 39, 0.82);
        color: #bfd5e3;
        font-size: 0.66rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        padding: 0.42rem 0.6rem;
        border-radius: 999px;
    }
    .status-card {
        border: 1px solid var(--line);
        border-radius: 12px;
        background: linear-gradient(180deg, rgba(15, 34, 47, 0.9), rgba(8, 17, 27, 0.96));
        padding: 1rem 1rem 0.8rem;
        min-height: 128px;
    }
    .status-card .value {
        color: #eafaff;
        display: block;
        font-size: 1.08rem;
        font-weight: 800;
        margin-top: 0.4rem;
    }
    .status-card .label {
        color: #9bb4c3;
        display: block;
        font-size: 0.67rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    .status-card .trail {
        display: block;
        color: #7ce5b8;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        margin-top: 0.5rem;
        text-transform: uppercase;
    }
    .status-card .trail.warning {
        color: #fbb96d;
    }
    .status-card .trail.alert {
        color: #ff909c;
    }
    .summary-box {
        border: 1px solid rgba(89, 214, 239, 0.18);
        border-radius: 12px;
        background: linear-gradient(180deg, rgba(8, 22, 32, 0.96), rgba(7, 17, 25, 0.96));
        padding: 1rem 1.1rem;
    }
    .summary-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid rgba(118, 167, 188, 0.14);
        color: #d8ebf8;
        gap: 0.8rem;
        padding: 0.55rem 0;
    }
    .summary-row:last-child {
        border-bottom: none;
        padding-bottom: 0;
    }
    .summary-row span:first-child {
        color: #9dbac7;
        font-size: 0.69rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    .summary-row strong {
        color: #ebfaff;
        font-size: 0.85rem;
        font-weight: 800;
    }
    .summary-row .threat {
        color: #ff989f;
    }
    .summary-row .safe {
        color: #82e4b8;
    }
    .decision-threat {
        border: 1px solid rgba(255, 122, 134, 0.5);
        border-left: 4px solid #ff7a86;
        border-radius: 10px;
        background: linear-gradient(90deg, rgba(79, 30, 38, 0.42), rgba(37, 18, 24, 0.18));
        color: #ffacb2;
        font-size: 1.17rem;
        font-weight: 800;
        line-height: 1.45;
        padding: 0.92rem 1rem;
    }
    .decision-legitimate {
        border: 1px solid rgba(86, 216, 170, 0.42);
        border-left: 4px solid #58d6a6;
        border-radius: 10px;
        background: linear-gradient(90deg, rgba(16, 62, 50, 0.34), rgba(10, 32, 28, 0.18));
        color: #8fe9bf;
        font-size: 1.17rem;
        font-weight: 800;
        line-height: 1.45;
        padding: 0.92rem 1rem;
    }
    .reason-card {
        border: 1px solid var(--line);
        border-radius: 10px;
        background: rgba(7, 18, 26, 0.8);
        color: #d2e7f4;
        line-height: 1.55;
        padding: 0.8rem 0.9rem;
    }
    .reason-label {
        color: #9ab6c7;
        display: block;
        font-size: 0.66rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        margin-bottom: 0.18rem;
        text-transform: uppercase;
    }
    .response-blocked, .response-allowed {
        border-radius: 8px;
        line-height: 1.5;
        padding: 0.8rem 0.9rem;
    }
    .response-blocked {
        background: rgba(80, 25, 35, 0.28);
        border: 1px solid rgba(255, 122, 134, 0.38);
        color: #ffadb6;
    }
    .response-allowed {
        background: rgba(14, 62, 49, 0.24);
        border: 1px solid rgba(110, 222, 177, 0.35);
        color: #b5efcd;
    }
    .verification-note {
        color: var(--muted);
        font-size: 0.76rem;
        line-height: 1.5;
        margin: 0 0 0.7rem;
    }
    .processing-label {
        color: #9dbac7;
        font-size: 0.66rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        margin-bottom: 0.35rem;
        text-transform: uppercase;
    }
    .processing-value {
        color: #ddf6ff;
        font-size: 0.83rem;
        font-weight: 700;
        line-height: 1.5;
        overflow-wrap: anywhere;
    }
    .processing-checklist {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.55rem;
    }
    .processing-step {
        border: 1px solid rgba(112, 224, 183, 0.2);
        border-radius: 8px;
        background: rgba(9, 31, 31, 0.58);
        color: #ccebdd;
        font-size: 0.76rem;
        font-weight: 650;
        line-height: 1.4;
        padding: 0.65rem 0.75rem;
    }
    .processing-step strong {
        color: #70e0b7;
        margin-right: 0.4rem;
    }
    .why-card {
        border-left: 3px solid var(--cyan);
        border-radius: 0 8px 8px 0;
        background: rgba(8, 24, 34, 0.82);
        color: #d4e9f4;
        line-height: 1.55;
        margin-top: 0.75rem;
        padding: 0.75rem 0.85rem;
    }
    .why-card strong {
        color: var(--cyan);
        display: block;
        font-size: 0.66rem;
        letter-spacing: 0.1em;
        margin-bottom: 0.2rem;
    }
    .event-log {
        border: 1px solid var(--line);
        border-radius: 10px;
        background: rgba(7, 16, 24, 0.7);
        overflow-x: auto;
    }
    .event-row, .event-heading {
        align-items: start;
        display: grid;
        gap: 0.75rem;
        grid-template-columns: 72px minmax(120px, 1.1fr) minmax(120px, 1.2fr) 88px 88px 88px 84px 90px 110px 150px 170px 200px;
        min-width: 1460px;
        padding: 0.8rem 0.9rem;
    }
    .event-heading {
        background: rgba(23, 47, 63, 0.56);
        border-bottom: 1px solid var(--line);
        color: #8ea9b9;
        font-size: 0.64rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    .event-row {
        border-bottom: 1px solid rgba(118, 167, 188, 0.12);
        color: #cce3f0;
        font-size: 0.75rem;
        line-height: 1.45;
    }
    .event-row:last-child {
        border-bottom: none;
    }
    .event-status {
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.04em;
    }
    .event-status.legitimate {
        color: #7fe7b8;
    }
    .event-status.threat {
        color: #ff9da6;
    }
    .event-empty {
        border: 1px dashed rgba(118, 167, 188, 0.22);
        border-radius: 10px;
        color: var(--muted);
        padding: 1.3rem;
        text-align: center;
    }
    [data-testid="stExpander"] {
        border-color: var(--line);
        border-radius: 10px;
        background: rgba(8, 17, 27, 0.7);
    }
    [data-testid="stExpander"] summary {
        color: #d7eff8;
    }
    div[data-testid="stPlotlyChart"] {
        border: 1px solid rgba(118, 167, 188, 0.15);
        border-radius: 10px;
        overflow: hidden;
    }
    @media (max-width: 720px) {
        .pipeline-track {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
        .pipeline-node:not(:last-child)::after { display: none; }
        .detection-paths { grid-template-columns: 1fr; }
        .processing-checklist { grid-template-columns: 1fr 1fr; }
        .event-row, .event-heading { padding-left: 0.7rem; padding-right: 0.7rem; }
        h1 { font-size: 2.1rem; }
    }
    </style>
    """,
    unsafe_allow_html=True
)


def render_header_indicators(container, quantum_engine_ready):
    quantum_label = (
        "● QUANTUM ENGINE READY"
        if quantum_engine_ready
        else "● QUANTUM ENGINE IDLE"
    )
    container.markdown(
        "<div class='header-indicators'>"
        "<div class='header-indicator online'>● QUANTUM SECURITY SYSTEM ACTIVE</div>"
        f"<div class='header-indicator quantum'>{quantum_label}</div>"
        "</div>",
        unsafe_allow_html=True
    )


def select_demo_scenario(scenario):
    st.session_state["pending_demo_scenario"] = scenario
    st.session_state["demo_run_requested"] = True


def render_live_status(container, scenarios):
    event_log = st.session_state.security_event_log
    legitimate_count = sum(
        event["status"] == "LEGITIMATE"
        for event in event_log
    )
    threat_count = len(event_log) - legitimate_count
    quantum_status = (
        "ACTIVE"
        if st.session_state.get("quantum_engine_operational", False)
        else "AWAITING RUN"
    )
    attack_status = "READY"
    detection_status = "ACTIVE"

    with container.container():
        status_cols = st.columns(5)
        with status_cols[0]:
            st.markdown(
                "<div class='status-card'><span class='label'>Quantum Engine</span><span class='value'>" + quantum_status + "</span><span class='trail'>Quantum simulation</span></div>",
                unsafe_allow_html=True
            )
        with status_cols[1]:
            st.markdown(
                "<div class='status-card'><span class='label'>Attack Engine</span><span class='value'>" + attack_status + "</span><span class='trail'>" + str(len(scenarios)) + " scenarios</span></div>",
                unsafe_allow_html=True
            )
        with status_cols[2]:
            st.markdown(
                "<div class='status-card'><span class='label'>Detection Engine</span><span class='value'>" + detection_status + "</span><span class='trail'>Verification checks</span></div>",
                unsafe_allow_html=True
            )
        with status_cols[3]:
            st.markdown(
                "<div class='status-card'><span class='label'>Events</span><span class='value'>" + str(len(event_log)) + "</span><span class='trail'>Session log</span></div>",
                unsafe_allow_html=True
            )
        with status_cols[4]:
            st.markdown(
                "<div class='status-card'><span class='label'>Threats Detected</span><span class='value'>" + str(threat_count) + "</span><span class='trail warning'>Live detection</span></div>",
                unsafe_allow_html=True
            )


def render_security_response(container, security_response):
    is_allowed = security_response["session_allowed"]
    response_class = "response-allowed" if is_allowed else "response-blocked"
    response_symbol = "✓" if is_allowed else "✕"

    with container.container(border=True):
        st.markdown(
            "<p class='eyebrow'>SECURITY RESPONSE</p>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div class='{response_class}'>"
            f"<strong>{response_symbol} {escape(security_response['action'])}</strong>"
            "</div>",
            unsafe_allow_html=True
        )
        st.write("**Action**", security_response["action_detail"])
        st.write("**Session Status**", security_response["session_status"])
        if security_response["communication_compromised"]:
            st.warning("Communication marked as compromised in this simulation.")


def render_quantum_processing(container, quantum_result):
    with container.container(border=True):
        st.markdown(
            "<p class='eyebrow'>QUANTUM EVIDENCE</p>",
            unsafe_allow_html=True
        )
        if not quantum_result:
            st.caption("Quantum output will appear after verification.")
            return

        state_col, bell_col, teleport_col, measurement_col = st.columns(4)
        with state_col:
            st.markdown("<div class='processing-label'>Quantum State</div>", unsafe_allow_html=True)
            st.code(quantum_result["quantum_state"])
        with bell_col:
            st.markdown("<div class='processing-label'>Bell State</div>", unsafe_allow_html=True)
            st.code(quantum_result["bell_state"])
        with teleport_col:
            st.markdown("<div class='processing-label'>Teleportation</div>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='processing-value'>✓ {escape(str(quantum_result['teleportation']))}</div>",
                unsafe_allow_html=True
            )
        with measurement_col:
            counts = quantum_result["measurement"]
            st.markdown("<div class='processing-label'>Measurement</div>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='processing-value'>✓ Generated · {len(counts)} outcomes · {sum(counts.values())} shots</div>",
                unsafe_allow_html=True
            )
        count_lines = "\n".join(
            f"|{state}⟩  {count}"
            for state, count in sorted(counts.items())
        )
        st.code(count_lines or "No measurement counts")
        probability_zero_col, probability_one_col = st.columns(2)
        with probability_zero_col:
            st.metric("Probability of |0⟩", f"{quantum_result['probability_zero']:.4f}")
        with probability_one_col:
            st.metric("Probability of |1⟩", f"{quantum_result['probability_one']:.4f}")


# ============================================================
# HEADER
# ============================================================

scenario_options = [
    "Normal",
    "Forgery",
    "Impersonation",
    "Replay",
    "Quantum Channel Manipulation"
]

hero_col, indicator_col = st.columns([3, 1])

with hero_col:
    st.markdown(
        "<div class='hero-shell'>"
        "<p class='hero-kicker'>SIH26141 | Controlled Quantum Security Prototype</p>"
        "<h1>SENTINEL-Q</h1>"
        "<h3>Quantum-Inspired Cyber Threat Detection &amp; Prevention</h3>"
        "<div class='prototype-note'>Quantum Simulation: ACTIVE · Controlled prototype · No real quantum hardware</div>"
        "</div>",
        unsafe_allow_html=True
    )

with indicator_col:
    header_indicator_placeholder = st.empty()
    render_header_indicators(
        header_indicator_placeholder,
        st.session_state.get("quantum_engine_operational", False)
    )

st.markdown("<p class='eyebrow'>SYSTEM OVERVIEW</p>", unsafe_allow_html=True)
pipeline_steps = [
    ("MESSAGE", "Input payload"),
    ("QUANTUM SIGNATURE", "Encode message state"),
    ("BELL STATE", "Entangle qubits"),
    ("QUANTUM TELEPORTATION", "Transfer quantum state"),
    ("ATTACK / SECURITY SCENARIO", "Run controlled scenario"),
    ("MEASUREMENT", "Read simulator output"),
    ("STATISTICAL ANALYSIS", "Compare deviation"),
    ("ATTACK VERIFICATION", "Check protocol integrity"),
    ("SECURITY DECISION", "Allow or block session")
]
pipeline_markup = "".join(
    "<div class='pipeline-node'>"
    f"<span class='pipeline-index'>{index:02d}</span>"
    f"<span class='pipeline-label'>{escape(step)}</span>"
    f"<span class='pipeline-detail'>{escape(detail)}</span>"
    "</div>"
    for index, (step, detail) in enumerate(pipeline_steps, start=1)
)
st.markdown(
    "<div class='overview-panel'>"
    f"<div class='pipeline-track'>{pipeline_markup}</div>"
    "<div class='detection-paths'>"
    "<div class='detection-path'><strong>MEASUREMENT ANALYSIS</strong>Checks statistical deviation against the configured threshold.</div>"
    "<div class='detection-path'><strong>ATTACK VERIFICATION</strong>Checks scenario-specific security conditions. Both paths inform the final security decision.</div>"
    "</div></div>",
    unsafe_allow_html=True
)

status_placeholder = st.empty()
render_live_status(status_placeholder, scenario_options)

scenario_markup = "".join(
    f"<span class='scenario-tag'>{escape(scenario.upper())}</span>"
    for scenario in scenario_options
)
st.markdown(
    "<p class='eyebrow'>CONTROLLED SECURITY SCENARIOS</p>"
    f"<div class='scenario-list'>{scenario_markup}</div>",
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# INPUT SECTION
# ============================================================

with st.container(border=True):
    st.markdown("<p class='eyebrow'>SECURITY VERIFICATION</p>", unsafe_allow_html=True)
    st.markdown(
        "<div class='verification-note'>Run the selected controlled scenario through the quantum simulator and security verification checks.</div>",
        unsafe_allow_html=True
    )
    input_col, scenario_col = st.columns([2, 1])

    with input_col:
        message = st.text_input(
            "Enter Message",
            placeholder="Example: Transfer request approved"
        )

    with scenario_col:
        attack_type = st.selectbox(
            "Select Simulation Scenario",
            scenario_options,
            key="attack_type_selector"
        )

    run_verification = st.button(
        "⚡ GENERATE & VERIFY",
        type="primary",
        use_container_width=True
    )

st.markdown("<p class='eyebrow'>DEMO SCENARIOS</p>", unsafe_allow_html=True)
demo_cols = st.columns(5)
demo_scenarios = [
    ("NORMAL TEST", "Normal"),
    ("FORGERY TEST", "Forgery"),
    ("IMPERSONATION TEST", "Impersonation"),
    ("REPLAY TEST", "Replay"),
    ("CHANNEL ATTACK TEST", "Quantum Channel Manipulation")
]
for demo_col, (label, scenario) in zip(demo_cols, demo_scenarios):
    with demo_col:
        st.button(
            label,
            key=f"demo_{scenario}",
            use_container_width=True,
            on_click=select_demo_scenario,
            args=(scenario,)
        )

run_verification = run_verification or st.session_state.pop(
    "demo_run_requested",
    False
)

quantum_processing_placeholder = st.empty()
render_quantum_processing(
    quantum_processing_placeholder,
    st.session_state.get("latest_quantum_result")
)

# ============================================================
# VERIFY BUTTON
# ============================================================

if run_verification:

    if not message.strip():

        st.warning(
            "Please enter a message before verification."
        )

        st.stop()


    # ========================================================
    # SIGNATURE / SESSION ID
    # ========================================================

    used_signature_ids = st.session_state.setdefault(
        "used_signature_ids",
        set()
    )

    signature_id = generate_signature_id(message)


    # ========================================================
    # QUANTUM ENGINE
    # ========================================================

    with st.spinner(
        "Running quantum simulation..."
    ):

        quantum_result = generate_quantum_signature(
            message
        )

    st.session_state["latest_quantum_result"] = quantum_result
    render_quantum_processing(
        quantum_processing_placeholder,
        quantum_result
    )


    # ========================================================
    # MEASUREMENT
    # ========================================================

    expected_probability = (
        quantum_result[
            "expected_probability_zero"
        ]
    )

    normal_observed_probability = (
        quantum_result[
            "probability_zero"
        ]
    )

    observed_probability = normal_observed_probability


    # ========================================================
    # ATTACK ENGINE
    # ========================================================

    if attack_type == "Normal":

        attack_result = simulate_normal(
            message,
            signature_id
        )


    elif attack_type == "Forgery":

        attack_result = simulate_forgery(
            message,
            signature_id
        )


    elif attack_type == "Impersonation":

        attack_result = simulate_impersonation(
            message,
            signature_id
        )


    elif attack_type == "Replay":

        previously_accepted_signature_id = st.session_state.get(
            "last_accepted_signature_id"
        )

        if previously_accepted_signature_id is not None:
            signature_id = previously_accepted_signature_id

        attack_result = simulate_replay(
            message,
            signature_id
        )

        attack_result["replayed"] = (
            signature_id in used_signature_ids
        )


    else:

        attack_result = simulate_channel_attack(
            message,
            signature_id
        )


    # ========================================================
    # DETECTION ENGINE
    # ========================================================

    threshold = 0.15

    detection_result = detect_attack(
        expected_probability,
        observed_probability,
        threshold,
        attack_result
    )

    signature_integrity = (
        not attack_result.get("modified", False)
        if attack_type == "Forgery"
        else True
    )

    identity_verified = None
    if attack_type == "Impersonation":
        claimed_identity = attack_result.get("claimed_identity")
        actual_identity = attack_result.get("actual_identity")
        identity_verified = (
            claimed_identity is not None
            and actual_identity is not None
            and claimed_identity == actual_identity
        )

    replay_detected = bool(
        attack_result.get("replayed", False)
    )
    channel_integrity = not bool(
        attack_result.get("channel_modified", False)
    )

    measurement_analysis = {
        "expected": expected_probability,
        "observed": observed_probability,
        "deviation": detection_result["deviation"],
        "threshold": threshold,
        "threshold_exceeded": detection_result["threshold_exceeded"]
    }

    attack_verification = {
        "signature_integrity": signature_integrity,
        "identity_verified": identity_verified,
        "replay_detected": replay_detected,
        "channel_integrity": channel_integrity
    }

    verification_failed = (
        not signature_integrity
        or identity_verified is False
        or replay_detected
        or not channel_integrity
    )

    if not signature_integrity:
        primary_reason = "Signature integrity verification failed"
    elif identity_verified is False:
        primary_reason = "Identity verification mismatch detected"
    elif replay_detected:
        primary_reason = "Previously used signature/session detected"
    elif not channel_integrity:
        primary_reason = "Quantum channel modification detected"
    elif measurement_analysis["threshold_exceeded"]:
        primary_reason = "Measurement deviation exceeded threshold"
    else:
        primary_reason = "All verification checks passed"

    security_decision = {
        "status": (
            "SECURITY THREAT DETECTED"
            if detection_result["attack_detected"] or verification_failed
            else "LEGITIMATE"
        ),
        "attack_type": attack_result["attack"],
        "primary_reason": primary_reason,
        "measurement_analysis": measurement_analysis,
        "attack_verification": attack_verification
    }

    security_response = generate_security_response(
        security_decision,
        attack_type,
        attack_verification
    )

    st.session_state.security_event_log.append({
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "scenario": security_decision["attack_type"],
        "signature_id": signature_id,
        "expected": measurement_analysis["expected"],
        "observed": measurement_analysis["observed"],
        "deviation": measurement_analysis["deviation"],
        "threshold": measurement_analysis["threshold"],
        "measurement_anomaly": measurement_analysis["threshold_exceeded"],
        "attack_verification": "Failed" if verification_failed else "Passed",
        "status": security_decision["status"],
        "primary_reason": security_decision["primary_reason"],
        "security_response": security_response.copy(),
        "session_allowed": security_response["session_allowed"]
    })

    quantum_engine_operational = (
        isinstance(quantum_result, dict)
        and bool(quantum_result.get("quantum_state"))
        and bool(quantum_result.get("bell_state"))
        and quantum_result.get("teleportation") == "Completed"
        and bool(quantum_result.get("measurement"))
        and "expected_probability_zero" in quantum_result
        and "probability_zero" in quantum_result
    )

    st.session_state["quantum_engine_operational"] = quantum_engine_operational
    render_live_status(status_placeholder, scenario_options)

    if security_response["mark_signature_used"]:
        used_signature_ids.add(signature_id)

    if security_response["session_allowed"]:
        used_signature_ids.add(signature_id)
        if attack_type == "Normal":
            st.session_state["last_accepted_signature_id"] = signature_id


    render_header_indicators(
        header_indicator_placeholder,
        quantum_engine_operational
    )

    st.markdown(
        "<p class='eyebrow'>LIVE SECURITY DASHBOARD</p>",
        unsafe_allow_html=True
    )

    processing_steps = [
        ("Message Received", bool(message.strip())),
        ("Quantum Signature Generated", bool(quantum_result.get("quantum_state"))),
        ("Bell State Prepared", bool(quantum_result.get("bell_state"))),
        ("Teleportation Completed", quantum_result.get("teleportation") == "Completed"),
        ("Security Scenario Applied", bool(attack_result.get("attack"))),
        ("Measurement Completed", bool(quantum_result.get("measurement"))),
        ("Statistical Analysis Completed", "deviation" in detection_result),
        ("Attack Verification Completed", bool(attack_verification)),
        ("Security Decision Generated", bool(security_decision.get("status")))
    ]
    processing_markup = "".join(
        "<div class='processing-step'><strong>✓</strong>"
        f"{escape(label)}</div>"
        for label, completed in processing_steps
        if completed
    )
    with st.container(border=True):
        st.markdown("<p class='eyebrow'>PROCESSING STATUS</p>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='processing-checklist'>{processing_markup}</div>",
            unsafe_allow_html=True
        )

    pipeline_col, decision_col = st.columns([1.08, 0.92], gap="large")

    with pipeline_col:
        with st.container(border=True):
            st.markdown(
                "<p class='eyebrow'>2 · QUANTUM PIPELINE</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<div class='pipeline-flow'>"
                "<strong>MESSAGE</strong> → <strong>QUANTUM SIGNATURE</strong> → "
                "<strong>BELL STATE</strong> → <strong>TELEPORTATION</strong> → "
                "<strong>ATTACK SCENARIO</strong> → <strong>MEASUREMENT</strong> → "
                "<strong>STATISTICAL ANALYSIS</strong> → <strong>ATTACK VERIFICATION</strong> → "
                "<strong>SECURITY DECISION</strong>"
                "</div>",
                unsafe_allow_html=True
            )
            st.divider()
            st.write("**Message**")
            st.code(message)
            st.write("✓ **Quantum Signature**")
            st.code(quantum_result["quantum_state"])
            st.write("✓ **Bell State**")
            st.code(quantum_result["bell_state"])
            st.write("✓ **Teleportation**")
            st.success(quantum_result["teleportation"])
            st.write("✓ **Measurement**")
            measurement_counts = quantum_result["measurement"]
            measurement_total = sum(measurement_counts.values())
            st.caption(
                f"{len(measurement_counts)} measured states · "
                f"{measurement_total} simulator shots"
            )
            st.write("✓ **Statistical Analysis**")
            st.caption(
                f"Deviation {measurement_analysis['deviation']:.4f} "
                f"against the configured prototype threshold {measurement_analysis['threshold']:.4f}"
            )

    with decision_col:
        with st.container(border=True):
            st.markdown(
                "<p class='eyebrow'>4 · ATTACK SIMULATION</p>",
                unsafe_allow_html=True
            )
            st.write("**Scenario:**", security_decision["attack_type"])
            st.write("**Signature / Session:**", signature_id)

            if attack_result.get("modified", False):
                st.warning("Controlled modification applied")
            elif attack_result.get("replayed", False):
                st.warning("Previously used signature detected")
            else:
                st.success("No attack modification")

            st.divider()
            st.markdown(
                "<p class='eyebrow'>6 · FINAL SECURITY DECISION</p>",
                unsafe_allow_html=True
            )

            if security_decision["status"] == "SECURITY THREAT DETECTED":
                st.markdown(
                    f"<div class='decision-threat'>⚠ {security_decision['status']}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    "<div class='decision-legitimate'>✓ LEGITIMATE SIGNATURE VERIFIED</div>",
                    unsafe_allow_html=True
                )

            st.write("**Attack Type**", security_decision["attack_type"])
            st.markdown(
                "<div class='reason-card'>"
                "<div class='reason-label'>Primary Detection Reason</div>"
                f"{security_decision['primary_reason']}"
                "</div>",
                unsafe_allow_html=True
            )
            explanation_heading = (
                "WHY WAS THIS DETECTED?"
                if security_decision["status"] == "SECURITY THREAT DETECTED"
                else "WHY IS THIS LEGITIMATE?"
            )
            st.markdown(
                "<div class='why-card'><strong>"
                + explanation_heading
                + "</strong>"
                + escape(security_decision["primary_reason"])
                + "</div>",
                unsafe_allow_html=True
            )
            st.write("")

            check_col1, check_col2 = st.columns(2)
            with check_col1:
                st.caption("MEASUREMENT")
                st.write(
                    "⚠ ANOMALY"
                    if measurement_analysis["threshold_exceeded"]
                    else "✓ NORMAL"
                )
            with check_col2:
                st.caption("ATTACK VERIFICATION")
                st.write("✕ FAILED" if verification_failed else "✓ PASSED")

            render_security_response(st, security_response)

    st.divider()
    st.markdown(
        "<p class='eyebrow'>3 · QUANTUM MEASUREMENT ANALYSIS</p>",
        unsafe_allow_html=True
    )

    with st.container(border=True):
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        with metric_col1:
            st.metric(
                "Expected Probability",
                f"{measurement_analysis['expected']:.4f}"
            )
        with metric_col2:
            st.metric(
                "Observed Probability",
                f"{measurement_analysis['observed']:.4f}"
            )
        with metric_col3:
            st.metric(
                "Deviation",
                f"{measurement_analysis['deviation']:.4f}"
            )
        with metric_col4:
            st.metric(
                "Configured Threshold",
                f"{measurement_analysis['threshold']:.4f}"
            )

        measurement_status = (
            "⚠ Measurement Anomaly Detected"
            if measurement_analysis["threshold_exceeded"]
            else "✓ Measurement Within Threshold"
        )
        measurement_status_class = (
            "threat"
            if measurement_analysis["threshold_exceeded"]
            else "safe"
        )
        st.markdown(
            "<div class='summary-box'><div class='summary-row'><span>Measurement Status</span><strong class='"
            + measurement_status_class
            + "'>"
            + measurement_status
            + "</strong></div><div class='summary-row'><span>Configured Prototype Threshold</span><strong>"
            + f"{measurement_analysis['threshold']:.4f}"
            + "</strong></div></div>",
            unsafe_allow_html=True
        )

    measurement_states = sorted(measurement_counts)
    fig = go.Figure(
        go.Bar(
            x=measurement_states,
            y=[measurement_counts[state] for state in measurement_states],
            marker_color="#27bfd5",
            marker_line_color="#72e3ef",
            marker_line_width=0.5,
            hovertemplate="State %{x}<br>Counts %{y}<extra></extra>"
        )
    )
    fig.update_layout(
        template="plotly_dark",
        title="Quantum Measurement Distribution",
        xaxis_title="Measured State",
        yaxis_title="Counts",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(8,17,29,0.72)",
        font={"color": "#d8e8f3", "family": "Segoe UI, sans-serif"},
        xaxis={"gridcolor": "rgba(75,110,135,0.16)"},
        yaxis={"gridcolor": "rgba(75,110,135,0.28)"},
        margin={"l": 12, "r": 12, "t": 55, "b": 12},
        height=330
    )
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    signature_integrity_status = (
        "✓ Passed"
        if attack_verification["signature_integrity"]
        else "✕ Signature integrity verification failed"
    )
    identity_status = (
        "Not applicable"
        if attack_verification["identity_verified"] is None
        else (
            "✓ Identity verified"
            if attack_verification["identity_verified"]
            else "✕ Identity verification mismatch detected"
        )
    )
    replay_status = (
        "✕ Previously used signature/session detected"
        if attack_verification["replay_detected"]
        else "✓ No replay detected"
    )
    channel_integrity_status = (
        "✓ Passed"
        if attack_verification["channel_integrity"]
        else "✕ Quantum channel modification detected"
    )

    if attack_type == "Normal":
        verification_rows = [
            ("Signature Integrity", signature_integrity_status),
            ("Identity Verification", identity_status),
            ("Replay Status", replay_status),
            ("Channel Integrity", channel_integrity_status)
        ]
    elif attack_type == "Forgery":
        verification_rows = [("Signature Integrity", signature_integrity_status)]
    elif attack_type == "Impersonation":
        verification_rows = [("Identity Verification", identity_status)]
    elif attack_type == "Replay":
        verification_rows = [("Replay Status", replay_status)]
    else:
        verification_rows = [("Channel Integrity", channel_integrity_status)]

    verification_col, summary_col = st.columns([1, 1], gap="large")

    with verification_col:
        with st.container(border=True):
            st.markdown(
                "<p class='eyebrow'>5 · ATTACK VERIFICATION</p>",
                unsafe_allow_html=True
            )
            for label, status in verification_rows:
                st.write(f"**{label}**", status)

    with summary_col:
        with st.container(border=True):
            st.markdown(
                "<p class='eyebrow'>DETECTION SUMMARY</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<div class='summary-box'>"
                "<div class='summary-row'><span>Measurement Anomaly</span><strong class='" + ("threat" if measurement_analysis["threshold_exceeded"] else "safe") + "'>" + ("⚠ Yes" if measurement_analysis["threshold_exceeded"] else "✓ No") + "</strong></div>"
                "<div class='summary-row'><span>Attack Verification</span><strong class='" + ("threat" if verification_failed else "safe") + "'>" + ("✕ Failed" if verification_failed else "✓ Passed") + "</strong></div>"
                "<div class='summary-row'><span>Attack Type</span><strong>" + str(security_decision["attack_type"]) + "</strong></div>"
                "<div class='summary-row'><span>Final Status</span><strong class='" + ("threat" if security_decision["status"] == "SECURITY THREAT DETECTED" else "safe") + "'>" + str(security_decision["status"]) + "</strong></div>"
                "</div>",
                unsafe_allow_html=True
            )
            st.caption("A normal measurement does not imply a normal security state; both paths inform the final decision independently.")

    with st.expander("View structured security decision"):
        st.json(security_decision)

    with st.expander("🔬 View Quantum Simulation Data"):
        st.write("Measurement Counts")
        st.json(quantum_result["measurement"])
        st.write(
            "Probability of |0⟩:",
            quantum_result["probability_zero"]
        )
        st.write(
            "Probability of |1⟩:",
            quantum_result["probability_one"]
        )


# ============================================================
# SECURITY EVENT LOG
# ============================================================

st.divider()
log_title_col, clear_log_col = st.columns([3, 1])

with log_title_col:
    st.markdown(
        "<p class='eyebrow'>🛡 SECURITY EVENT LOG</p>",
        unsafe_allow_html=True
    )

with clear_log_col:
    if st.button("Clear Event Log", use_container_width=True):
        st.session_state.security_event_log = []
        st.rerun()

security_event_log = st.session_state.security_event_log
legitimate_events = sum(
    event["status"] == "LEGITIMATE"
    for event in security_event_log
)
threat_events = len(security_event_log) - legitimate_events

total_col, legitimate_col, threat_col = st.columns(3)
with total_col:
    st.metric("Total Events", len(security_event_log))
with legitimate_col:
    st.metric("Legitimate Events", legitimate_events)
with threat_col:
    st.metric("Threats Detected", threat_events)

if security_event_log:
    event_rows = "".join(
        "<div class='event-row'>"
        f"<span class='event-time'>{escape(str(event['timestamp']))}</span>"
        f"<span>{escape(str(event['scenario']))}</span>"
        f"<span class='event-signature'>{escape(str(event['signature_id']))}</span>"
        f"<span>{event['expected']:.4f}</span>"
        f"<span>{event['observed']:.4f}</span>"
        f"<span>{event['deviation']:.4f}</span>"
        f"<span>{event['threshold']:.4f}</span>"
        f"<span class='event-check'>{'⚠ YES' if event['measurement_anomaly'] else '✓ NO'}</span>"
        f"<span class='event-check'>{escape(str(event['attack_verification']).upper())}</span>"
        f"<span class='event-status {'legitimate' if event['status'] == 'LEGITIMATE' else 'threat'}'>"
        f"{'✓ LEGITIMATE' if event['status'] == 'LEGITIMATE' else '⚠ THREAT DETECTED'}</span>"
        f"<span>{escape(str(event['primary_reason']))}</span>"
        "</div>"
        for event in security_event_log
    )
    st.markdown(
        "<div class='event-log'>"
        "<div class='event-heading'>"
        "<span>TIME</span><span>SCENARIO</span><span>SIGNATURE ID</span>"
        "<span>EXPECTED</span><span>OBSERVED</span><span>DEVIATION</span><span>THRESHOLD</span>"
        "<span>MEAS ANOMALY</span><span>ATTACK VERIFICATION</span><span>FINAL STATUS</span><span>PRIMARY REASON</span>"
        "</div>"
        f"{event_rows}</div>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<div class='event-empty'>No verification events in this session.</div>",
        unsafe_allow_html=True
    )