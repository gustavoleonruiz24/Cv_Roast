import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import random
import urllib.parse

# --- 1. CONFIGURACIÓN DE SEGURIDAD ---
try:
    # Asegúrate de que en Streamlit Secrets esté como GEMINI_API_KEY
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("⚠️ Error: Configura la API Key en los Secrets de Streamlit.")
    st.stop()

# --- SELECCIÓN DE MODELO ESTABLE (BASADO EN TUS CUOTAS) ---
# Usamos el nombre base que aparece en tu consola de Google AI Studio
model = genai.GenerativeModel('gemini-1.5-flash') 

def extraer_texto_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

# --- 2. INTERFAZ ---
st.set_page_config(page_title="CV Roast AI 2026", page_icon="💀", layout="centered")

# Botón de Café (Monetización)
st.markdown(
    """<div style="text-align: right;">
    <a href="https://www.buymeacoffee.com/gleon" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 40px !important;width: 145px !important;" >
    </a></div>""", 
    unsafe_allow_html=True
)

st.title("🔥 CV Roast: Edición 2026")
st.subheader("Humillación profesional nivel Dios")

# Contador dinámico
if 'contador_visitas' not in st.session_state:
    st.session_state.contador_visitas = random.randint(1580, 1650)
else:
    st.session_state.contador_visitas += 1

st.markdown(f"**{st.session_state.contador_visitas:,}** profesionales humillados hoy. ⚡")
st.markdown("---")

archivo_subido = st.file_uploader("Sube tu CV (PDF)", type=["pdf"])

if archivo_subido is not None:
    with st.spinner('Escaneando mediocridad laboral...'):
        try:
            texto_cv = extraer_texto_pdf(archivo_subido).lower()
            
            prompt = f"""
            Actúa como un reclutador de TI extremadamente sarcástico de Jacona, Michoacán. 
            Analiza este CV y haz un roast brutal, corto y muy directo. 
            Identifica si tiene Power BI, Python o SQL.
            Texto: {texto_cv}
            """
            
            # Generación de contenido
            response = model.generate_content(prompt)
            
            # --- Visualización BI ---
            st.divider()
            score = random.randint(5, 38)
            col1, col2, col3 = st.columns(3)
            col1.metric("Empleabilidad", f"{score}%", "-62%")
            col2.metric("Nivel de Clichés", "Crítico", "⚠️")
            col3.metric("Ego Tech", "99%", "Fijo")

            st.markdown("### 💀 Veredicto Brutal:")
            st.write(response.text)

            # --- Cursos Sugeridos ---
            st.divider()
            st.subheader("🛠️ Mejora tu perfil:")
            if "power bi" not in texto_cv:
                st.warning("⚠️ Sin Power BI no eres nadie en BI.")
                st.link_button("👉 Curso Power BI", "https://www.udemy.com/")
            if "python" not in texto_cv:
                st.info("🐍 Sin Python la IA te va a comer vivo.")
                st.link_button("👉 Curso Python", "https://www.coursera.org/")

            # --- LinkedIn ---
            st.divider()
            app_url = "https://cvroast-f5zmjjlaeonzcj8sncuzqc.streamlit.app/" 
            resumen = f"🔥 ¡Mi CV fue humillado por una IA! 💀\n\n📊 Score: {score}%\n\nPruébalo aquí: {app_url}\n\n#CVRoast #AI #TechHumor"
            
            st.subheader("📲 Paso 1: Copia tu Roast")
            st.code(resumen, language="text")
            
            st.subheader("📲 Paso 2: Publica en LinkedIn")
            share_url = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(app_url)}"
            st.link_button("Ir a LinkedIn", share_url)
            
        except Exception as e:
            st.error("💣 Error de conexión con la IA.")
            st.info("Google está validando los permisos de tu nueva cuenta Pay-as-you-go.")
            st.write(f"Log técnico: `{str(e)}`")

st.markdown("---")
st.caption("2026. Basado en IA real.")

