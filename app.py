import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import random
import urllib.parse

# 1. Configuración de Seguridad y Modelo
# Se recomienda usar st.secrets para la producción en Streamlit Cloud
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    # Llave de respaldo para pruebas locales
    API_KEY = "AIzaSyAQrDcDeYjS4Z6JCCF_Hk5-05EfWPasQX8"

genai.configure(api_key=API_KEY)

# Usando Gemini 3 Flash Preview según disponibilidad detectada
model = genai.GenerativeModel('gemini-3-flash-preview')

def extraer_texto_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

# --- Configuración de Interfaz ---
st.set_page_config(page_title="CV Roast AI 2026", page_icon="💀", layout="centered")

# Estilo personalizado para el botón de LinkedIn
st.markdown("""
    <style>
    .stDownloadButton, .stButton button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔥 CV Roast: Edición 2026")
st.subheader("Humillación profesional nivel Dios con Gemini 3")
st.markdown("---")

archivo_subido = st.file_uploader("Sube tu CV en formato PDF para ser destruido", type=["pdf"])

if archivo_subido is not None:
    with st.spinner('Escaneando tu triste existencia profesional...'):
        try:
            # Procesamiento del archivo
            texto_cv = extraer_texto_pdf(archivo_subido)
            
            # Prompt optimizado para humor negro y jerga técnica
            prompt = f"""
            Actúa como un reclutador de TI extremadamente amargado, sarcástico y cínico. 
            Analiza el texto de este CV y haz un 'Roast' corto pero brutalmente honesto. 
            Mención especial si ves clichés como 'trabajo bajo presión' o habilidades básicas como 'Office'.
            Usa jerga de TI, BI (Power BI, DAX) y si detectas algo de la industria de berries o JDEdwards, sé más ácido.
            
            Al final, entrega:
            1. Un veredicto de una sola frase lapidaria.
            2. 3 consejos directos que no pidieron pero necesitan.
            
            Texto del CV:
            {texto_cv}
            """
            
            response = model.generate_content(prompt)
            
            # --- Visualización de Resultados ---
            st.divider()
            
            # Métricas estilo Dashboard de BI
            col1, col2, col3 = st.columns(3)
            score_emp = random.randint(8, 38)
            col1.metric("Empleabilidad", f"{score_emp}%", "-62%")
            col2.metric("Nivel de Ego", f"{random.randint(85, 99)}%", "Crítico")
            col3.metric("Clichés", "100%", "Fijo")
            
            st.markdown("### 💀 Veredicto del Reclutador Tóxico:")
            st.write(response.text)
            
            # --- Funcionalidad Viral para LinkedIn ---
            st.divider()
            st.subheader("📢 ¡Comparte tu humillación!")
            
            # Texto resumido para el post
            # Puedes personalizar la URL final con la que te asigne Streamlit Cloud
            app_url = "https://cv-roast-ai-2026.streamlit.app" 
            
            texto_post = f"""🔥 ¡Mi CV acaba de ser destruido por una IA de Reclutamiento! 💀

📊 Mis resultados:
- Empleabilidad: {score_emp}% (Casi nula)
- Probabilidad de ser filtrado: 99.9%
- Ganas de llorar: Altas

Veredicto: "Tu CV tiene más parches que un sistema legacy de los 90".

¿Crees que tu CV es mejor? Pruébalo aquí bajo tu propio riesgo:
{app_url}

#CVRoast #Gemini3 #ITLife #DataScience #HumillacionTI"""

            # Codificación para URL de LinkedIn
            texto_codificado = urllib.parse.quote(texto_post)
            linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(app_url)}&summary={texto_codificado}"
            
            st.info("Copia este texto y usa el botón de abajo:")
            st.code(texto_post, language="text")
            
            # Botón directo a LinkedIn
            st.link_button("📲 Publicar Resultado en LinkedIn", linkedin_url)
            
        except Exception as e:
            st.error(f"Error técnico: {e}")
            st.info("Asegúrate de haber configurado la GEMINI_API_KEY en los Secrets de Streamlit.")

# Pie de página
st.markdown("---")
st.caption("Desarrollado para profesionales valientes. No apto para sensibles. 2026.")
