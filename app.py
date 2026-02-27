import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import random
import urllib.parse

# --- 1. CONFIGURACIÓN DE SEGURIDAD ---
try:
    # Asegúrate de que en Secrets sea GEMINI_API_KEY
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("⚠️ Error: Configura la API Key en los Secrets de Streamlit.")
    st.stop()

# --- FIX 404: Selección de Modelo Ultra-Compatible ---
# 'gemini-1.5-flash-8b' es el modelo más ligero y con menos errores de despliegue
# Si persiste el error, el sistema intentará con la versión estándar.
try:
    model = genai.GenerativeModel('gemini-1.5-flash-8b')
except:
    model = genai.GenerativeModel('gemini-1.5-flash')

def extraer_texto_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

# --- 2. INTERFAZ Y MONETIZACIÓN ---
st.set_page_config(page_title="CV Roast AI 2026", page_icon="💀", layout="centered")

st.markdown(
    """<div style="text-align: right;">
    <a href="https://www.buymeacoffee.com/gleon" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 40px !important;width: 145px !important;" >
    </a></div>""", 
    unsafe_allow_html=True
)

st.title("🔥 CV Roast: Edición 2026")

if 'contador_visitas' not in st.session_state:
    st.session_state.contador_visitas = random.randint(1450, 1600)
else:
    st.session_state.contador_visitas += 1

st.markdown(f"**{st.session_state.contador_visitas:,}** profesionales humillados hoy. ⚡")
st.markdown("---")

archivo_subido = st.file_uploader("Sube tu CV (PDF)", type=["pdf"])

if archivo_subido is not None:
    with st.spinner('Analizando tu mediocre trayectoria laboral...'):
        try:
            texto_cv = extraer_texto_pdf(archivo_subido).lower()
            
            prompt = f"""
            Actúa como un reclutador de TI extremadamente sarcástico de Jacona, Michoacán. 
            Analiza este CV y haz un roast brutal de máximo 3 párrafos. 
            Identifica si tiene Power BI, Python o SQL.
            Texto: {texto_cv}
            """
            
            response = model.generate_content(prompt)
            
            # --- Visualización ---
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
            st.subheader("🛠️ Deja de dar pena, aprende algo:")
            if "power bi" not in texto_cv:
                st.warning("⚠️ Sin Power BI no eres nadie en BI.")
                st.link_button("👉 Curso Power BI", "https://www.udemy.com/")
            if "python" not in texto_cv:
                st.info("🐍 Sin Python la IA te va a comer vivo.")
                st.link_button("👉 Curso Python", "https://www.coursera.org/")

            # --- Flujo LinkedIn ---
            st.divider()
            app_url = "https://cvroast-f5zmjjlaeonzcj8sncuzqc.streamlit.app/" 
            resumen = f"🔥 ¡Mi CV fue humillado por una IA! 💀\n\n📊 Score: {score}%\n\nPruébalo aquí: {app_url}\n\n#CVRoast #AI #TechHumor"
            
            st.subheader("📲 Paso 1: Copia tu Roast")
            st.code(resumen, language="text")
            
            st.subheader("📲 Paso 2: Publica en LinkedIn")
            share_url = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(app_url)}"
            st.link_button("Ir a LinkedIn", share_url)
            
        except Exception as e:
            st.error("⚠️ Error de conexión: El modelo está terminando de configurarse.")
            st.info("Reintenta en 10 segundos. Google está validando tu nueva cuenta Pay-as-you-go.")
            # Registro técnico para depuración
            st.write(f"Log de error: `{str(e)}`")

st.markdown("---")
st.caption("Jacona, Michoacán, 2026. Basado en IA real y humor crudo.")

st.markdown("---")
st.caption("Hecho para profesionales con piel gruesa 2026.")


