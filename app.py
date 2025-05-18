
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Symptom MediCare", page_icon="🩺", layout="centered")

# --- Custom CSS Styling ---
 st.markdown("""
    <style>
        .stApp {
            background-color: #e3f2fd;
            font-size: 18px;
        }

        h1, h2, h3, h4 {
            color: white !important;
            font-size: 24px !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #bbdefb;
        }

        /* Markdown and paragraph text */
        .markdown-text-container p,
        .stMarkdown p,
        .stMarkdown span {
            color: white !important;
            font-size: 18px !important;
        }

        /* Selectbox, Inputs, and Form Styling */
        .stSelectbox, .stTextInput, .stForm {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 8px;
            box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
        }

        /* Button Styling */
        .stButton>button {
            background-color: #1565c0;
            color: white;
            border-radius: 10px;
            padding: 10px 16px;
            font-size: 18px !important;
        }

        .stButton>button:hover {
            background-color: #0d47a1;
            color: #ffffff;
        }

        body {
            overflow-x: hidden;
        }
    </style>
""", unsafe_allow_html=True)


             

# --- Sample Data ---
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

# --- Title & Intro ---
st.title("🩺 Symptom MediCare")
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

# --- Input Form ---
user_symptoms = {}
with st.form("symptom_form"):
    for symptom, options in symptom_option_mapping.items():
        user_symptoms[symptom] = st.selectbox(symptom, options)
    submitted = st.form_submit_button("Predict Disease")

# --- Naive Bayes Classifier ---
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
    confidence = probs.get(prediction, 0)

    st.success(f"🎯 Based on your symptoms, the most likely disease is: **{prediction}**")
    st.info(f"🧪 Prediction Confidence: **{confidence:.2f}%**")

    if probs:
        # --- Annotated Bar Chart ---
        fig, ax = plt.subplots()
        diseases = list(probs.keys())
        values = list(probs.values())

        sns.barplot(x=diseases, y=values, palette='coolwarm', ax=ax)

        for i, (disease, prob) in enumerate(zip(diseases, values)):
            ax.text(i, prob + 1, f"{prob:.1f}%", ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')

        ax.set_ylabel("Probability (%)")
        ax.set_title("Disease Prediction Probability")
        ax.set_ylim(0, max(values) + 10)

        st.pyplot(fig)
    

# --- Sidebar Info ---
st.sidebar.header("About")
st.sidebar.info("""
**Created by:** Edidiong Moses (Edimosphy) 
**Initiated by:** 3MTT Nigeria  
**Built with:** Streamlit + Python Libraries
""")
