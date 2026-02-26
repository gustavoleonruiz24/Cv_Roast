import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import os

# 1. Configuración con el modelo que SÍ tienes disponible
API_KEY = "AIzaSyAQrDcDeYjS4Z6JCCF_Hk5-05EfWPasQX8"
genai.configure(api_key=API_KEY)

# Usamos la joya de la corona que te apareció en la lista
model = genai.GenerativeModel('gemini-3-flash-preview')

def extraer_texto_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

# --- Interfaz de Streamlit ---
st.set_page_config(page_title="CV Roast AI 2026", page_icon="💀")

st.title("🔥 CV Roast: Edición 2026")
st.subheader("Humillación profesional nivel Dios con Gemini 3")

archivo_subido = st.file_uploader("Sube tu CV (PDF)", type=["pdf"])

if archivo_subido is not None:
    with st.spinner('Escaneando mediocridad...'):
        try:
            texto_cv = extraer_texto_pdf(archivo_subido)
            
            prompt = f"""
            Actúa como un reclutador de TI amargado y sarcástico. 
            Analiza este CV y haz un roast brutal. 
            Critica la falta de proyectos reales, las habilidades de relleno y los clichés.
            Usa jerga de TI moderna (IA, Cloud, BI).
            
            Al final, da 3 consejos 'brutalmente honestos'.
            
            Texto del CV:
            {texto_cv}
            """
            
            response = model.generate_content(prompt)
            
            st.divider()
            st.markdown("### 💀 Veredicto Brutal:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Error técnico: {e}")