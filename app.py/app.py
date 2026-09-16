import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- 🔐 API SECRETS MANAGEMENT ---
try:
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_KEY)
except Exception:
    st.error("⚠️ API Key missing! Please set GEMINI_API_KEY in your .streamlit/secrets.toml file.")
    st.stop()

# 1. ಭಾಷೆಯ ಆಯ್ಕೆ
language = st.sidebar.selectbox("🌐 Choose Language / ಭಾಷೆಯನ್ನು ಆಯ್ಕೆ ಮಾಡಿ", ["English", "ಕನ್ನಡ"])

# 2. ಇಂಟರ್ಫೇಸ್ ಭಾಷಾ ಅನುವಾದಗಳು
translations = {
    "English": {
        "title": "🌱 AgriShield AI - Smart Farming Doctor",
        "upload_title": "🖼️ 1. Upload Crop / Leaf Image",
        "upload_prompt": "Please upload a photo of the crop to see the live AI report.",
        "upload_success": "Image uploaded successfully!",
        "detection_title": "🦠 2. Live AI Plant Recognition & Health Diagnosis",
        "prompt_context": "You are an expert plant pathologist. Analyze this image. Identify the plant (e.g. Coconut, Corn, Tomato, Potato, Ginger, etc.) and check for health issues. Respond strictly in English in this specific format:\n\n**Crop Name:** [Name]\n**Status:** [Healthy or Describe disease]\n**Advice:** [Actionable advice for farmer]\n**Alert:** [Warning if any]"
    },
    "ಕನ್ನಡ": {
        "title": "🌱 AgriShield AI - ಬೆಳೆ ವೈದ್ಯ",
        "upload_title": "🖼️ 1. ಬೆಳೆ ಅಥವಾ ಎಲೆಯ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "upload_prompt": "ದಯವಿಟ್ಟು ವರದಿ ನೋಡಲು ಮೊದಲು ಬೆಳೆಯ ಫೋಟೋ ಅಪ್ಲೋಡ್ ಮಾಡಿ.",
        "upload_success": "ಫೋಟೋ ಯಶಸ್ವಿಯಾಗಿ ಅಪ್‌ಲೋಡ್ ಆಗಿದೆ!",
        "detection_title": "🦠 2. ಲೈವ್ AI ಬೆಳೆ ಪತ್ತೆ ಮತ್ತು ರೋಗ ತಪಾಸಣೆ",
        "prompt_context": "ನೀವು ಪರಿಣಿತ ಸಸ್ಯ ತಜ್ಞರು. ಈ ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸಿ, ಸಸ್ಯವನ್ನು (ತೆಂಗಿನಕಾಯಿ, ಜೋಳ, ಟೊಮೆಟೊ, ಆಲೂಗಡ್ಡೆ, ಶುಂಠಿ ಇತ್ಯಾದಿ) ಗುರುತಿಸಿ ಮತ್ತು ರೋಗಗಳನ್ನು ಪತ್ತೆಹಚ್ಚಿ. ಕಡ್ಡಾಯವಾಗಿ ಕನ್ನಡದಲ್ಲೇ ಈ ಕೆಳಗಿನ ಮಾದರಿಯಲ್ಲಿ ಉತ್ತರಿಸಿ:\n\n**ಬೆಳೆಯ ಹೆಸರು:** [ಹೆಸರು]\n**ಸ್ಥಿತಿ:** [ಆರೋಗ್ಯವಾಗಿದೆ ಅಥವಾ ರೋಗದ ವಿವರ]\n**ರೈತರಿಗೆ ಸಲಹೆ:** [ಕೈಗೊಳ್ಳಬೇಕಾದ ಕ್ರಮಗಳು]\n**ಮುನ್ನೆಚ್ಚರಿಕೆ:** [ಮುನ್ಸೂಚನೆ ವಿವರ]"
    }
}

text = translations[language]
st.title(text["title"])

# --- 🖼️ UPLOAD SECTION ---
st.header(text["upload_title"])
uploaded_file = st.file_uploader("Choose a photo / ಫೋಟೋ ಆಯ್ಕೆ ಮಾಡಿ...", type=["jpg", "jpeg", "png"])

if uploaded_file is None:
    st.info(f"👋 {text['upload_prompt']}")
else:
    st.success(text["upload_success"])
    user_image = Image.open(uploaded_file)
    st.image(user_image, caption="Uploaded Specimen", use_container_width=True)
    
    # --- 🧠 LIVE AI ANALYSIS ENGINE ---
    st.header(text["detection_title"])
    
    with st.spinner("AI is analyzing the leaf specimen... / AI ವಿಶ್ಲೇಷಿಸುತ್ತಿದೆ..."):
        try:
            # 🚀 ಇತ್ತೀಚಿನ ಅತ್ಯಾಧುನಿಕ ಮಾಡೆಲ್ 'gemini-3.6-flash' ಗೆ ಅಪ್‌ಡೇಟ್ ಮಾಡಲಾಗಿದೆ
            model = genai.GenerativeModel('gemini-3.6-flash')
            ai_response = model.generate_content([text["prompt_context"], user_image])
            
            # ಫಲಿತಾಂಶ ಪ್ರದರ್ಶನ
            st.markdown(ai_response.text)
            
        except Exception as e:
            st.error(f"AI Analysis failed. Error detail: {str(e)}")
