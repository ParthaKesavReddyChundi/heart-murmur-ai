import os
import shutil
import kagglehub

from src.utils.config import RAW_DATA_DIR

def download_dataset():
    print("Downloading dataset from Kaggle...")

    # Download dataset
    path = kagglehub.dataset_download(
        "bjoernjostein/the-circor-digiscope-phonocardiogram-dataset-v2"
    )

    print(f"Downloaded to: {path}")

    # Move dataset to our project structure
    destination = os.path.join(RAW_DATA_DIR, "circor_dataset")

    if not os.path.exists(destination):
        shutil.copytree(path, destination)
        print(f"Dataset copied to: {destination}")
    else:
        print("Dataset already exists in project directory.")

if __name__ == "__main__":
    download_dataset()