
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Symptom MediCare", page_icon="🩺", layout="centered")

st.markdown("""
<style>
    .stApp {
        background-color: #ffffff;
        color: #111 !important;
    }

    h1, h2, h3, .stMarkdown p {
        color: #111 !important;
    }

    .stButton > button {
        background-color: #1976d2;
        color: white;
        border-radius: 6px;
        padding: 10px 16px;
        font-size: 16px;
    }

    .stButton > button:hover {
        background-color: #125aa0;
    }

    div[data-baseweb="select"] > div {
        background-color: white !important;
        color: black !important;
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

user_symptoms = {}

with st.form("symptom_form"):
    st.markdown("### 📝 Please select your symptom levels below:")

    for symptom, options in symptom_option_mapping.items():
        # Custom visible label
        #st.markdown(f"<label style='font-weight: 600; color: #000;'>{symptom}</label>", unsafe_allow_html=True)
        # Blank label in the selectbox so only the styled markdown shows
        user_symptoms[symptom] = st.selectbox("", options, key=symptom)

    submitted = st.form_submit_button("🧪 Predict Disease")
    



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

    st.markdown(f"<div style='color:#111;font-size:18px;'><strong>🎯 Based on your symptoms, the most likely disease is:</strong> <span style='font-size:20px;color:#0d47a1'><strong>{prediction}</strong></span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:#333;font-size:16px;'>🧪 <strong>Prediction Confidence:</strong> {confidence:.2f}%</div>", unsafe_allow_html=True)

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
