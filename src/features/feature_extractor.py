import os
import numpy as np
import pandas as pd
import librosa
from tqdm import tqdm

from src.utils.config import SAMPLE_RATE, N_MFCC, RAW_DATA_DIR, PROCESSED_DATA_DIR

MAX_LEN = 100


def get_all_wav_files(folder):
    wav_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".wav"):
                wav_files.append(os.path.join(root, file))
    return wav_files


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
    def pad_or_truncate(feature):
        if feature.shape[1] < MAX_LEN:
            pad_width = MAX_LEN - feature.shape[1]
            feature = np.pad(feature, ((0, 0), (0, pad_width)), mode='constant')
        else:
            feature = feature[:, :MAX_LEN]
        return feature

    mfcc = pad_or_truncate(mfcc)

    pitch = pitch.reshape(1, -1)
    pitch = pad_or_truncate(pitch)

    combined = np.vstack((mfcc, pitch))

    return combined


def build_dataset():
    dataset_path = os.path.join(RAW_DATA_DIR, "circor_dataset")
    audio_folder = os.path.join(dataset_path, "training_data")
    csv_path = os.path.join(dataset_path, "training_data.csv")

    print("Loading metadata...")
    df = pd.read_csv(csv_path)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Create label mapping
    label_map = {
        "Absent": 0,
        "Present": 1,
        "Unknown": -1
    }

    df["label"] = df["Murmur"].map(label_map)

    # Create patient → label dictionary
    patient_labels = dict(zip(df["Patient ID"], df["label"]))

    files = get_all_wav_files(audio_folder)

    X = []
    y = []

    print("Processing all audio files...")

    for file_path in tqdm(files):
        try:
            # Extract patient ID from filename
            filename = os.path.basename(file_path)
            patient_id = int(filename.split("_")[0])

            if patient_id not in patient_labels:
                continue

            label = patient_labels[patient_id]

            # Skip unknown for now
            if label == -1:
                continue

            features = extract_features(file_path)

            X.append(features)
            y.append(label)

        except Exception as e:
            print(f"Skipping file due to error: {file_path}")
            continue

    X = np.array(X)
    y = np.array(y)

    print(f"\nFinal dataset shape: {X.shape}")
    print(f"Labels shape: {y.shape}")

    # Save dataset
    np.save(os.path.join(PROCESSED_DATA_DIR, "X.npy"), X)
    np.save(os.path.join(PROCESSED_DATA_DIR, "y.npy"), y)

    print("\nDataset saved successfully!")


if __name__ == "__main__":
    build_dataset()