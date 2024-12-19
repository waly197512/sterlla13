import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import os

# DEBE SER EL PRIMER COMANDO DE STREAMLIT
st.set_page_config(page_title="Tu compañia perfecta", layout="wide")

# Estilos personalizados integrados en el archivo
def load_custom_css():
    st.markdown("""
    <style>
    body {
        background: linear-gradient(to bottom, #E0FFFF, #B0E0E6);
        position: relative;
        overflow: hidden;
    }

    body::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 5px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 3px),
            radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 4px);
        background-size: 550px 550px, 350px 350px, 250px 250px;
        background-position: 0 0, 40px 60px, 130px 270px;
        z-index: -1;
    }

    .title {
        text-align: center;
        color: #333333;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    .stApp {
        background: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

# Aplicar estilos personalizados
load_custom_css()

try:
    # 1. DEFINICIÓN DEL DATASET (Tipos de mascotas + lemas)
    data = {
        'mascota': ['Perro', 'Perro', 'Gato', 'Gato', 'Ave', 'Ave', 'Roedor', 'Roedor', 'Otro', 'Otro'],
        'tipo': ['친절한 (Amigable)', '활동적인 (Activo)', '우아한 (Elegante)', '독립적인 (Independiente)', 
                '쾌활한 (Alegre)', '노래하는 (Cantor)', '귀여운 (Adorable)', '호기심 많은 (Curioso)', 
                '이국적인 (Exótico)', '조용한 (Tranquilo)'],
        'horario': ['Diurno', 'Nocturno', 'Diurno', 'Nocturno', 'Diurno', 'Diurno', 'Nocturno', 'Nocturno', 'Diurno', 'Diurno'],
        'actividad': ['Alta', 'Muy Alta', 'Baja', 'Media', 'Alta', 'Media', 'Baja', 'Media', 'Baja', 'Baja'],
        'ambiente': ['Exterior', 'Exterior', 'Interior', 'Interior', 'Exterior', 'Interior', 'Interior', 'Interior', 'Exterior', 'Interior'],
        'ruido': ['Alto', 'Medio', 'Bajo', 'Bajo', 'Alto', 'Alto', 'Bajo', 'Medio', 'Bajo', 'Bajo'],
        'companero': ['Sí', 'Sí', 'No', 'Sí', 'Sí', 'No', 'Sí', 'No', 'No', 'No'],
        'lema': [
            "Siempre a tu lado,\ncon amor incondicional,\nladridos de sol.",
            "Energía pura,\ncorre sin mirar atrás,\nun salto al futuro.",
            "Garras en silencio,\nelegancia y mirada,\nbelleza que cuida.",
            "Libre y sereno,\nla noche es su refugio,\nsus ojos te miran.",
            "El viento le canta,\nvuelos de alegría viva,\nluz en cada ala.",
            "Notas que resuenan,\nun canto en la mañana,\nes tu despertar.",
            "Pequeño y leal,\nun corazón que palpita,\nmirada que ama.",
            "Curiosidad fiel,\nun viaje de aventuras,\nsilencio y amor.",
            "El mundo es su hogar,\nexótico y misterioso,\nsu calma te abraza.",
            "Quieto en la brisa,\nel silencio es su fuerza,\ncompañero fiel."
        ],
        'imagen': [
            "https://www.infobae.com/resizer/v2/74NIPN7HBZAZLDYZ2NGDSNNNCU.jpg?auth=235f72d1047a3c0d8040da192cbde3d85403c2ab391d4684af36239dcf6e70c9",
            "https://www.infobae.com/resizer/v2/74NIPN7HBZAZLDYZ2NGDSNNNCU.jpg?auth=235f72d1047a3c0d8040da192cbde3d85403c2ab391d4684af36239dcf6e70c9",
            "https://www.infobae.com/resizer/v2/74NIPN7HBZAZLDYZ2NGDSNNNCU.jpg?auth=235f72d1047a3c0d8040da192cbde3d85403c2ab391d4684af36239dcf6e70c9",
            "https://www.infobae.com/resizer/v2/74NIPN7HBZAZLDYZ2NGDSNNNCU.jpg?auth=235f72d1047a3c0d8040da192cbde3d85403c2ab391d4684af36239dcf6e70c9",
            "https://www.infobae.com/resizer/v2/74NIPN7HBZAZLDYZ2NGDSNNNCU.jpg?auth=235f72d1047a3c0d8040da192cbde3d85403c2ab391d4684af36239dcf6e70c9",
            "https://www.infobae.com/resizer/v2/74NIPN7HBZAZLDYZ2NGDSNNNCU.jpg?auth=235f72d1047a3c0d8040da192cbde3d85403c2ab391d4684af36239dcf6e70c9",
            "https://www.infobae.com/resizer/v2/74NIPN7HBZAZLDYZ2NGDSNNNCU.jpg?auth=235f72d1047a3c0d8040da192cbde3d85403c2ab391d4684af36239dcf6e70c9",
            "https://www.infobae.com/resizer/v2/74NIPN7HBZAZLDYZ2NGDSNNNCU.jpg?auth=235f72d1047a3c0d8040da192cbde3d85403c2ab391d4684af36239dcf6e70c9",
            "https://www.infobae.com/resizer/v2/74NIPN7HBZAZLDYZ2NGDSNNNCU.jpg?auth=235f72d1047a3c0d8040da192cbde3d85403c2ab391d4684af36239dcf6e70c9",
            "https://www.infobae.com/resizer/v2/74NIPN7HBZAZLDYZ2NGDSNNNCU.jpg?auth=235f72d1047a3c0d8040da192cbde3d85403c2ab391d4684af36239dcf6e70c9"
        ]
    }
    df = pd.DataFrame(data)

    # 2. ENCABEZADO CON IMAGEN
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h1 class='title'>Tu compañía perfecta. '동반자 (Dongbanja)'</h1>", unsafe_allow_html=True)
    with col2:
        st.image("https://www.infobae.com/resizer/v2/74NIPN7HBZAZLDYZ2NGDSNNNCU.jpg?auth=235f72d1047a3c0d8040da192cbde3d85403c2ab391d4684af36239dcf6e70c9", width=120)

    # 3. FORMULARIO DE ENTRADA
    st.sidebar.header("Responde el cuestionario:")
    horario = st.sidebar.selectbox("¿Tu horario es principalmente?", ['Diurno', 'Nocturno'])
    actividad = st.sidebar.selectbox("Tu nivel de actividad es:", ['Baja', 'Media', 'Alta', 'Muy Alta'])
    ambiente = st.sidebar.selectbox("Prefieres ambientes:", ['Interior', 'Exterior'])
    ruido = st.sidebar.selectbox("¿Toleras niveles de ruido?", ['Bajo', 'Medio', 'Alto'])
    companero = st.sidebar.selectbox("¿Buscas un compañero cercano?", ['Sí', 'No'])

    # 4. PROCESAR RESPUESTAS Y CALCULAR SIMILITUD
    if st.sidebar.button("Descubrir mi mascota ideal"):
        try:
            # Codificar las respuestas del usuario
            usuario_respuestas = {
                'horario': horario,
                'actividad': actividad,
                'ambiente': ambiente,
                'ruido': ruido,
                'companero': companero
            }
            encoder = OneHotEncoder(sparse=False)
            df_encoded = pd.DataFrame(encoder.fit_transform(df[['horario', 'actividad', 'ambiente', 'ruido', 'companero']]))
            usuario_encoded = encoder.transform([[usuario_respuestas['horario'], 
                                            usuario_respuestas['actividad'], 
                                            usuario_respuestas['ambiente'], 
                                            usuario_respuestas['ruido'], 
                                            usuario_respuestas['companero']]])

            # Calcular similitud
            similaridades = np.dot(df_encoded, usuario_encoded.T)
            df['Similitud'] = similaridades
            mascota_recomendada = df.sort_values(by='Similitud', ascending=False).iloc[0]

            # 5. MOSTRAR RESULTADO
            st.subheader("🐾 Tu mascota ideal es:")
            st.markdown(f"### **{mascota_recomendada['mascota']}** ({mascota_recomendada['tipo']})")
            st.write("✨ Lema especial:")
            st.markdown(f"_{mascota_recomendada['lema']}_")
            
            # Mostrar imagen de la mascota recomendada
            st.image(mascota_recomendada['imagen'], 
                    caption=f"{mascota_recomendada['mascota']} - {mascota_recomendada['tipo']}", 
                    use_column_width=True)

        except Exception as e:
            st.error(f"Error en el cálculo: {str(e)}")
            
except Exception as e:
    st.error(f"Error en la aplicación: {str(e)}")