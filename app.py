import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import random
import urllib.parse

# 1. CONFIGURACIÓN DE SEGURIDAD (La forma correcta)
# Buscamos la llave en los Secrets de Streamlit Cloud. 
# Si no existe (local), intenta usar una variable de entorno o falla con elegancia.
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("⚠️ Error de Configuración: No se encontró la API Key en los Secrets.")
    st.stop()

# Usamos el modelo más reciente disponible en tu cuenta (Gemini 3)
model = genai.GenerativeModel('gemini-3-flash-preview')

def extraer_texto_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

# --- Interfaz de Usuario ---
st.set_page_config(page_title="CV Roast AI 2026", page_icon="💀", layout="centered")

# Barra lateral para monetización y apoyo
st.sidebar.markdown('### ☕ ¿Te dolió el Roast?')
st.sidebar.markdown(
    """<a href="https://www.buymeacoffee.com/tu_usuario" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 50px !important;width: 180px !important;" >
    </a>""", 
    unsafe_allow_html=True
)
st.sidebar.caption("Ayúdame a pagar los tokens de la IA")

st.title("🔥 CV Roast: Edición 2026")
st.subheader("Humillación profesional nivel Dios con Gemini 3")

archivo_subido = st.file_uploader("Sube tu CV (PDF)", type=["pdf"])

if archivo_subido is not None:
    with st.spinner('Analizando tu triste existencia profesional...'):
        try:
            texto_cv = extraer_texto_pdf(archivo_subido).lower()
            
            # Prompt ácido con enfoque en TI y BI
            prompt = f"""
            Actúa como un reclutador de TI extremadamente sarcástico y experto en BI. 
            Analiza este CV y haz un roast brutal. 
            Identifica si tiene Power BI, Python o SQL.
            Asigna un 'Arquetipo de Falla' gracioso.
            Texto: {texto_cv}
            """
            
            response = model.generate_content(prompt)
            
            # --- Visualización de Datos (BI Style) ---
            st.divider()
            score_emp = random.randint(5, 35)
            col1, col2, col3 = st.columns(3)
            col1.metric("Empleabilidad", f"{score_emp}%", "-75%")
            col2.metric("Nivel de Clichés", "Crítico", "⚠️")
            col3.metric("Ego Tech", "99%", "Fijo")

            st.markdown("### 💀 Veredicto Brutal:")
            st.write(response.text)

            # --- MONETIZACIÓN: Cursos Recomendados ---
            st.divider()
            st.subheader("🛠️ Deja de dar pena, invierte en ti:")
            
            # Lógica de recomendación basada en el contenido del CV
            if "power bi" not in texto_cv:
                st.warning("⚠️ **Falla de BI:** Tu CV no tiene Power BI. Sigues viviendo en la era de piedra.")
                st.link_button("🚀 Curso: Power BI & DAX Maestro", "https://www.udemy.com/")
            
            if "python" not in texto_cv:
                st.info("🐍 **Sugerencia:** Sin Python, la IA te reemplazará antes del viernes.")
                st.link_button("🐍 Ver: Python para Datos", "https://www.coursera.org/")

            # --- COMPARTIR: Botón Viral para LinkedIn ---
            st.divider()
            app_url = "https://tu-app-url.streamlit.app" # Cambia esto por tu URL final
            
            resumen_post = f"""🔥 ¡Mi CV fue humillado por una IA de Reclutamiento! 💀

📊 Resultados de mi dolor:
- Empleabilidad: {score_emp}%
- Veredicto: "Tu perfil tiene menos impacto que un reporte sin filtros".

¿Crees que tu trayectoria sobrevive? Pruébalo aquí:
{app_url}

#CVRoast #ITManagement #Gemini3 #TechHumor"""

            st.code(resumen_post, language="text")
            texto_share = urllib.parse.quote(resumen_post)
            link_linkedin = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(app_url)}&summary={texto_share}"
            
            st.link_button("📲 Publicar en LinkedIn", link_linkedin)
            
        except Exception as e:
            st.error(f"Error técnico: {e}")

st.markdown("---")
st.caption("Hecho para profesionales con piel gruesa, 2026.")


