import os

# ==============================
# PROJECT ROOT PATH
# ==============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ==============================
# DATA PATHS
# ==============================
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

# ==============================
# MODEL PATHS
# ==============================
MODEL_DIR = os.path.join(BASE_DIR, "models")

# ==============================
# OUTPUT PATHS
# ==============================
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# ==============================
# AUDIO PARAMETERS
# ==============================
SAMPLE_RATE = 4000   # CirCor dataset standard
N_MFCC = 40

# ==============================
# TRAINING PARAMETERS (will use later)
# ==============================
BATCH_SIZE = 32
EPOCHS = 30
LEARNING_RATE = 0.001