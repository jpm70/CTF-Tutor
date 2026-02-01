import streamlit as st
import google.generativeai as genai
import time

# 1. CONFIGURACIÓN
st.set_page_config(page_title="CTF Mentor", page_icon="📟", layout="wide")

# 2. ESTILO HACKER
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    * { color: #00FF41 !important; font-family: 'Courier New', monospace !important; }
    .stChatMessage { border: 1px solid #00FF41 !important; background-color: #050505 !important; }
    .stButton > button { background-color: #004d00 !important; border: 1px solid #00FF41 !important; color: #00FF41 !important; }
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #00FF41; }
    .stChatInput input { background-color: #0d0d0d !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; }
</style>
""", unsafe_allow_html=True)

# 3. CONEXIÓN ESTABLE
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de configuración: {e}")
    st.stop()

# 4. MENÚ LATERAL
with st.sidebar:
    st.title("📟 CTF_PROTOCOL_V1")
    modo = st.selectbox("MODO_DE_AYUDA:", ["Pista Ligera", "Guía Paso a Paso", "Explicador Conceptual"])
    cat = st.selectbox("CATEGORÍA_RETO:", ["Web Exploitation", "Reconocimiento", "Privilege Escalation", "Forensics", "Cryptography"])
    if st.button("REINICIAR TERMINAL"):
        st.session_state.messages = []
        st.rerun()

# 5. CHAT
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
        sys_instr = f"Eres 'CTF Mentor'. Ayuda en {cat} modo {modo}. NO des la flag, guía con metodología técnica."
        
        try:
            response = model.generate_content(sys_instr + "\n\nUsuario: " + prompt)
            for word in response.text.split():
                full_res += word + " "
                time.sleep(0.03)
                m_placeholder.markdown(full_res + "▌")
            m_placeholder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception as e:
            st.error(f"❌ ERROR DE PROTOCOLO: {str(e)}")
