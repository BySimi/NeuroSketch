from flask import Flask, render_template, request, jsonify
import base64
from io import BytesIO
from PIL import Image, ImageOps
import numpy as np
import uuid
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load the trained model
model = load_model("./keras_model.h5", compile=False)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Function to generate a unique filename for user input
def generate_user_input_filename():
    unique_id = uuid.uuid4().hex
    filename = f"user_input_{unique_id}.png"
    return filename

# Function to predict Parkinson's disease
def predict_parkinsons(image):
    # Load class names
    class_names = open("labels.txt", "r").readlines()

    # Prepare the input data for the model
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array

    # Make prediction
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]

    return f"The model detected {class_name[2:]}, Confidence Score: {str(np.round(confidence_score * 100))[:-2]}%", prediction[0]

# Route for homepage
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if the post request has the file part
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                # Save the uploaded image to a temporary file
                image = Image.open(file).convert("RGB")
                result, prediction = predict_parkinsons(image)

                return render_template("index.html", result=result, predictions=prediction)

    return render_template("index.html")

# Route to handle canvas image submission
@app.route("/submit_canvas", methods=["POST"])
def submit_canvas():
    if request.method == "POST":
        canvas_data = request.form['canvasImage']
        # Remove the "data:image/png;base64," prefix from the base64 string
        canvas_data = canvas_data.replace('data:image/png;base64,', '')
        canvas_image = base64.b64decode(canvas_data)

        # Convert binary image data to a PIL image
        image = Image.open(BytesIO(canvas_image)).convert("RGB")

        # Make prediction
        result, prediction = predict_parkinsons(image)

        # Return result as JSON response
        return jsonify({'result': result})

if __name__ == "__main__":
    app.run(debug=True)
