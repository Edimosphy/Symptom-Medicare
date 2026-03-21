
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

user_name = st.text_input("📝 What is your name?", placeholder="e.g., Edidiong")

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
            user_symptoms[symptom] = st.selectbox(f"{symptom}", options, key=f"symptom_{symptom}")
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
    
    st.success(f"🎯 Hello {user_name if user_name else 'Guest'}, your Likely Condition is: **{prediction}** ({confidence:.2f}%)")
    
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

# --- AI Bot Section (Symptom MediCare Assistant) ---
st.markdown("---")
st.subheader("💬 Chat with Symptom MediCare Assistant")

from google import genai
from google.genai import types

# 1. Setup Gemini Client
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"Missing or Invalid API Key! Error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. Capture Input
if prompt := st.chat_input("Ask about recovery, biology, or precautions..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. GET DYNAMIC CONTEXT
    current_pred = st.session_state.get('prediction', None)
    
    # Check if this is the FIRST assistant message to handle greeting
    is_first_message = len(st.session_state.messages) <= 1

    # 4. THE OMNI-INSTRUCTION (Step 4 - Corrected for Repetition)
    sys_instr = f"""
    You are the 'Symptom MediCare Assistant', a professional Nigerian Health Professional.
    User Name: {user_name if user_name else 'Guest'}.
    Current Prediction: {current_pred if current_pred else 'NONE'}.

    GREETING LOGIC:
    - IF this is the first message: Always start with "Hello {user_name if user_name else 'Guest'}, I am your Symptom MediCare Assistant."
    - IF this is a follow-up question (history exists): DO NOT repeat the formal greeting. Just answer the question directly.

    CRITICAL LOGIC (THE SICKNESS TRIGGER):
    - IF the user says 'I feel sick' AND Prediction is 'NONE', 
      YOU MUST RESPOND: "I'm sorry you feel ill, {user_name if user_name else 'Guest'}. To give you the right medical recommendation, please fill out the Symptom Selection form above and click 'Predict' first."
    
    KNOWLEDGE DOMAIN:
    - PREVENTIVE CARE: Advise on Treated Nets (Malaria), Boiling Water (Typhoid), and Protection/Safe practices (HIV).
    - BIOLOGY & BIOCHEMISTRY: Explain the liver stage of Malaria and CD4+ T-cell attack in HIV.
    - MEDICAL TERMINOLOGY: Define terms as they relate to these diseases.
    - SUBSTITUTIONS: Suggest local alternative (Garlic/Scent Leaf if Ginger is unavailable).

    STRICT GUARDRAILS:
    - NEVER prescribe drugs or dosages. 
    - If asked for meds, say: "I am specialized only in nutritional recommendations and healthy tips. For prescriptions, please consult your medical workers or click 'Find Nearest Hospital'."
    - Greeting status: {'New Conversation' if is_first_message else 'Ongoing Discussion'}.
    """

    # 5. Generate Response (Fixed for Gemini 3 SDK)
    with st.chat_message("assistant"):
        try:
            # CORRECT SYNTAX: client.chats.create
            chat_session = client.chats.create(
                model="gemini-3-flash-preview",
                config=types.GenerateContentConfig(
                    system_instruction=sys_instr,
                    thinking_config=types.ThinkingConfig(include_thoughts=True)
                ),
                history=[
                    types.Content(role=m["role"], parts=[types.Part.from_text(text=m["content"])])
                    for m in st.session_state.messages[:-1]
                ]
            )
            
            # Send the new prompt to the session
            response = chat_session.send_message(prompt)
            
            if response and response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("No response text found.")
                
        except Exception as e:
            st.error(f"Gemini 3 Error: {e}")
 
# --- Sidebar ---
st.sidebar.header("About")
st.sidebar.info("Created by: Edidiong Moses. \nAim: Reducing antimicrobial resistance through smarter diagnosis.")
