# -*- coding: utf-8 -*-
import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client

# 1) Configuración de página: debe ser la PRIMERA llamada de Streamlit
st.set_page_config(page_title="Ronda Hídrica - AMVA", layout="wide")  # debe ir primero
# Referencia sobre orden de st.set_page_config.  # docs: ver cita en el informe

# 2) Cargar credenciales y cliente Supabase
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Opcional: tu procesamiento de logos ---
import mejorar_imagenes as mi_funcion_1
img_logos = mi_funcion_1.process_image(
    "Logos_ronda.png", scale_factor=1.5, contrast=1.3, brightness=1.2, color=1.4, sharpness=2.0
)

# 3) Estructura del nuevo formulario (grupos y preguntas abiertas)
SECCIONES = [
    {
        "titulo": "Servicios ecosistémicos del río Medellín–Aburrá",
        "preguntas": [
            ("🌱 ¿Sabe usted qué es un servicio ecosistémico?", "q1_definicion_se"),
            ("🧩 ¿Cómo se clasifican/agrupan los servicios ecosistémicos?", "q2_clasificacion_se"),
            ("🔎 ¿Cuáles servicios ecosistémicos identifica en la ronda hídrica del río Medellín?", "q3_servicios_identificados"),
            ("📍 Si identifica algún servicio ecosistémico, podria indicar ¿en qué sitio o sector se puede acceder a ese servicio?", "q4_ubicacion_servicios"),
            ("👥 ¿Reconoce beneficiarios o segmentos poblacionales que acceden a dichos servicios?", "q5_beneficiarios"),
            ("📈 ¿Considera relevante establecer estrategias, programas, proyectos e intervenciones para para la conservación, potenciación y ampliación de dichos servicios ecosistémicos?", "q6_relevancia_estrategias"),
            ("📚 ¿Qué estrategias, programas, proyectos e intervenciones conoce que existan en los distintos ejercicios de planificación municipal y regional para la conservación, potenciación y ampliación de dichos servicios ecosistémicos?", "q7_conoce_instrumentos"),
            ("💡 ¿Qué nuevas estrategias, programas, proyectos e intervenciones sugiere que se deban adoptar para la conservación, potenciación y ampliación de dichos servicios ecosistémicos?", "q8_nuevas_estrategias"),
        ],
    },
    {
        "titulo": "Criterios para definir áreas con características similares",
        "preguntas": [
            ("💧 ¿Qué criterios sugiere para la definición de áreas con características similares desde la envolvente hidrológica?", "q9_criterios_hidrologia"),
            ("⛰️ ¿Qué criterios sugiere para la definición de áreas con características similares desde la envolvente geomorfológica?", "q10_criterios_geomorfologia"),
            ("🌿 ¿Qué criterios sugiere para la definición de áreas con características similares desde la envolvente ecosistémica?", "q11_criterios_ecosistema"),
            ("🏘️ ¿Qué criterios sugiere para la definición de áreas con características similares desde el ambito de ocupación de la ronda?", "q12_criterios_ocupacion"),
            ("🗺️ ¿Qué criterios sugiere para la definición de áreas con características similares desde el ambito de instrumento de planificación y desarrollo existentes en la ronda?", "q13_criterios_instrumentos"),
        ],
    },
    {
        "titulo": "Posibles medidas de manejo para áreas con características similares",
        "preguntas": [
            ("🛠️ ¿Qué estrategias de manejo (conservación, restauración y aprovechamiento sostenible) se podrian considerar para áreas con caracteristicas similares?", "q14_estrategias_manejo"),
            ("🧭 ¿Qué programas y proyectos se podrian asociar a las estrategias de manejo anteriormente sugeridas para áreas con caracteristicas similares?", "q15_programas_proyectos"),
            ("✅ ¿Qué mecanismos de evaluación y seguimiento sugiere para las estrategias, programas y proyectos sugeridos para el manejo de áreas con caracteristicas similares?", "q16_evaluacion_seguimiento"),
        ],
    },
]

def get_respuestas():
    return supabase.table("respuestas2").select("*").execute().data

def add_respuesta(info: dict):
    return supabase.table("respuestas2").insert(info).execute()

def main():
    # Encabezado
    st.image(img_logos, use_container_width=True)
    st.title("Acotamiento de la Ronda Hídrica del río Medellín-Aburrá en Jurisdicción del Área Metropolitana del Valle de Aburrá-AMVA")
    st.markdown(
        "El presente instrumento constituye un ejemplo de prueba para la participación de actores interesados en el ejercicio de definición y establecimiento de estrategias de manejo de la ronda hídrica del río Medellín."
        "Desde el equipo social, agradecemos su participación ayudando a responder los siguientes interrogantes, para la elaboración conjunta de las medidas de manejo:"
    )

    # Formulario
    with st.form("form_abierto"):
        st.subheader("👤 Datos del participante")
        nombre = st.text_input("Nombre completo*")
        ocupacion = st.text_input("Ocupación*")
        entidad = st.text_input("Entidad u organización*")
        municipio = st.text_input("Municipio de residencia o trabajo*")

        st.markdown("---")

        # Render de secciones y preguntas
        respuestas = {}
        for seccion in SECCIONES:
            st.markdown(f"### {seccion['titulo']}")
            for label, key in seccion["preguntas"]:
                respuestas[key] = st.text_area(
                    label,
                    key=key,
                    placeholder="Escriba aquí...",
                    height=120
                )
            st.markdown("---")

        submit = st.form_submit_button("Enviar respuestas")

    # Validación e inserción
    if submit:
        obligatorios = [nombre, ocupacion, entidad, municipio] + list(respuestas.values())
        if any((x is None) or (isinstance(x, str) and not x.strip()) for x in obligatorios):
            st.error("Complete todos los campos obligatorios.")
            return

        info = {
            "nombre": nombre.strip(),
            "ocupacion": ocupacion.strip(),
            "entidad": entidad.strip(),
            "municipio": municipio.strip(),
            **{k: v.strip() for k, v in respuestas.items()},
        }

        # Evita duplicados por persona (además del UNIQUE en SQL)
        ya = (
            supabase.table("respuestas2")
            .select("id")
            .eq("nombre", info["nombre"])
            .eq("ocupacion", info["ocupacion"])
            .eq("entidad", info["entidad"])
            .eq("municipio", info["municipio"])
            .execute()
        ).data

        if ya:
            st.error("Ya existe un registro para esta persona.")
            return

        try:
            add_respuesta(info)  # inserta en Postgres vía Supabase
            st.success("Respuestas guardadas correctamente.")
        except Exception as e:
            st.error(f"No se pudo guardar. Detalle: {e}")

if __name__ == "__main__":
    main()
