"""
predict.py

Prediction module for the Fake Review Detection System.
========================================================
Provides:
  - predict_review(text)  → dict with prediction, confidence, probabilities
  - analyze_patterns(text) → list of human-readable suspicious pattern strings

The trained model and tokenizer are loaded ONCE when this module
is first imported, so they stay in memory for subsequent calls.

DO NOT retrain the model here. Run train_model.py for that.
"""

import os
import sys
import re
import pickle
import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# ─────────────────────────────────────────────────────────────
# FILE PATHS — same as used in train_model.py
# ─────────────────────────────────────────────────────────────
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH      = os.path.join(BASE_DIR, "model", "fake_review_model.keras")
TOKENIZER_PATH  = os.path.join(BASE_DIR, "model", "tokenizer.pkl")

# Training parameters — must match train_model.py exactly
MAX_SEQUENCE_LENGTH = 150

# ─────────────────────────────────────────────────────────────
# Add project root to path for preprocessing import
# ─────────────────────────────────────────────────────────────
sys.path.insert(0, BASE_DIR)
from preprocessing.text_cleaner import clean_text

# ─────────────────────────────────────────────────────────────
# Lazy-loaded globals — loaded once on first prediction call
# ─────────────────────────────────────────────────────────────
_model     = None
_tokenizer = None


def _load_assets():
    """
    Load model and tokenizer from disk into memory.
    Called automatically on first prediction; cached afterwards.
    Raises FileNotFoundError with a helpful message if files are missing.
    """
    global _model, _tokenizer

    if _model is not None and _tokenizer is not None:
        return  # Already loaded; nothing to do

    # ── Load Keras model ──────────────────────────────────────
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Trained model not found at '{MODEL_PATH}'.\n"
            "Please run the training script first:\n"
            "  python train_model.py"
        )

    # Import TensorFlow only when needed (faster module import)
    import tensorflow as tf
    _model = tf.keras.models.load_model(MODEL_PATH)

    # ── Load tokenizer ────────────────────────────────────────
    if not os.path.exists(TOKENIZER_PATH):
        raise FileNotFoundError(
            f"Tokenizer not found at '{TOKENIZER_PATH}'.\n"
            "Please run the training script first:\n"
            "  python train_model.py"
        )

    with open(TOKENIZER_PATH, "rb") as f:
        _tokenizer = pickle.load(f)


# ═════════════════════════════════════════════════════════════
# MAIN PREDICTION FUNCTION
# ═════════════════════════════════════════════════════════════
def predict_review(review_text: str) -> dict:
    """
    Predict whether a review is Fake or Genuine.

    Parameters
    ----------
    review_text : str
        Raw review text as entered by the user.

    Returns
    -------
    dict with keys:
        prediction        : "Fake Review" or "Genuine Review"
        confidence        : float 0–100  (e.g. 87.4)
        fake_probability  : float 0–1
        genuine_probability : float 0–1
        cleaned_text      : the preprocessed version (for debugging)
        reasons           : list of suspicious pattern strings

    Raises
    ------
    ValueError   : if input is empty or too short after cleaning
    RuntimeError : if model/tokenizer cannot be loaded
    """
    # ── Input validation ──────────────────────────────────────
    if not isinstance(review_text, str):
        raise ValueError("Review must be a string.")

    stripped = review_text.strip()
    if not stripped:
        raise ValueError("Review cannot be empty.")

    if len(stripped.split()) < 3:
        raise ValueError(
            "Review is too short for meaningful analysis. "
            "Please provide at least 3 words."
        )

    # ── Load model & tokenizer (no-op if already loaded) ──────
    try:
        _load_assets()
    except FileNotFoundError as e:
        raise RuntimeError(str(e)) from e

    # ── Preprocess text ───────────────────────────────────────
    cleaned = clean_text(stripped)

    if not cleaned:
        # Cleaning removed all words — very unusual; treat as short review
        raise ValueError(
            "After preprocessing, no meaningful words remain in the review."
        )

    # ── Tokenise + pad ────────────────────────────────────────
    # texts_to_sequences converts words → integer IDs using the fitted vocabulary
    sequence = _tokenizer.texts_to_sequences([cleaned])

    # pad_sequences ensures the array is MAX_SEQUENCE_LENGTH long
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    padded = pad_sequences(
        sequence,
        maxlen=MAX_SEQUENCE_LENGTH,
        padding="pre",
        truncating="pre"
    )

    # ── LSTM prediction ───────────────────────────────────────
    # Output is a probability between 0 (Genuine) and 1 (Fake)
    fake_prob = float(_model.predict(padded, verbose=0).flatten()[0])
    genuine_prob = 1.0 - fake_prob

    # ── Interpret probability ─────────────────────────────────
    is_fake = fake_prob >= 0.5
    prediction = "Fake Review" if is_fake else "Genuine Review"

    # Confidence = how sure the model is (distance from the 0.5 decision boundary)
    confidence = fake_prob * 100 if is_fake else genuine_prob * 100

    # ── Suspicious pattern analysis ───────────────────────────
    reasons = analyze_patterns(stripped)

    return {
        "prediction":         prediction,
        "confidence":         round(confidence, 1),
        "fake_probability":   round(fake_prob, 4),
        "genuine_probability": round(genuine_prob, 4),
        "cleaned_text":       cleaned,
        "reasons":            reasons,
    }


# ═════════════════════════════════════════════════════════════
# RULE-BASED SUSPICIOUS PATTERN ANALYSER
# ═════════════════════════════════════════════════════════════
def analyze_patterns(text: str) -> list:
    """
    Inspect the ORIGINAL (uncleaned) review for suspicious writing patterns.

    This is a SEPARATE rule-based heuristic analysis layer.
    It does NOT represent the LSTM model's reasoning — it is
    supporting evidence presented alongside the model's prediction.

    Patterns detected
    ─────────────────
    1. Promotional language keywords
    2. Excessive capitalisation
    3. Excessive punctuation (!! ??? etc.)
    4. Repeated consecutive words
    5. Extreme emotional language
    6. Abnormally short review
    7. Abnormally repetitive structure
    """
    reasons = []
    text_lower = text.lower()
    words = text_lower.split()

    # ── 1. Promotional language ───────────────────────────────
    promo_keywords = [
        "buy now", "must buy", "buy this", "buy immediately",
        "highly recommended", "best product", "best purchase",
        "amazing product", "everyone should buy", "do not miss",
        "must have", "number one", "best ever", "greatest ever",
        "changed my life", "life changing", "must own",
        "runs out", "don't wait", "do not wait", "before stock"
    ]
    found_promo = [kw for kw in promo_keywords if kw in text_lower]
    if found_promo:
        reasons.append(
            f"Promotional language detected "
            f"(e.g., '{found_promo[0]}')"
        )

    # ── 2. Excessive capitalisation ───────────────────────────
    # Count UPPERCASE words (length > 2 to ignore 'I', 'OK', etc.)
    upper_words = [w for w in text.split() if w.isupper() and len(w) > 2]
    total_words = max(len(text.split()), 1)
    upper_ratio = len(upper_words) / total_words

    if upper_ratio > 0.30:
        reasons.append(
            f"Excessive capitalisation detected "
            f"({int(upper_ratio * 100)}% of words are all-caps)"
        )

    # ── 3. Excessive punctuation ──────────────────────────────
    # Count clusters of repeated ! or ? (e.g., "!!!" counts as 1 cluster)
    exclamation_clusters = len(re.findall(r"!{2,}", text))
    question_clusters    = len(re.findall(r"\?{2,}", text))
    total_exclamations   = text.count("!")

    if exclamation_clusters >= 3 or total_exclamations >= 5:
        reasons.append(
            f"Excessive punctuation detected "
            f"({total_exclamations} exclamation marks)"
        )

    # ── 4. Repeated consecutive words ─────────────────────────
    # Look for patterns like "amazing amazing amazing"
    repeated_pattern = re.findall(r"\b(\w+)\s+\1\b", text_lower)
    unique_repeated  = list(set(repeated_pattern))

    if unique_repeated:
        reasons.append(
            f"Repeated consecutive words detected "
            f"(e.g., '{unique_repeated[0]} {unique_repeated[0]}')"
        )

    # Also check for single words repeated many times (not necessarily adjacent)
    from collections import Counter
    word_counts = Counter(words)
    highly_repeated = [
        w for w, cnt in word_counts.items()
        if cnt >= 4 and len(w) > 3        # Ignore short filler words
    ]
    if highly_repeated:
        reasons.append(
            f"High-frequency word repetition "
            f"('{highly_repeated[0]}' appears {word_counts[highly_repeated[0]]}× in the review)"
        )

    # ── 5. Extreme emotional/sentiment language ────────────────
    extreme_words = [
        "absolutely", "unbelievable", "incredible", "outstanding",
        "extraordinary", "spectacular", "magnificent", "astonishing",
        "miraculous", "phenomenal", "exceptional", "breathtaking",
        "mind-blowing", "mind blowing", "jaw-dropping", "flawless",
        "perfect", "perfection", "greatest", "happiest", "obsessed"
    ]
    found_extreme = [w for w in extreme_words if w in text_lower]
    if len(found_extreme) >= 3:
        reasons.append(
            f"Extreme emotional language detected "
            f"({len(found_extreme)} superlative/extreme words)"
        )

    # ── 6. Abnormally short review ─────────────────────────────
    word_count = len(words)
    if word_count < 8:
        reasons.append(
            f"Very short review ({word_count} words) — may lack specific detail"
        )

    # ── 7. Absence of specific detail ─────────────────────────
    # Genuine reviews often mention specific aspects; fake ones stay vague
    specific_indicators = [
        "delivery", "shipping", "packaging", "warranty", "customer service",
        "battery", "size", "weight", "colour", "color", "material",
        "instructions", "assembly", "week", "month", "day", "days",
        "compared", "versus", "replaced", "previous", "model"
    ]
    has_specifics = any(ind in text_lower for ind in specific_indicators)
    if not has_specifics and word_count > 15:
        reasons.append(
            "Lacks specific product details (no mention of delivery, specs, or usage experience)"
        )

    return reasons


# ═════════════════════════════════════════════════════════════
# QUICK DEMO (run directly: python predict.py)
# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    test_reviews = [
        "BEST PRODUCT EVER!!! BUY THIS NOW!!! Absolutely amazing!!! Everyone should buy it!!!",
        "I purchased this two weeks ago. Delivery was quick and the product works as expected. The battery could be better.",
        "Great product great quality great price highly recommended to everyone!!!",
    ]

    print("=" * 65)
    print("  Prediction Module — Demo")
    print("=" * 65)

    for review in test_reviews:
        print(f"\nReview: {review[:70]}...")
        try:
            result = predict_review(review)
            print(f"  Prediction   : {result['prediction']}")
            print(f"  Confidence   : {result['confidence']}%")
            print(f"  Fake prob    : {result['fake_probability']}")
            print(f"  Genuine prob : {result['genuine_probability']}")
            print(f"  Patterns     : {result['reasons'] or 'None detected'}")
        except (ValueError, RuntimeError) as e:
            print(f"  ERROR: {e}")
        print()
