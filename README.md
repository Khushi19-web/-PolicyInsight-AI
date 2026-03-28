# 📄 README.md (Copy This)

```markdown
# 📑 PolicyInsight AI

## 🚀 AI-Based Insurance Policy Summarization System

PolicyInsight AI is an NLP-based project that automatically analyzes insurance policy documents and generates a concise, easy-to-understand summary along with important extracted information.

---

## 📌 Problem Statement

Insurance policy documents are long and complex, making them difficult for users to understand. Important details such as coverage, exclusions, claim information, and key dates are often hard to find.

This project solves the problem by using AI and NLP techniques to automatically extract and summarize key information from policy documents.

---

## 🎯 Features

- 📄 Upload Policy PDF
- 🧠 AI-Based Text Summarization (TF-IDF)
- 📊 Named Entity Recognition (spaCy)
- 💰 Extract Coverage Amount, Dates, and Names
- 📌 Claim Information Detection
- 📋 Bullet / Paragraph / Highlights Summary
- 📏 Custom Summary Length (Short, Medium, Detailed)
- ☁ Word Cloud Visualization
- ⚠ Policy Risk Detection
- ⬇ Download Summary

---

## 🛠 Technologies Used

- Python
- Natural Language Processing (NLP)
- spaCy
- Scikit-learn (TF-IDF)
- PyMuPDF (PDF Extraction)
- Streamlit (Web App)
- Matplotlib & WordCloud

---

## ⚙️ Project Workflow

1. Upload policy PDF
2. Extract text from PDF
3. Clean and preprocess text
4. Convert text into sentences
5. Apply TF-IDF algorithm
6. Rank sentences based on importance
7. Generate summary
8. Extract entities (Name, Date, Money, Organization)
9. Detect claim information
10. Display results using Streamlit UI

---

## 📂 Project Structure

```

PolicyInsight_AI
│
├── app.py
├── main.ipynb
├── requirements.txt
└── sample_policy.pdf

```

---

## ▶️ How to Run the Project

### Step 1: Install Dependencies
```

pip install -r requirements.txt

```

### Step 2: Download NLP Model
```

python -m spacy download en_core_web_sm

```

### Step 3: Run Streamlit App
```

streamlit run app.py

```

---

## 📊 Output

- Generated Policy Summary
- Extracted Information:
  - Policy Holder Name
  - Important Dates
  - Coverage Amount
  - Claim Details
- Word Cloud Visualization

---

## 📌 Example Use Case

Upload an insurance policy PDF → System generates summary → Extracts key details → Helps users understand policy quickly.

---

## 🙌 Acknowledgment

This project was developed with guidance and assistance from AI tools like ChatGPT to enhance understanding and implementation.

---

## 👩‍💻 Author

Khushi Shinde  
B.Tech Computer Engineering  
Data Analytics & Data Science Enthusiast

---


