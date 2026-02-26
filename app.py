import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import random
import urllib.parse
import time

# --- 1. CONFIGURACIÓN DE SEGURIDAD ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("⚠️ Error de Configuración: No se encontró la API Key en los Secrets de Streamlit.")
    st.info("Asegúrate de añadir GEMINI_API_KEY en Settings > Secrets.")
    st.stop()

model = genai.GenerativeModel('gemini-3-flash-preview')

def extraer_texto_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

# --- 2. CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(page_title="CV Roast AI 2026", page_icon="💀", layout="centered")

# Estilo para el botón de café y contador
st.markdown(
    """<div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <a href="https://www.buymeacoffee.com/gleon" target="_blank">
                <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 40px !important;width: 145px !important;" >
            </a>
        </div>
    </div>""", 
    unsafe_allow_html=True
)

st.title("🔥 CV Roast: Edición 2026")
st.subheader("Humillación profesional nivel Dios con Gemini 3")

# --- 3. CONTADOR FICTICIO DINÁMICO ---
# Usamos session_state para que el número crezca mientras el usuario navega
if 'contador_visitas' not in st.session_state:
    st.session_state.contador_visitas = random.randint(1450, 1600)
else:
    st.session_state.contador_visitas += random.randint(1, 3)

st.markdown(f"**{st.session_state.contador_visitas:,}** profesionales humillados el día de hoy. ⚡")
st.markdown("---")

# --- 4. CARGA DE ARCHIVOS ---
archivo_subido = st.file_uploader("Sube tu CV (PDF) para ser destruido por la IA", type=["pdf"])

if archivo_subido is not None:
    with st.spinner('Analizando tu triste realidad laboral...'):
        try:
            texto_cv = extraer_texto_pdf(archivo_subido).lower()
            
            prompt = f"""
            Actúa como un reclutador de TI amargado y experto en BI. 
            Analiza este CV y haz un roast brutal, corto y muy sarcástico. 
            Identifica si tiene Power BI, Python o SQL.
            Asigna un 'Arquetipo de Falla' gracioso.
            Texto del CV: {texto_cv}
            """
            
            response = model.generate_content(prompt)
            
            # --- 5. VISUALIZACIÓN DE RESULTADOS (BI STYLE) ---
            st.divider()
            
            score_emp = random.randint(5, 38)
            col1, col2, col3 = st.columns(3)
            col1.metric("Empleabilidad", f"{score_emp}%", "-62%")
            col2.metric("Nivel de Clichés", "Crítico", "⚠️")
            col3.metric("Ego Tech", "99%", "Fijo")

            st.markdown("### 💀 Veredicto del Reclutador Tóxico:")
            st.write(response.text)

            # --- 6. MONETIZACIÓN: CURSOS RECOMENDADOS ---
            st.divider()
            st.subheader("🛠️ Deja de dar pena, invierte en ti:")
            
            if "power bi" not in texto_cv and "dax" not in texto_cv:
                st.warning("⚠️ **Falla de BI:** Tu CV no tiene Power BI. Sigues en la era de piedra.")
                st.link_button("🚀 Curso Maestro: Power BI & DAX", "https://www.udemy.com/")
            
            if "python" not in texto_cv:
                st.info("🐍 **Sugerencia:** Sin Python, la IA te reemplazará antes del viernes.")
                st.link_button("🐍 Ver: Python para Análisis de Datos", "https://www.coursera.org/")

            # --- 7. COMPARTIR: BOTÓN VIRAL PARA LINKEDIN ---
            st.divider()
            # REEMPLAZA ESTA URL CON LA TUYA REAL CUANDO ESTÉ LISTA
            app_url = "https://cvroast-f5zmjjlaeonzcj8sncuzqc.streamlit.app/" 
            
            resumen_post = f"""🔥 ¡Mi CV acaba de ser triturado por una IA! 💀

📊 Diagnóstico Final:
- Empleabilidad: {score_emp}% 
- Veredicto: "Tu perfil tiene menos impacto que un reporte de BI sin filtros".

¿Crees que tu trayectoria sobrevive a Gemini 3? Pruébalo aquí:
{app_url}

#CVRoast #ITManagement #DataAnalytics #TechHumor #MichoacanTech"""

            st.code(resumen_post, language="text")
            texto_share = urllib.parse.quote(resumen_post)
            linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(app_url)}&summary={texto_share}"
            
            st.link_button("📲 Publicar en LinkedIn", linkedin_url)
            
        except Exception as e:
            st.error(f"Error técnico: {e}")

st.markdown("---")
st.caption("Hecho para profesionales con piel gruesa. Michoacán, 2026.")



