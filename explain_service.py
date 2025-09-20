# services/explain_service.py
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import json

# we'll use t5-small for instruction-style explanations
def explain_with_model(text: str, analysis: dict):
    return f"Explanation for '{text}': Based on analysis {analysis}"

tokenizer = AutoTokenizer.from_pretrained("t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

def explain_with_model(content: str, nlp_summary: dict, role_context: str = None):
    prompt = f"Explain why the following content might be misleading. Content: {content}\nNLP summary: {nlp_summary}\nProvide: highlights, credibility_score, explanation, verification_steps."
    out = generator(prompt, max_length=250)
    # generator returns text - we return raw text for display; parsing can be implemented
    return out[0]['generated_text']
