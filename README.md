# 💓 AI-Powered Heart Murmur Detection System

## 🚀 Overview
This project is an end-to-end deep learning system for detecting heart murmurs from phonocardiogram (PCG) audio signals.

It combines signal processing and deep learning to analyze heart sounds and classify them as **Normal** or **Murmur**.

---

## 🧠 Key Features
- 🎧 Audio processing using Librosa
- 📊 Feature extraction (MFCC + Pitch)
- 🧠 Hybrid CNN + LSTM deep learning model
- ⚖️ Class imbalance handling
- 🎯 Threshold tuning for medical sensitivity
- 🌐 Hugging Face model deployment
- 🖥️ Interactive Streamlit web application

---

## 🗂️ Project Structure
heart_murmur_ai/
│
├── data/ # Dataset (ignored in Git)
├── src/
│ ├── preprocessing/
│ ├── features/
│ ├── training/
│ ├── evaluation/
│ └── utils/
│
├── models/ # Saved models (ignored)
├── outputs/
├── app/ # Streamlit app
│ └── app.py
│
├── requirements.txt
└── README.md

---

## ⚙️ Installation

```bash
git clone https://github.com/<your-username>/heart-murmur-ai.git
cd heart-murmur-ai

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

📊 Dataset
CirCor DigiScope Phonocardiogram Dataset v2
Downloaded via KaggleHub

🧠 Model Architecture
CNN layers → extract local audio patterns
LSTM layers → capture temporal dependencies
Fully connected layer → classification

📈 Performance
Accuracy: ~78–82%
Murmur Recall: ~53–77% (threshold dependent)
Optimized for medical sensitivity

🖥️ Run Application
streamlit run app/app.py

🔍 Example Output
Upload heart sound (.wav)
View waveform
Get prediction + confidence score

☁️ Model Deployment
Model hosted on Hugging Face:
👉 https://huggingface.co/KesavReddy/heart-murmur-detection-model

⚠️ Disclaimer
This project is for research and educational purposes only.
It is not a substitute for professional medical diagnosis.

👨‍💻 Author
Kesav Reddy

⭐ If you like this project
Give it a star on GitHub!

