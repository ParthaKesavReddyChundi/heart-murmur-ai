# 💓 AI-Powered Heart Murmur Detection System

## 🚀 Overview

This project is an end-to-end deep learning system for detecting heart murmurs from phonocardiogram (PCG) audio signals. It combines advanced signal processing, deep learning, and a modern web interface to analyze heart sounds and classify them as **Normal** or **Murmur**.

The system features both a **Streamlit-based backend application** for scientific exploration and a **modern React frontend** for user-friendly interaction.

---

## 🧠 Key Features

### Core AI Capabilities
- 🎧 **Audio Processing** using Librosa with 4000 Hz sampling rate
- 📊 **Advanced Feature Extraction** - MFCC (Mel-Frequency Cepstral Coefficients) + Pitch analysis
- 🧠 **Hybrid CNN + LSTM** deep learning model for temporal audio pattern recognition
- ⚖️ **Class Imbalance Handling** for accurate minority class detection
- 🎯 **Threshold Tuning** optimized for medical sensitivity (adjustable threshold for risk stratification)

### Frontend Features
- 📱 **Modern React UI** with glassmorphism design and smooth animations
- 🎯 **Drag-and-Drop Upload** for .wav files with real-time file preview
- 🎵 **Interactive Audio Player** with waveform visualization and spectrogram mock
- 📊 **Real-Time Analysis** with animated progress indicator
- 🎨 **Intuitive Results Display**:
  - Risk level indicators (Low/Moderate/High Risk)
  - Circular progress visualization showing confidence score
  - Detailed clinical assessment messages
- 📈 **Analysis History** - Track the last 5 predictions with timestamps and probability bars
- 🌐 **Responsive Design** - Works seamlessly on desktop and mobile
- ⚡ **Smooth Animations** using Framer Motion

### Deployment
- 🌐 Hugging Face model deployment for easy access
- 📦 Vite-optimized React build for fast production deployment
- 🐍 Streamlit app for scientific exploration and debugging

---

## 🗂️ Project Structure

```
heart-murmur-ai/
│
├── frontend/                          # Modern React UI (NEW!)
│   ├── src/
│   │   ├── App.jsx                   # Main React component
│   │   ├── index.css                 # Glassmorphism styling
│   │   └── main.jsx                  # React entry point
│   ├── package.json                  # Frontend dependencies
│   ├── vite.config.js                # Vite configuration
│   └── index.html                    # HTML entry point
│
├── app/
│   └── app.py                        # Streamlit web application
│
├── src/
│   ├── preprocessing/
│   │   └── audio_loader.py          # Audio file loading and preprocessing
│   ├── features/
│   │   └── feature_extractor.py     # MFCC + Pitch extraction
│   ├── training/
│   │   └── train.py                 # Model training script
│   ├── evaluation/
│   │   └── evaluate.py              # Model evaluation metrics
│   └── utils/
│       ├── config.py                # Configuration & paths
│       └── inference.py             # Model loading and prediction
│
├── models/                           # Saved model weights (ignored in Git)
├── data/
│   ├── raw/                         # Raw dataset
│   └── processed/                   # Processed features
├── outputs/                         # Training outputs
│
├── main.py                          # Entry point for dataset download
├── dataset_download.py              # Kaggle dataset downloader
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

---

## 🛠️ Tech Stack

### Backend
- **PyTorch** 2.5.1 - Deep Learning Framework
- **Librosa** 0.11.0 - Audio Signal Processing
- **NumPy & Pandas** - Data Processing
- **Streamlit** 1.56.0 - Interactive Web App
- **Scikit-learn** 1.8.0 - Machine Learning Utilities

### Frontend
- **React** 19.2.5 - UI Framework
- **Vite** 8.0.10 - Build Tool & Dev Server
- **Framer Motion** 12.38.0 - Animations
- **Lucide React** 1.11.0 - Icon Library
- **CSS3** - Glassmorphism & Custom Styling

### Dataset
- **CirCor DigiScope Phonocardiogram Dataset v2** (via Kaggle)
- Includes 3,240 recordings with murmur labels

---

## ⚙️ Installation

### Prerequisites
- Python 3.9+
- Node.js 16+ (for frontend)
- Kaggle API credentials (for dataset download)

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/ParthaKesavReddyChundi/heart-murmur-ai.git
cd heart-murmur-ai

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Backend stays in main directory for Streamlit integration
cd ..
```

### Dataset Download

```bash
# Set up Kaggle API credentials first (https://www.kaggle.com/settings/account)
# Then run:
python main.py
```

---

## 🧠 Model Architecture

The model uses a **Hybrid CNN-LSTM** architecture optimized for temporal audio pattern recognition:

```
Input: (Batch, 100 timesteps, 41 features)  [MFCC (40) + Pitch (1)]
  ↓
CNN Block 1: Conv1d(41→64, kernel=3) + ReLU + MaxPool
CNN Block 2: Conv1d(64→128, kernel=3) + ReLU + MaxPool
  ↓
LSTM: 2 layers, 128→64 hidden units, bidirectional processing
  ↓
Dropout (0.5) for regularization
  ↓
Fully Connected: 64→2 (Binary Classification: Normal vs Murmur)
  ↓
Output: Softmax probabilities
```

**Design Rationale:**
- **CNN Layers**: Extract local audio patterns and spectral features
- **LSTM Layers**: Capture temporal dependencies in heart sound sequences
- **Dropout**: Prevent overfitting during training
- **Binary Classification**: Normal (0) vs Murmur (1)

---

## 📈 Performance Metrics

- **Overall Accuracy**: ~78–82%
- **Murmur Recall**: ~53–77% (threshold dependent)
- **Optimization**: Tuned for medical sensitivity (prioritizing murmur detection over false positives)
- **Model Size**: ~2.5 MB (lightweight for deployment)

---

## 🚀 Running the Application

### Option 1: React Frontend (Modern UI - Recommended)

```bash
# Navigate to frontend
cd frontend

# Start development server
npm run dev

# Then open http://localhost:5173 in your browser
```

**Frontend Features:**
- Upload .wav files via drag-and-drop
- Play and visualize audio
- Get instant predictions with confidence scores
- View analysis history
- Responsive design for all devices

### Option 2: Streamlit Application (Scientific Exploration)

```bash
# From project root
streamlit run app/app.py

# Opens at http://localhost:8501
```

**Streamlit Features:**
- File upload interface
- Waveform visualization
- Direct prediction with confidence score
- Medical risk assessment with color coding

---

## 📊 User Features & Capabilities

### For Patient/User
1. ✅ **Upload Heart Sound** - Simple drag-and-drop or file selection
2. ✅ **Real-Time Playback** - Listen to uploaded audio before analysis
3. ✅ **Instant Prediction** - Get results in ~2.5 seconds
4. ✅ **Risk Assessment** - Clear indicators: Low Risk 🟢, Moderate Risk 🟠, High Risk 🔴
5. ✅ **Confidence Score** - Visual representation of AI confidence
6. ✅ **Analysis History** - Track last 5 analyses
7. ✅ **Clinical Guidance** - Recommendations based on results

### For Healthcare Professionals
1. ✅ **Batch Analysis** - Process multiple files sequentially
2. ✅ **Threshold Adjustment** - Configure sensitivity (default: 0.45)
3. ✅ **Detailed Metrics** - Access probability scores and feature data
4. ✅ **Model Information** - Understand architecture and training data

---

## 🔧 Configuration

Edit `src/utils/config.py` to customize:

```python
SAMPLE_RATE = 4000        # Hz
N_MFCC = 40               # Number of MFCC coefficients
MODEL_DIR = "models/"     # Model weights location
DATA_DIR = "data/"        # Dataset location
THRESHOLD = 0.45          # Prediction threshold (adjust for sensitivity)
```

---

## 🌐 Model Deployment

The trained model is hosted on **Hugging Face** for easy integration:

📍 **Model Hub**: [KesavReddy/heart-murmur-detection-model](https://huggingface.co/KesavReddy/heart-murmur-detection-model)

### Using the Model Programmatically

```python
from src.utils.inference import predict

# Make prediction on audio file
prediction, probability = predict("path/to/audio.wav", threshold=0.45)

print(f"Prediction: {prediction}")
print(f"Murmur Probability: {probability:.4f}")
```

---

## 🎯 Training & Evaluation

### Train the Model

```bash
# Ensure dataset is downloaded first
python main.py

# Then train
python src/training/train.py
```

### Evaluate Model

```bash
python src/evaluation/evaluate.py
```

---

## 📱 Frontend Development

### Build for Production

```bash
cd frontend
npm run build

# Output in frontend/dist/
```

### Code Structure
- **App.jsx**: Main component managing state, file upload, and analysis
- **index.css**: Inline styles with glassmorphism and animations
- **Mock API**: Currently uses simulated predictions for demo

### Customization
- Modify colors in `App.jsx` CSS variables (`--primary`, `--success`, `--warning`, `--danger`)
- Adjust animation timing in Framer Motion configs
- Update clinical assessment messages in the result display section

---

## ⚠️ Disclaimer

**Important Medical Information:**

⚠️ **This project is for research and educational purposes only.**

- It is **NOT a substitute** for professional medical diagnosis
- Results should be **reviewed by qualified healthcare professionals**
- Use only as a **screening tool**, not for definitive diagnosis
- Always **consult a doctor** for proper cardiac evaluation
- Accuracy varies based on audio quality and recording equipment

**Limitations:**
- Model trained on CirCor DigiScope recordings only
- Performance may vary with different recording devices
- Environmental noise can affect predictions
- Cannot replace clinical stethoscopy

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Multi-language support
- Additional audio preprocessing techniques
- Advanced visualizations
- API endpoint documentation
- Docker containerization
- Mobile app

---

## 👨‍💻 Author

**Kesav Reddy**

---

## ⭐ Support

If you find this project helpful:

- ⭐ **Star the repository** on GitHub
- 🐛 **Report issues** for bugs or improvements
- 💡 **Suggest features** via GitHub Issues
- 📧 **Share feedback** and use cases

---

## 📄 License

This project is provided as-is for educational and research purposes.

---

## 🔗 Resources

- [Librosa Documentation](https://librosa.org/)
- [PyTorch Documentation](https://pytorch.org/)
- [React Documentation](https://react.dev/)
- [CirCor Dataset](https://www.kaggle.com/datasets/bjoernjostein/the-circor-digiscope-phonocardiogram-dataset-v2)
- [Hugging Face Hub](https://huggingface.co/)

---

**© 2026 CardiacAI Solutions. For screening purposes only. Always consult a medical professional.**
