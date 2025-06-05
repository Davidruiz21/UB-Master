import streamlit as st
import matplotlib.pyplot as plt
import time

# Inicializar tiempo de inicio y paso
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = time.time()

if 'step' not in st.session_state:
    st.session_state['step'] = 0

# Función para mostrar progreso
def update_progress():
    progress = int((st.session_state['step'] / 8) * 100)
    st.progress(progress)

st.title("Asesor Financiero Virtual")
st.write("Bienvenido. Esta herramienta te ayudará a comprender cómo diversificar tu patrimonio.")

# Paso 1: Consentimiento
st.session_state['step'] = 1
update_progress()
if not st.checkbox("Acepto que esta herramienta es solo educativa y no constituye asesoramiento financiero profesional."):
    st.stop()

# Paso 2: Patrimonio
st.session_state['step'] = 2
update_progress()
efectivo = st.number_input("Efectivo (€)", min_value=0)
inmuebles = st.number_input("Inmuebles (€)", min_value=0)
vehiculos = st.number_input("Vehículos (€)", min_value=0)
bolsa = st.number_input("Bolsa (€)", min_value=0)
otros = st.number_input("Otros activos (€)", min_value=0)

# Paso 3: Perfil personal
st.session_state['step'] = 3
update_progress()
edad = st.number_input("Edad", min_value=18, max_value=100)
ingresos = st.number_input("Ingresos mensuales (€)", min_value=0)
riesgo = st.selectbox("Nivel de riesgo", ["Conservador", "Moderado", "Agresivo"])
horizonte = st.selectbox("Horizonte temporal de inversión", ["Corto plazo", "Medio plazo", "Largo plazo"])

# Paso 4: Calcular patrimonio
st.session_state['step'] = 4
update_progress()
patrimonio_total = efectivo + inmuebles + vehiculos + bolsa + otros
st.write(f"Tu patrimonio neto total es de: €{patrimonio_total:,.2f}")

# Paso 5: Evaluación de diversificación
st.session_state['step'] = 5
update_progress()
if inmuebles > 0.6 * patrimonio_total:
    st.warning("Estás muy expuesto al sector inmobiliario. Considera diversificar más tus inversiones.")

# Paso 6: Recomendación
st.session_state['step'] = 6
update_progress()

def asignar_porcentaje(riesgo, horizonte):
    if riesgo == "Conservador":
        return [10, 50, 30, 0, 5, 5, 0]
    elif riesgo == "Moderado":
        return [20, 35, 20, 5, 10, 5, 5]
    else:  # Agresivo
        return [35, 20, 10, 10, 10, 10, 5]

etiquetas = ["Acciones", "Bonos", "Liquidez", "Cripto", "Commodities", "Inversiones alternativas", "ETFs temáticos"]
porcentajes = asignar_porcentaje(riesgo, horizonte)
valores = [round((p/100) * patrimonio_total, 2) for p in porcentajes]

# Mostrar gráfico
fig, ax = plt.subplots()
ax.pie(porcentajes, labels=etiquetas, autopct='%1.1f%%')
st.pyplot(fig)

# Mostrar desglose
st.write("### Recomendación personalizada:")
for e, p, v in zip(etiquetas, porcentajes, valores):
    st.write(f"- {e}: {p}% → €{v:,.2f}")

# Paso 7: Evaluación del usuario
st.session_state['step'] = 7
update_progress()
satisfaccion = st.slider("¿Qué tan útil te resultó esta herramienta?", 1, 10)
comentarios = st.text_area("¿Comentarios o sugerencias?")

# Paso 8: Finalizar y mostrar duración
st.session_state['step'] = 8
update_progress()
end_time = time.time()
duration = round(end_time - st.session_state['start_time'], 2)
st.success(f"Has completado el análisis en {duration} segundos.")

