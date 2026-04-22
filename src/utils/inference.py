import torch
import numpy as np
import librosa
import os

from src.utils.config import SAMPLE_RATE, N_MFCC, MODEL_DIR

# ==============================
# DEVICE
# ==============================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ==============================
# MODEL (same as training)
# ==============================
import torch.nn as nn

class HeartMurmurCNNLSTM(nn.Module):
    def __init__(self):
        super().__init__()

        self.cnn = nn.Sequential(
            nn.Conv1d(41, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(2),

            nn.Conv1d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(2)
        )

        self.lstm = nn.LSTM(128, 64, num_layers=2, batch_first=True)

        self.dropout = nn.Dropout(0.5)
        self.fc = nn.Linear(64, 2)

    def forward(self, x):
        x = x.permute(0, 2, 1)
        x = self.cnn(x)
        x = x.permute(0, 2, 1)

        out, _ = self.lstm(x)
        out = out[:, -1, :]
        out = self.dropout(out)
        out = self.fc(out)

        return out


# ==============================
# FEATURE EXTRACTION
# ==============================
MAX_LEN = 100

def extract_features(file_path):
    signal, sr = librosa.load(file_path, sr=SAMPLE_RATE)

    # MFCC
    mfcc = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=N_MFCC)

    # Pitch
    pitches, magnitudes = librosa.piptrack(y=signal, sr=sr)
    pitch = []
    for i in range(pitches.shape[1]):
        index = magnitudes[:, i].argmax()
        pitch.append(pitches[index, i])

    pitch = np.array(pitch)

    # Padding / Truncation
    def pad(feature):
        if feature.shape[1] < MAX_LEN:
            pad_width = MAX_LEN - feature.shape[1]
            feature = np.pad(feature, ((0, 0), (0, pad_width)), mode='constant')
        else:
            feature = feature[:, :MAX_LEN]
        return feature

    mfcc = pad(mfcc)
    pitch = pad(pitch.reshape(1, -1))

    combined = np.vstack((mfcc, pitch))

    return combined


# ==============================
# LOAD MODEL
# ==============================
def load_model():
    model = HeartMurmurCNNLSTM().to(device)
    model.load_state_dict(torch.load(os.path.join(MODEL_DIR, "best_model.pth"), weights_only=True))
    model.eval()
    return model


# ==============================
# NORMALIZATION (same as training)
# ==============================
def normalize(features):
    mean = np.mean(features)
    std = np.std(features) + 1e-6
    return (features - mean) / std


# ==============================
# PREDICT FUNCTION
# ==============================
def predict(file_path, threshold=0.45):
    model = load_model()

    features = extract_features(file_path)
    features = normalize(features)

    # reshape to (1, time, features)
    features = np.transpose(features, (1, 0))
    features = np.expand_dims(features, axis=0)

    features = torch.tensor(features, dtype=torch.float32).to(device)

    with torch.no_grad():
        outputs = model(features)
        probs = torch.softmax(outputs, dim=1)

    murmur_prob = probs[0][1].item()

    prediction = "Murmur" if murmur_prob > threshold else "Normal"

    return prediction, murmur_prob

if __name__ == "__main__":
    test_file = "data/raw/circor_dataset/training_data/training_data/13918_AV.wav"

    pred, prob = predict(test_file)

    print(f"\nPrediction: {pred}")
    print(f"Murmur Probability: {prob:.4f}")