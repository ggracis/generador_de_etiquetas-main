import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import io
import datetime
import time
import pytz
import pandas as pd
import os

# Configuración para ocultar elementos de la UI
st.set_page_config(
    page_title="Generador de Etiquetas - CAME",
    page_icon="imgs/CAME-Transparente.ico.ico",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Agregar metadatos para SEO
st.markdown("""
    <head>
        <meta name="description" content="Generador de etiquetas de precios según la resolución 04/2025. Herramienta oficial de CAME para comercios.">
        <meta name="keywords" content="etiquetas, precios, CAME, comercio, resolución 04/2025, IVA, precios al consumidor">
        <meta name="author" content="CAME - Confederación Argentina de la Mediana Empresa">
        <meta name="robots" content="index, follow">
        <meta property="og:title" content="Generador de Etiquetas - CAME">
        <meta property="og:description" content="Generador de etiquetas de precios según la resolución 04/2025. Herramienta oficial de CAME para comercios.">
        <meta property="og:image" content="https://came.ar/imgs/CAME-Transparente.png">
        <meta property="og:url" content="https://came.ar/generador-etiquetas">
        <link rel="canonical" href="https://came.ar/generador-etiquetas">
    </head>
""", unsafe_allow_html=True)

# Agregar schema.org markup
st.markdown("""
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Generador de Etiquetas CAME",
        "description": "Herramienta para generar etiquetas de precios según la resolución 04/2025",
        "url": "https://came.ar/generador-etiquetas",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Web",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "ARS"
        },
        "provider": {
            "@type": "Organization",
            "name": "CAME",
            "url": "https://came.ar"
        }
    }
    </script>
""", unsafe_allow_html=True)

# Ocultar el footer de Streamlit y personalizar estilos
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Quitar el cursor de enlace */
a {
    cursor: default !important;
    text-decoration: none !important;
}

/* Opcional: si quieres que el enlace cambie de color al pasar el mouse */
a:hover {
    color: inherit !important;
}

/* Estilos para SEO */
.description {
    margin: 20px 0;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 5px;
}

.breadcrumb {
    padding: 8px 15px;
    margin-bottom: 20px;
    list-style: none;
    background-color: #f5f5f5;
    border-radius: 4px;
}

.breadcrumb-item {
    display: inline-block;
}

.breadcrumb-item + .breadcrumb-item::before {
    content: ">";
    padding: 0 5px;
    color: #6c757d;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Agregar breadcrumbs
st.markdown("""
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="https://came.ar">Inicio</a></li>
            <li class="breadcrumb-item"><a href="https://came.ar/herramientas">Herramientas</a></li>
            <li class="breadcrumb-item active" aria-current="page">Generador de Etiquetas</li>
        </ol>
    </nav>
""", unsafe_allow_html=True)

# Configuración de rutas para archivos locales
DATA_DIR = "data"
CALIFICACIONES_FILE = os.path.join(DATA_DIR, "calificaciones.csv")
PROVINCIAS_FILE = os.path.join(DATA_DIR, "provincias.csv")

# Crear directorio de datos si no existe
os.makedirs(DATA_DIR, exist_ok=True)

# Inicializar archivos CSV si no existen
def init_csv_files():
    if not os.path.exists(CALIFICACIONES_FILE):
        pd.DataFrame(columns=['Fecha', 'Hora', 'Evaluación']).to_csv(CALIFICACIONES_FILE, index=False)
    if not os.path.exists(PROVINCIAS_FILE):
        pd.DataFrame(columns=['Fecha', 'Hora', 'Provincia']).to_csv(PROVINCIAS_FILE, index=False)

# Inicializar archivos
init_csv_files()

# Creamos la función para agregar datos    
def calificacion(fecha_actual, hora_actual, evaluation):
    # Leer el CSV existente
    df = pd.read_csv(CALIFICACIONES_FILE)
    
    # Create a DataFrame with the new data
    new_data = pd.DataFrame({
        'Fecha': [fecha_actual],
        'Hora': [hora_actual],
        'Evaluación': [evaluation],
    })
    
    # Append the new DataFrame to the existing DataFrame
    df = pd.concat([df, new_data], ignore_index=True)
    
    # Save the updated DataFrame
    df.to_csv(CALIFICACIONES_FILE, index=False)
    
# Creamos la función para agregar datos    
def provincia(fecha_actual, hora_actual, provincia):
    # Leer el CSV existente
    df = pd.read_csv(PROVINCIAS_FILE)
    
    # Create a DataFrame with the new data
    new_data = pd.DataFrame({
        'Fecha': [fecha_actual],
        'Hora': [hora_actual],
        'Provincia': [provincia],
    })
    
    # Append the new DataFrame to the existing DataFrame
    df = pd.concat([df, new_data], ignore_index=True)
    
    # Save the updated DataFrame
    df.to_csv(PROVINCIAS_FILE, index=False)

columna_titulo, columna_logo = st.columns([2,1])
with columna_titulo:
    # Aplicar estilos de formato CSS para agrandar el título
    st.markdown("<h1 style='text-align: left; font-size: 54px; font-family: Verdana, sans-serif;'>Generador de Etiquetas de Precios - CAME</h1>", unsafe_allow_html=True)
with columna_logo:
    st.write("")
    st.write("")
    st.image("imgs/CAME-Transparente.png", use_container_width=True, alt="Logo CAME - Confederación Argentina de la Mediana Empresa")
    
# Agregar descripción semántica
st.markdown("""
    <div class="description">
        <h2>Herramienta oficial para generar etiquetas de precios según la resolución 04/2025</h2>
        <p>Esta aplicación permite a los comercios generar etiquetas de precios cumpliendo con la normativa vigente, incluyendo el desglose de IVA y precios por unidad.</p>
    </div>
""", unsafe_allow_html=True)

st.write("#### De acuerdo a la [resolución 04/2025.](https://www.argentina.gob.ar/sites/default/files/exhibicion_de_precios_resolucion_4_2025.pdf)")

st.write("---")

st.write("Según la Ley N° 23.349 - ley de IVA - las alícuotas se aplican del siguiente modo: ")
st.write("+ **21% =** Consumo general (electrodomésticos, textiles, alimentos procesados, etc.).")
st.write("+ **10,5% =** Productos agropecuarios, carne, pan, frutas y verduras.")
st.write("+ **0% =** Libros, folletos, diarios.")

st.write("---")
def draw_wrapped_text(draw= None, text= None, font= None, max_width = 235, x = 30, y = 25+8, fill = None):
    lines = []
    words = text.split()
    line = ""

    for word in words:
        test_line = line + " " + word if line else word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = bbox[2] - bbox[0]

        if text_width <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)

    # Dibujar las líneas en la imagen
    for i, l in enumerate(lines):
        bbox = draw.textbbox((0, 0), l, font=font)
        line_height = bbox[3] - bbox[1]
        draw.text((x, y + i * (line_height + 9)), l, font=font, fill=fill)


# Entrada de precio final y selección de IVA
# listado de provincias
provincias = [
    "-",
    "Buenos Aires",
    "CABA",
    "Catamarca",
    "Chaco",
    "Chubut",
    "Córdoba",
    "Corrientes",
    "Entre Ríos",
    "Formosa",
    "Jujuy",
    "La Pampa",
    "La Rioja",
    "Mendoza",
    "Misiones",
    "Neuquén",
    "Río Negro",
    "Salta",
    "San Juan",
    "San Luis",
    "Santa Cruz",
    "Santa Fe",
    "Santiago del Estero",
    "Tierra del Fuego",
    "Tucumán"
]

# Seleccionar provincia
provincia_seleccionada = st.selectbox("Seleccione su provincia",provincias) 
col1, col2 = st.columns([2, 1])
with col1:
    producto = st.text_input("Producto", "")
    precio_final = st.text_input("Precio Final del Producto", value="$")
    # Se formatea el valor ingresado
    precio_final_procesado = precio_final.strip()
    precio_final_procesado = precio_final_procesado.replace("$", "").replace(".","").replace(",,",",").replace(",",".")  
with col2:
    iva = st.selectbox("IVA", ["21%", "10.5%", "Exento"])
    dividir_por_litro_o_kg = st.selectbox("Unidad", ["Sin unidades", "Kilogramos", "Litros"])
    if dividir_por_litro_o_kg != "Sin unidades":
        cantidad =st.number_input("Cantidad", min_value=0.1, value=1.00,  format="%.2f")
      

# Validar si el precio final es un número válido
try:
    precio_final_float = float(precio_final_procesado)
    precio_valido = True
except ValueError:
    precio_valido = False

st.write("---")
# Mostrar preview de la imagen si el precio es válido
if precio_valido and provincia_seleccionada != "-":
    color1,color2,color3,color4,color5 = st.columns(5)
    # Configuración de colores
    with color1:
        color_texto = st.color_picker("Texto", "#000000")
    with color2:
        color_fondo_superior = st.color_picker("Fondo Superior", "#F5F5F5")
    with color3:    
        color_fondo_inferior = st.color_picker("Fondo Inferior", "#FFFFFF")
    with color4:
        color_borde_interior = st.color_picker("Borde Interior", "#000000")
    with color5:
        color_borde_exterior = st.color_picker("Borde Exterior", "#FFFFFF")

 
    # Calcular precio sin IVA y precio por litro
    if iva == "21%":
        precio_sin_iva = precio_final_float / 1.21
    elif iva == "10.5%":
        precio_sin_iva = precio_final_float / 1.105
    else:  # Exento
        precio_sin_iva = precio_final_float

    # SI TIENE KG O L
    if dividir_por_litro_o_kg != "Sin unidades":
        precio_cantidad = precio_final_float / cantidad
    else: precio_cantidad = 0

    # Creamos lista de variables
    lista_variables = [ precio_final_float, precio_sin_iva, precio_cantidad]
        
    # iteramos para el formato
    for i in range (len(lista_variables)) :
        lista_variables[i] = '{:,.2f}'.format(lista_variables[i]).replace(',', ' ')
        lista_variables[i] = lista_variables[i].replace(".",",")
        lista_variables[i] = lista_variables[i].replace(" ",".")

    # Crear imagen
    img = Image.new("RGB", (720, 300), color=color_fondo_superior)
    draw = ImageDraw.Draw(img)

    # Dibujar fondo inferior
    draw.rectangle([0, 190, 720, 300], fill=color_fondo_inferior)

    # Fuentes
    font_large = ImageFont.truetype("Fuentes/Inter/Inter-Medium.ttf", 45)
    font_medium = ImageFont.truetype("Fuentes/Inter/Inter-Medium.ttf", 24)
    font_small = ImageFont.truetype("Fuentes/Inter/Inter-Medium.ttf", 16)
    
    # Dibujar texto
    producto = producto.upper()

    draw_wrapped_text(draw, producto, font_medium, fill=color_texto)

    draw.text((320, 25 + 8), "Precio final al consumidor", fill=color_texto, font=font_small)
    draw.text((320,   48 + 8), f"${lista_variables[0]}", fill=color_texto, font=font_large)
    draw.text((320,  109 + 8), f"Precio sin impuestos nacionales (IVA) ${lista_variables[1]}", fill=color_texto, font=font_small)

    if dividir_por_litro_o_kg == "Kilogramos":
        draw.text((320,  130 + 8), f"Precio al consumidor por kilogramo ${lista_variables[2]}", fill=color_texto, font=font_small)
    elif dividir_por_litro_o_kg == "Litros":
        draw.text((320,  130 + 8), f"Precio al consumidor por litro ${lista_variables[2]}", fill=color_texto, font=font_small)    

    # Dibujar borde negro
    draw.rectangle([0, 0, 719, 299], outline=color_borde_exterior, width=10)
    # Dibujar borde negro
    draw.rectangle([10, 10, 709, 289], outline=color_borde_interior, width=2)

    # Cargar imagen de marca de agua (asegurate de que el PNG tenga fondo transparente)
    marca_agua = Image.open("imgs/CAME_baja-solo.jpg").convert("RGBA")
    # Redimensionar si hace falta
    marca_agua = marca_agua.resize((720, 270))  # Ajustá tamaño según prefieras

    # Cambiar transparencia (más baja = más transparente)
    alpha = 9  # de 0 (invisible) a 255 (opaco)
    # Separar canales y aplicar nuevo alpha
    r, g, b, a = marca_agua.split()
    marca_agua.putalpha(alpha)

    # Posición de la marca de agua (abajo a la derecha, por ejemplo)
    pos_x = img.width - marca_agua.width - 10
    pos_y = img.height - marca_agua.height - 10

    # Pegar la marca de agua sobre la imagen principal
    img.paste(marca_agua, (pos_x, pos_y), marca_agua)
 
    escala = st.slider("Tamaño de la etiqueta", min_value=0.1, max_value=3.0, value=1.0, step=0.1)

    # Redimensionar imagen
    nuevo_ancho = int(img.width * escala)
    nuevo_alto = int(img.height * escala)
    img_redimensionada = img.resize((nuevo_ancho, nuevo_alto))

    # Mostrar imagen redimensionada
    st.image(img_redimensionada, caption=f"Tamaño: {nuevo_ancho} x {nuevo_alto}")

    # Botón para descargar la imagen
    buf = io.BytesIO()
    img_redimensionada.save(buf, format="PNG")
    buf.seek(0)
     
    if st.download_button(
        label="Descargar Etiqueta",
        data=buf,
        file_name="etiqueta.png",
        mime="image/png"
        ):
        # Establecer la zona horaria a Buenos Aires
        zona_horaria = pytz.timezone('America/Argentina/Buenos_Aires')
    
        # Obtener la fecha y hora actual en la zona horaria especificada
        fecha_hora_actual = datetime.datetime.now(zona_horaria)
    
        # Obtener la fecha en formato dd/mm/aa
        fecha_actual = fecha_hora_actual.strftime("%d/%m/%y")
    
        # Obtener la hora en formato hh:mm:ss
        hora_actual = fecha_hora_actual.strftime("%H:%M:%S")
        # Agregar st.write para verificar el valor de evaluation
        try:
            provincia(fecha_actual, hora_actual, provincia_seleccionada)
        # Si salta error, esperar dos segundos y volver a cargar    
        except Exception:
            try:
                time.sleep(2)
                provincia(fecha_actual, hora_actual, provincia_seleccionada)
            except Exception:
                pass
    else: pass

    
    # FORMULARIO DE CALIFICACIÓN
    with st.form(key='calificacion usuario'):
        # Evaluación       
        evaluation = st.radio("¿Cómo calificaría el funcionamiento de la calculadora?", ["Excelente", "Buena", "Regular", "Mala", "Muy mala"],horizontal=True)
        # Botón de calificación
        submit_button = st.form_submit_button(label='Enviar')
        # Verificar si el formulario se ha enviado
        if submit_button:
             # Establecer la zona horaria a Buenos Aires
            zona_horaria = pytz.timezone('America/Argentina/Buenos_Aires')
        
            # Obtener la fecha y hora actual en la zona horaria especificada
            fecha_hora_actual = datetime.datetime.now(zona_horaria)
        
            # Obtener la fecha en formato dd/mm/aa
            fecha_actual = fecha_hora_actual.strftime("%d/%m/%y")
        
            # Obtener la hora en formato hh:mm:ss
            hora_actual = fecha_hora_actual.strftime("%H:%M:%S")
            # Agregar st.write para verificar el valor de evaluation
        
            try:
                calificacion(fecha_actual, hora_actual, evaluation)
                st.success("Calificación enviada exitosamente!")
            # Si salta error, esperar dos segundos y volver a cargar    
            except Exception:
                try:
                    time.sleep(2)
                    calificacion(fecha_actual, hora_actual, evaluation)
                    st.success("Calificación enviada exitosamente!")
                except Exception:
                    pass
else:
    st.warning("Por favor, seleccione su provincia y ingrese un número válido en el campo de Precio Final.")

st.write("---")
st.write("**Aclaración**")
st.write("El usuario reconoce y acepta que los datos generados son a título meramente informativo y orientativo. La herramienta no apunta a establecer precios finales para ninguna operación sino brindar, de manera detallada, la información que un comercio puede necesitar para definir, por decisión propia, los precios de los productos y servicios que comercializa. Asimismo, CAME no se responsabiliza por la información brindada por el sistema, su actualización o su falta de disponibilidad.")
st.markdown("Para mayor información [click aquí](https://www.argentina.gob.ar/sites/default/files/exhibicion_de_precios_resolucion_4_2025.pdf)")
st.write("---")

# Columnas inferiores
col1, col2, col3 = st.columns([2,2,2])

with col1 :
    st.write("")

with col2 : 
    st.image("imgs/LOGO. ESTADÍSTICAS.png", use_container_width=True)
    
with col3 :
    st.write("")

st.write("---")
# Titulo para las redes con estilo personalizado
st.markdown(
    """
    <div style="text-align: center; padding: 10px 0; margin-top: 0;">
        <h1 style="
            border: 2px solid #004AAD;
            padding: 10px 10px;
            font-size: 24px;
            border-radius: 10px;
            display: inline-block;
            margin: 0 auto;
        ">
            ¡Seguí a CAME en redes sociales!
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Columnas para centrar
col_izq, col_centro, colder = st.columns([0.7,1.8,0.5])
with col_izq :
    st.write("")

with col_centro:
    colFc, colIg, colTw, colLk, colYt = st.columns(5)
    with colFc:
        # URL de tu perfil de Instagram
        facebook_url = "https://www.facebook.com/redcame"
        # Cargar la imagen del logotipo de Instagram
        logo_image = "imgs/facebook.png"  # Reemplaza con la ruta de tu imagen
        # Mostrar el logotipo de Instagram
        st.image(logo_image, width=32)
        # Crear un enlace clickeable
        st.markdown(f"[Facebook]({facebook_url})", unsafe_allow_html=True)

    with colIg:
        # URL de tu perfil de Instagram
        instagram_url = "https://www.instagram.com/redcame/"
        # Cargar la imagen del logotipo de Instagram
        logo_image = "imgs/ig.png"  # Reemplaza con la ruta de tu imagen
        # Mostrar el logotipo de Instagram
        st.image(logo_image, width=32)
        # Crear un enlace clickeable
        st.markdown(f"[Instagram]({instagram_url})", unsafe_allow_html=True)

    with colTw:
        # URL de tu perfil de Instagram
        twiter_url = "https://twitter.com/redcame"
        # Cargar la imagen del logotipo de Instagram
        logo_image = "imgs/twiter.png"  # Reemplaza con la ruta de tu imagen
        # Mostrar el logotipo de Instagram
        st.image(logo_image, width=32)
        # Crear un enlace clickeable
        st.markdown(f"[Twitter]({twiter_url})", unsafe_allow_html=True)

    with colLk:
        # URL de tu perfil de Instagram
        linkedin_url = "https://ar.linkedin.com/company/redcame"
        # Cargar la imagen del logotipo de Instagram
        logo_image = "imgs/linkedin.png"  # Reemplaza con la ruta de tu imagen
        # Mostrar el logotipo de Instagram
        st.image(logo_image, width=32)
        # Crear un enlace clickeable
        st.markdown(f"[LinkedIn]({linkedin_url})", unsafe_allow_html=True) 

    with colYt:
        # URL de tu perfil de Instagram
        youtube_url = "https://www.youtube.com/c/CAMEar"
        # Cargar la imagen del logotipo de Instagram
        logo_image = "imgs/yutu.png"  # Reemplaza con la ruta de tu imagen
        # Mostrar el logotipo de Instagram
        st.image(logo_image, width = 40)
        # Crear un enlace clickeable
        st.markdown(f"[Youtube]({youtube_url})", unsafe_allow_html=True)               

with colder :
    st.write("")


# Agrega CSS personalizado para el marcador en la parte inferior
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        padding: 5px;
        text-align: left;
        font-size: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


