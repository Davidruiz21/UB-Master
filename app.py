import streamlit as st

st.set_page_config(page_title="Asesor Financiero Virtual", page_icon="🧠")

st.title("🧠 Asesor Financiero Virtual - Demo")

# Pantalla de consentimiento previo
st.markdown("### 🔒 Consentimiento informado")
st.markdown("""
Antes de continuar, por favor acepta el siguiente aviso:

> Esta herramienta es una demo de asesoramiento financiero automatizado. Toda la información que proporciones será procesada de forma **local y temporal**, sin ser almacenada ni vinculada a tu identidad. No se realiza ningún tipo de trazabilidad posterior ni análisis de comportamiento personal. Tu privacidad está completamente protegida.

Para continuar, debes autorizar el tratamiento temporal y anónimo de los datos ingresados.
""")

consentimiento = st.checkbox("Autorizo el tratamiento temporal y anónimo de los datos ingresados.")

if consentimiento:
    if st.button("Continuar al asesor financiero"):
        st.session_state.autorizado = True

# Mostrar encuesta solo si ya aceptó el consentimiento
if st.session_state.get("autorizado", False):

    st.markdown("### 🔗 Brokers recomendados para empezar a invertir")
    brokers = {
        "Degiro": "https://www.degiro.es",
        "eToro": "https://www.etoro.com",
        "Interactive Brokers": "https://www.interactivebrokers.com",
        "Revolut": "https://www.revolut.com",
        "Trade Republic": "https://traderepublic.com"
    }

    for nombre, url in brokers.items():
        st.markdown(f"- [{nombre}]({url})", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("Responde estas preguntas para obtener una recomendación de inversión personalizada.")

    # Entradas del usuario
    edad = st.number_input("¿Cuál es tu edad?", min_value=18, max_value=100)
    ingresos = st.selectbox("¿Cuál es tu nivel de ingresos mensuales?",
                            ["< 1000€", "1000€ - 3000€", "3000€ - 6000€", "> 6000€"])
    riesgo = st.radio("¿Qué tan cómodo/a te sientes asumiendo riesgos en tus inversiones?",
                      ["Nada cómodo", "Algo cómodo", "Muy cómodo"])
    horizonte = st.slider("¿En cuántos años esperas usar este dinero?", 1, 30, 5)

    if st.button("Obtener recomendación"):
        # Lógica de perfilamiento simple
        score = 0
        if ingresos in ["3000€ - 6000€", "> 6000€"]: score += 1
        if riesgo == "Muy cómodo": score += 2
        elif riesgo == "Algo cómodo": score += 1
        if horizonte >= 10: score += 1

        # Recomendaciones detalladas según perfil
        if score <= 1:
            perfil = "Conservador"
            recomendacion = """
            - **70% renta fija:** bonos del Estado de países desarrollados (ej. Bunds alemanes, bonos del Tesoro de EE. UU.).
            - **20% ETFs de bajo riesgo:** como iShares Core Global Aggregate Bond (AGGG) o Vanguard Total Bond Market (BND).
            - **10% efectivo o cuentas remuneradas.**
            - **Asesor sugerido:** Consultar con un planificador financiero con certificación CFP® o EFPA.
            """
        elif score == 2:
            perfil = "Moderado"
            recomendacion = """
            - **50% renta fija:** incluir bonos corporativos de grado de inversión.
            - **30% ETFs diversificados:** como Vanguard FTSE All-World (VWRL) o iShares MSCI World.
            - **20% renta variable:** acciones estables como Nestlé, Johnson & Johnson, Unilever.
            - **Exposición sugerida:** 70% en países desarrollados (EE.UU., Europa) y 30% en emergentes (India, Brasil).
            - **Asesor sugerido:** Profesional con certificación EFPA o CFA.
            """
        else:
            perfil = "Agresivo"
            recomendacion = """
            - **30% renta fija:** bonos de alto rendimiento (high yield).
            - **40% ETFs globales:** ARK Innovation ETF (ARKK), SPDR MSCI ACWI.
            - **30% renta variable:** acciones como Nvidia, Tesla, MercadoLibre, Sea Ltd, ASML.
            - **Otros activos:** exposición a criptoactivos (BTC, ETH), commodities (oro, litio) y fondos de private equity si están disponibles.
            - **Exposición sugerida:** balance entre EE. UU., Europa, Asia y LATAM.
            - **Asesor sugerido:** CFA Charterholder o asesor certificado FINRA Series 7/63 si se opera en EE. UU.
            """

        st.success(f"🎯 Tu perfil es: **{perfil}**")
        st.markdown("📊 **Recomendación sugerida:**")
        st.markdown(recomendacion)

        feedback = st.radio("¿Te ha sido útil esta recomendación?", ["Sí", "No", "Parcialmente"])

        # Mensaje de privacidad
        st.markdown("---")
        st.markdown("🔐 **Privacidad y seguridad de tus datos**")
        st.markdown("Esta interacción es completamente anónima y no se guarda ningún dato ingresado. No existe trazabilidad posterior ni almacenamiento de información personal, lo que reduce significativamente los riesgos asociados al manejo de datos sensibles.")
