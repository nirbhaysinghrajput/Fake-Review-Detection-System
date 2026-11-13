"""
preprocessing/text_cleaner.py

Reusable text preprocessing functions shared by:
  - train_model.py  (during training)
  - predict.py      (during inference)

Pipeline:
  1. Lowercase
  2. Remove URLs and HTML tags
  3. Remove special characters (keep alphabets and spaces)
  4. Remove excessive whitespace
  5. Tokenise into words
  6. Remove NLTK English stop words (but keep sentiment words)
  7. Lemmatise words using WordNetLemmatizer

NOTE: Stop-word removal is intentionally conservative.
      Words like "not", "no", "never" carry sentiment meaning,
      so they are NOT removed.
"""

import re
import string
import nltk

# Standard English stopwords fallback list (in case NLTK corpus is absent)
FALLBACK_STOPWORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she",
    "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
    "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of",
    "at", "by", "for", "with", "about", "against", "between", "into", "through",
    "during", "before", "after", "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under", "again", "further", "then",
    "once", "here", "there", "when", "where", "why", "how", "all", "any",
    "both", "each", "few", "other", "some", "such", "own", "same", "than"
}

# ─── Configuration ────────────────────────────────────────────
SENTIMENT_WORDS_TO_KEEP = {
    "not", "no", "never", "very", "so", "too", "most", "more",
    "less", "only", "just", "really", "quite", "rather", "hardly",
    "barely", "worst", "best", "better", "worse"
}

try:
    from nltk.corpus import stopwords
    _base_stopwords = set(stopwords.words("english"))
except Exception:
    _base_stopwords = FALLBACK_STOPWORDS

STOP_WORDS = _base_stopwords - SENTIMENT_WORDS_TO_KEEP

# Setup word normalizer: WordNetLemmatizer if available offline, otherwise PorterStemmer
try:
    from nltk.stem import WordNetLemmatizer
    _lemmatizer = WordNetLemmatizer()
    _lemmatizer.lemmatize("running")
    def _normalize_word(w: str) -> str:
        return _lemmatizer.lemmatize(w)
except Exception:
    from nltk.stem import PorterStemmer
    _stemmer = PorterStemmer()
    def _normalize_word(w: str) -> str:
        return _stemmer.stem(w)


# ─── Core cleaning function ───────────────────────────────────
def clean_text(text: str) -> str:
    """
    Clean and normalise a review string.

    Parameters
    ----------
    text : str
        Raw review text from the user or CSV dataset.

    Returns
    -------
    str
        Cleaned, lowercase, lemmatised text with stop words removed.

    Example
    -------
    >>> clean_text("This PRODUCT is REALLY amazing!!!")
    'product really amazing'
    """
    if not isinstance(text, str) or not text.strip():
        return ""

    # Step 1: Lowercase
    text = text.lower()

    # Step 2: Remove URLs (http://..., www....)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)

    # Step 3: Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Step 4: Remove everything that is not a letter or whitespace
    #         (removes numbers, punctuation, emojis, special chars)
    text = re.sub(r"[^a-z\s]", " ", text)

    # Step 5: Collapse multiple spaces / newlines into a single space
    text = re.sub(r"\s+", " ", text).strip()

    # Step 6: Tokenise into individual words
    words = text.split()

    # Step 7: Remove stop words and very short tokens (length < 2)
    words = [w for w in words if w not in STOP_WORDS and len(w) > 1]

    # Step 8: Lemmatise / stem — reduce words to base form
    #         e.g. "buying" → "buy", "products" → "product"
    words = [_normalize_word(w) for w in words]

    return " ".join(words)


# ─── Batch helper ─────────────────────────────────────────────
def clean_texts(texts) -> list:
    """
    Apply clean_text() to a list or pandas Series of strings.

    Parameters
    ----------
    texts : iterable of str
        Collection of raw review strings.

    Returns
    -------
    list of str
        Cleaned texts in the same order.
    """
    return [clean_text(t) for t in texts]


# ─── Quick smoke test ─────────────────────────────────────────
if __name__ == "__main__":
    samples = [
        "This PRODUCT is REALLY amazing!!!",
        "BEST PURCHASE EVER!!! BUY NOW!!!",
        "I bought this product last week. The delivery was on time.",
        "WOW!!!!! Everyone should buy this amazing product!!!!!",
        "",
    ]
    print("Text Cleaner — Smoke Test")
    print("=" * 60)
    for s in samples:
        print(f"  IN : {s!r}")
        print(f"  OUT: {clean_text(s)!r}")
        print()
