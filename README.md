🧠 NeuroSketch

NeuroSketch is an AI-powered early screening tool for Parkinson’s disease that combines spiral drawing analysis, voice assessment, and motor movement tracking. It is designed to assist paramedical workers, especially in rural and low-resource settings, to identify early symptoms and enable timely referrals.

🚀 Overview

Parkinson’s disease is often diagnosed late due to limited access to neurologists and the absence of a definitive early diagnostic test. NeuroSketch addresses this gap by providing a simple, non-invasive, and accessible screening solution that can be used outside specialized clinical environments.

🩺 What NeuroSketch Does

NeuroSketch performs early risk screening using three diagnostic tests:

Spiral Test:
Detects hand tremors by analyzing irregularities in spiral drawings.

Voice Analysis:
Examines changes in pitch, frequency, and stability that are commonly affected in Parkinson’s.

Motor Movement Test:
Uses computer vision to analyze movement speed, rhythm, and consistency.

The results from all tests are combined to generate an overall early detection signal.

🛠 Built With

Language: Python

Frameworks & Libraries: Streamlit, OpenCV, NumPy, Pandas, Scikit-learn

AI & ML: Computer Vision, Audio Feature Extraction

Cloud & APIs: Google Cloud Platform, Gemini API

Tools: Git/GitHub, Jupyter Notebook

Data: Open-source medical datasets

📽 Demo

🎥 YouTube Demo: https://youtu.be/CmgFPUcbX3M


⚙️ How It Works (High Level)

User performs spiral, voice, and movement tests through the interface

Features are extracted from image, audio, and video inputs

AI models analyze each modality independently

Outputs are combined into a final risk indication

Paramedical staff can use this output to guide referrals

⚠️ Current Limitations

Model accuracy is still being improved

Limited access to large, diverse real-world datasets

Requires further clinical validation before medical deployment

NeuroSketch is intended as a screening and assistive tool, not a standalone diagnostic system.

🌱 Future Scope

Train models on larger and more diverse datasets

Add additional diagnostic tests such as gait and facial expression analysis

Improve accuracy, robustness, and real-world validation

Deploy as a scalable screening tool for public health programs


📜 License

This project is currently shared for academic and demonstration purposes.
Licensing details will be added in future versions.
