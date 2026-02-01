import streamlit as st
from google import genai
import time

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="CTF Mentor", page_icon="📟", layout="wide")

# 2. DISEÑO HACKER (Versión Ultra-Compatible)
hacker_style = """
<style>
    .main { background-color: #000000 !important; color: #00FF41 !important; }
    .stApp { background-color: #000000; }
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #00FF41; }
    .stChatMessage { border: 1px solid #00FF41 !important; background-color: #050505 !important; color: #00FF41 !important; }
    h1, h2, h3, p, span, label, .stMarkdown { font-family: 'Courier New', monospace !important; color: #00FF41 !important; }
    .stButton > button { background-color: #004d00 !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; }
    .stChatInput input { background-color: #0d0d0d !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; }
</style>
"""
st.markdown(hacker_style, unsafe_allow_value=True)

# 3. CONEXIÓN CON GEMINI
try:
    # Intentamos conectar con la API Key de Secrets
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("❌ ERROR: Configura GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop()

# 4. LÓGICA DE LA BARRA LATERAL
with st.sidebar:
    st.title("📟 CTF_PROTOCOL")
    st.markdown("---")
    modo = st.selectbox("MODO:", ["Pista Ligera", "Guía Paso a Paso", "Conceptual"])
    cat = st.selectbox("SISTEMA:", ["Web", "Reconocimiento", "PrivEsc", "Forensics", "Crypto"])
    
    if st.button("RESET TERMINAL"):
        st.session_state.messages = []
        st.rerun()

# 5. INSTRUCCIONES DEL MENTOR (Basado en tu doc)
sys_instructions = f"Eres CTF Mentor. Ayuda en {cat} modo {modo}. No des flags. Guía con nmap, gobuster, etc."

# 6. INTERFAZ DE CHAT
st.title("🟢 CTF MENTOR: ON-LINE")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Escribe tu duda técnica..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        m_placeholder = st.empty()
        full_res = ""
        
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
