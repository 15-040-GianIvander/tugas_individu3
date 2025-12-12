# services/keypoints.py
import os
import logging

logger = logging.getLogger(__name__)
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def extract_keypoints(text: str) -> str:
    """
    Try to call Google Gemini via google.generativeai if available + key.
    If not available / fails, returns a simple fallback key points string.
    """
    # Fallback extractor (always available)
    def fallback(text: str) -> str:
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        first = sentences[0] if sentences else text
        # produce 3 simple bullets: first sentence, length, and a crude keyword list
        words = [w.strip(" ,.!?") for w in text.split()]
        keywords = ", ".join(list(dict.fromkeys(words[:6])))  # first unique words up to 6
        return f"- {first}\n- length: {len(text)} chars\n- keywords: {keywords}"

    if not GEMINI_KEY:
        logger.warning("GEMINI_API_KEY not set - using fallback keypoint extractor")
        return fallback(text)

    # Try to import google.generativeai and call it.
    try:
        import google.generativeai as genai
    except Exception as e:
        logger.exception("google.generativeai import failed - using fallback")
        return fallback(text)

    try:
        # configure using key
        genai.configure(api_key=GEMINI_KEY)

        # NOTE: the exact method / signature depends on library version.
        # We'll try a couple of likely variants; if none work, fallback.
        prompt = f"Extract 3 concise key points from this product review:\n\n{text}\n\nReturn as bullets."

        # Variant A: older/newer library may use model.generate or model.generate_text
        try:
            # newer pattern (example)
            res = genai.generate_text(model="gemini-pro", input=prompt)
            # res might be object with .text or string-like
            if hasattr(res, "text"):
                return res.text
            return str(res)
        except Exception:
            # Variant B: model.generate_content / model.generate
            try:
                model = genai.GenerativeModel("gemini-pro")
                out = model.generate_content(prompt)
                if hasattr(out, "text"):
                    return out.text
                return str(out)
            except Exception:
                logger.exception("Gemini generate attempt failed - using fallback")
                return fallback(text)

    except Exception as e:
        logger.exception("Gemini call failed - using fallback")
        return fallback(text)

# services/keypoints.py
import os
import logging

logger = logging.getLogger(__name__)
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def extract_keypoints(text: str) -> str:
    """
    Try to call Google Gemini via google.generativeai if available + key.
    If not available / fails, returns a simple fallback key points string.
    """
    # Fallback extractor (always available)
    def fallback(text: str) -> str:
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        first = sentences[0] if sentences else text
        # produce 3 simple bullets: first sentence, length, and a crude keyword list
        words = [w.strip(" ,.!?") for w in text.split()]
        keywords = ", ".join(list(dict.fromkeys(words[:6])))  # first unique words up to 6
        return f"- {first}\n- length: {len(text)} chars\n- keywords: {keywords}"

    if not GEMINI_KEY:
        logger.warning("GEMINI_API_KEY not set - using fallback keypoint extractor")
        return fallback(text)

    # Try to import google.generativeai and call it.
    try:
        import google.generativeai as genai
    except Exception as e:
        logger.exception("google.generativeai import failed - using fallback")
        return fallback(text)

    try:
        # configure using key
        genai.configure(api_key=GEMINI_KEY)

        # NOTE: the exact method / signature depends on library version.
        # We'll try a couple of likely variants; if none work, fallback.
        prompt = f"Extract 3 concise key points from this product review:\n\n{text}\n\nReturn as bullets."

        # Variant A: older/newer library may use model.generate or model.generate_text
        try:
            # newer pattern (example)
            res = genai.generate_text(model="gemini-pro", input=prompt)
            # res might be object with .text or string-like
            if hasattr(res, "text"):
                return res.text
            return str(res)
        except Exception:
            # Variant B: model.generate_content / model.generate
            try:
                model = genai.GenerativeModel("gemini-pro")
                out = model.generate_content(prompt)
                if hasattr(out, "text"):
                    return out.text
                return str(out)
            except Exception:
                logger.exception("Gemini generate attempt failed - using fallback")
                return fallback(text)

    except Exception as e:
        logger.exception("Gemini call failed - using fallback")
        return fallback(text)
