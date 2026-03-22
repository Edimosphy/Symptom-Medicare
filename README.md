
# Symptom MediCare
## Project Overview -Symptom Medicare
This health-simulated demo application addresses the critical public health crisis of self-medication and Antimicrobial Resistance (AMR) in Nigeria.
​By providing early prediction for Malaria, Typhoid, and HIV/AIDS, Symptom Medicare empowers users to seek clinical testing before starting drug regimens, preventing germs (bacteria, viruses, and parasites) from causing harms or conplicate health.

## The Science & The "Why"
Self-medication is a primary driver of Antimicrobial Resistance (AMR). When drugs are used improperly, pathogens evolve to withstand treatment. Symptom Medicare acts as a digital triage system that:
1. Reduces the reliance on "symptom guesswork."
2. Promotes clinical testing through active hospital mapping.
3. Educates users on the long-term impact of health decisions.

"Stay healthy while getting your desired dream and purpose through building wealth for your better today, tomorrow, and future."

## Project Key Features:
1. ​Disease Prediction Engine: Uses machine learning to analyze physical symptoms and predict the likelihood of specific disease conditions.
2. ​Nutritional Recovery Plans: Provides data-driven healthy lifestyle and nutritional tips tailored to the predicted condition.
3. ​Geospatial Hospital Locator: Integrated with Google Maps API to help users find the nearest clinical facility for formal diagnosis.
4. ​AI Support Bot: A conversational assistant built to answer health-related inquiries and provide clinical guidance.

## How it Works (4 Simple Steps): 
1. Predict: Enter your name, physical symptoms to predict the likely condition (Malaria, Typhoid, or HIV/AIDS).
2. Recover: Access a tailored nutritional and recovery plan based on the prediction results.
3. Locate: Click the 'Find Nearest Hospital' button to instantly map out the closest healthcare facilities via Google Maps.
4.Support: Use the Symptom Medicare Assistant Bot for real-time health guidance and to answer any medical inquiries.

## Result
### 📊 Result Output
After submitting your symptoms, the app shows:
- The most likely disease
-![Screenshot_20260322-070240](https://github.com/user-attachments/assets/798b7121-46c5-4ad9-a1fa-314fb680f4eb)
![Screenshot_20260322-070353](https://github.com/user-attachments/assets/b9c2ceae-399c-4339-b112-b68310896021)
![Screenshot_20260322-070407](https://github.com/user-attachments/assets/e0b8108d-e6b5-431d-b781-e9e0ad0d8f63)
![Screenshot_20260322-070426](https://github.com/user-attachments/assets/283bf657-b16d-4ac8-890e-844a2636ded9)

- You can also use the assistant without running a prediction
![Screenshot_20260322-070505](https://github.com/user-attachments/assets/f3c64b69-2460-44f0-96f3-d80b39b2dc9f)

## APP Deployment
This health simulated demo app is depolyed on Streamlit
The API Keys for the AIis added in the Streamlit secret 

Here is the link of the app **https://symptom-medicare.streamlit.app/**

##🛠️ Tech Stack
- Language: Python
- Framework: Streamlit
- API: Gemini API (Assistant Bot) / Google Maps API
- Data Science: Scikit-learn / Pandas (for prediction modeling)

##🛠️ Technical Challenges & Solutions
1. Seamless Gemini API Integration
Challenge: Ensuring the Symptom Medicare Assistant Bot provided medically grounded responses while maintaining a conversational tone.
Solution: Implemented custom system prompting (Prompt Engineering) to restrict the model’s scope to health informatics and recovery guidance, ensuring every response includes a clinical disclaimer.
2. Real-Time Geospatial Mapping
Challenge: Transitioning users from a prediction result to an external action (finding a hospital) without breaking the user experience.
Solution: Leveraged the Google Maps URL API to dynamically generate location-based search queries. When a user clicks 'Find Nearest Hospital,' the app automatically triggers a localized search for "Hospitals near me" based on their current browser coordinates.
3. Streamlining the Prediction Logic
Challenge: Building a lightweight, fast-loading prediction engine within the Streamlit framework that handles multiple symptom inputs.
Solution: Optimized the data flow by using a structured symptom-mapping dictionary. This allows the model to process physical symptoms rapidly, providing an instant prediction without the lag often associated with cloud-based AI.

## Future plan, Innovation and Collaboration:
1. Advanced Machine Learning to build an even more robust AI model.
2. Introduce databases where vital user information like age, gender, and location can be securely stored. This data will be valuable for medical research and crucial for tracking disease outbreaks across Nigeria and the World at large
3. Introduce other diseases that are of global concern and have similar symptoms.


## 📬 Feedback
Suggestions or improvements? Reach out or open an issue on the GitHub repo.

## Collaboration
Contact via email - edimosphy@gmail.com

## Disclaimer
This is not a replacement to medical treatment, diagnosis and test but to aid in medical diagnosis, research, treatment and education.
