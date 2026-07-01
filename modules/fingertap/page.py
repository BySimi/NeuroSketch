import streamlit as st
from modules.fingertap.detector import run_assessment, generate_graph


def show():
    # Prototype Disclaimer
    st.info(
        """
    **Prototype Disclaimer**  
    This module demonstrates hand tracking and finger tapping visualization.  
    Clinical prediction using finger tapping data has not yet been implemented.
    """
    )

    # Title
    st.title("Finger Tapping Assessment")

    # Instructions
    st.markdown(
        """
    ### Instructions
    1. Place your hand in front of the webcam.
    2. Repeatedly tap your thumb and index finger.
    3. The test will automatically stop after the predefined duration.
    """
    )

    # Session state initialization for dictionary if it doesn't exist
    if "results" not in st.session_state:
        st.session_state.results = {}

    # Assessment trigger
    if st.button("Start Assessment"):

        # Placeholders for dynamic UI updates
        col1, col2 = st.columns([3, 1])
        with col1:
            video_placeholder = st.empty()
        with col2:
            time_placeholder = st.empty()

        # Variables to hold the final output lists
        final_times = []
        final_distances = []

        # Process frames via the generator
        for frame, remaining_time, times, distances in run_assessment(
            capture_duration=20
        ):
            # Display webcam feed directly inside Streamlit
            video_placeholder.image(frame, channels="RGB")

            # Display remaining time
            time_placeholder.metric("Time Left", f"{remaining_time} s")

            # Keep track of the latest data points
            final_times = times
            final_distances = distances

        # Clear the live placeholders when done
        video_placeholder.empty()
        time_placeholder.empty()

        # Display completion message
        st.success("Assessment Complete")

        # Update Session State exactly as requested
        st.session_state.fingertap_completed = True
        st.session_state.results["fingertap"] = {"status": "Completed"}

        # Render graph directly inside Streamlit
        fig = generate_graph(final_times, final_distances)
        st.pyplot(fig)
