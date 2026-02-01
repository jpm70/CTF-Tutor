import streamlit as st
from google import genai
from google.genai import types # Importación adicional para mayor control
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

# 3. CONEXIÓN API (Forzando versión estable)
try:
    # Usamos la configuración por defecto que apunta a la v1 estable
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
        
        # System Instructions basadas en tu documento original
        sys_instructions = f"Eres 'CTF Mentor'. Ayuda en {cat} modo {modo}. No des la flag. Guía con metodología técnica."
        
        try:
            # CAMBIO CLAVE: Usamos el ID de modelo más básico y compatible
            # En la nueva librería 'google-genai', a veces basta con poner el nombre corto
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=sys_instructions,
                    temperature=0.7
                ),
                contents=prompt
            )
            
            if response.text:
                for word in response.text.split():
                    full_res += word + " "
                    time.sleep(0.03)
                    m_placeholder.markdown(full_res + "▌")
                m_placeholder.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
            else:
                st.warning("La IA no devolvió texto. Revisa tu cuota en AI Studio.")
            
        except Exception as e:
            # Capturamos el error detallado para saber si es 404 o 429
            st.error(f"❌ ERROR DE CONEXIÓN: {str(e)}")
            if "429" in str(e):
                st.info("💡 Tip: Has agotado la cuota gratuita por ahora. Espera 60 segundos.")
