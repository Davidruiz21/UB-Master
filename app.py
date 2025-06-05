import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Asesor Financiero Virtual", layout="centered")

st.title("🧠 Asesor Financiero Virtual")
st.markdown("Bienvenido a tu asesor personalizado. Esta herramienta te ayudará a evaluar tu diversificación actual y te propondrá una estrategia profesional para redistribuir tu patrimonio.")

# Consentimiento
if not st.session_state.get("consent_given", False):
    consent = st.checkbox("Acepto que mis datos sean usados de forma anónima y temporal")
    if consent:
        st.session_state["consent_given"] = True
    else:
        st.stop()

st.header("1. Tu situación actual")
efectivo = st.number_input("¿Cuánto tienes en efectivo o cuentas bancarias (€)?", min_value=0)
inmuebles = st.number_input("¿Valor estimado de tus inmuebles (€)?", min_value=0)
vehiculos = st.number_input("¿Valor estimado de tus vehículos (€)?", min_value=0)
bolsa = st.number_input("¿Cuánto tienes invertido en bolsa u otros productos financieros (€)?", min_value=0)
otros = st.number_input("¿Cuánto tienes en otros activos (cripto, arte, negocios, etc.) (€)?", min_value=0)

st.header("2. Perfil financiero")
edad = st.slider("Edad", 18, 100, 30)
ingresos = st.number_input("Ingresos mensuales (€)", min_value=0)
riesgo = st.selectbox("Nivel de tolerancia al riesgo", ["Bajo", "Medio", "Alto"])
horizonte = st.slider("¿Por cuántos años planeas mantener esta inversión?", 1, 30, 10)

# Cálculo de patrimonio total
patrimonio_total = efectivo + inmuebles + vehiculos + bolsa + otros

if patrimonio_total == 0:
    st.warning("Por favor, ingresa al menos un valor para calcular tu patrimonio.")
    st.stop()

st.subheader("🔎 Diagnóstico de diversificación actual")

comentarios = []
if inmuebles / patrimonio_total > 0.6:
    comentarios.append("Tienes una alta concentración en inmuebles. Considera diversificar hacia activos más líquidos.")
if vehiculos / patrimonio_total > 0.3:
    comentarios.append("Tienes una proporción alta en vehículos, los cuales se deprecian con el tiempo.")
if bolsa / patrimonio_total < 0.1:
    comentarios.append("Tienes poca exposición a activos financieros con potencial de crecimiento.")

if not comentarios:
    st.success("Tu portafolio muestra una buena diversificación inicial.")
else:
    for c in comentarios:
        st.warning(c)

st.header("3. Recomendación de distribución")

# Reglas por perfil
if riesgo == "Bajo":
    distribucion = {
        "Renta fija": 0.50,
        "Renta variable": 0.15,
        "Real estate": 0.15,
        "Liquidez": 0.15,
        "Alternativos": 0.05
    }
elif riesgo == "Medio":
    distribucion = {
        "Renta fija": 0.30,
        "Renta variable": 0.30,
        "Real estate": 0.15,
        "Liquidez": 0.10,
        "Alternativos": 0.10,
        "Cripto": 0.05
    }
else:  # Alto
    distribucion = {
        "Renta fija": 0.15,
        "Renta variable": 0.40,
        "Real estate": 0.10,
        "Liquidez": 0.05,
        "Alternativos": 0.15,
        "Cripto": 0.15
    }

labels = list(distribucion.keys())
percentages = [v for v in distribucion.values()]
amounts = [v * patrimonio_total for v in distribucion.values()]

# Mostrar tabla de recomendación
st.subheader("💼 Asignación recomendada:")
for i in range(len(labels)):
    st.markdown(f"- **{labels[i]}**: {percentages[i]*100:.0f}% → {amounts[i]:,.2f} €")

# Gráfico
fig, ax = plt.subplots()
ax.pie(percentages, labels=labels, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

st.info("Esta recomendación es orientativa y educativa. Para decisiones reales, consulta con un asesor financiero certificado.")

