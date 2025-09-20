# services/text_service.py
from transformers import pipeline
import spacy # type: ignore

# Load sentiment pipeline with explicit model
sentiment = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

# Load spaCy safely
try:
    nlp_spacy = spacy.load("en_core_web_sm")
except OSError:
    # fallback if model not downloaded
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp_spacy = spacy.load("en_core_web_sm")


def analyze_text_nlp(text: str) -> dict:
    """Run sentiment + NER analysis"""
    result = {
        "sentiment": sentiment(text)[0],
        "entities": [(ent.text, ent.label_) for ent in nlp_spacy(text).ents]
    }
    return result
