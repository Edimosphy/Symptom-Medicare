
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Symptom MediCare", page_icon="🩺", layout="centered")

st.markdown("""
    <style>
        .main { background-color: #f4f9fd; }
        h1, h3 { color: #0f4c75; }
        .stButton>button {
            background-color: #3282b8;
            color: white;
            border-radius: 8px;
        }
        .stSelectbox > div > div:first-child {
            background-color: #ffffff;
            border: 1px solid #d9d9d9;
            border-radius: 6px;
        }
    </style>
""", unsafe_allow_html=True)

data = {
    'Disease': ['Malaria', 'Malaria', 'Malaria',
                'Typhoid', 'Typhoid', 'Typhoid',
                'HIV/AIDS', 'HIV/AIDS', 'HIV/AIDS'],
    'Fever': ['High', 'Medium', 'High', 'High', 'High', 'Medium', 'Medium', 'Low', 'Low'],
    'Fatigue': ['Very High', 'High', 'High', 'High', 'Medium', 'Low', 'Very High', 'High', 'High'],
    'Headache': ['High', 'Medium', 'High', 'Very High (Heaviness)', 'High', 'Medium', 'Low', 'Medium', 'Medium'],
    'Vomiting': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'Yes'],
    'Skin Rash': ['Mild', 'Mild', 'None', 'Rose spots', 'Mild', 'None', 'High', 'High', 'Medium'],
    'Muscle Joint Pain': ['Yes', 'No', 'Medium', 'No', 'Yes', 'Medium', 'Yes', 'Yes', 'Yes'],
    'Weight Loss': ['Moderate', 'Mild', 'Severe', 'Mild', 'Mild', 'Moderate', 'Severe', 'Severe', 'Severe'],
    'Diarrhea': ['No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes'],
    'Night Sweats': ['Yes', 'Yes', 'No', 'No', 'No', 'No', 'Yes', 'Yes', 'Yes'],
    'Lymph Node Swelling': ['No', 'No', 'No', 'No', 'No', 'No', 'Yes', 'Yes', 'High']
}
df = pd.DataFrame(data)

symptom_options = {
    'Fever': ['High', 'Medium', 'Low'],
    'Fatigue': ['Very High', 'High', 'Medium', 'Low'],
    'Headache': ['Very High (Heaviness)', 'High', 'Medium', 'Low'],
    'Vomiting': ['Yes', 'No'],
    'Skin Rash': ['High', 'Medium', 'Mild', 'None', 'Rose spots'],
    'Muscle Joint Pain': ['Yes', 'No', 'Medium'],
    'Weight Loss': ['Severe', 'Moderate', 'Mild'],
    'Diarrhea': ['Yes', 'No'],
    'Night Sweats': ['Yes', 'No'],
    'Lymph Node Swelling': ['High', 'Yes', 'No']
}

st.title("🩺 Symptom MediCare")
st.markdown("A smart diagnostic tool to help predict **Malaria**, **Typhoid**, or **HIV/AIDS** based on your symptoms.")

st.markdown("### 🔎 Tell us about your symptoms")
user_symptoms = {}
with st.form("assessment_form"):
    cols = st.columns(2)
    for i, (symptom, options) in enumerate(symptom_options.items()):
        with cols[i % 2]:
            user_symptoms[symptom] = st.selectbox(f"🩹 {symptom}", options, key=symptom)
    submitted = st.form_submit_button("🧪 Predict Disease")

def predict_disease(df, user_symptoms):
    disease_probs = {}
    total_count = len(df)
    diseases = df['Disease'].unique()

    for disease in diseases:
        sub_df = df[df['Disease'] == disease]
        prior = len(sub_df) / total_count
        likelihood = 1.0
        for symptom, value in user_symptoms.items():
            match_count = len(sub_df[sub_df[symptom] == value])
            symptom_prob = (match_count + 1) / (len(sub_df) + len(df[symptom].unique()))
            likelihood *= symptom_prob
        disease_probs[disease] = prior * likelihood

    total_prob = sum(disease_probs.values())
    if total_prob == 0:
        return "No Match Found", {}
    for disease in disease_probs:
        disease_probs[disease] = (disease_probs[disease] / total_prob) * 100

    predicted = max(disease_probs, key=disease_probs.get)
    return predicted, disease_probs

if submitted:
    prediction, probs = predict_disease(df, user_symptoms)
    st.markdown("### 🧾 Prediction Result")
    if prediction == "No Match Found":
        st.error("⚠️ We could not match your symptoms with any known disease in our model.")
    else:
        st.success(f"✅ The most likely disease is: **{prediction}**")
    if probs:
        st.markdown("### 📊 Prediction Probability Chart")
        fig, ax = plt.subplots()
        sns.barplot(x=list(probs.keys()), y=list(probs.values()), palette="Blues", ax=ax)
        ax.set_ylabel("Probability (%)")
        ax.set_xlabel("Disease")
        ax.set_ylim(0, 100)
        ax.set_title("Likelihood of Each Disease")
        st.pyplot(fig)

st.sidebar.header("About")
st.sidebar.info("""
**Created by:** Edidiong Moses  
**Initiated by:** 3MTT Nigeria  
**Built with:** Streamlit + Naive Bayes  
""")
