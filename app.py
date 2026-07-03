import streamlit as st

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

NeuroSketch is an AI-assisted Parkinson's screening application designed to analyze digital biomarkers from handwriting, voice, and motor assessments.\n\n

-This application is intended for screening purposes only.\n
-It does not provide a medical diagnosis.\n
-Results should be interpreted alongside professional clinical evaluation.\n
-If you experience symptoms of Parkinson's disease, consult a qualified healthcare professional.
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

    from modules.spiral.page import show

    show()

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

    from modules.voice.page import show

    show()

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

# elif st.session_state.step == 3:

#     from modules.fingertap.page import show

#     show()

#     st.divider()

#     col1, col2, col3 = st.columns(3)

#     with col1:

#         if st.button(
#             "⬅ Back",
#             use_container_width=True,
#             key="finger_back",
#         ):
#             previous_step()
#             st.rerun()

#     with col2:

#         if st.button(
#             "Finish ➜",
#             disabled=not st.session_state.fingertap_completed,
#             use_container_width=True,
#             key="finger_finish",
#         ):
#             next_step()
#             st.rerun()

#     with col3:

#         if st.button(
#             "Skip",
#             use_container_width=True,
#             key="finger_skip",
#         ):
#             st.session_state.results["fingertap"] = "Skipped"
#             st.session_state.fingertap_completed = True
#             next_step()
#             st.rerun()
elif st.session_state.step == 3:
    from modules.fingertap.page import show

    show()

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬅ Back", use_container_width=True):
            previous_step()
            st.rerun()

    with col2:
        st.button(
            "Next ➜",
            disabled=True,
            use_container_width=True,
        )

    with col3:
        if st.button("Skip", use_container_width=True):
            next_step()
            st.rerun()

# ==========================================================
# SUMMARY
# ==========================================================

else:

    st.title("📋 Assessment Summary")

    st.success("NeuroSketch Prototype Assessment Completed Successfully")

    st.divider()

    spiral = st.session_state.results["spiral"]
    voice = st.session_state.results["voice"]
    finger = st.session_state.results["fingertap"]

    st.subheader("🌀 Spiral Assessment")

    if spiral is None:
        st.warning("Not Performed")

    elif spiral == "Skipped":
        st.info("Skipped")

    else:

        c1, c2 = st.columns(2)

        c1.metric("Prediction", spiral["label"][2:])
        c2.metric("Confidence", f"{spiral['confidence']*100:.1f}%")

    st.divider()

    st.subheader("🎤 Voice Assessment")

    if voice is None:
        st.warning("Not Performed")

    elif voice == "Skipped":
        st.info("Skipped")

    else:

        st.metric("Prediction", voice["label"])

    st.divider()

    st.subheader("✋ Finger Tapping Assessment")

    if finger is None:
        st.warning("Not Performed")

    elif finger == "Skipped":
        st.info("Skipped")

    else:

        st.success("Motion visualization completed.")

    st.divider()

    st.info(
        """
This assessment represents an AI-generated screening result and should not be considered a medical diagnosis. Clinical evaluation by a qualified healthcare professional is recommended for any medical concerns.
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
