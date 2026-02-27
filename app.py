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
    st.error("⚠️ Error: Configura la API Key en los Secrets de Streamlit.")
    st.stop()

model = genai.GenerativeModel('gemini-3-flash-preview')

def extraer_texto_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

# --- 2. INTERFAZ ---
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
st.subheader("Humillación profesional nivel Dios con Gemini 3")

if 'contador_visitas' not in st.session_state:
    st.session_state.contador_visitas = random.randint(1580, 1650)
else:
    st.session_state.contador_visitas += random.randint(1, 2)

st.markdown(f"**{st.session_state.contador_visitas:,}** profesionales humillados hoy. ⚡")
st.markdown("---")

archivo_subido = st.file_uploader("Sube tu CV (PDF)", type=["pdf"])

if archivo_subido is not None:
    with st.spinner('Analizando tu triste realidad laboral...'):
        try:
            texto_cv = extraer_texto_pdf(archivo_subido)
            
            # PROMPT DINÁMICO: Extrae ubicación y profesión automáticamente
            prompt = f"""
            Actúa como un reclutador extremadamente cínico, amargado y sarcástico.
            1. Detecta la ubicación (ciudad/país) y la profesión principal del CV.
            2. Adapta tu roast basándote en su ubicación y mercado laboral actual.
            
            Responde ÚNICAMENTE en formato JSON con esta estructura:
            {{
                "ubicacion_detectada": "ciudad, país",
                "profesion": "título detectado",
                "roast": "crítica brutal de 3 párrafos usando jerga local de su zona si es posible",
                "arquetipo": "nombre gracioso del perfil",
                "veredicto_corto": "frase corta para redes",
                "habilidades_faltantes": [
                    {{"habilidad": "nombre", "link_busqueda": "url de búsqueda en udemy o coursera"}}
                ]
            }}
            Texto del CV: {texto_cv}
            """
            
            response = model.generate_content(prompt)
            # Limpieza de JSON
            clean_response = response.text.replace('```json', '').replace('```', '').strip()
            json_data = json.loads(clean_response)
            
            # --- 3. VISUALIZACIÓN ---
            st.divider()
            score_emp = random.randint(1, 35)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Ubicación", json_data["ubicacion_detectada"])
            col2.metric("Empleabilidad", f"{score_emp}%", f"-{100-score_emp}%")
            col3.metric("Ego", "En peligro", "💀")

            st.markdown(f"### 💀 Veredicto para este '{json_data['arquetipo']}':")
            st.write(json_data["roast"])

            # --- 4. RECOMENDACIONES DINÁMICAS ---
            st.divider()
            st.subheader(f"🛠️ Deja de dar pena en {json_data['ubicacion_detectada']}, aprende esto:")
            
            for hab in json_data["habilidades_faltantes"]:
                # Aquí puedes pasar el link_busqueda por tu acortador de Linkvertise
                st.link_button(f"👉 Especialízate en: {hab['habilidad']}", hab['link_busqueda'])

            # --- 5. COMPARTIR ---
            st.divider()
            app_url = "https://cvroast-f5zmjjlaeonzcj8sncuzqc.streamlit.app/" 
            
            resumen_post = f"""🔥 ¡Mi CV fue destruido por una IA! 💀

📊 Diagnóstico en {json_data['ubicacion_detectada']}:
- Perfil: {json_data['arquetipo']}
- Score: {score_emp}%
- Veredicto: "{json_data['veredicto_corto']}"

¿Tu carrera sobrevive a Gemini 3? Pruébalo aquí:
{app_url}

#CVRoast #CareerHumor #Gemini3 #{json_data['ubicacion_detectada'].replace(' ', '')}"""

            st.subheader("📲 ¡Comparte tu humillación!")
            st.code(resumen_post, language="text")
            
            linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(app_url)}"
            st.link_button("Publicar en LinkedIn 🚀", linkedin_url)
            
        except Exception as e:
            st.error("💣 La IA se colapsó con tu CV. Intenta con un archivo más claro.")
            st.write(f"Log: `{str(e)}`")

st.markdown("---")
st.caption("Análisis global, humor local. Powered by Gemini 3 Flash. 2026.")
