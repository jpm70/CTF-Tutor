import streamlit as st
from google import genai
import time

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="CTF Mentor", page_icon="📟", layout="wide")

# 2. DISEÑO HACKER
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
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("⚠️ PROTOCOLO FALLIDO: Configura GEMINI_API_KEY en Secrets.")
    st.stop()

# 4. INTERFAZ LATERAL
with st.sidebar:
    st.title("📟 CTF_PROTOCOL_V1")
    st.markdown("---")
    modo = st.selectbox("MODO_DE_AYUDA:", ["Pista Ligera", "Guía Paso a Paso", "Explicador Conceptual"])
    cat = st.selectbox("CATEGORÍA_RETO:", ["Web Exploitation", "Reconocimiento", "Privilege Escalation", "Forensics", "Cryptography", "Reverse Engineering"])
    
    if st.button("LIMPIAR REGISTROS"):
        st.session_state.messages = []
        st.rerun()

# 5. INTERFAZ DE CHAT
st.title("🟢 CTF MENTOR: ON-LINE")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Inserta consulta técnica..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        m_placeholder = st.empty()
        full_res = ""
        
        sys_instructions = f"""
        Eres 'CTF Mentor', un experto en ciberseguridad. 
        Reto actual: {cat}. Modo de ayuda: {modo}.
        REGLAS:
        - NUNCA des la flag ni el payload final.
        - Guía paso a paso en la metodología (Recon -> Vuln -> Exploit).
        - Recomienda herramientas técnicas.
        """
        
        try:
            # CORRECCIÓN: Nombre de modelo estándar para la librería google-genai
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                config={'system_instruction': sys_instructions},
                contents=prompt
            )
            
            for word in response.text.split():
                full_res += word + " "
                time.sleep(0.03)
                m_placeholder.markdown(full_res + "▌")
            m_placeholder.markdown(full_res)
            
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            
        except Exception as e:
            # Si hay error de cuota (429), se mostrará aquí de forma legible
            st.error(f"❌ ERROR EN EL ENLACE: {str(e)}")
