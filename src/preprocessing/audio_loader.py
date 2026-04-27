import os
import librosa
import librosa.display
import matplotlib.pyplot as plt

from src.utils.config import RAW_DATA_DIR, SAMPLE_RATE

def get_all_wav_files(folder):
    wav_files = []
    
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".wav"):
                wav_files.append(os.path.join(root, file))
    
    return wav_files


def explore_audio():
    dataset_path = os.path.join(RAW_DATA_DIR, "circor_dataset")
    audio_folder = os.path.join(dataset_path, "training_data")

    # Get all wav files recursively
    files = get_all_wav_files(audio_folder)

    print(f"Total audio files found: {len(files)}")

    if len(files) == 0:
        print("No audio files found. Check dataset structure.")
        return

    sample_path = files[0]

    print(f"Loading sample file: {sample_path}")

    # Load audio
    signal, sr = librosa.load(sample_path, sr=SAMPLE_RATE)

    print(f"Signal shape: {signal.shape}")
    print(f"Sample rate: {sr}")

    # Plot waveform
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(signal, sr=sr)
    plt.title("Heart Sound Waveform")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    explore_audio()