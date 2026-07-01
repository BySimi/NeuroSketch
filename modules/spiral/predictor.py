import os
import uuid
import numpy as np
import keras
from keras.models import load_model
from PIL import Image, ImageOps

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Resolve paths relative to this file's directory (modules/spiral/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "keras_model.h5")
LABELS_PATH = os.path.join(BASE_DIR, "labels.txt")

# ---------------------------------------------------------
# LOAD MODEL & LABELS ONLY ONCE (Global Scope)
# ---------------------------------------------------------
best_model = load_model(MODEL_PATH, compile=False)

with open(LABELS_PATH, "r") as f:
    class_names = f.readlines()


def generate_user_input_filename():
    """Generates a unique filename and ensures the temp folder exists."""
    # Create temp directory in the root folder (where the app is executed)
    temp_dir = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_dir, exist_ok=True)

    unique_id = uuid.uuid4().hex
    filename = os.path.join(temp_dir, f"user_input_{unique_id}.png")
    return filename


def predict_parkinsons(canvas_image_data):
    """
    Accepts the raw numpy image array from the canvas, processes it,
    and returns a structured prediction dictionary.
    """
    # Create the array of the right shape to feed into the keras model
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Get the numpy array (4-channel RGBA 100,100,4)
    input_numpy_array = np.array(canvas_image_data)

    # Get the RGBA PIL image
    input_image = Image.fromarray(input_numpy_array.astype("uint8"), "RGBA")

    # Generate a unique filename for the user input
    user_input_filename = generate_user_input_filename()

    # Save the image with the generated filename
    input_image.save(user_input_filename)

    # Replace this with the path to your image
    image = Image.open(user_input_filename).convert("RGB")

    # Resize the image to be at least 224x224 and then crop from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # Turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predict the model
    prediction = best_model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Return structured data instead of Streamlit text
    return {
        "label": class_name,
        "confidence": confidence_score,
        "prediction": prediction,
    }
