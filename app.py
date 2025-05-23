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

    # Clasificación
    if score <= 1:
        perfil = "Conservador"
        recomendacion = "70% renta fija, 20% ETFs de bajo riesgo, 10% efectivo"
    elif score == 2:
        perfil = "Moderado"
        recomendacion = "50% renta fija, 30% ETFs diversificados, 20% renta variable"
    else:
        perfil = "Agresivo"
        recomendacion = "30% renta fija, 40% ETFs, 30% renta variable global"

    st.success(f"🎯 Tu perfil es: **{perfil}**")
    st.info(f"📊 Recomendación sugerida: {recomendacion}")

    feedback = st.radio("¿Te ha sido útil esta recomendación?", ["Sí", "No", "Parcialmente"])
