import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# Import the decoupled prediction logic
from .predictor import predict_parkinsons


def show():
    # --- SESSION STATE INITIALIZATION ---
    # Safely initialize the results dictionary and completion flag
    if "results" not in st.session_state:
        st.session_state.results = {}
    if "spiral_completed" not in st.session_state:
        st.session_state.spiral_completed = False
    # ------------------------------------

    # Define the layout
    st.title("NeuroSketch")
    st.header("Unveiling Parkinson's with Precision")
    st.write(
        "Try drawing a Spiral and watch how an AI Model will detect the Parkinson Disease."
    )
    st.warning(
        "Warning: Do not click Submit Sketch button before drawing spiral on below Canvas."
    )

    # Base directory to locate labels.txt accurately inside the new folder structure
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Sidebar configurations
    with st.sidebar:
        st.subheader("About NeuroSketch")
        link_text = "Distinguishing Different Stages of Parkinson’s Disease Using Composite Index of Speed and Pen-Pressure of Sketching a Spiral"
        link_url = "https://www.frontiersin.org/articles/10.3389/fneur.2017.00435/full"
        st.write(
            "Parkinson's disease is a neurodegenerative disorder that affects motor functions, leading to tremors, stiffness, and impaired movement. The research presented in the article link mentioned below explores the use of spiral and wave sketch images to develop a robust algorithm for Parkinson's disease detection. NeuroSketch leverages these sketch images to train an AI model, achieving an impressive accuracy rate of 83%."
        )
        st.markdown(f"[{link_text}]({link_url})")

        st.header("Dataset")

        st.header("Drawing Canvas Configurations")
        drawing_mode = "freedraw"
        stroke_width = st.slider("Stroke width: ", 1, 25, 3)
        stroke_color = st.color_picker("Stroke color hex: ")
        bg_color = st.color_picker("Background color hex: ", "#eee")
        bg_image = st.file_uploader("Background image:", type=["png", "jpg"])
        realtime_update = st.checkbox("Update in realtime", True)

    # Create canvas component
    canvas_size = 345
    canvas_image = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        width=canvas_size,
        height=canvas_size,
        background_image=Image.open(bg_image) if bg_image else None,
        update_streamlit=realtime_update,
        drawing_mode=drawing_mode,
        key="canvas",
    )

    # Display preview of the sketch
    # st.subheader("Preview")
    # if canvas_image.image_data is not None:
    #     input_numpy_array = np.array(canvas_image.image_data)
    #     input_image = Image.fromarray(input_numpy_array.astype("uint8"), "RGBA")
    #     st.image(input_image, use_column_width=True)

    # Predict Parkinson's disease on button click
    submit = st.button(label="Submit Sketch")

    if submit:
        st.subheader("Output")
        if canvas_image.image_data is not None:
            with st.spinner(text="This may take a moment..."):
                # Pass only the raw numpy image data to remove Streamlit dependencies in the predictor
                result = predict_parkinsons(canvas_image.image_data)

                # --- SESSION STATE STORAGE ---
                # Update completion flag and store exact prediction dictionary structure
                st.session_state.spiral_completed = True
                st.session_state.results["spiral"] = {
                    "label": result["label"],
                    "confidence": result["confidence"],
                    "prediction": result["prediction"],
                }
                # -----------------------------

                # Reconstruct the string result inside the UI module
                class_name = result["label"]
                confidence_score = result["confidence"]
                prediction = result["prediction"]

                Detection_Result = f"The model has detected {class_name[2:]}, with Confidence Score: {str(np.round(confidence_score * 100))[:-2]}%."
                st.write(Detection_Result)

                # Display confidence scores for other classes (using relative path for labels)
                labels_file_path = os.path.join(BASE_DIR, "labels.txt")
                with open(labels_file_path, "r") as f:
                    class_names = f.readlines()

                data = {"Class": class_names, "Confidence Score": prediction[0]}
                df = pd.DataFrame(data)
                df["Confidence Score"] = df["Confidence Score"].apply(
                    lambda x: f"{str(np.round(x*100))[:-2]}%"
                )
                df["Class"] = df["Class"].apply(lambda x: x.split(" ")[1])
                st.subheader("Confidence Scores on other classes:")
                st.write(df)
