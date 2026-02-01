import streamlit as st
from google import genai
import time

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="CTF Mentor Terminal", page_icon="📟", layout="wide")

# 2. ESTILO HACKER (Limpiado para evitar TypeErrors)
st.markdown("""
<style>
.main { background-color: #000000; color: #00FF41; }
.stTextInput > div > div > input { background-color: #0d0d0d; color: #00FF41; border: 1px solid #00FF41; }
.stChatMessage { border: 1px solid #00FF41; border-radius: 5px; background-color: #050505; color: #00FF41; }
.stButton > button { background-color: #004d00; color: #00FF41; border: 1px solid #00FF41; width: 100%; }
.stSidebar { background-color: #050505; border-right: 1px solid #00FF41; }
h1, h2, h3, p, span, label { font-family: 'Courier New', Courier, monospace; color: #00FF41 !important; }
</style>
""", unsafe_allow_value=True)

# 3. CONEXIÓN CON GEMINI
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("❌ ERROR DE PROTOCOLO: API_KEY no detectada.")
    st.stop()

# 4. BARRA LATERAL (Basado en tu documento CTF Mentor)
with st.sidebar:
    st.title("📟 CTF_PROTOCOL_V1")
    st.markdown("---")
    modo_ayuda = st.selectbox("MODO_OPERACIÓN:", ["Pista Ligera", "Guía Paso a Paso", "Explicador Conceptual"])
    categoria = st.selectbox("OBJETIVO_SISTEMA:", ["Web Exploitation", "Reconocimiento", "Forensics", "Cryptography", "Reverse Engineering", "Privilege Escalation"])
    
    if st.button("LIMPIAR REGISTROS"):
        st.session_state.messages = []
        st.rerun()

# 5. LÓGICA DEL SYSTEM PROMPT (Toda la chicha de tu Word)
instructions = f"""
Eres 'CTF Mentor', un asistente experto en seguridad. 
Tu misión: Guiar en el reto de {categoria}. Modo: {modo_ayuda}.
REGLAS:
- NO des la flag ni payloads directos.
- Usa metodología: Reconocimiento -> Vulnerabilidad -> Explotación.
- Si piden la respuesta, explica el concepto teórico detrás.
- Menciona herramientas como nmap, gobuster, linpeas o burp según el caso.
"""

# 6. INTERFAZ DE CHAT
st.title("🟢 CTF MENTOR: ON-LINE")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Esperando comandos..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Generación con Gemini
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            config={'system_instruction': instructions},
            contents=prompt
        )
        
        # Efecto de terminal hacker
        for chunk in response.text.split():
            full_response += chunk + " "
            time.sleep(0.04)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
