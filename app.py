import streamlit as st

# ==========================================================
# IMPORT PAGES
# ==========================================================

from modules.spiral.page import show as spiral_page
from modules.voice.page import show as voice_page
from modules.fingertap.page import show as fingertap_page

# Uncomment when Summary page is ready
# from modules.summary.page import show as summary_page

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(page_title="NeuroSketch", page_icon="🧠", layout="wide")

# ==========================================================
# SESSION STATE
# ==========================================================

defaults = {
    "step": 0,
    "spiral_completed": False,
    "voice_completed": False,
    "fingertap_completed": False,
    "results": {
        "spiral": None,
        "voice": None,
        "fingertap": None,
    },
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==========================================================
# HELPERS
# ==========================================================

LAST_STEP = 4


def next_step():
    if st.session_state.step < LAST_STEP:
        st.session_state.step += 1


def previous_step():
    if st.session_state.step > 0:
        st.session_state.step -= 1


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🧠 NeuroSketch")

    st.divider()

    progress = st.session_state.step / LAST_STEP
    st.progress(progress)

    st.write(f"Step {st.session_state.step + 1} of {LAST_STEP + 1}")

    st.divider()

    pages = [
        "Disclaimer",
        "Spiral Test",
        "Voice Test",
        "Finger Tapping",
        "Summary",
    ]

    for index, page in enumerate(pages):

        if index < st.session_state.step:
            st.success(f"✓ {page}")

        elif index == st.session_state.step:
            st.info(f"● {page}")

        else:
            st.write(f"○ {page}")

# ==========================================================
# DISCLAIMER
# ==========================================================

if st.session_state.step == 0:

    st.title("NeuroSketch Assessment")

    st.warning(
        """
## Prototype Disclaimer

NeuroSketch is an educational AI prototype.

- It is NOT a medical device.
- It cannot diagnose Parkinson's disease.
- Results are for educational and demonstration purposes only.
- Some modules are still under development.
"""
    )

    accepted = st.checkbox("I understand the disclaimer.")

    if st.button("Start Assessment ➜", use_container_width=True):

        if accepted:
            next_step()
            st.rerun()

        else:
            st.error("Please accept the disclaimer.")

# ==========================================================
# SPIRAL
# ==========================================================

elif st.session_state.step == 1:

    spiral_page()

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "⬅ Back",
            use_container_width=True,
            key="spiral_back",
        ):
            previous_step()
            st.rerun()

    with col2:

        if st.button(
            "Next ➜",
            disabled=not st.session_state.spiral_completed,
            use_container_width=True,
            key="spiral_next",
        ):
            next_step()
            st.rerun()

    with col3:

        if st.button(
            "Skip",
            use_container_width=True,
            key="spiral_skip",
        ):
            st.session_state.results["spiral"] = "Skipped"
            st.session_state.spiral_completed = True
            next_step()
            st.rerun()

# ==========================================================
# VOICE
# ==========================================================

elif st.session_state.step == 2:

    voice_page()

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "⬅ Back",
            use_container_width=True,
            key="voice_back",
        ):
            previous_step()
            st.rerun()

    with col2:

        if st.button(
            "Next ➜",
            disabled=not st.session_state.voice_completed,
            use_container_width=True,
            key="voice_next",
        ):
            next_step()
            st.rerun()

    with col3:

        if st.button(
            "Skip",
            use_container_width=True,
            key="voice_skip",
        ):
            st.session_state.results["voice"] = "Skipped"
            st.session_state.voice_completed = True
            next_step()
            st.rerun()

# ==========================================================
# FINGER TAPPING
# ==========================================================

elif st.session_state.step == 3:

    fingertap_page()

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "⬅ Back",
            use_container_width=True,
            key="finger_back",
        ):
            previous_step()
            st.rerun()

    with col2:

        if st.button(
            "Finish ➜",
            disabled=not st.session_state.fingertap_completed,
            use_container_width=True,
            key="finger_finish",
        ):
            next_step()
            st.rerun()

    with col3:

        if st.button(
            "Skip",
            use_container_width=True,
            key="finger_skip",
        ):
            st.session_state.results["fingertap"] = "Skipped"
            st.session_state.fingertap_completed = True
            next_step()
            st.rerun()

# ==========================================================
# SUMMARY
# ==========================================================

else:

    st.title("📋 Assessment Summary")

    st.success("NeuroSketch Prototype Assessment Completed Successfully")

    st.write("Below is a summary of all assessments performed during this session.")

    st.divider()

    # ==========================
    # Spiral Result
    # ==========================

    spiral = st.session_state.results["spiral"]

    st.subheader("🌀 Spiral Assessment")

    if spiral is None:
        st.warning("Test not performed.")

    elif spiral == "Skipped":
        st.info("Skipped by user.")

    else:

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Prediction", spiral["label"][2:])

        with col2:
            st.metric("Confidence", f"{spiral['confidence']*100:.1f}%")

    st.divider()

    # ==========================
    # Voice Result
    # ==========================

    voice = st.session_state.results["voice"]

    st.subheader("🎤 Voice Assessment")

    if voice is None:
        st.warning("Test not performed.")

    elif voice == "Skipped":
        st.info("Skipped by user.")

    else:

        st.metric("Prediction", voice["label"])

    st.divider()

    # ==========================
    # Finger Result
    # ==========================

    finger = st.session_state.results["fingertap"]

    st.subheader("✋ Finger Tapping Assessment")

    if finger is None:
        st.warning("Test not performed.")

    elif finger == "Skipped":
        st.info("Skipped by user.")

    else:

        st.success("Motion visualization completed successfully.")

    st.divider()

    st.info(
        """
**Disclaimer**

NeuroSketch is an educational AI prototype.

It is not a certified medical device and should not be used as a substitute for professional neurological diagnosis.
"""
    )

    if st.button("Start New Assessment"):

        st.session_state.step = 0

        st.session_state.spiral_completed = False
        st.session_state.voice_completed = False
        st.session_state.fingertap_completed = False

        st.session_state.results = {
            "spiral": None,
            "voice": None,
            "fingertap": None,
        }

        st.rerun()
# python -m streamlit run app.py
