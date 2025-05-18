
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Symptom MediCare", page_icon="🩺", layout="centered")

st.markdown("""
    <style>
        .main { background-blue: #f4f9fd; }
        h1, h3 { color: #0f4c75; }
        .stButton>button {
            background-color: #3282b8;
            color: white;
            border-radius: 8px;
        }
        
        
    </style>
""", unsafe_allow_html=True)

# --- Load data ---
data = {
    'Disease': ['Malaria', 'Malaria', 'Malaria',
                'Typhoid', 'Typhoid', 'Typhoid',
                'HIV/AIDS', 'HIV/AIDS', 'HIV/AIDS'],
    'Fever': ['High', 'Medium', 'High',
              'High', 'High', 'Medium',
              'Medium', 'Low', 'Low'],
    'Fatigue': ['Very High', 'High', 'High',
                'High', 'Medium', 'Low',
                'Very High', 'High', 'High'],
    'Headache': ['High', 'Medium', 'High',
                 'Very High (Heaviness)', 'High', 'Medium',
                 'Low', 'Medium', 'Medium'],
    'Vomiting': ['Yes', 'Yes', 'Yes',
                 'Yes', 'Yes', 'No',
                 'Yes', 'Yes', 'Yes'],
    'Skin Rash': ['Mild', 'Mild', 'None',
                  'Rose spots', 'Mild', 'None',
                  'High', 'High', 'Medium'],
    'Muscle Joint Pain': ['Yes', 'No', 'Medium',
                          'No', 'Yes', 'Medium',
                          'Yes', 'Yes', 'Yes'],
    'Weight Loss': ['Moderate', 'Mild', 'Severe',
                    'Mild', 'Mild', 'Moderate',
                    'Severe', 'Severe', 'Severe'],
    'Diarrhea': ['No', 'Yes', 'No',
                 'Yes', 'No', 'Yes',
                 'Yes', 'Yes', 'Yes'],
    'Night Sweats': ['Yes', 'Yes', 'No',
                     'No', 'No', 'No',
                     'Yes', 'Yes', 'Yes'],
    'Lymph Node Swelling': ['No', 'No', 'No',
                             'No', 'No', 'No',
                             'Yes', 'Yes', 'High']
}
df = pd.DataFrame(data)

# --- Title ---
st.title("🩺 Symptom MediCare")

# --- Intro ---
st.markdown("""
Welcome to **Symptom MediCare**!

This demo app is designed to assist healthcare workers and individuals in predicting the likelihood of **Malaria**, **Typhoid**, or **HIV/AIDS** based on symptom input.

Please select your symptom levels below:
""")

# --- Symptom Options ---
symptom_option_mapping = {
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

user_symptoms = {}
with st.form("symptom_form"):
    for symptom, options in symptom_option_mapping.items():
        user_symptoms[symptom] = st.selectbox(symptom, options)
    submitted = st.form_submit_button("Predict Disease")

# --- Naive Bayes Prediction ---
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

# --- Display Result ---
if submitted:
    prediction, probs = predict_disease(df, user_symptoms)
    st.success(f"🎯 Based on your symptoms, the most likely disease is: **{prediction}**")

    if probs:
        # Plot probabilities
        fig, ax = plt.subplots()
        diseases = list(probs.keys())
        values = list(probs.values())
        sns.barplot(x=diseases, y=values, palette='coolwarm', ax=ax)
        ax.set_ylabel("Probability (%)")
        ax.set_title("Disease Prediction Probability")
        st.pyplot(fig)
        
st.sidebar.header("About")
st.sidebar.info("""
**Created by:** Edidiong Moses  
**Initiated by:** 3MTT Nigeria  
**Built with:** Streamlit + Naive Bayes  
