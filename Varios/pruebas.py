import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO

st.title("Generador de Códigos de Barras 🖨️")

# Personalización en sidebar
with st.sidebar:
    st.header("Configuración")
    formato = st.selectbox("Formato", ["code128", "ean13", "code39"])
    texto = st.text_input("Datos a codificar", "PRUEBASCAME")
    mostrar_texto = st.checkbox("Mostrar texto debajo", False)
    ancho_modulo = st.slider("Ancho de barras", 0.1, 1.0, 0.4)
    altura_modulo = st.slider("Altura de barras", 10, 50, 20)

def generar_codigo():
    try:
        # Generar código en memoria
        buffer = BytesIO()
        codigo = barcode.generate(
            formato,
            texto,
            writer=ImageWriter(),
            output=buffer,
            writer_options={
                "write_text": mostrar_texto,
                "module_width": ancho_modulo,
                "module_height": altura_modulo
            }
        )
        buffer.seek(0)
        return buffer
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Botón de generación
if st.button("Generar Código"):
    codigo_bytes = generar_codigo()
    
    if codigo_bytes:
        # Mostrar previsualización
        st.image(codigo_bytes, caption="Vista previa del código")
        
        # Botón de descarga
        st.download_button(
            label="Descargar código de barras",
            data=codigo_bytes,
            file_name=f"codigo_{texto}.png",
            mime="image/png"
        )

# Instrucciones
st.markdown("""
**Instrucciones:**
1. Ingresa el texto a codificar
2. Personaliza la apariencia en la barra lateral
3. Haz clic en 'Generar Código'
4. Descarga el resultado cuando aparezca
""")