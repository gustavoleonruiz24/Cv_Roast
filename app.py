import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import random
import urllib.parse

# --- 1. CONFIGURACIÓN DE SEGURIDAD ---
# Se utiliza el sistema de Secrets de Streamlit para proteger la API Key
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("⚠️ Error de Configuración: No se encontró la API Key en los Secrets de Streamlit.")
    st.info("Asegúrate de añadir GEMINI_API_KEY en Settings > Secrets.")
    st.stop()

# --- 2. CONFIGURACIÓN DEL MODELO ---
# Usamos el identificador exacto validado mediante el script de diagnóstico local
model = genai.GenerativeModel('gemini-3-flash-preview')

def extraer_texto_pdf(file):
    """Extrae texto de un archivo PDF subido."""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

# --- 3. CONFIGURACIÓN DE INTERFAZ (UI) ---
st.set_page_config(page_title="CV Roast AI 2026", page_icon="💀", layout="centered")

# Botón de Café para monetización
st.markdown(
    """<div style="text-align: right;">
        <a href="https://www.buymeacoffee.com/gleon" target="_blank">
            <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 40px !important;width: 145px !important;" >
        </a>
    </div>""", 
    unsafe_allow_html=True
)

st.title("🔥 CV Roast: Edición 2026")
st.subheader("Humillación profesional nivel Dios con Gemini 3")

# --- 4. CONTADOR DINÁMICO (SOCIAL PROOF) ---
# Simula actividad constante incrementando el número en cada sesión
if 'contador_visitas' not in st.session_state:
    st.session_state.contador_visitas = random.randint(1580, 1650)
else:
    st.session_state.contador_visitas += random.randint(1, 2)

st.markdown(f"**{st.session_state.contador_visitas:,}** profesionales humillados el día de hoy. ⚡")
st.markdown("---")

# --- 5. CARGA Y PROCESAMIENTO DE ARCHIVOS ---
archivo_subido = st.file_uploader("Sube tu CV (PDF) para ser destruido por la IA", type=["pdf"])

if archivo_subido is not None:
    with st.spinner('Gemini 3 analizando tu mediocre realidad laboral...'):
        try:
            texto_cv = extraer_texto_pdf(archivo_subido).lower()
            
            # Prompt diseñado para un perfil de TI/BI con humor local
            prompt = f"""
            Actúa como un reclutador de TI extremadamente cínico y amargado de Jacona, Michoacán. 
            Analiza este CV y haz un roast brutal, corto y muy sarcástico de máximo 3 párrafos. 
            Identifica si el candidato sabe Power BI, Python o SQL.
            Asigna un 'Arquetipo de Falla' gracioso.
            Texto del CV: {texto_cv}
            """
            
            response = model.generate_content(prompt)
            
            # --- 6. VISUALIZACIÓN DE RESULTADOS ---
            st.divider()
            
            # Métricas ficticias para estilo BI
            score_emp = random.randint(5, 38)
            col1, col2, col3 = st.columns(3)
            col1.metric("Empleabilidad", f"{score_emp}%", "-62%")
            col2.metric("Nivel de Clichés", "Crítico", "⚠️")
            col3.metric("Ego Tech", "99%", "Fijo")

            st.markdown("### 💀 Veredicto del Reclutador Tóxico:")
            st.write(response.text)

            # --- 7. MONETIZACIÓN: CURSOS RECOMENDADOS ---
            st.divider()
            st.subheader("🛠️ Deja de dar pena, invierte en ti:")
            
            # Recomendaciones dinámicas basadas en el contenido del CV
            if "power bi" not in texto_cv and "dax" not in texto_cv:
                st.warning("⚠️ **Falla de BI:** Tu CV no tiene Power BI. Sigues en la era de piedra.")
                st.link_button("🚀 Curso Maestro: Power BI & DAX", "https://www.udemy.com/")
            
            if "python" not in texto_cv:
                st.info("🐍 **Sugerencia:** Sin Python, la IA te reemplazará antes del viernes.")
                st.link_button("🐍 Ver: Python para Análisis de Datos", "https://www.coursera.org/")

            # --- 8. FLUJO DE COMPARTIR EN LINKEDIN ---
            st.divider()
            app_url = "https://cvroast-f5zmjjlaeonzcj8sncuzqc.streamlit.app/" 
            
            resumen_post = f"""🔥 ¡Mi CV acaba de ser triturado por una IA en el CV Roast 2026! 💀

📊 Mi Diagnóstico:
- Empleabilidad: {score_emp}% 
- Veredicto: "Tu perfil tiene menos impacto que un reporte de BI sin filtros".

¿Crees que tu trayectoria sobrevive a Gemini 3? Pruébalo aquí:
{app_url}

#CVRoast #ITManagement #DataAnalytics #TechHumor #MichoacanTech"""

            st.subheader("📲 ¡Comparte tu humillación!")
            
            # Paso 1: Copiar el texto (UX optimizada)
            st.write("1. Copia este mensaje (usa el botón de la esquina superior derecha del cuadro):")
            st.code(resumen_post, language="text")
            
            # Paso 2: Publicar en LinkedIn
            st.write("2. Pégalo en tu muro de LinkedIn:")
            linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(app_url)}"
            
            st.link_button("Ir a publicar en LinkedIn 🚀", linkedin_url)
            st.caption("Nota: Para que el mensaje aparezca completo, pégalo manualmente en LinkedIn.")
            
        except Exception as e:
            st.error("💣 Error de conexión con la IA.")
            st.info("Estamos ajustando los modelos para tu cuenta Pay-as-you-go.")
            st.write(f"Log técnico: `{str(e)}`")

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("Desarrollado para profesionales con piel gruesa. 2026.")



