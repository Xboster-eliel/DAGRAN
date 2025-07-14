import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

def get_respuestas():
    res = supabase.table("respuestas").select("*").execute()
    return res.data

def add_respuesta(info):
    supabase.table("respuestas").insert(info).execute()

# LISTA DE VARIABLES Y SUS CÓDIGOS INTERNOS (para los inputs y la BD)
variables = [
    ("Índice de pobreza multidimensional (IPM)", "ipm", "🚨 Recuerda dar enter para actualizar tu respuesta"),
    ("Desempeño fiscal", "desempeño_fiscal", "🚨 Recuerda dar enter para actualizar tu respuesta"),
    ("Ingreso promedio por hogar", "ingreso_hogar", "🚨 Recuerda dar enter para actualizar tu respuesta"),
    ("Tasa de desempleo", "desempleo", "🚨 Recuerda dar enter para actualizar tu respuesta"),
    ("Tasa de subempleo", "subempleo", "🚨 Recuerda dar enter para actualizar tu respuesta"),
    ("Población con menor capacidad de respuesta", "menor_respuesta", "🚨 Recuerda dar enter para actualizar tu respuesta"),
    ("Apoyo institucional", "apoyo_inst", "🚨 Recuerda dar enter para actualizar tu respuesta"),
    ("Número de organizaciones comunitarias", "num_org_comunitarias", "🚨 Recuerda dar enter para actualizar tu respuesta"),
    ("Territorio PDET", "territorio_pdet", "🚨 Recuerda dar enter para actualizar tu respuesta"),
    ("Porcentaje de hogares sin servicios básicos", "hogares_sin_servicios", "🚨 Recuerda dar enter para actualizar tu respuesta"),
    ("Densidad de viviendas", "densidad_viviendas", "🚨 Recuerda dar enter para actualizar tu respuesta"),
    ("Densidad poblacional", "densidad_poblacional", "🚨 Recuerda dar enter para actualizar tu respuesta"),
    ("Vías", "vias", "🚨 Recuerda dar enter para actualizar tu respuesta") 
]
print("Variables definidas para el formulario.")

# FUNCIÓN PRINCIPAL: CREACIÓN DEL FORMULARIO
def main():
    """Formulario para determinar el Índice de Vulnerabilidad mediante técnica del Ábaco de Régnier."""

    # TÍTULO DEL FORMULARIO
    st.title("📊 Formulario de Priorización de Variables")
    st.subheader("Grupo Hidraulica Fluvial")
    st.image("LOGO.jpg", width=120)

    # INSTRUCCIONES GENERALES
    st.markdown("""
    ## 📋 **Instrucciones para el Formulario:**

    ✅ Debes asignar exactamente:
    - 🔴 **4 variables con importancia Alta (valor = 3)**
    - 🟡 **5 variables con importancia Media (valor = 2)**
    - 🔵 **4 variables con importancia Baja (valor = 1)**
    
    ⚠️ **Importante:**
    - Todos los campos son obligatorios.
    - No puedes exceder los límites de asignación de valores.


    """)

    # AGRUPACIÓN DEL FORMULARIO
    with st.form("formulario_variables"):

        # DATOS CONTEXTUALES
        st.markdown("### 👤 **Información del participante:** Completa tus datos claramente.")
        nombre = st.text_input("Nombre completo")
        ocupacion = st.text_input("Ocupación")
        entidad = st.text_input("Entidad u organización")
        municipio = st.text_input("Municipio de residencia o trabajo")

        # DIVISIÓN ENTRE SECCIONES
        st.markdown("---")
        st.markdown("### Evaluación de Variables")
        st.markdown("🚨 Recuerda asignar un valor a cada variable según su importancia:")
        st.write("- **1**: (🟥 Alta Importancia)<br><span style='color:gray; font-size:12px;'>(max 4 veces)</span>", unsafe_allow_html=True)
        st.write("- **2**: (🟨 Importancia Media)<br><span style='color:gray; font-size:12px;'>(max 5 veces)</span>", unsafe_allow_html=True)
        st.write("- **3**: (🟦 Baja Importancia)<br><span style='color:gray; font-size:12px;'>(max 4 veces)</span>", unsafe_allow_html=True)

        # INPUTS PARA LAS VARIABLES
        respuestas = []
        st.markdown("""
            <style>
            /* Reduce el margen inferior de los títulos y notas */
            .variable-label { margin-bottom: -2px !important; }
            .variable-note { margin-top: 0px !important; margin-bottom: 6px !important; font-size:12px; color: gray;}
            /* Opcional: achica el espacio arriba del input numérico */
            div[data-testid="stNumberInput"] { margin-top: -2px !important; }
            </style>
        """, unsafe_allow_html=True)

        for var, code, nota in variables:
            st.markdown(f"<div class='variable-label'><b>{var}</b></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='variable-note'>{nota}</div>", unsafe_allow_html=True)
            valor = st.number_input(
                label="",  # Deja el label vacío
                min_value=1, max_value=3, step=1, key=code,
                help="Usa: 3 (maximo 4 veces), 2 (maximo 5 veces), 1 (maximo 4 veces)"
            )
            respuestas.append(valor)
            
            # VALIDACIÓN EN TIEMPO REAL
            if valor == 3 and respuestas.count(3) > 4:
                st.warning(f"🔴 Máximo alcanzado: solo 4 variables pueden tener importancia Alta (valor = 3).")
            if valor == 2 and respuestas.count(2) > 5:
                st.warning(f"🟡 Máximo alcanzado: solo 5 variables pueden tener importancia Media (valor = 2).")
            if valor == 1 and respuestas.count(1) > 4:
                st.warning(f"🔵 Máximo alcanzado: solo 4 variables pueden tener importancia Baja (valor = 1).")
                
        submit = st.form_submit_button("Enviar respuestas")


    if submit:
        n3 = respuestas.count(3); n2 = respuestas.count(2); n1 = respuestas.count(1)
        if not (nombre and ocupacion and entidad and municipio):
            st.error("❌ Completa los datos personales.")
        elif n3 != 4 or n2 != 5 or n1 != 4:
            st.error("❌ Distribución incorrecta:  Asegúrate de cumplir los límites exactos (4 veces 1 | 5 veces 2 | 4 veces 3)")
        else:
            info = { "nombre": nombre, "ocupacion": ocupacion,
                     "entidad": entidad, "municipio": municipio }
            for (var, code, _), val in zip(variables, respuestas):
                info[code] = val
            existentes = supabase.table("respuestas")\
                .select("nombre").eq("nombre", nombre)\
                .eq("ocupacion", ocupacion)\
                .eq("entidad", entidad)\
                .eq("municipio", municipio)\
                .execute().data
            if existentes:
                st.error("Ya has enviado el formulario anteriormente. Solo se permite un registro por persona.")
            else:
                supabase.table("respuestas").insert(info).execute()
                st.success("✅ ¡Formulario enviado exitosamente! Tus respuestas se guardaron correctamente.")

        st.write("## Registros existentes")
        for fila in supabase.table("respuestas").select("*").execute().data or []:
            st.write(f"- {fila['nombre']} ({fila['municipio']})")

if __name__ == "__main__":
    main()
