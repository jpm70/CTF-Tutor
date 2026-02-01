import streamlit as st
from google import genai
import time

# Configuración de la página con estilo oscuro
st.set_page_config(page_title="CTF Mentor Terminal", page_icon="📟", layout="wide")

# Estilo CSS para el "Hacker Look"
st.markdown("""
    <style>
    .main { background-color: #000000; color: #00FF41; }
    .stTextInput > div > div > input { background-color: #0d0d0d; color: #00FF41; border: 1px solid #00FF41; }
    .stChatMessage { border: 1px solid #00FF41; border-radius: 5px; background-color: #050505; }
    .stButton > button { background-color: #004d00; color: #00FF41; border: 1px solid #00FF41; width: 100%; }
    .stSidebar { background-color: #050505; border-right: 1px solid #00FF41; }
    h1, h2, h3, p { font-family: 'Courier New', Courier, monospace; color: #00FF41 !important; }
    </style>
    """, unsafe_allow_value=True)

# Inicializar cliente de Google GenAI
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("⚠️ API Key no encontrada en Secrets. Configúrala en Streamlit Cloud.")
    st.stop()

# --- BARRA LATERAL (CONFIGURACIÓN DEL RETO) ---
with st.sidebar:
    st.title("📟 CTF_PROTOCOL_V1")
    st.markdown("---")
    
    # Nivel de ayuda
    modo_ayuda = st.selectbox(
        "MODO_DE_OPERACIÓN:",
        ["Pista Ligera", "Guía Paso a Paso", "Explicador Conceptual"]
    )
    
    # Especialidad
    categoria = st.selectbox(
        "OBJETIVO_SISTEMA:",
        ["Web Exploitation", "Reconocimiento (Nmap/Gobuster)", "Forensics", "Cryptography", "Reverse Engineering", "Privilege Escalation"]
    )
    
    if st.button("REINICIAR TERMINAL"):
        st.session_state.messages = []
        st.rerun()

# --- LÓGICA DEL SYSTEM PROMPT ---
# Construimos el prompt dinámico basado en las opciones del usuario
instructions = f"""
Eres 'CTF Mentor', un asistente experto en seguridad informática. 
Tu misión es guiar al usuario en el reto: {categoria}.
MODO ACTUAL: {modo_ayuda}.

REGLAS ESTRICTAS:
1. NO entregues la 'flag' ni payloads finales.
2. Si el modo es 'Pista Ligera', sé vago y sugiere dónde mirar.
3. Si es 'Guía Paso a Paso', sugiere la metodología (recon -> vul -> exp).
4. Si el usuario te pide la respuesta directa, niégate amablemente y ofrece un concepto teórico.
5. Usa terminología técnica (SUID, LFI, SQLi, etc.) pero explica la herramienta sugerida.
"""

# --- CHAT INTERFACE ---
st.title("🟢 CTF MENTOR: ON-LINE")
st.write(f"Conectado: Sector_{categoria.split()[0].upper()} | Modo_{modo_ayuda.replace(' ', '_').upper()}")

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if prompt := st.chat_input("Insertar comando o duda..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta de la IA con streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Simulación de efecto de escritura de terminal
        response_stream = client.models.generate_content(
            model="gemini-3-flash-preview",
            config={'system_instruction': instructions},
            contents=prompt
        )
        
        # Mostramos la respuesta poco a poco para estilo hacker
        for chunk in response_stream.text.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})