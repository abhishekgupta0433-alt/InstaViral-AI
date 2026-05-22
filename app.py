import streamlit as st
from groq import Groq

# 1. Groq API Key Configuration
# Apni nayi Groq wali chabi yahan single quotes ke andar daaliye bhai
GROQ_API_KEY = 'GROQ_API_KEY = st.secrets["GROQ_API_KEY"]'

try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error("Key configure karne mein dikkat aayi.")

# 2. Premium Looks & Colors
st.set_page_config(page_title="InstaViral AI Premium", page_icon="⚡", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0A0E1A; color: #F1F5F9; }
    section[data-testid="stSidebar"] { background-color: #111827 !important; border-right: 1px solid #1F2937; }
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%);
        color: white; border: none; border-radius: 10px;
        padding: 0.75rem 2.5rem; font-weight: bold; font-size: 16px;
        width: 100%; box-shadow: 0 4px 20px rgba(168, 85, 247, 0.4);
    }
    div.stButton > button:first-child:hover { transform: translateY(-2px); box-shadow: 0 6px 25px rgba(168, 85, 247, 0.6); }
    .premium-box { background: linear-gradient(145deg, #1E293B, #0F172A); border: 1px solid #334155; padding: 25px; border-radius: 16px; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- FREE TRIAL SYSTEM ---
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

max_free_trials = 3
rem_trials = max_free_trials - st.session_state.usage_count

# --- SIDEBAR ACCESS ---
with st.sidebar:
    st.markdown("<h2 style='color: #A855F7;'>⚡ InstaViral AI</h2>", unsafe_allow_html=True)
    st.caption("Developed by Abhishek Gupta")
    st.write("---")
    st.subheader("👤 My Account")
    if st.session_state.is_premium:
        st.success("👑 Plan: Creator Pro (Active)")
    else:
        st.info("Plan: Free Trial")
        if rem_trials > 0:
            st.write(f"⏳ Free Uses Left: **{rem_trials} / {max_free_trials}**")
        else:
            st.error("❌ Free Trial Expired!")
    st.write("---")
    if st.checkbox("Simulate Premium Purchase"):
        st.session_state.is_premium = True
    else:
        st.session_state.is_premium = False

# --- MAIN PAGE DESIGN ---
st.markdown("<h1 style='text-align: center; color: white;'>🚀 AI Viral Post & Hook Generator</h1>", unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("📝 Enter Your Video/Post Topic", placeholder="e.g., Gym Motivation, Coding Secrets")
    category = st.selectbox("🎯 Content Category", ["Reels/Shorts Content", "Motivation", "Gaming", "Business/Finance", "Fitness", "Education"])
with col2:
    tone = st.selectbox("🎭 Select AI Tone", ["Catchy/Viral", "Funny", "Emotional", "Professional", "Storytelling"])
    lang = st.selectbox("🌐 Output Language", ["Hinglish (Mix)", "English", "Pure Hindi"])

# --- GENERATION ---
if st.button("One-Click Content Generation ✨"):
    if not st.session_state.is_premium and st.session_state.usage_count >= max_free_trials:
        st.error("🚫 Free Trial Over! Please activate Premium Plan from sidebar.")
    else:
        if topic:
            with st.spinner("🤖 AI Aapke Liye Soch Raha Hai... Please Wait..."):
                prompt_text = f"""
                You are a world-class social media viral expert. Generate content for:
                Topic: {topic}
                Category: {category}
                Tone: {tone}
                Language: {lang}
                
                Provide the output strictly in this format:
                🔥 2 VIRAL HOOKS:
                (Write here)
                
                📝 ENGAGING CAPTION:
                (Write here)
                
                📈 TRENDING HASHTAGS:
                (Write here)
                """
                
                try:
                    # Groq engine setup (Super Fast)
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt_text}],
                    )
                    ai_output = completion.choices[0].message.content
                    
                    if not st.session_state.is_premium:
                        st.session_state.usage_count += 1
                    
                    st.balloons()
                    
                    # Output Screen
                    st.markdown(f"""
                    <div class="premium-box">
                        <h2 style="color: #A855F7; margin-top: 0;">🎯 Generated Content</h2>
                        <p style="color: #94A3B8;">Topic: {topic} | Language: {lang}</p>
                        <hr style="border-color: #334155;">
                        <div style="white-space: pre-wrap; font-size: 15px; line-height: 1.6; color: #F1F5F9;">
                        {ai_output}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as ai_error:
                    st.error("⚠️ AI Connection mein dikkat aayi:")
                    st.code(str(ai_error))
        else:
            st.error("Bhai, pehle Topic waale box mein kuch likho! 😊")