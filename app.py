import streamlit as st
from google import genai
import time

# 1. CONFIGURACIÓN
st.set_page_config(page_title="CTF Mentor", page_icon="📟", layout="wide")

# 2. ESTILO HACKER (Corregido: unsafe_allow_html)
hacker_style = """
<style>
    .stApp { background-color: #000000; }
    * { color: #00FF41 !important; font-family: 'Courier New', monospace !important; }
    .stChatMessage { border: 1px solid #00FF41 !important; background-color: #050505 !important; }
    .stButton > button { background-color: #004d00 !important; border: 1px solid #00FF41 !important; }
</style>
"""
st.markdown(hacker_style, unsafe_allow_html=True)

# 3. CONEXIÓN API
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Configura GEMINI_API_KEY en Secrets.")
    st.stop()

# 4. INTERFAZ LATERAL
with st.sidebar:
    st.title("📟 CTF_PROTOCOL")
    modo = st.selectbox("MODO:", ["Pista Ligera", "Guía Paso a Paso", "Conceptual"])
    cat = st.selectbox("SISTEMA:", ["Web", "Reconocimiento", "PrivEsc", "Forensics"])

# 5. CHAT
st.title("🟢 CTF MENTOR: ON-LINE")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        m_placeholder = st.empty()
        full_res = ""
        
        # Instrucciones basadas en tu doc
        sys_instructions = f"Eres CTF Mentor. Ayuda en {cat} modo {modo}. No des flags. Guía con herramientas técnicas."
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            config={'system_instruction': sys_instructions},
            contents=prompt
        )
        
        for word in response.text.split():
            full_res += word + " "
            time.sleep(0.04)
            m_placeholder.markdown(full_res + "▌")
        m_placeholder.markdown(full_res)
    
    st.session_state.messages.append({"role": "assistant", "content": full_res})
