import streamlit as st

st.title("🧠 Asesor Financiero Virtual - Demo")

# Sección de brokers
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

    # Recomendaciones detalladas por perfil
    if score <= 1:
        perfil = "Conservador"
        recomendacion = (
            "70% en bonos de gobiernos europeos AAA (ej. bonos alemanes a 10 años), "
            "20% en ETFs de renta fija como iShares Euro Government Bond 1-3yr (bajo riesgo y baja comisión), "
            "10% en efectivo para liquidez inmediata. Considera evitar mercados emergentes o criptoactivos por ahora."
        )
    elif score == 2:
        perfil = "Moderado"
        recomendacion = (
            "50% en bonos grado de inversión (por ejemplo, bonos corporativos europeos), "
            "30% en ETFs globales como Vanguard FTSE All-World o iShares MSCI World (diversificación global y baja comisión), "
            "10% en renta variable de grandes empresas como Nestlé, Apple, Microsoft, y 10% en oro o commodities para protección."
        )
    else:
        perfil = "Agresivo"
        recomendacion = (
            "30% en renta fija (bonos high yield o bonos emergentes como los de India o Brasil), "
            "30% en ETFs de alto rendimiento como ARK Innovation o QQQ, "
            "20% en acciones individuales de crecimiento como Nvidia, Tesla, MercadoLibre, Adyen y ASML, "
            "10% en criptoactivos líderes (BTC, ETH), "
            "10% en Private Equity o REITs internacionales para diversificación adicional."
        )

    st.success(f"🎯 Tu perfil es: **{perfil}**")
    st.info(f"📊 Recomendación sugerida: {recomendacion}")

    feedback = st.radio("¿Te ha sido útil esta recomendación?", ["Sí", "No", "Parcialmente"])
