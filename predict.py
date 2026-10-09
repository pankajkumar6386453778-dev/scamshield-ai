def predict_message(model, text: str) -> dict:
    """Return a simple prediction result from a fitted scikit-learn Pipeline."""
    cleaned = (text or "").strip()
    if not cleaned:
        raise ValueError("Message cannot be empty.")

    label = str(model.predict([cleaned])[0]).lower()
    probability = None

    if hasattr(model, "predict_proba"):
        try:
            probs = model.predict_proba([cleaned])[0]
            classes = [str(c).lower() for c in model.classes_]
            predicted_index = classes.index(label)
            probability = float(probs[predicted_index])
        except (ValueError, AttributeError, IndexError):
            probability = None

    return {
        "label": label,
        "estimated_probability": probability,
    }
