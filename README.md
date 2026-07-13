# 🌸 AI-Powered Women's Health Support Platform

A modular AI and Machine Learning application that combines **Retrieval-Augmented Generation (RAG), Machine Learning, structured health knowledge, and rule-based tracking workflows** within a single interactive Gradio interface.

The platform provides educational support for women's health questions, PCOS-associated pattern assessment, structured symptom exploration, pregnancy journey tracking, and menstrual cycle estimation.

Rather than using a single general-purpose AI model for every task, the application applies **specialized technical approaches to different health-support workflows**.

> ⚠️ **Medical Disclaimer:** This application is intended for educational and informational purposes only. It does not diagnose medical conditions and should not replace consultation, examination, or treatment by a qualified healthcare professional.

---

## ✨ Features

### 🤖 AI Women's Health Chatbot

A women's health-focused chatbot built using a **Retrieval-Augmented Generation (RAG)** pipeline.

The system retrieves relevant information from local medical datasets before providing the retrieved context to a Hugging Face-hosted language model.

### RAG Workflow

1. Medical information is loaded from CSV datasets.
2. Dataset rows are converted into LangChain documents.
3. Documents are divided into smaller text chunks using `RecursiveCharacterTextSplitter`.
4. Sentence embeddings are generated using a Hugging Face embedding model.
5. FAISS stores the embedded medical knowledge.
6. Relevant documents are retrieved using similarity search.
7. Retrieved context is provided to the language model.
8. The model generates a concise educational response using the retrieved information.

The chatbot is instructed to focus on women's health-related questions, avoid definite diagnoses, and provide short educational responses.

### Chatbot Technologies

* LangChain
* FAISS
* Hugging Face Embeddings
* Sentence Transformers
* Hugging Face Inference API
* `HuggingFaceH4/zephyr-7b-beta`

---

## 🧪 Machine Learning-Based PCOS Risk Checker

The PCOS Risk Checker uses a trained **Random Forest Classifier** to perform a pattern-based assessment using selected health and lifestyle indicators.

The module is designed as a Machine Learning classification workflow and does not provide a clinical PCOS diagnosis.

### Model Input Features

The model uses 13 features:

* Age
* Weight
* Height
* BMI
* Menstrual cycle regularity
* Cycle length
* Recent weight gain
* Excess facial or body hair growth
* Skin darkening
* Hair loss
* Pimples
* Fast food consumption
* Regular exercise

BMI is automatically calculated from the user's height and weight.

### Model Training Pipeline

The PCOS model is trained using a structured PCOS dataset.

The training pipeline:

1. Loads the dataset using Pandas.
2. Selects the required 13 model features.
3. Separates the PCOS target variable.
4. Splits the dataset into 80% training and 20% testing data.
5. Trains a Random Forest classifier with 100 estimators.
6. Evaluates model accuracy.
7. Generates a classification report.
8. Generates a confusion matrix.
9. Calculates Random Forest feature importance.
10. Saves the trained model using Joblib.

The trained model is stored at:

```text
models/pcos_model.pkl
```

The application loads the saved model and uses it for pattern assessment.

### PCOS Assessment Output

The PCOS module displays:

* PCOS-associated pattern classification
* Model prediction confidence
* Pattern-level interpretation
* Calculated BMI
* BMI category
* PCOS-associated symptoms reported by the user
* Educational lifestyle and health recommendations

The model evaluates the **overall combination of available input features based on patterns learned during model training**.

### ⚠️ PCOS Assessment Disclaimer

The PCOS Risk Checker **cannot diagnose PCOS with certainty and should not be used as a diagnostic tool**.

The Machine Learning model performs a **pattern-based assessment using the limited health and lifestyle features available in the application and patterns learned from the training dataset**.

The result is based only on selected indicators including menstrual cycle regularity, weight changes, hair growth, skin darkening, hair loss, pimples, BMI, and other model input features.

A detected PCOS-associated pattern does not confirm that a user has PCOS. Similarly, the absence of a strong detected pattern does not rule out PCOS.

The displayed confidence represents the Machine Learning model's prediction confidence based on learned data patterns. It does **not** represent the medical probability that a user has PCOS.

PCOS diagnosis may require professional medical evaluation, clinical history, laboratory testing, hormone assessment, and imaging such as ultrasound.

Users should consult a qualified healthcare professional or gynecologist for proper evaluation and diagnosis.

---

## 🔎 Structured Symptom Checker

The Symptom Checker compares user-entered symptoms against a structured JSON health knowledge base containing approximately **100 conditions included within the application's available health data**.

Each condition contains:

* Condition name
* Medical category
* Description
* Common symptoms

### Symptom Matching Workflow

The Symptom Checker performs:

1. Exact symptom matching.
2. Similarity-based symptom matching using Python's `SequenceMatcher`.
3. Match scoring based on detected symptoms.
4. Condition ranking using the calculated match score.

The application returns up to **four possible matching conditions**.

For each possible condition, the system displays:

* Condition name
* Medical category
* Matched symptoms
* Condition description

If the entered symptoms cannot be matched with the available knowledge base, the user is encouraged to consult a qualified healthcare professional or use the AI Health Chatbot for further educational information.

### ⚠️ Symptom Checker Disclaimer

The Symptom Checker does not diagnose medical conditions.

Symptoms frequently overlap across multiple health conditions. Displayed results represent **possible symptom associations based only on the structured health data available to the application**.

Users should consult a qualified healthcare professional or gynecologist for proper examination, diagnosis, and treatment.

---

## 🤰 Pregnancy Journey Tracker

The Pregnancy Journey Tracker estimates pregnancy progress using the user's **Last Menstrual Period (LMP)** date.

The tracker calculates:

* Current pregnancy week
* Number of days pregnant
* Current trimester
* Estimated due date

The estimated due date is calculated using a standard **280-day pregnancy duration from the LMP date**.

Pregnancy weeks are mapped to structured information stored in:

```text
data/pregnancy_data.json
```

When information for the calculated pregnancy week is available, the tracker displays:

* Baby size comparison
* Baby development information
* Maternal changes
* Week-specific recommendations

The supported pregnancy tracking range is limited to weeks **1–42**.

### ⚠️ Pregnancy Tracker Disclaimer

Pregnancy calculations are estimates based on the entered Last Menstrual Period date.

Actual gestational age and estimated due dates may differ.

The Pregnancy Journey Tracker provides general educational information only and does not replace prenatal care, ultrasound assessment, or consultation with a qualified healthcare professional.

---

## 🩸 Menstrual Cycle Tracker

The Menstrual Cycle Tracker provides basic cycle information using:

* Last menstrual period date
* Average cycle length
* Period duration

The tracker calculates:

* Expected next period date
* Current cycle day
* Estimated menstrual cycle phase

Possible estimated phases include:

* Menstrual Phase
* Follicular Phase
* Ovulation Phase
* Luteal Phase

The application also checks whether the entered cycle length falls within the **21–35 day range used by the tracker**.

### ⚠️ Cycle Tracker Disclaimer

Menstrual cycle phases displayed by the application are simple date-based estimates.

Actual ovulation timing and cycle phases may vary between individuals and between cycles.

The Cycle Tracker should not be used for medical diagnosis, fertility planning, or contraception decisions.

---

## 🖥️ Gradio Interface

The current MVP uses **Gradio Blocks** to provide an interactive tab-based interface.

The application contains five primary workflows:

* 🤖 AI Health Chatbot
* 🧪 PCOS Risk Checker
* 🔎 Symptom Checker
* 🤰 Pregnancy Tracker
* 🩸 Cycle Tracker

Each health feature is implemented as an independent Python module and connected to the central Gradio application.

This modular structure allows individual workflows to use different technical approaches while remaining accessible through a single interface.

---

## 🛠️ Tech Stack

* Python
* Gradio
* Pandas
* NumPy
* Scikit-learn
* Random Forest Classifier
* Joblib
* LangChain
* FAISS
* Hugging Face Inference API
* Hugging Face Embeddings
* Sentence Transformers
* PyTorch
* JSON
* Matplotlib

---

## 📂 Project Structure

```text
AI-Womens-Health-Tracker/
│
├── data/
│   ├── Diseases_Symptoms.csv
│   ├── period-Copy.csv
│   ├── PCOS_extended_dataset.csv
│   ├── pregnancy_data.json
│   └── women_diseases.json
│
├── models/
│   └── pcos_model.pkl
│
├── modules/
│   ├── medical_chatbot.py
│   ├── symptom_checker.py
│   ├── cycle_tracker.py
│   ├── pregnancy_tracker.py
│   └── pcos_checker.py
│
├── gradio-app.py
├── train_pcos_model.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd <repository-folder>
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root directory.

Add your Hugging Face token:

```env
HF_TOKEN=your_hugging_face_token
```

The Hugging Face token is loaded using `python-dotenv` and used by the Hugging Face `InferenceClient`.

> Never commit API tokens or the `.env` file to GitHub.

---

## ▶️ Running the Application

Run the Gradio application:

```bash
python gradio-app.py
```

Gradio will display the application URL in the terminal.

Open the provided URL in a browser to access the application.

---

## 🧠 Training the PCOS Model

The repository includes a separate model training script.

Run:

```bash
python train_pcos_model.py
```

The training script:

1. Loads the PCOS dataset.
2. Selects the model input features.
3. Splits the dataset into training and testing sets.
4. Trains the Random Forest classifier.
5. Calculates model accuracy.
6. Displays the classification report.
7. Displays the confusion matrix.
8. Saves the trained model.
9. Displays a feature importance visualization.

The trained model is saved as:

```text
models/pcos_model.pkl
```

---

## 🏗️ Application Architecture

```text
Gradio Interface
       │
       ├── AI Health Chatbot
       │        │
       │        ├── CSV Medical Data
       │        ├── LangChain Documents
       │        ├── Text Splitting
       │        ├── Hugging Face Embeddings
       │        ├── FAISS Vector Database
       │        └── Hugging Face Language Model
       │
       ├── PCOS Risk Checker
       │        │
       │        └── Random Forest Model
       │
       ├── Symptom Checker
       │        │
       │        └── JSON Health Knowledge Base
       │
       ├── Pregnancy Tracker
       │        │
       │        └── Pregnancy Week JSON Data
       │
       └── Menstrual Cycle Tracker
                │
                └── Date and Cycle Calculations
```

---

## ⚠️ General Limitations

* The application cannot diagnose medical conditions.
* PCOS assessment is limited to selected model features and patterns learned from the training dataset.
* High Machine Learning model accuracy does not represent clinical diagnostic accuracy.
* Symptom matching depends on conditions and symptoms available in the JSON knowledge base.
* Similar symptoms may occur across multiple health conditions.
* Similarity-based text matching may not understand every natural-language symptom description.
* Pregnancy calculations depend on the entered LMP date.
* Menstrual cycle phases are simple date-based estimates.
* AI-generated responses may contain incomplete or inaccurate information.
* Laboratory tests, physical examinations, imaging, and clinical evaluation cannot be replaced by this application.

---

## 🚀 Future Roadmap

The current Gradio application represents the first working MVP of the platform.

Planned technical and product improvements include:

* Migrate the Gradio MVP to a React frontend and FastAPI backend.
* Introduce authenticated user profiles and persistent user-specific health history.
* Build a longitudinal health timeline for structured cycle and symptom records.
* Connect relevant historical records across independent health workflows.
* Add grounded medical report terminology and report-impression explanation.
* Introduce rule-based pattern-awareness workflows using historical user records.
* Improve natural-language symptom normalization and medical terminology mapping.
* Improve RAG retrieval quality, source filtering, and retrieval evaluation.
* Add stronger input validation.
* Add automated unit and integration tests.
* Improve menstrual cycle phase estimation.
* Improve vector database management.
* Deploy the platform as a publicly accessible web application.

Future development will continue to prioritize **responsible AI boundaries, transparent system limitations, and modular architecture**.

---

## 🎯 Project Purpose

The project explores a **modular AI architecture for women's health support** by combining grounded information retrieval, Machine Learning-based pattern assessment, structured symptom exploration, and deterministic health tracking workflows.

Rather than relying on a single general-purpose AI model, the application uses specialized techniques for different tasks:

* **Retrieval-Augmented Generation (RAG)** for women's health information retrieval and educational responses.
* **Machine Learning classification** for PCOS-associated pattern assessment.
* **Structured knowledge matching** for symptom exploration.
* **Rule-based calculations** for pregnancy and menstrual cycle tracking.

The project focuses on **modular system design, responsible AI boundaries, and the practical integration of multiple AI and software engineering techniques within a domain-focused application**.

The current implementation serves as a working MVP and a foundation for exploring persistent health timelines, connected health context, and more structured women's health support workflows.

---

## 👩‍💻 Author

**Umaima Mughal**

Software Engineering Student

Interested in Artificial Intelligence, Machine Learning, Generative AI, and Software Development.
