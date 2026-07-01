import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from modules.fingertap.detector import FingerTapProcessor, generate_graph


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

    # Initialize Session States
    if "results" not in st.session_state:
        st.session_state.results = {}
    if "webrtc_playing" not in st.session_state:
        st.session_state.webrtc_playing = False
    if "capture_done" not in st.session_state:
        st.session_state.capture_done = False

    # Assessment trigger
    if not st.session_state.webrtc_playing and not st.session_state.capture_done:
        if st.button("Start Assessment"):
            st.session_state.webrtc_playing = True
            st.rerun()

    # WebRTC Streamer Block
    if st.session_state.webrtc_playing:
        ctx = webrtc_streamer(
            key="fingertap",
            mode=WebRtcMode.SENDRECV,
            desired_playing_state=True,
            video_processor_factory=FingerTapProcessor,
            media_stream_constraints={"video": True, "audio": False},
            rtc_configuration={
                "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
            },
        )

        # Main Thread Synchronization: Non-blocking polling
        if ctx.state.playing and ctx.video_processor:
            with st.spinner("Recording in progress... Please tap your fingers."):

                # Instantly catch completion via the internal processor flag
                if ctx.video_processor.finished:
                    # Extract data safely from the processor
                    st.session_state.final_times = ctx.video_processor.times
                    st.session_state.final_distances = ctx.video_processor.distances

                    # Update states to trigger the finish screen and shut down camera
                    st.session_state.webrtc_playing = False
                    st.session_state.capture_done = True

                    st.session_state.fingertap_completed = True
                    st.session_state.results["fingertap"] = {"status": "Completed"}
                    st.rerun()
                else:
                    # Poll safely without while loops or thread locking
                    st.rerun()

    # Results Block
    if st.session_state.capture_done:
        st.success("Assessment Complete")

        # Render graph directly inside Streamlit
        fig = generate_graph(
            st.session_state.final_times, st.session_state.final_distances
        )
        st.pyplot(fig)
