import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# ---cargando la api de supabase---
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def get_respuestas():
    res = supabase.table("respuestas").select("*").execute()
    return res.data

def add_respuesta(info):
    supabase.table("respuestas").insert(info).execute()
    
# ---mejorando la imagen---
import mejorar_imagenes as mi_funcion_1

# Procesar cada logo
img_logos = mi_funcion_1.process_image(
    "Logos.png",
    scale_factor=1.5,
    contrast=1.3,
    brightness=1.2,
    color=1.4,
    sharpness=2.0
)

# LISTA DE VARIABLES Y SUS CÓDIGOS INTERNOS (para los inputs y la BD)
variables = [
    (
        "🏚️ Índice de pobreza multidimensional (IPM)",
        "ipm",
        "❗ Recuerda dar enter para actualizar tu respuesta.",
        "Mide las privaciones simultáneas que enfrentan los hogares en educación, salud, empleo, vivienda y servicios."
    ),
    (
        "💰 Desempeño fiscal",
        "desempeño_fiscal",
        "❗ Recuerda dar enter para actualizar tu respuesta.",
        "Evalúa la capacidad de un municipio para gestionar eficazmente sus recursos públicos y cumplir con sus obligaciones financieras."
    ),
    (
        "👪 Ingreso promedio por hogar",
        "ingreso_hogar",
        "❗ Recuerda dar enter para actualizar tu respuesta.",
        "Valor medio de los ingresos mensuales de los hogares, incluyendo todas las fuentes de ingreso."  # basada en definición del INEGI :contentReference[oaicite:1]{index=1}
    ),
    (
        "📉 Tasa de desempleo",
        "desempleo",
        "❗ Recuerda dar enter para actualizar tu respuesta.",
        "Porcentaje de personas en edad de trabajar que buscan empleo y no lo consiguen."  # :contentReference[oaicite:2]{index=2}
    ),
    (
        "📈 Tasa de subempleo",
        "subempleo",
        "❗ Recuerda dar enter para actualizar tu respuesta.",
        "Proporción de trabajadores ocupados que desean y buscan mejorar sus condiciones laborales."  # :contentReference[oaicite:3]{index=3}
    ),
    (
        "🧒👵♿ Población con menor capacidad de respuesta",
        "menor_respuesta",
        "❗ Recuerda dar enter para actualizar tu respuesta.",
        "Personas más vulnerables ante emergencias: niños, adultos mayores, personas con discapacidad."  # descripción proporcionada
    ),
    (
        "🏛️ Apoyo institucional",
        "apoyo_inst",
        "❗ Recuerda dar enter para actualizar tu respuesta.",
        "Presencia y funcionamiento de entidades y planes municipales para la gestión del riesgo (bomberos, Cruz Roja, entre otros)."  # asumida de contexto institucional
    ),
    (
        "🤝 Número de organizaciones comunitarias",
        "num_org_comunitarias",
        "❗ Recuerda dar enter para actualizar tu respuesta.",
        "Cantidad de agrupaciones sociales en el municipio que reflejan el nivel de cohesión, participación ciudadana y capacidad de autogestión en diversos asuntos."  # :contentReference[oaicite:4]{index=4}
    ),
    (
        "🕊️ Territorio PDET",
        "territorio_pdet",
        "❗ Recuerda dar enter para actualizar tu respuesta.",
        "Municipios priorizados por el posconflicto debido a condiciones históricas de exclusión y pobreza estructural."  # :contentReference[oaicite:5]{index=5}
    ),
    (
        "🚿⚡🚽 Porcentaje de hogares sin servicios básicos",
        "hogares_sin_servicios",
        "❗ Recuerda dar enter para actualizar tu respuesta.",
        "Proporción de viviendas que carecen de energía, gas o recolección de residuos."  # :contentReference[oaicite:6]{index=6}
    ),
    (
        "🏙️ Densidad de viviendas",
        "densidad_viviendas",
        "❗ Recuerda dar enter para actualizar tu respuesta.",
        "Número de viviendas construidas por kilómetro cuadrado, muestra concentración de infraestructura habitacional."
    ),
    (
        "👥 Densidad poblacional",
        "densidad_poblacional",
        "❗ Recuerda dar enter para actualizar tu respuesta.",
        "Número de viviendas construidas por kilómetro cuadrado, indicador que permite conocer la concentración de infraestructura habitacional en el territorio."
    ),
    (
        "🛣️ Vías",
        "vias",
        "❗ Recuerda dar enter para actualizar tu respuesta.",
        "Condiciones de conectividad vial del municipio, claves para evacuación y atención en emergencias."
    ),
]

print("Variables definidas para el formulario.")

# FUNCIÓN PRINCIPAL: CREACIÓN DEL FORMULARIO
def main():
    """Formulario para determinar el Índice de Vulnerabilidad mediante técnica del Ábaco de Régnier."""

    # TÍTULO DEL FORMULARIO
    # 1) Configuro la página en ancho completo
    st.set_page_config(layout="wide")
    
    st.image(img_logos, use_container_width=True)

    # INSTRUCCIONES GENERALES
    st.title(
            """Ejercicio de priorización de variables por expertos como aporte a la construcción del Índice de Vulnerabilidad Socioeconómica ante inundaciones."""
            )
    st.markdown(
    """
    <p>
    <strong> Estimado(a) experto(a): </strong>
    </p>
    
    <p>
    En el marco del estudio de <strong> evaluación de la susceptibilidad, amenaza, vulnerabilidad y riesgo por inundaciones en el departamento de Antioquia </strong>, realizado por la Gobernación de Antioquia a través del DAGRAN y la Universidad Nacional de Colombia, le invitamos a participar como parte del panel de expertos que contribuirá a la priorización de variables para la construcción del <strong> Índice de Vulnerabilidad Socioeconómica ante inundaciones </strong>.
    </p>
    <p>
    Agradecemos pueda realizar el diligenciamiento del formulario en un plazo no mayor a <strong> los 3 días siguientes después de recibirlo </strong>.
    </p>
    <p>
    Usted encontrará un listado de 13 variables que requieren ser evaluadas según su <strong> nivel de importancia relativa </strong> dentro del análisis de vulnerabilidad:
    </p>
    
    <!--========== Estableciendo los Estilos CSS de la tabla ==========-->
    <style>
      /* Centrar la tabla en la página */
      table.center {
        margin-left: auto;
        margin-right: auto;
      }
      /* Encabezado: fondo negro y texto blanco */
      table.center thead th {
        background-color: #000000;
        color: #ffffff;
        text-align: center;
        padding: 10px;
        border: 2px solid #444;
      }
      /* Celdas de datos: fondo gris claro, texto centrado */
      table.center tbody td {
        text-align: center;
        padding: 8px;
        border: 1px solid #ccc;
      }
    </style>
    
    <!-- Aquí comienza la Tabla HTML con la clase center-->
    <table class="center" style="width:40%; border-collapse: collapse;">
      <thead>
        <tr>
          <th>Nombre de la variable</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>Índice de pobreza multidimensional (IPM)</td></tr>
        <tr><td>Desempeño fiscal</td></tr>
        <tr><td>Ingreso promedio por hogar</td></tr>
        <tr><td>Tasa de desempleo</td></tr>
        <tr><td>Tasa de subempleo</td></tr>
        <tr><td>Población con menor capacidad de respuesta</td></tr>
        <tr><td>Apoyo institucional</td></tr>
        <tr><td>Número de organizaciones comunitarias</td></tr>
        <tr><td>Territorio PDET</td></tr>
        <tr><td>Porcentaje de hogares sin servicios básicos</td></tr>
        <tr><td>Densidad de viviendas</td></tr>
        <tr><td>Densidad poblacional</td></tr>
        <tr><td>Vías</td></tr>
      </tbody>
    </table>
    """,unsafe_allow_html=True)
    

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
        columa_1, columna_2 = st.columns([2, 3], gap="small")
        def mostrar_aviso():
          st.markdown("### ✍ **Lineamientos para el diligenciamiento del formulario:**")
          st.markdown("""
          <style>
          .titulo-aviso {
              color: #e03131;
              font-size: 22px;
              font-weight: bold;
              margin-bottom: 6px;
              display: flex;
              align-items: center;
              gap: 8px;
          }
          .campo-obligatorio {
              color: #f59f00;
              font-size: 14px;
              margin-bottom: 2px;
              display: flex;
              align-items: center;
              gap: 7px;
          }
          .restriccion {
              color: #e8590c;
              font-size: 14px;
              margin-bottom: 4px;
              display: flex;
              align-items: center;
              gap: 7px;
          }
          .titulo-lista {
              margin-top: 12px;
              font-size: 15px;
              font-weight: 500;
              color: #dee2e6;
          }
          ul.lista-valores {
              margin-left: 10px;
              margin-top: 3px;
              margin-bottom: 10px;
              font-size: 14px;
          }
          li.alta { color: #e03131; font-weight: bold;}
          li.media { color: #f59f00; font-weight: bold;}
          li.baja { color: #228be6; font-weight: bold;}
          </style>

          <div class='titulo-aviso'>🚨 <span>Recuerda:</span></div>
          <div class='campo-obligatorio'>⚠️ Todos los campos son obligatorios.</div>
          <div class='restriccion'>⚠️ No puedes exceder los límites de asignación de valores.</div>
          <div class='titulo-lista'>Debes asignar exactamente:</div>
          <ul class='lista-valores'>
          <li class='alta'>🔴 4 variables con importancia Alta <span style='font-weight:normal;'>(valor = 3)</span></li>
          <li class='media'>🟡 5 variables con importancia Media <span style='font-weight:normal;'>(valor = 2)</span></li>
          <li class='baja'>🔵 4 variables con importancia Baja <span style='font-weight:normal;'>(valor = 1)</span></li>
          </ul>
          """, unsafe_allow_html=True)

        def lineamientos_formulario():
            st.markdown("""
            <style>
                .info-box {
                    background-color: #1e3a8a;
                    color: white;
                    border-radius: 8px;
                    padding: 15px;
                    margin-bottom: 20px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                }
                .info-box h3 {
                    color: #ffdd57;
                    margin-bottom: 12px;
                }
                .info-box ul {
                    margin-left: 15px;
                }
                .info-box li {
                    margin-bottom: 8px;
                }
                .info-box li span {
                    font-weight: bold;
                    color: #ffdd57;
                }
            </style>

            <div class="info-box">
                <h3>📌 Aspectos importantes para diligenciar el formulario:</h3>
                <ul>
                    <li>
                        Cada casilla para asignar la importancia de cada variable contiene información sobre la variable para facilitar su comprensión.
                    </li>
                    <li>
                        Por defecto, todas las variables tienen asignado el valor <span>1</span>. Para cambiarlo, puede:
                        <ul>
                            <li>Usar los botones <span>(+)</span> y <span>(-)</span> del recuadro.</li>
                            <li>Digitar directamente el valor deseado.</li>
                        </ul>
                    </li>
                    <li>
                        Para guardar y validar su respuesta:
                        <ul>
                            <li>Presione la tecla <span>Enter</span> después de ingresar el valor en cada casilla.</li>
                            <li>O haga clic en el botón <span>"Enviar respuestas"</span> al finalizar todo el formulario.</li>
                        </ul>
                    </li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        

        # 3. Llama a la función en ambas columnas
        with columa_1:
            mostrar_aviso()

        with columna_2:
            lineamientos_formulario()
        
        # INPUTS PARA LAS VARIABLES
        respuestas = []
        st.markdown("""
        <style>
        .variable-label {
        margin-bottom: -2px !important;
        }
        .variable-warning {
        color: #e03131;
        font-size: 12px;
        margin-top: 4px;
        margin-bottom: 2px;
        }
        .variable-note {
        margin-top: 0px !important;
        margin-bottom: 6px !important;
        font-size: 14px;
        color: gray;
        }
        div[data-testid="stNumberInput"] {
        margin-top: -2px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        for var, code, warning, contexto in variables:
            # Label en negrita
            st.markdown("---")
            st.markdown(f"<div class='variable-label'><b>{var}</b></div>", unsafe_allow_html=True)
            # Contexto en gris (misma clase que antes)
            st.markdown(f"<div class='variable-note'>{contexto}</div>", unsafe_allow_html=True)
            # 🚨 warning en rojo
            st.markdown(f"<div class='variable-warning'>{warning}</div>", unsafe_allow_html=True)
            # Input numérico
            valor = st.number_input(
                label="",
                min_value=1, max_value=3, step=1, key=code,
                help="Usa: 3 (máx 4 veces), 2 (máx 5 veces), 1 (máx 4 veces)"
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
            for (var, code, _, _), val in zip(variables, respuestas):
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
