from pathlib import Path
import joblib
import pandas as pd
import streamlit as st
import plotly.express as px

from src.url_analyzer import analyze_url
from src.predict import predict_message

ROOT = Path(__file__).parent
MODEL_PATH = ROOT / "models" / "message_model.joblib"
METRICS_PATH = ROOT / "models" / "metrics.json"

st.set_page_config(page_title="ScamShield AI", page_icon="🛡️", layout="wide")

st.title("🛡️ ScamShield AI")
st.caption("Explainable scam-risk screening for messages and URLs")
st.warning(
    "This is a prototype, not a guarantee of safety. Do not share passwords, OTPs, "
    "payment PINs, or private financial information. The app does not open submitted URLs."
)

tab_message, tab_url, tab_batch, tab_metrics, tab_about = st.tabs(
    ["Message Check", "URL Check", "Batch Check", "Model Evaluation", "About & Safety"]
)

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)

model = load_model()

with tab_message:
    st.subheader("Check a suspicious message")
    message = st.text_area(
        "Paste SMS or email text",
        placeholder="Example: Your account is locked. Verify immediately...",
        height=150,
        max_chars=10000,
    )
    if st.button("Analyze message", type="primary"):
        if not message.strip():
            st.error("Enter a message first.")
        elif model is None:
            st.error("Model file not found. Follow README instructions to train the model.")
        else:
            result = predict_message(model, message)
            label = result["label"].upper()
            st.metric("Model classification", label)
            if result.get("estimated_probability") is not None:
                st.caption(
                    f"Estimated model score for the predicted class: "
                    f"{result['estimated_probability']:.1%}. This is not a calibrated real-world scam probability."
                )
            if result["label"] == "spam":
                st.error("This message resembles spam in the training data. Verify independently before acting.")
            else:
                st.info("The model did not classify this as spam. This does NOT prove the message is safe.")
            st.markdown("**Safety checklist**")
            st.write("- Do not share OTPs, passwords or payment PINs.")
            st.write("- Verify the sender through an independently obtained official channel.")
            st.write("- Do not click suspicious links to test them.")

with tab_url:
    st.subheader("Inspect URL structure")
    url = st.text_input("URL to analyze", placeholder="https://example.com/account/verify")
    if st.button("Analyze URL"):
        result = analyze_url(url)
        if result.get("error"):
            st.error(result["error"])
        else:
            st.metric("Heuristic risk level", result["risk_level"])
            st.caption("This is a rule-based heuristic, not a trained phishing classifier.")
            st.write(f"**Host:** `{result['host']}`")
            st.write(f"**Scheme:** `{result['scheme'] or 'not provided'}`")
            st.write("**Indicators found**")
            if result["indicators"]:
                for item in result["indicators"]:
                    st.write(f"- {item}")
            else:
                st.write("No configured structural warning indicators were triggered.")
            st.info("HTTPS does not prove a site is trustworthy, and a warning indicator alone does not prove fraud. Do not open suspicious links.")

with tab_batch:
    st.subheader("Batch-check a CSV")
    st.write("Upload a CSV containing a column named `message`. Avoid uploading private or sensitive messages.")
    uploaded = st.file_uploader("CSV file", type=["csv"])
    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            if "message" not in df.columns:
                st.error("CSV must contain a `message` column.")
            elif model is None:
                st.error("Model file not found. Train it using the README instructions.")
            else:
                if st.button("Analyze CSV"):
                    df["prediction"] = df["message"].fillna("").astype(str).map(
                        lambda x: predict_message(model, x)["label"]
                    )
                    st.dataframe(df, use_container_width=True)
                    st.download_button(
                        "Download results",
                        df.to_csv(index=False).encode("utf-8"),
                        file_name="scamshield_results.csv",
                        mime="text/csv",
                    )
        except Exception as exc:
            st.error(f"Could not read CSV: {exc}")

with tab_metrics:
    st.subheader("Held-out model evaluation")
    if METRICS_PATH.exists():
        import json
        metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
        c1, c2, c3 = st.columns(3)
        c1.metric("Accuracy", f"{metrics.get('accuracy', 0):.3f}")
        c2.metric("Spam precision", f"{metrics.get('spam_precision', 0):.3f}")
        c3.metric("Spam recall", f"{metrics.get('spam_recall', 0):.3f}")
        st.metric("Spam F1-score", f"{metrics.get('spam_f1', 0):.3f}")
        matrix = metrics.get("confusion_matrix", [])
        if matrix:
            cm = pd.DataFrame(
                matrix,
                index=["Actual ham", "Actual spam"],
                columns=["Predicted ham", "Predicted spam"],
            )
            st.write("Confusion matrix")
            st.dataframe(cm, use_container_width=True)
        st.caption("Metrics reflect the dataset and split used during training, not guaranteed real-world performance.")
    else:
        st.info("No metrics found yet. Run `python -m src.train_model` after placing the dataset.")

with tab_about:
    st.subheader("About this project")
    st.write(
        "ScamShield AI combines a supervised SMS spam classifier with a separate "
        "rule-based URL structure analyzer. The two outputs are intentionally distinguished."
    )
    st.markdown("""
    **Limitations**
    - The SMS dataset represents spam/ham labels, not every kind of financial scam.
    - A negative model prediction does not mean a message is safe.
    - URL indicators are heuristics and can flag legitimate links.
    - The app does not query live threat-intelligence services.
    - Submitted text is processed by the app; do not enter sensitive information.
    """)
