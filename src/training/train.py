import torch
import torch.nn as nn
import numpy as np
import os
from sklearn.model_selection import train_test_split
from collections import Counter
from torch.utils.data import TensorDataset, DataLoader
from src.utils.config import PROCESSED_DATA_DIR, MODEL_DIR

# ==============================
# DEVICE
# ==============================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)


# ==============================
# MODEL
# ==============================
class HeartMurmurCNNLSTM(nn.Module):
    def __init__(self):
        super().__init__()

        # CNN for feature extraction
        self.cnn = nn.Sequential(
            nn.Conv1d(in_channels=41, out_channels=64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(2),

            nn.Conv1d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(2)
        )

        # LSTM
        self.lstm = nn.LSTM(
            input_size=128,
            hidden_size=64,
            num_layers=2,
            batch_first=True
        )

        self.dropout = nn.Dropout(0.5)
        self.fc = nn.Linear(64, 2)

    def forward(self, x):
        # x: (batch, time, features)

        # Convert to (batch, features, time) for CNN
        x = x.permute(0, 2, 1)

        x = self.cnn(x)

        # Back to (batch, time, features)
        x = x.permute(0, 2, 1)

        out, _ = self.lstm(x)
        out = out[:, -1, :]
        out = self.dropout(out)
        out = self.fc(out)

        return out


# ==============================
# CLASS WEIGHTS
# ==============================
def compute_class_weights(y):
    counter = Counter(y)
    total = len(y)

    weights = {}
    for label in counter:
        weights[label] = total / (len(counter) * counter[label])

    return weights


# ==============================
# LOAD DATA
# ==============================
def load_data():
    X = np.load(os.path.join(PROCESSED_DATA_DIR, "X.npy"))
    y = np.load(os.path.join(PROCESSED_DATA_DIR, "y.npy"))

    # reshape for LSTM
    X = np.transpose(X, (0, 2, 1))

    # ==============================
    # NORMALIZATION (IMPORTANT)
    # ==============================
    mean = np.mean(X, axis=(0, 1), keepdims=True)
    std = np.std(X, axis=(0, 1), keepdims=True) + 1e-6

    X = (X - mean) / std

    return X, y


# ==============================
# TRAIN FUNCTION
# ==============================
def train():
    X, y = load_data()

    # Split
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Convert to tensors
    X_train = torch.tensor(X_train, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.long)

    X_val = torch.tensor(X_val, dtype=torch.float32)
    y_val = torch.tensor(y_val, dtype=torch.long)

    # Create DataLoader
    train_dataset = TensorDataset(X_train, y_train)
    val_dataset = TensorDataset(X_val, y_val)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32)

    # Model
    model = HeartMurmurCNNLSTM().to(device)

    # Class weights
    weights = compute_class_weights(y_train.numpy())
    class_weights = torch.tensor([weights[0], weights[1]], dtype=torch.float32).to(device)

    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    epochs = 20
    best_acc = 0
    patience = 3
    counter = 0

    for epoch in range(epochs):
        model.train()
        total_loss = 0

        for X_batch, y_batch in train_loader:
            X_batch = X_batch.to(device)
            y_batch = y_batch.to(device)

            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        # Validation
        model.eval()
        correct = 0
        total = 0

        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                X_batch = X_batch.to(device)
                y_batch = y_batch.to(device)

                outputs = model(X_batch)
                _, preds = torch.max(outputs, 1)

                correct += (preds == y_batch).sum().item()
                total += y_batch.size(0)

        acc = correct / total
        avg_loss = total_loss / len(train_loader)

        print(f"Epoch [{epoch+1}/{epochs}] Loss: {avg_loss:.4f} Val Acc: {acc:.4f}")

        if acc > best_acc:
            best_acc = acc
            counter = 0
            torch.save(model.state_dict(), os.path.join(MODEL_DIR, "best_model.pth"))
        else:
            counter += 1

        if counter >= patience:
            print("\nEarly stopping triggered!")
            break

    print("\nTraining complete!")
    print(f"Best Validation Accuracy: {best_acc:.4f}")

if __name__ == "__main__":
    train()