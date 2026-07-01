import os
import pandas as pd
import streamlit as st
from modules.voice.predictor import predict_voice

# Original dataset column names in exact order
FEATURE_NAMES = [
    "MDVP:Fo(Hz)",
    "MDVP:Fhi(Hz)",
    "MDVP:Flo(Hz)",
    "MDVP:Jitter(%)",
    "MDVP:Jitter(Abs)",
    "MDVP:RAP",
    "MDVP:PPQ",
    "Jitter:DDP",
    "MDVP:Shimmer",
    "MDVP:Shimmer(dB)",
    "Shimmer:APQ3",
    "Shimmer:APQ5",
    "MDVP:APQ",
    "Shimmer:DDA",
    "NHR",
    "HNR",
    "RPDE",
    "DFA",
    "spread1",
    "spread2",
    "D2",
    "PPE",
]


def load_demo_data(filename):
    """
    Reads the specified headerless CSV and populates the session state with a random sample.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, filename)

    try:
        # FIXED: Added header=None and names=FEATURE_NAMES to handle the headerless CSVs
        df = pd.read_csv(csv_path, header=None, names=FEATURE_NAMES)

        # Pick one random row from the chosen file
        sample_row = df.sample(1).iloc[0]

        # Populate session state for exactly the 22 expected features
        for name in FEATURE_NAMES:
            st.session_state[f"voice_{name}"] = float(sample_row[name])

    except FileNotFoundError:
        st.error(
            f"Could not find '{filename}'. Please ensure it is in the 'modules/voice/' directory."
        )
    except Exception as e:
        st.error(f"Error loading sample from CSV: {e}")


def show():
    # 1. Prototype Disclaimer
    st.info(
        "Automatic extraction of voice features from audio is currently under development. "
        "For demonstration purposes this prototype accepts manually extracted acoustic features."
    )

    # 2. Title
    st.title("Voice Assessment")

    # Ensure results dict exists in session state for Summary page integration
    if "results" not in st.session_state:
        st.session_state.results = {}

    st.markdown("### Auto-Fill Demo Data")
    st.write("Use these buttons to instantly load real test data for the judges.")

    # 4. Auto-Fill Buttons mapped to the new individual files
    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        if st.button("Load Healthy Sample"):
            load_demo_data("healthy_test.csv")

    with btn_col2:
        if st.button("Load Parkinson Sample"):
            load_demo_data("parkinson_test.csv")

    st.markdown("---")

    # Bonus: UI Organization (Split 22 fields into two groups of 11)
    col1, col2 = st.columns(2)

    # Group 1: Baseline Frequencies and Jitter metrics
    col1_features = FEATURE_NAMES[:8] + FEATURE_NAMES[14:17]

    # Group 2: Shimmer metrics and Non-linear models
    col2_features = FEATURE_NAMES[8:14] + FEATURE_NAMES[17:]

    # 5. Display the 22 feature inputs grouped by columns
    with col1:
        st.markdown("#### Frequency & Jitter")
        for name in col1_features:
            if f"voice_{name}" not in st.session_state:
                st.session_state[f"voice_{name}"] = 0.000000
            st.number_input(name, key=f"voice_{name}", format="%f")

    with col2:
        st.markdown("#### Shimmer & Non-linear")
        for name in col2_features:
            if f"voice_{name}" not in st.session_state:
                st.session_state[f"voice_{name}"] = 0.000000
            st.number_input(name, key=f"voice_{name}", format="%f")

    st.markdown("---")

    # 6. Analyze Voice Button
    if st.button("Analyze Voice"):
        # Assemble feature array safely in exact dataset order
        features_to_predict = [
            st.session_state[f"voice_{name}"] for name in FEATURE_NAMES
        ]

        # Pass exactly the 22 numeric features
        result = predict_voice(features_to_predict)

        # 8. Store prediction globally
        st.session_state.results["voice"] = result["label"]

        # 7. Display cleanly without probability/confidence scores
        st.write(f"### Prediction:\n{result['label']}")

        st.session_state.voice_completed = True
        st.session_state.results["voice"] = result
