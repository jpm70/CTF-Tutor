import streamlit as st
from google import genai
import time

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="CTF Mentor", page_icon="📟", layout="wide")

# 2. DISEÑO HACKER (Corregido para compatibilidad total)
hacker_style = """
<style>
    .stApp { background-color: #000000; }
    * { color: #00FF41 !important; font-family: 'Courier New', monospace !important; }
    .stChatMessage { border: 1px solid #00FF41 !important; background-color: #050505 !important; }
    .stButton > button { background-color: #004d00 !important; border: 1px solid #00FF41 !important; color: #00FF41 !important; }
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #00FF41; }
    .stChatInput input { background-color: #0d0d0d !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; }
</style>
"""
st.markdown(hacker_style, unsafe_allow_html=True)

# 3. CONEXIÓN API
try:
    # Se conecta usando la API Key configurada en Streamlit Cloud Secrets
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("⚠️ PROTOCOLO FALLIDO: Configura GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop()

# 4. INTERFAZ LATERAL (Basada en tu documentación)
with st.sidebar:
    st.title("📟 CTF_PROTOCOL_V1")
    st.markdown("---")
    modo = st.selectbox("MODO_DE_AYUDA:", ["Pista Ligera", "Guía Paso a Paso", "Explicador Conceptual"])
    cat = st.selectbox("CATEGORÍA_RETO:", ["Web Exploitation", "Reconocimiento", "Privilege Escalation", "Forensics", "Cryptography", "Reverse Engineering"])
    
    if st.button("LIMPIAR CACHÉ"):
        st.session_state.messages = []
        st.rerun()

# 5. INTERFAZ DE CHAT PRINCIPAL
st.title("🟢 CTF MENTOR: ON-LINE")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Entrada de usuario y lógica de respuesta
if prompt := st.chat_input("Inserta consulta técnica..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        m_placeholder = st.empty()
        full_res = ""
        
        # System Instructions dinámicas según selección lateral
        sys_instructions = f"""
        Eres 'CTF Mentor', un experto en ciberseguridad. 
        Reto actual: {cat}. Modo de ayuda: {modo}.
        REGLAS:
        - NUNCA des la flag ni el payload final.
        - Guía paso a paso en la metodología (Recon -> Vuln -> Exploit).
        - Recomienda herramientas específicas (nmap, gobuster, burp, linpeas, etc.).
        - Si el usuario se rinde, explícale el concepto teórico para que lo intente de nuevo.
        """
        
        try:
            # Uso del modelo estable gemini-2.0-flash para evitar ServerError
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config={'system_instruction': sys_instructions},
                contents=prompt
            )
            
            # Efecto visual de escritura de terminal
            for word in response.text.split():
                full_res += word + " "
                time.sleep(0.03)
                m_placeholder.markdown(full_res + "▌")
            m_placeholder.markdown(full_res)
            
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            
        except Exception as e:
            st.error(f"❌ ERROR EN EL ENLACE NEURONAL: {str(e)}")
