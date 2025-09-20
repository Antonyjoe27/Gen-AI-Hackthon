# services/image_service.py
from PIL import Image
import io, hashlib
import pytesseract
from transformers import CLIPProcessor, CLIPModel
import torch

# Load CLIP for image-text similarity (optional, lightweight use)
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def simple_image_hash(image: Image.Image) -> str:
    """
    Compute a simple hash for the image using average pixel values.
    Replaces the imagehash dependency.
    """
    # Resize to 8x8 grayscale
    small = image.resize((8, 8)).convert("L")
    pixels = list(small.getdata())
    avg = sum(pixels) / len(pixels)
    bits = "".join(['1' if p > avg else '0' for p in pixels])
    # Convert binary string → hex
    return f"{int(bits, 2):016x}"

def analyze_image_bytes(img_bytes: bytes):
    im = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    # OCR for any text in the image
    try:
        text = pytesseract.image_to_string(im)
    except Exception:
        text = ""

    # Simple perceptual hash (instead of imagehash)
    phash = simple_image_hash(im)

    # CLIP similarity with predefined labels
    inputs = clip_processor(
        text=["a photo", "a poster", "an advertisement", "a screenshot"],
        images=im,
        return_tensors="pt",
        padding=True
    )
    outputs = clip_model(**inputs)

    return {
        "ocr": text.strip(),
        "phash": phash,
        "clip_logits": outputs.logits_per_image.detach().cpu().numpy().tolist()
    }
