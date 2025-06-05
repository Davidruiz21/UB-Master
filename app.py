import streamlit as st
import matplotlib.pyplot as plt

# Inicializar estados
if "pagina" not in st.session_state:
    st.session_state.pagina = "consentimiento"
if "contador" not in st.session_state:
    st.session_state.contador = 0

# Función para calcular el perfil
def calcular_perfil(edad, ingresos, riesgo, horizonte):
    score = 0

    # Edad
    if edad < 30:
        score += 2
    elif edad < 50:
        score += 1

    # Ingresos
    if ingresos == "<1000":
        score += 0
    elif ingresos == "1000-3000":
        score += 1
    elif ingresos == "3000-6000":
        score += 2
    else:
        score += 3

    # Riesgo
    if riesgo == "Bajo":
        score += 0
    elif riesgo == "Medio":
        score += 2
    else:
        score += 4

    # Horizonte temporal
    if horizonte < 3:
        score += 0
    elif horizonte < 10:
        score += 2
    else:
        score += 4

    # Clasificación
    if score <= 5:
        return "Conservador"
    elif score <= 10:
        return "Moderado"
    else:
        return "Agresivo"

# Función para mostrar recomendación
def generar_recomendacion(perfil):
    st.subheader("📊 Recomendación de inversión:")

    if perfil == "Conservador":
        asignacion = {"Bonos": 70, "Acciones": 20, "Liquidez": 10}
    elif perfil == "Moderado":
        asignacion = {"Bonos": 40, "Acciones": 50, "Liquidez": 10}
    else:
        asignacion = {"Bonos": 20, "Acciones": 75, "Liquidez": 5}

    # Mostrar texto
    st.write(f"Perfil detectado: **{perfil}**")
    st.write("Asignación recomendada:")
    for k, v in asignacion.items():
        st.write(f"- {k}: {v}%")

    # Mostrar gráfico
    fig, ax = plt.subplots()
    ax.pie(asignacion.values(), labels=asignacion.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    # Enlaces útiles
    st.markdown("🔗 Puedes explorar plataformas como [Indexa Capital](https://indexacapital.com), [MyInvestor](https://myinvestor.es) o [Raisin](https://www.raisin.es/) para empezar.")

# PÁGINA DE CONSENTIMIENTO
if st.session_state.pagina == "consentimiento":
    st.title("Asesor Financiero Virtual")
    st.markdown("Esta herramienta educativa te dará una recomendación de inversión personalizada en función de tu perfil.")
    st.info("❗ Esta aplicación no almacena datos y no sustituye asesoría financiera profesional.")
    
    consentimiento = st.checkbox("He leído y acepto el tratamiento temporal y anónimo de mis datos.")
    
    if consentimiento:
        if st.button("Continuar"):
            st.session_state.pagina = "formulario"
    else:
        st.warning("Debes aceptar el consentimiento para continuar.")

# PÁGINA DEL FORMULARIO Y RESULTADO
elif st.session_state.pagina == "formulario":
    st.header("📝 Cuestionario de perfil financiero")

    edad = st.number_input("¿Cuál es tu edad?", min_value=18, max_value=100, step=1)
    ingresos = st.selectbox("¿Cuál es tu nivel de ingresos mensuales?", options=["<1000", "1000-3000", "3000-6000", ">6000"])
    riesgo = st.selectbox("¿Qué nivel de riesgo estás dispuesto/a a asumir?", options=["Bajo", "Medio", "Alto"])
    horizonte = st.slider("¿Cuántos años piensas mantener tu inversión?", min_value=1, max_value=30, value=5)

    if st.button("Obtener recomendación"):
        perfil = calcular_perfil(edad, ingresos, riesgo, horizonte)
        generar_recomendacion(perfil)

        st.session_state.contador += 1
        st.success(f"Esta herramienta ha sido usada {st.session_state.contador} veces en esta sesión.")

        utilidad = st.radio("¿Te ha sido útil esta recomendación?", ["Sí", "No"])
        if utilidad == "Sí":
            st.balloons()
        else:
            st.write("Gracias por tu retroalimentación. Seguiremos mejorando.")

    # Botón de reinicio opcional
    if st.button("Volver al inicio"):
        st.session_state.pagina = "consentimiento"
