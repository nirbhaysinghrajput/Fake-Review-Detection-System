"""
train_model.py

LSTM-based Fake Review Detector — Training Pipeline
=====================================================
Run this script ONCE to:
  1. Load and validate the dataset
  2. Preprocess review text
  3. Train/test split (80/20, stratified)
  4. Fit a Keras Tokenizer on training data only
  5. Build and train an LSTM model
  6. Evaluate on the test set (Accuracy, Precision, Recall, F1)
  7. Save the trained model  → model/fake_review_model.keras
  8. Save the tokenizer      → model/tokenizer.pkl

After this script completes, start the Flask app with:
  python app.py

DO NOT re-run this script every time you start the app.
"""

import os
import sys
import pickle
import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# ─── Suppress TensorFlow startup verbosity ────────────────────
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Embedding, LSTM, Dropout, Dense, SpatialDropout1D, Bidirectional
)
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)

# Add the project root to sys.path so preprocessing can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprocessing.text_cleaner import clean_texts

# ─────────────────────────────────────────────────────────────
# CONFIGURABLE HYPERPARAMETERS
# Adjust these if you swap in a larger real-world dataset.
# ─────────────────────────────────────────────────────────────
MAX_WORDS          = 5000     # Maximum vocabulary size
MAX_SEQUENCE_LENGTH = 150     # Pad/truncate every review to this length
EMBEDDING_DIM      = 64       # Dimension of word-embedding vectors
LSTM_UNITS         = 64       # Number of LSTM memory units
DROPOUT_RATE       = 0.3      # Fraction of units to drop (regularisation)
BATCH_SIZE         = 16       # Reviews per gradient update step (smaller batch = more steps)
EPOCHS             = 25       # Maximum training epochs (EarlyStopping kicks in)
VALIDATION_SPLIT   = 0.15     # Fraction of training data used for validation
TEST_SIZE          = 0.20     # Fraction of full dataset held out for final test
RANDOM_STATE       = 42       # Seed for reproducibility

# ─────────────────────────────────────────────────────────────
# FILE PATHS
# ─────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH  = os.path.join(BASE_DIR, "dataset", "reviews.csv")
MODEL_DIR     = os.path.join(BASE_DIR, "model")
MODEL_PATH    = os.path.join(MODEL_DIR, "fake_review_model.keras")
TOKENIZER_PATH = os.path.join(MODEL_DIR, "tokenizer.pkl")


# ═════════════════════════════════════════════════════════════
# STEP 1 — LOAD & VALIDATE DATASET
# ═════════════════════════════════════════════════════════════
def load_and_validate(path: str) -> pd.DataFrame:
    """Load reviews.csv and perform basic validation checks."""
    print("\n[1/6] Loading dataset ...")

    if not os.path.exists(path):
        sys.exit(
            f"ERROR: Dataset not found at '{path}'.\n"
            "Run the dataset generator first:\n"
            "  python dataset/generate_dataset.py\n"
        )

    df = pd.read_csv(path, encoding="utf-8")
    print(f"      Raw rows loaded : {len(df)}")

    # Check required columns
    required_cols = {"review_text", "label"}
    missing = required_cols - set(df.columns)
    if missing:
        sys.exit(f"ERROR: Dataset is missing columns: {missing}")

    # Remove rows with empty review text
    initial_count = len(df)
    df = df.dropna(subset=["review_text"])
    df = df[df["review_text"].astype(str).str.strip() != ""]
    print(f"      After removing empty rows : {len(df)} (removed {initial_count - len(df)})")

    # Remove rows with invalid labels (must be 0 or 1)
    df["label"] = pd.to_numeric(df["label"], errors="coerce")
    df = df[df["label"].isin([0, 1])].copy()
    df["label"] = df["label"].astype(int)
    print(f"      After removing invalid labels : {len(df)}")

    # Remove duplicate review texts
    df = df.drop_duplicates(subset=["review_text"])
    print(f"      After removing duplicates : {len(df)}")

    # Class distribution
    counts = df["label"].value_counts().sort_index()
    print(f"\n      Class distribution:")
    print(f"        Genuine reviews (0) : {counts.get(0, 0)}")
    print(f"        Fake reviews    (1) : {counts.get(1, 0)}")

    if len(df) < 50:
        sys.exit("ERROR: Dataset is too small to train meaningfully (< 50 rows).")

    return df


# ═════════════════════════════════════════════════════════════
# STEP 2 — PREPROCESS TEXT
# ═════════════════════════════════════════════════════════════
def preprocess(df: pd.DataFrame):
    """Clean review text and prepare X, y arrays."""
    print("\n[2/6] Preprocessing text ...")

    # Apply the shared text cleaner (lowercase, lemmatise, etc.)
    df = df.copy()
    df["cleaned"] = clean_texts(df["review_text"].astype(str).tolist())

    # Drop rows where cleaning produced an empty string
    df = df[df["cleaned"].str.strip() != ""]
    print(f"      Rows after cleaning : {len(df)}")

    X = df["cleaned"].tolist()
    y = df["label"].tolist()

    return X, y


# ═════════════════════════════════════════════════════════════
# STEP 3 — TRAIN / TEST SPLIT
# ═════════════════════════════════════════════════════════════
def split_data(X, y):
    """Stratified 80/20 train-test split."""
    print("\n[3/6] Splitting data ...")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y          # Keeps class ratios the same in both splits
    )

    print(f"      Training samples : {len(X_train)}")
    print(f"      Test samples     : {len(X_test)}")

    return X_train, X_test, y_train, y_test


# ═════════════════════════════════════════════════════════════
# STEP 4 — TOKENISATION
# ═════════════════════════════════════════════════════════════
def build_tokenizer_and_sequences(X_train, X_test):
    """
    Fit a Keras Tokenizer on TRAINING data only (no data leakage).
    Then convert text → integer sequences → padded arrays.

    Tokenisation:
      Each unique word is assigned an integer ID.
      "best product ever" → [3, 17, 42]

    Padding:
      All sequences are made the same length by adding zeros.
      [3, 17, 42] → [0, 0, ..., 0, 3, 17, 42]
    """
    print("\n[4/6] Tokenising and padding sequences ...")

    # Fit tokenizer on training text ONLY
    tokenizer = Tokenizer(num_words=MAX_WORDS, oov_token="<OOV>")
    tokenizer.fit_on_texts(X_train)

    vocab_size = min(len(tokenizer.word_index) + 1, MAX_WORDS)
    print(f"      Vocabulary size  : {vocab_size}")

    # Convert text to integer sequences
    train_sequences = tokenizer.texts_to_sequences(X_train)
    test_sequences  = tokenizer.texts_to_sequences(X_test)

    # Pad sequences to fixed length (pre-padding is optimal for LSTMs)
    X_train_pad = pad_sequences(
        train_sequences, maxlen=MAX_SEQUENCE_LENGTH, padding="pre", truncating="pre"
    )
    X_test_pad = pad_sequences(
        test_sequences, maxlen=MAX_SEQUENCE_LENGTH, padding="pre", truncating="pre"
    )

    print(f"      Training matrix shape  : {X_train_pad.shape}")
    print(f"      Test matrix shape      : {X_test_pad.shape}")

    return tokenizer, X_train_pad, X_test_pad


# ═════════════════════════════════════════════════════════════
# STEP 5 — BUILD LSTM MODEL
# ═════════════════════════════════════════════════════════════
def build_model(vocab_size: int) -> tf.keras.Model:
    """
    Build a Bidirectional LSTM binary classification model.

    Architecture
    ─────────────
    Input (padded integer sequence of length MAX_SEQUENCE_LENGTH)
        ↓
    Embedding layer  — learns dense vector for each word token
        ↓
    SpatialDropout1D — drops entire feature maps (good for text)
        ↓
    Bidirectional LSTM — captures sequential patterns in both directions
        ↓
    Dense(32, relu)  — feature transformation
        ↓
    Dropout          — regularisation to reduce overfitting
        ↓
    Dense(1, sigmoid)— outputs a probability between 0 and 1
                        0 → Genuine Review
                        1 → Fake Review
    """
    model = Sequential([
        Embedding(
            input_dim=vocab_size,
            output_dim=EMBEDDING_DIM,
            name="embedding"
        ),
        SpatialDropout1D(DROPOUT_RATE, name="spatial_dropout"),
        Bidirectional(LSTM(LSTM_UNITS // 2), name="bilstm"),
        Dense(32, activation="relu", name="dense_hidden"),
        Dropout(DROPOUT_RATE, name="dropout"),
        Dense(1, activation="sigmoid", name="output")
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.002),
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    return model


# ═════════════════════════════════════════════════════════════
# STEP 6 — TRAIN, EVALUATE, SAVE
# ═════════════════════════════════════════════════════════════
def train_evaluate_save(model, X_train_pad, X_test_pad, y_train, y_test, tokenizer):
    """Train the model, evaluate it, and persist both model and tokenizer."""
    y_train_arr = np.array(y_train)
    y_test_arr  = np.array(y_test)

    print("\n[5/6] Training the model ...")
    print(f"      Batch size       : {BATCH_SIZE}")
    print(f"      Max epochs       : {EPOCHS}")
    print(f"      Validation split : {VALIDATION_SPLIT}")
    print()

    # Ensure model/ directory exists
    os.makedirs(MODEL_DIR, exist_ok=True)

    # EarlyStopping: halt training if validation loss stops improving
    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=6,                 # Wait 6 epochs without improvement before stopping
        restore_best_weights=True,  # Revert to the epoch with lowest val_loss
        verbose=1
    )

    # ModelCheckpoint: save the best model weights during training
    checkpoint = ModelCheckpoint(
        filepath=MODEL_PATH,
        monitor="val_accuracy",
        save_best_only=True,
        verbose=0
    )

    history = model.fit(
        X_train_pad, y_train_arr,
        validation_split=VALIDATION_SPLIT,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=[early_stop, checkpoint],
        verbose=1
    )

    # Explicitly persist the final/best model
    model.save(MODEL_PATH)

    # ── Evaluation on held-out test set ───────────────────────
    print("\n[6/6] Evaluating on test set ...")
    y_pred_prob = model.predict(X_test_pad, verbose=0).flatten()
    y_pred      = (y_pred_prob >= 0.5).astype(int)

    acc  = accuracy_score(y_test_arr, y_pred)
    prec = precision_score(y_test_arr, y_pred, zero_division=0)
    rec  = recall_score(y_test_arr, y_pred, zero_division=0)
    f1   = f1_score(y_test_arr, y_pred, zero_division=0)
    cm   = confusion_matrix(y_test_arr, y_pred)

    print("\n" + "=" * 50)
    print("  TEST SET RESULTS (honest evaluation)")
    print("=" * 50)
    print(f"  Accuracy  : {acc:.4f}  ({acc*100:.1f}%)")
    print(f"  Precision : {prec:.4f}")
    print(f"  Recall    : {rec:.4f}")
    print(f"  F1 Score  : {f1:.4f}")
    print()
    print("  Confusion Matrix:")
    print(f"    True Negative  (Genuine predicted Genuine) : {cm[0][0]}")
    print(f"    False Positive (Genuine predicted Fake)    : {cm[0][1]}")
    print(f"    False Negative (Fake predicted Genuine)    : {cm[1][0]}")
    print(f"    True Positive  (Fake predicted Fake)       : {cm[1][1]}")
    print()
    print("  Classification Report:")
    print(classification_report(y_test_arr, y_pred, target_names=["Genuine", "Fake"]))
    print("=" * 50)

    # ── Save tokenizer ────────────────────────────────────────
    with open(TOKENIZER_PATH, "wb") as f:
        pickle.dump(tokenizer, f)

    print(f"\n  Model saved     -> {MODEL_PATH}")
    print(f"  Tokenizer saved -> {TOKENIZER_PATH}")
    print("\n  Training complete. Run 'python app.py' to start the web app.")

    return history


# ═════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("  Fake Review Detection — Model Training Pipeline")
    print("=" * 60)

    # Step 1: Load & validate
    df = load_and_validate(DATASET_PATH)

    # Step 2: Preprocess
    X, y = preprocess(df)

    # Step 3: Split
    X_train, X_test, y_train, y_test = split_data(X, y)

    # Step 4: Tokenise & pad
    tokenizer, X_train_pad, X_test_pad = build_tokenizer_and_sequences(X_train, X_test)

    # Step 5: Build model
    vocab_size = min(len(tokenizer.word_index) + 1, MAX_WORDS)
    model = build_model(vocab_size)
    model.summary()

    # Step 6: Train, evaluate, save
    train_evaluate_save(model, X_train_pad, X_test_pad, y_train, y_test, tokenizer)
