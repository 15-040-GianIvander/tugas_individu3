# services/sentiment.py
import os
import logging
import httpx

logger = logging.getLogger(__name__)
HF_API_KEY = os.getenv("HF_API_KEY")

# Model endpoint (can be changed to another HF model)
HF_MODEL_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"

async def analyze_sentiment(text: str) -> str:
    """
    Calls HuggingFace Inference API asynchronously.
    Returns one of: 'positive', 'negative', 'neutral', or a fallback 'unknown'.
    """
    if not HF_API_KEY:
        logger.warning("HF_API_KEY not set - returning 'unknown' sentiment")
        return "unknown"

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": text}

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(HF_MODEL_URL, headers=headers, json=payload)
        if resp.status_code != 200:
            logger.error("Hugging Face returned %s: %s", resp.status_code, resp.text)
            return "unknown"

        data = resp.json()

        # safe parsing: many HF models return list-of-list with label key
        label = None
        try:
            # try common structure
            if isinstance(data, list) and len(data) and isinstance(data[0], list):
                label = data[0][0].get("label")
            elif isinstance(data, dict) and "label" in data:
                label = data.get("label")
            # some models return list of dicts
            elif isinstance(data, list) and len(data) and isinstance(data[0], dict) and "label" in data[0]:
                label = data[0].get("label")
        except Exception:
            label = None

        if not label:
            # fallback try to introspect any text inside response
            flat = str(data).lower()
            if "pos" in flat:
                return "positive"
            if "neg" in flat:
                return "negative"
            if "neu" in flat:
                return "neutral"
            return "unknown"

        l = label.lower()
        if "pos" in l:
            return "positive"
        if "neg" in l:
            return "negative"
        if "neu" in l:
            return "neutral"
        # if label is something else, return normalized string
        return label

    except Exception as e:
        logger.exception("Exception while calling Hugging Face inference")
        return "unknown"
