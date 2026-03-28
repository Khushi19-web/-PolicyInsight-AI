import streamlit as st
import fitz
import re
import spacy
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="PolicyPro AI",
    page_icon="📑",
    layout="wide"
)

# -----------------------------------
# CUSTOM UI STYLE
# -----------------------------------

st.markdown("""
<style>

.stApp {
background: linear-gradient(120deg,#eef2ff,#f9fbff);
}

h1,h2,h3{
color:#1f3c88;
}

.summary-box{
background:white;
padding:20px;
border-radius:10px;
border-left:6px solid #4b6cb7;
box-shadow:0 3px 8px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

st.title("📑 PolicyPro – AI Insurance Policy Analyzer")
st.write("Upload your policy and instantly understand coverage, exclusions and key details.")

# -----------------------------------
# LOAD NLP MODEL
# -----------------------------------

nlp = spacy.load("en_core_web_sm")

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("⚙ Settings")

policy_type = st.sidebar.selectbox(
"Policy Type",
["Vehicle","Health","Life","Travel","Other"]
)

summary_mode = st.sidebar.selectbox(
"Summary Mode",
["TF-IDF","GenAI Style"]
)

summary_length = st.sidebar.slider(
"Summary Length",
3,10,5
)

# -----------------------------------
# TEXT EXTRACTION
# -----------------------------------

def extract_text_from_pdf(file):

    text=""

    doc=fitz.open(stream=file.read(),filetype="pdf")

    for page in doc:
        text+=page.get_text()

    return text


def extract_text_from_txt(file):

    return file.read().decode("utf-8")

# -----------------------------------
# CLEAN TEXT
# -----------------------------------

def clean_text(text):

    text=text.lower()

    text=re.sub(r'[^a-zA-Z0-9₹\s]',' ',text)

    text=re.sub(r'\s+',' ',text)

    return text.strip()

# -----------------------------------
# SENTENCE TOKENIZATION
# -----------------------------------

def sentence_tokenize(text):

    doc=nlp(text)

    return [sent.text.strip() for sent in doc.sents]

# -----------------------------------
# TF-IDF SUMMARY
# -----------------------------------

def tfidf_summary(sentences,n):

    vectorizer=TfidfVectorizer(stop_words="english")

    tfidf_matrix=vectorizer.fit_transform(sentences)

    scores=np.sum(tfidf_matrix.toarray(),axis=1)

    ranked=np.argsort(scores)[-n:]

    selected=[sentences[i] for i in sorted(ranked)]

    return " ".join(selected)

# -----------------------------------
# GENAI STYLE SUMMARY
# -----------------------------------

def genai_summary(text):

    doc=nlp(text)

    sentences=[sent.text for sent in doc.sents][:6]

    return " ".join(sentences)

# -----------------------------------
# KEYWORDS
# -----------------------------------

def extract_keywords(text):

    vectorizer=TfidfVectorizer(stop_words="english",max_features=10)

    vectorizer.fit([text])

    return vectorizer.get_feature_names_out()

# -----------------------------------
# ENTITIES
# -----------------------------------

def extract_entities(text):

    doc=nlp(text)

    return [(ent.text,ent.label_) for ent in doc.ents]

# -----------------------------------
# COVERAGE
# -----------------------------------

def detect_coverage(text):

    words=["coverage","covered","benefit","protection"]

    sentences=sentence_tokenize(text)

    return [s for s in sentences if any(w in s.lower() for w in words)]

# -----------------------------------
# EXCLUSIONS
# -----------------------------------

def detect_exclusions(text):

    words=["not covered","excluded","exclusion"]

    sentences=sentence_tokenize(text)

    return [s for s in sentences if any(w in s.lower() for w in words)]

# -----------------------------------
# CLAIM INFO
# -----------------------------------

def detect_claims(text):

    words=["claim","damage","accident","theft"]

    sentences=sentence_tokenize(text)

    return [s for s in sentences if any(w in s.lower() for w in words)]

# -----------------------------------
# MONEY DETECTION
# -----------------------------------

def extract_money(text):

    doc=nlp(text)

    return [ent.text for ent in doc.ents if ent.label_=="MONEY"]

# -----------------------------------
# DATE DETECTION
# -----------------------------------

def extract_dates(text):

    doc=nlp(text)

    return [ent.text for ent in doc.ents if ent.label_=="DATE"]

# -----------------------------------
# RISK LEVEL
# -----------------------------------

def risk_level(exclusions):

    if len(exclusions)>5:
        return "High Risk"

    elif len(exclusions)>2:
        return "Medium Risk"

    else:
        return "Low Risk"

# -----------------------------------
# FILE UPLOAD
# -----------------------------------

uploaded_file=st.file_uploader(
"Upload Policy Document",
type=["pdf","txt"]
)

# -----------------------------------
# PROCESSING
# -----------------------------------

if uploaded_file:

    with st.spinner("Analyzing policy..."):

        if uploaded_file.type=="application/pdf":
            raw_text=extract_text_from_pdf(uploaded_file)
        else:
            raw_text=extract_text_from_txt(uploaded_file)

        cleaned=clean_text(raw_text)

        sentences=sentence_tokenize(cleaned)

        if summary_mode=="TF-IDF":
            summary=tfidf_summary(sentences,summary_length)
        else:
            summary=genai_summary(raw_text)

        keywords=extract_keywords(raw_text)

        entities=extract_entities(raw_text)

        coverage=detect_coverage(raw_text)

        exclusions=detect_exclusions(raw_text)

        claims=detect_claims(raw_text)

        money=extract_money(raw_text)

        dates=extract_dates(raw_text)

        risk=risk_level(exclusions)

    st.success("Analysis Complete")

    # -----------------------------------
    # METRICS
    # -----------------------------------

    col1,col2,col3,col4=st.columns(4)

    col1.metric("Sentences",len(sentences))
    col2.metric("Coverage Clauses",len(coverage))
    col3.metric("Exclusions",len(exclusions))
    col4.metric("Risk Level",risk)

    # -----------------------------------
    # TABS
    # -----------------------------------

    tab1,tab2,tab3,tab4,tab5=st.tabs([
    "Summary",
    "Insights",
    "Coverage",
    "Policy Details",
    "Entities"
    ])

    # SUMMARY
    with tab1:

        st.markdown(
        f'<div class="summary-box">{summary}</div>',
        unsafe_allow_html=True
        )

        st.download_button(
        "Download Summary",
        summary,
        file_name="policy_summary.txt"
        )

    # INSIGHTS
    with tab2:

        chart_data=pd.DataFrame({
        "Type":["Coverage","Exclusions"],
        "Count":[len(coverage),len(exclusions)]
        })

        st.bar_chart(chart_data.set_index("Type"))

        st.subheader("Keywords")

        st.write(list(keywords))

    # COVERAGE
    with tab3:

        st.subheader("Coverage")

        for c in coverage[:5]:
            st.write("✔",c)

        st.subheader("Exclusions")

        for e in exclusions[:5]:
            st.write("❌",e)

        st.subheader("Claim Related")

        for cl in claims[:5]:
            st.write("📌",cl)

    # POLICY DETAILS
    with tab4:

        st.subheader("Coverage Amounts")

        st.write(money)

        st.subheader("Important Dates")

        st.write(dates)

    # ENTITIES
    with tab5:

        df=pd.DataFrame(entities,columns=["Entity","Type"])

        st.dataframe(df)

# -----------------------------------
# SIMPLE POLICY Q&A
# -----------------------------------

st.subheader("Ask About Policy")

question=st.text_input("Ask a question about the uploaded policy")

if question and uploaded_file:

    if "coverage" in question.lower():
        st.write("Coverage information:",coverage[:2])

    elif "claim" in question.lower():
        st.write("Claim related clauses:",claims[:2])

    elif "date" in question.lower():
        st.write("Policy dates:",dates)

    else:
        st.write("Please ask about coverage, claims or dates.")