
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Enforce Light UI Styling ---
st.set_page_config(page_title="Symptom MediCare", layout="centered")
st.markdown("""
    <style>
        .stApp { background-color: #ffffff; color: #111; }
        h1, h2, h3, .stMarkdown p { color: #111 !important; }
        .stButton > button {
            background-color: #1565c0 !important;
            color: white !important;
            border-radius: 8px;
            padding: 10px 18px;
        }
        .stButton > button:hover { background-color: #0d47a1 !important; }
    </style>
""", unsafe_allow_html=True)

# --- Title & Intro ---
st.title("Symptom MediCare 🩺")
st.markdown("Welcome to **Symptom MediCare**! This tool predicts the likelihood of **Malaria**, **Typhoid**, or **HIV/AIDS** and provides biochemical nutritional guidance.")

# --- Symptom Options & Dataset (Keep your existing data) ---
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

data = {
    'Disease': ['Malaria', 'Malaria', 'Malaria', 'Typhoid', 'Typhoid', 'Typhoid', 'HIV/AIDS', 'HIV/AIDS', 'HIV/AIDS'],
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

# --- Naive Bayes Classifier Function ---
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
    if total_prob == 0: return "No Match Found", {}
    for disease in disease_probs:
        disease_probs[disease] = (disease_probs[disease] / total_prob) * 100
    return max(disease_probs, key=disease_probs.get), disease_probs

# --- Form Section ---
user_symptoms = {}
with st.form("symptom_form"):
    st.markdown("### 📝 Select your symptoms:")
    cols = st.columns(2)
    for i, (symptom, options) in enumerate(symptom_option_mapping.items()):
        with cols[i % 2]:
            user_symptoms[symptom] = st.selectbox(f"{symptom}", options, key=symptom)
    submitted = st.form_submit_button("🧪 Predict Disease")

# --- Logic After Prediction ---
if submitted:
    prediction, probs = predict_disease(df, user_symptoms)
    st.session_state['prediction'] = prediction
    st.session_state['confidence'] = probs.get(prediction, 0)
    st.session_state['probs'] = probs

if 'prediction' in st.session_state:
    prediction = st.session_state['prediction']
    confidence = st.session_state['confidence']
    
    st.success(f"🎯 Likely Condition: **{prediction}** ({confidence:.2f}%)")
    
    # --- The Two New Buttons ---
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Recommendations"):
            st.markdown("---")
            st.subheader(f"Recovery Plan for {prediction}")
            
            if prediction == "Malaria":
                st.write("""
                **Medical Note:** Malaria causes oxidative stress and red blood cell turnover. Focus on liver recovery and hydration
                * **Hydration:** Drink Coconut water (replaces electrolytes lost to fever).
                * **Anti-inflammatory:** Take Ginger and Turmeric tea to reduce systemic inflammation.
                * **Recovery:** Take Pawpaw leaf extract (widely studied for platelet support) and Vitamin C from Oranges/Guavas to boost immunity.
                * **Tip:** Avoid heavy fats; your liver is currently working hard to clear the parasite.
                         Avoid self medication with previously prescribed antimalarials as this might result to antimicrobial resistance.
                         Get a proper prescription from a healthcare provider.
                """)
            elif prediction == "Typhoid":
                st.write("""
                **Medical Note:** Typhoid affects the intestinal lining. Focus on gut health.
                * **Diet:** Eat soft, bland foods (Pap/Akamu, boiled carrots).
                * **Antibacterial Support:** Take Garlic and Honey (natural antimicrobial properties, but *not* a replacement for prescribed medicines).
                * **Probiotics:** Take local yogurt or fermented foods to restore gut flora.
                * **Tip:** Boil all drinking water to 100°C to prevent re-infection.
                         Avoid self medication with previously prescribed antibiotics as this might result to antimicrobial resistance.
                         Get a proper prescription from a healthcare provider.
                """)
            elif prediction == "HIV/AIDS":
                st.write("""
                **Medical Note:** Focus on immune system and preventing muscle wasting.
                * **Protein:** High-quality protein (Beans, Lean Meat, Soya) to prevent weight loss.
                * **Micronutrients:** Moringa oleifera (rich in iron and vitamins) and Selenium-rich foods.
                * **Tip:** Avoid raw or unpasteurized foods to prevent opportunistic infections.
                         Go to the nearest hospital to know your HIV status and get a proper prescription from a healthcare provider.
                         
                """)
            
            st.warning("⚠️ **Note on Resistance:** Do NOT take leftover antibiotics. Incomplete dosages create 'Superbugs'. Use these diets to support, not replace, clinical treatment.")

    with col2:
        # Link to Google Maps for "Hospital near me"
        map_url = "https://www.google.com/maps/search/hospital+near+me"
        st.link_button("🏥 Find Nearest Hospital", map_url)

    # --- Chart (Keep existing) ---
    st.markdown("### 📊 Probability Chart")
    fig, ax = plt.subplots()
    sns.barplot(x=list(st.session_state['probs'].keys()), y=list(st.session_state['probs'].values()), palette='coolwarm', ax=ax)
    st.pyplot(fig)

# --- AI Bot Section (Guardrailed) ---
# This section is intentionally left out to avoid any potential issues with AI-generated content. The focus is on providing accurate, evidence-based recommendations without the risk of misinformation.
st.markdown("---")
st.subheader("💬 Ask Your Symptom MediCare Assistant Bot")

# Initialize Chat History and Name in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Logic
if prompt := st.chat_input("Ask me about your diet or recovery tips..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_low = prompt.lower()
        
        # 1. Handle Greetings and Name Acquisition
        if st.session_state.user_name is None:
            if any(word in p_low for word in ["hello", "hi", "hey", "how far"]):
                response = "Hello! I am your Symptom MediCare assistant. Before we dive into your health tips, **what is your name?**"
            elif "name is" in p_low or "call me" in p_low:
                # Simple logic to extract the last word as the name
                name = prompt.split()[-1].strip("!?.")
                st.session_state.user_name = name
                response = f"Nice to meet you, **{name}**! How can I help you with your recovery or diet today?"
            else:
                response = "Hello! I'd love to help, but may I know **your name** first?"
        
        # 2. Handle Predictions and Nutritional Logic (Starting with the User's Name)
        else:
            user_name = st.session_state.user_name
            
            if 'prediction' in st.session_state:
                current_disease = st.session_state['prediction']
                
                # Biochemist Guardrail Logic
                nutritional_keywords = ["eat", "drink", "food", "diet", "nutrition", "moringa", "pap", "water", "fruit", "recovery", "better"]
                
                if any(word in p_low for word in nutritional_keywords):
                    response = f"**{user_name}**, regarding **{current_disease}**, you should follow the natural diet tips listed in the 'Recommendations' section above. I recommend focusing on locally sourced antioxidants to help your body clear the infection naturally alongside your clinical treatment."
                else:
                    # The "Redirect to Medical Workers" Fallback
                    response = f"**{user_name}**, I am specialized only in nutritional recovery and biochemical health tips. For diagnosis, drug prescriptions, or more advanced medical knowledge, please consult your **medical workers** or use the 'Find Nearest Hospital' button."
            else:
                response = f"**{user_name}**, please complete the symptom selection and click 'Predict Disease' first so I can give you relevant advice."
        
        # Display and Save the Response
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

#AI ends here. The bot is designed to provide safe, evidence-based nutritional advice while redirecting users to healthcare professionals for any medical concerns beyond its scope.    

# --- Sidebar ---
st.sidebar.header("About")
st.sidebar.info("Created by: Edidiong Moses. \nAim: Reducing antimicrobial resistance through smarter diagnosis.")
