import torch
import numpy as np
import os
from sklearn.metrics import classification_report, confusion_matrix, f1_score

from src.utils.config import PROCESSED_DATA_DIR, MODEL_DIR
from src.training.train import HeartMurmurCNNLSTM

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def find_best_threshold(outputs, y_true):
    probs = torch.softmax(outputs, dim=1)[:, 1].cpu().numpy()
    y_true = y_true.cpu().numpy()

    best_threshold = 0
    best_f1 = 0

    for t in np.arange(0.1, 0.9, 0.05):
        preds = (probs > t).astype(int)
        f1 = f1_score(y_true, preds)

        print(f"Threshold: {t:.2f} | F1: {f1:.4f}")

        if f1 > best_f1:
            best_f1 = f1
            best_threshold = t

    print(f"\nBest Threshold: {best_threshold:.2f} with F1: {best_f1:.4f}")

    return best_threshold

def load_data():
    X = np.load(os.path.join(PROCESSED_DATA_DIR, "X.npy"))
    y = np.load(os.path.join(PROCESSED_DATA_DIR, "y.npy"))

    X = np.transpose(X, (0, 2, 1))

    # Same normalization (IMPORTANT!)
    mean = np.mean(X, axis=(0, 1), keepdims=True)
    std = np.std(X, axis=(0, 1), keepdims=True) + 1e-6
    X = (X - mean) / std

    return X, y


def evaluate():
    X, y = load_data()

    X_tensor = torch.tensor(X, dtype=torch.float32).to(device)
    y_tensor = torch.tensor(y, dtype=torch.long).to(device)

    # Load model
    model = HeartMurmurCNNLSTM().to(device)
    model.load_state_dict(torch.load(os.path.join(MODEL_DIR, "best_model.pth")))
    model.eval()

    with torch.no_grad():
        outputs = model(X_tensor)

    # ==============================
    # FIND BEST THRESHOLD
    # ==============================
    from sklearn.metrics import f1_score

    probs = torch.softmax(outputs, dim=1)[:, 1].cpu().numpy()
    y_true = y_tensor.cpu().numpy()

    best_threshold = 0
    best_f1 = 0

    print("\nSearching for best threshold...\n")

    for t in np.arange(0.1, 0.9, 0.05):
        preds_temp = (probs > t).astype(int)
        f1 = f1_score(y_true, preds_temp)

        print(f"Threshold: {t:.2f} | F1: {f1:.4f}")

        if f1 > best_f1:
            best_f1 = f1
            best_threshold = t

    print(f"\n✅ Best Threshold: {best_threshold:.2f} with F1: {best_f1:.4f}")

    # ==============================
    # FINAL PREDICTIONS USING BEST THRESHOLD
    # ==============================
    final_preds = (probs > best_threshold).astype(int)

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_true, final_preds))

    print("\nClassification Report:")
    print(classification_report(y_true, final_preds, target_names=["Normal", "Murmur"]))


if __name__ == "__main__":
    evaluate()