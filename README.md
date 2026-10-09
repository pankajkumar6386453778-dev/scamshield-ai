# Dataset setup

1. Download the UCI SMS Spam Collection:
   https://archive.ics.uci.edu/dataset/228/sms+spam+collection
2. Extract the `SMSSpamCollection` file into this directory.
3. Expected path: `data/SMSSpamCollection`
4. The file is tab-separated and should contain `label<TAB>message`.

The raw dataset is not included in this repository. Review the source terms and cite the dataset in your submission.
# 🛡️ ScamShield AI

# 🛡️ ScamShield AI

### AI-Powered Scam Message and Suspicious URL Detection

ScamShield AI is a machine learning-based project designed to identify potentially fraudulent SMS messages and analyze suspicious URLs. It uses Natural Language Processing (NLP), Python, and machine learning techniques to help users recognize possible online scams.

## 🚀 Features

* **SMS Scam Detection:** Classifies SMS messages as spam or legitimate using machine learning.
* **Suspicious URL Analysis:** Analyzes URL patterns and identifies potentially risky characteristics.
* **Interactive Dashboard:** User-friendly web interface built with Streamlit.
* **Batch Message Checking:** Supports checking multiple messages.
* **Model Evaluation:** Provides model evaluation functionality.
* **Automated Tests:** Includes tests for prediction and URL analysis modules.

## 🛠️ Technologies Used

* Python
* Streamlit
* Scikit-learn
* Natural Language Processing (NLP)
* Pandas
* Machine Learning
* Pytest

## 📂 Project Structure

```text
scamshield-ai/
├── app.py
├── src/
│   ├── __init__.py
│   ├── predict.py
│   ├── url_analyzer.py
│   └── train_model.py
├── tests/
│   ├── test_predict.py
│   └── test_url_analyzer.py
├── data/
│   └── README.md
├── models/
│   └── .gitkeep
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## ⚙️ Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR-USERNAME/scamshield-ai.git
cd scamshield-ai
```

Replace `YOUR-USERNAME` with your GitHub username.

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

## 📊 Dataset and Model Training

This project uses the UCI SMS Spam Collection dataset for SMS spam classification.

Dataset: https://archive.ics.uci.edu/dataset/228/sms+spam+collection

1. Download the dataset.
2. Extract the `SMSSpamCollection` file into the project's `data/` folder.
3. Train the machine learning model:

```bash
python -m src.train_model
```

Follow the training script's output and ensure the trained model artifacts are saved in the locations expected by the application.

## ▶️ Run the Application

After completing the required model training, start the Streamlit dashboard:

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to use the application.

## 🧪 Run Tests

```bash
pytest
```

## 🔍 How It Works

1. The user enters an SMS message or a URL.
2. The application analyzes the input using its configured machine learning model or URL heuristics.
3. The application displays a prediction or risk assessment.
4. Users can review the result and take appropriate precautions.

## 🔐 Safety Disclaimer

ScamShield AI is an educational project and should be used as a preliminary screening tool. It cannot guarantee that a message or URL is safe or malicious. Avoid clicking suspicious links, sharing passwords or OTPs, or providing sensitive information to unknown sources.

URL analysis uses heuristic checks and does not prove whether a website is genuinely safe. Always verify suspicious messages and websites independently.

## 🎯 Project Objective

The goal of ScamShield AI is to explore how machine learning and automated URL analysis can help raise awareness about SMS scams and online fraud.

## 🔮 Future Improvements

* Integrate more advanced NLP models.
* Improve detection accuracy using larger datasets.
* Add phishing website intelligence and reputation checks.
* Support additional languages.
* Deploy the application online for public testing.

## 👨‍💻 Author

**YOUR NAME**

GitHub: https://github.com/YOUR-USERNAME

## 📄 License

This project is distributed under the license included in this repository. See the `LICENSE` file for details.

