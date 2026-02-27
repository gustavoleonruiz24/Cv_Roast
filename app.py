import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import random
import urllib.parse
import json

# --- 1. CONFIGURACIÓN DE SEGURIDAD ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("⚠️ Error de Configuración: Revisa los Secrets.")
    st.stop()

# --- 2. CONFIGURACIÓN DEL MODELO ---
model = genai.GenerativeModel('gemini-3-flash-preview')

def extraer_texto_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

# --- 3. UI ---
st.set_page_config(page_title="CV Roast AI 2026", page_icon="💀", layout="centered")

st.markdown(
    """<div style="text-align: right;">
        <a href="https://www.buymeacoffee.com/gleon" target="_blank">
            <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 40px !important;width: 145px !important;" >
        </a>
    </div>""", 
    unsafe_allow_html=True
)

st.title("🔥 CV Roast: Edición 2026")
st.subheader("Humillación profesional nivel Dios")

if 'contador_visitas' not in st.session_state:
    st.session_state.contador_visitas = random.randint(1580, 1650)
else:
    st.session_state.contador_visitas += random.randint(1, 2)

st.markdown(f"**{st.session_state.contador_visitas:,}** profesionales humillados hoy. ⚡")
st.markdown("---")

archivo_subido = st.file_uploader("Sube tu CV (PDF) para ser destruido", type=["pdf"])

if archivo_subido is not None:
    with st.spinner('Analizando tu triste realidad...'):
        try:
            texto_cv = extraer_texto_pdf(archivo_subido)
            
            # PROMPT MAESTRO: Pide una respuesta estructurada en JSON para manejar la lógica
            prompt = f"""
            Actúa como un reclutador extremadamente cínico y sarcástico de Jacona, Michoacán.
            Analiza el texto de este CV y responde ÚNICAMENTE en formato JSON con la siguiente estructura:
            {{
                "roast": "tu crítica brutal de 3 párrafos",
                "arquetipo": "Nombre gracioso del tipo de profesional",
                "veredicto_corto": "Una frase lapidaria para compartir en redes",
                "habilidades_faltantes": [
                    {{"habilidad": "nombre", "link_busqueda": "url de búsqueda en udemy o coursera"}},
                    {{"habilidad": "nombre", "link_busqueda": "url de búsqueda en udemy o coursera"}}
                ]
            }}
            Usa términos de búsqueda reales en los links (ej: https://www.udemy.com/courses/search/?q=power+bi).
            Texto del CV: {texto_cv}
            """
            
            response = model.generate_content(prompt)
            # Limpiamos la respuesta para asegurar que sea JSON válido
            json_data = json.loads(response.text.replace('```json', '').replace('```', ''))
            
            # --- 6. VISUALIZACIÓN ---
            st.divider()
            score_emp = random.randint(1, 40)
            col1, col2, col3 = st.columns(3)
            col1.metric("Empleabilidad", f"{score_emp}%", f"-{100-score_emp}%")
            col2.metric("Arquetipo", json_data["arquetipo"])
            col3.metric("Ego", "Inflado", "⚠️")

            st.markdown(f"### 💀 Veredicto para este '{json_data['arquetipo']}':")
            st.write(json_data["roast"])

            # --- 7. CURSOS DINÁMICOS (Basados en el análisis) ---
            st.divider()
            st.subheader("🛠️ Deja de dar pena, aprende esto:")
            
            for hab in json_data["habilidades_faltantes"]:
                # Aquí puedes envolver el link_busqueda con Linkvertise manualmente
                # o dejar que la IA genere el link directo de búsqueda
                st.link_button(f"👉 Mejorar en: {hab['habilidad']}", hab['link_busqueda'])

            # --- 8. LINKEDIN DINÁMICO ---
            st.divider()
            app_url = "https://cvroast-f5zmjjlaeonzcj8sncuzqc.streamlit.app/" 
            
            resumen_post = f"""🔥 ¡Mi CV fue destruido por una IA! 💀

📊 Diagnóstico:
- Arquetipo: {json_data['arquetipo']}
- Score: {score_emp}%
- Veredicto: "{json_data['veredicto_corto']}"

Pruébalo aquí (bajo tu propio riesgo):
{app_url}

#CVRoast #CareerHumor #Gemini3 #TechLife"""

            st.subheader("📲 Comparte tu humillación")
            st.code(resumen_post, language="text")
            
            linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(app_url)}"
            st.link_button("Publicar en LinkedIn 🚀", linkedin_url)
            
        except Exception as e:
            st.error("💣 Error de procesamiento. Intenta con un CV más legible.")
            st.write(f"Log técnico: `{str(e)}`")

st.markdown("---")
st.caption("Basado en análisis de IA real.")



