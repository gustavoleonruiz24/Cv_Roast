import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import random
import urllib.parse

# 1. Configuración de Seguridad y Modelo
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    # Llave para pruebas locales
    API_KEY = "AIzaSyAQrDcDeYjS4Z6JCCF_Hk5-05EfWPasQX8"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-3-flash-preview')

def extraer_texto_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

# --- Configuración de Interfaz ---
st.set_page_config(page_title="CV Roast AI 2026", page_icon="💀", layout="centered")

st.title("🔥 CV Roast: Edición 2026")
st.subheader("Humillación profesional nivel Dios con Gemini 3")
st.markdown("---")

archivo_subido = st.file_uploader("Sube tu CV (PDF) para ser destruido", type=["pdf"])

if archivo_subido is not None:
    with st.spinner('Analizando tu triste realidad laboral...'):
        try:
            texto_cv = extraer_texto_pdf(archivo_subido)
            
            # Prompt avanzado con peticiones específicas de arquetipo y métricas
            prompt = f"""
            Actúa como un reclutador de TI amargado, experto en BI y ERPs.
            Analiza este CV y:
            1. Haz un roast brutal y corto.
            2. Asigna un 'Arquetipo de Falla' (ej: Dinosaurio del ERP, Mago del Excel 97, Eterno Junior, Señor Cliché).
            3. Identifica el cliché más imperdonable.
            
            Usa jerga de TI, Power BI y sector agro (si aplica). 
            
            Texto del CV:
            {texto_cv}
            """
            
            response = model.generate_content(prompt)
            
            # --- Lógica de BI y "Humillación Visual" ---
            st.divider()
            
            # Generación de métricas para el impacto visual
            score_emp = random.randint(5, 38)
            score_fatiga = random.randint(80, 100)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Empleabilidad", f"{score_emp}%", "-65%")
            col2.metric("Fatiga del Reclutador", f"{score_fatiga}%", "Crítico")
            col3.metric("Clichés TI", "100%", "Fijo")
            
            # Gráfico de barras de "Habilidades vs. Realidad"
            st.write("### 📊 Análisis de Skills Reales")
            chart_data = {
                "Habilidad": ["Autoestima", "Uso de Clichés", "Skills de LinkedIn", "Habilidad Real"],
                "Nivel": [95, 100, 85, score_emp]
            }
            st.bar_chart(chart_data, x="Habilidad", y="Nivel")

            st.markdown("### 💀 Veredicto del Reclutador Tóxico:")
            st.write(response.text)
            
            # --- Funcionalidad Viral para LinkedIn ---
            st.divider()
            st.subheader("🚀 Hazlo Viral (Si tienes valor)")
            
            # Lista de arquetipos para el post
            arquetipos = ["Dinosaurio del ERP", "Mago de Tablas Planas", "Señor Cliché", "Eterno Junior", "Candidato Fantasma"]
            tu_arquetipo = random.choice(arquetipos)
            
            app_url = "https://tu-app-url.streamlit.app" # Cambia por tu URL real
            
            texto_post = f"""🔥 ¡Mi CV acaba de ser triturado por una IA de Reclutamiento! 💀

📊 Resultados de mi humillación:
- Arquetipo: {tu_arquetipo}
- Empleabilidad: {score_emp}% (Casi nula)
- Índice de Fatiga: {score_fatiga}% 💤

Veredicto: "Tu CV es un 45% más genérico que el promedio de los Managers de TI".

¿Te atreves a que Gemini 3 destruya tu trayectoria? Pruébalo aquí:
{app_url}

#CVRoast #ITManagement #DataAnalytics #TechHumor #MichoacanTech"""

            texto_codificado = urllib.parse.quote(texto_post)
            linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(app_url)}&summary={texto_codificado}"
            
            st.info("Copia este texto y pégalo en LinkedIn:")
            st.code(texto_post, language="text")
            
            st.link_button("📲 Publicar en LinkedIn", linkedin_url)
            
        except Exception as e:
            st.error(f"Error técnico: {e}")

st.markdown("---")
st.caption("Desarrollado para profesionales con piel gruesa. 2026.")

