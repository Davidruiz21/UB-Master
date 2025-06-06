import streamlit as st
import matplotlib.pyplot as plt
import time

# --- Configuración Inicial y Estado de Sesión ---
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = time.time()
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 0 # Usaremos páginas en lugar de un paso lineal simple

PAGES = ["Bienvenida y Consentimiento", "Tu Patrimonio", "Tu Perfil de Inversor",
         "Resultados y Recomendaciones", "Evaluación y Cierre"]

# --- Funciones de Utilidad ---
def update_progress(page_index):
    progress = int((page_index / (len(PAGES) - 1)) * 100)
    st.progress(progress)

def calculate_net_worth(assets, liabilities):
    return sum(assets.values()) - sum(liabilities.values())

def get_risk_profile_questions():
    # Aquí puedes añadir un cuestionario de perfil de riesgo más detallado
    return [
        {"pregunta": "¿Cómo reaccionarías si tus inversiones cayeran un 20% en un mes?",
         "opciones": ["Entraría en pánico y vendería todo", "Me preocuparía, pero mantendría la calma", "Lo vería como una oportunidad para comprar más"]},
        {"pregunta": "¿Cuál es tu experiencia previa invirtiendo?",
         "opciones": ["Ninguna", "Poca, solo algunas acciones", "Moderada, he invertido en diferentes instrumentos", "Mucha, soy un inversor experimentado"]},
        # Agrega más preguntas para construir un perfil robusto
    ]

def assign_asset_allocation(edad, riesgo_perfil, horizonte_temporal):
    # Lógica más sofisticada de asignación de activos
    # Considera la edad y el horizonte para ajustar los porcentajes
    allocation = {}
    if riesgo_perfil == "Conservador":
        allocation = {"Acciones": 10, "Bonos": 50, "Liquidez": 30, "Inversiones alternativas": 5, "ETFs temáticos": 5}
    elif riesgo_perfil == "Moderado":
        allocation = {"Acciones": 30, "Bonos": 30, "Liquidez": 20, "Cripto": 5, "Commodities": 5, "Inversiones alternativas": 5, "ETFs temáticos": 5}
    else:  # Agresivo
        allocation = {"Acciones": 50, "Bonos": 10, "Liquidez": 10, "Cripto": 10, "Commodities": 5, "Inversiones alternativas": 10, "ETFs temáticos": 5}

    # Ajustes basados en edad y horizonte
    if edad < 40 and horizonte_temporal == "Largo plazo":
        allocation["Acciones"] = min(allocation.get("Acciones", 0) + 10, 70) # Aumenta acciones para jóvenes
        allocation["Bonos"] = max(allocation.get("Bonos", 0) - 10, 0)
    elif edad > 60 and horizonte_temporal == "Corto plazo":
        allocation["Acciones"] = max(allocation.get("Acciones", 0) - 15, 0) # Reduce acciones para mayores
        allocation["Bonos"] = min(allocation.get("Bonos", 0) + 15, 70)
    
    # Asegúrate de que los porcentajes sumen 100
    total_percent = sum(allocation.values())
    if total_percent != 100:
        factor = 100 / total_percent
        allocation = {k: v * factor for k, v in allocation.items()}

    return allocation

# --- Contenido de la Aplicación ---
st.title("Asesor Financiero Personalizado 📈")
st.write("Bienvenido. Esta herramienta avanzada te ayudará a comprender y optimizar la diversificación de tu patrimonio.")

update_progress(st.session_state['current_page'])

# --- Navegación entre Páginas ---
col1, col2 = st.columns([1, 1])
with col1:
    if st.session_state['current_page'] > 0:
        if st.button("⬅️ Anterior"):
            st.session_state['current_page'] -= 1
            st.rerun()
with col2:
    if st.session_state['current_page'] < len(PAGES) - 1:
        if st.button("Siguiente ➡️"):
            st.session_state['current_page'] += 1
            st.rerun()

st.markdown("---")

# --- Páginas del Asesor ---

# Página 0: Bienvenida y Consentimiento
if st.session_state['current_page'] == 0:
    st.header(PAGES[0])
    st.markdown("""
    Este simulador está diseñado con **fines exclusivamente educativos** y no debe considerarse como asesoramiento financiero profesional, personalizado o vinculante.
    Las recomendaciones generadas se basan en algoritmos predefinidos y no tienen en cuenta tu situación fiscal individual ni tus objetivos específicos más allá de los introducidos.
    Para una planificación financiera completa, siempre consulta con un asesor financiero certificado.
    """)
    if not st.checkbox("Entiendo y acepto las condiciones.", key="consent_checkbox"):
        st.stop()
    st.info("Haz click en 'Siguiente' para comenzar tu análisis.")


# Página 1: Tu Patrimonio
elif st.session_state['current_page'] == 1:
    st.header(PAGES[1])
    st.subheader("Tus Activos")
    assets = {
        "efectivo": st.number_input("Efectivo y Depósitos (€)", min_value=0.0, format="%.2f"),
        "inmuebles": st.number_input("Bienes Inmuebles (Valor de mercado estimado) (€)", min_value=0.0, format="%.2f"),
        "vehiculos": st.number_input("Vehículos y Otros Bienes de Alto Valor (€)", min_value=0.0, format="%.2f"),
        "bolsa": st.number_input("Inversiones en Bolsa (Acciones, Fondos, ETFs) (€)", min_value=0.0, format="%.2f"),
        "otros_activos": st.number_input("Otros Activos (Joyas, Colecciones, etc.) (€)", min_value=0.0, format="%.2f")
    }

    st.subheader("Tus Pasivos (Deudas)")
    liabilities = {
        "hipoteca": st.number_input("Deuda Hipotecaria Pendiente (€)", min_value=0.0, format="%.2f"),
        "prestamos": st.number_input("Préstamos Personales o de Coche (€)", min_value=0.0, format="%.2f"),
        "tarjetas": st.number_input("Deuda de Tarjetas de Crédito (€)", min_value=0.0, format="%.2f"),
        "otras_deudas": st.number_input("Otras Deudas (€)", min_value=0.0, format="%.2f")
    }

    st.session_state['assets'] = assets
    st.session_state['liabilities'] = liabilities
    
    patrimonio_total = calculate_net_worth(assets, liabilities)
    st.session_state['patrimonio_total'] = patrimonio_total

    if patrimonio_total < 0:
        st.error("Tu patrimonio neto es negativo. Esto indica que tus deudas superan tus activos.")
    elif patrimonio_total == 0:
        st.warning("Tu patrimonio neto es cero. Es importante empezar a construir activos y reducir deudas.")
    else:
        st.success(f"Tu Patrimonio Neto Total es de: €{patrimonio_total:,.2f}")
    
    # Validación antes de pasar a la siguiente página
    if st.session_state['patrimonio_total'] <= 0 and st.session_state['current_page'] == 1:
        st.warning("Para continuar, asegúrate de haber introducido valores válidos y un patrimonio neto positivo o al menos cero.")
        # Podrías deshabilitar el botón "Siguiente" aquí si quieres ser más estricto
        # if st.button("Siguiente ➡️", disabled=True): pass


# Página 2: Tu Perfil de Inversor
elif st.session_state['current_page'] == 2:
    st.header(PAGES[2])
    
    st.subheader("Información Personal")
    edad = st.slider("Edad", min_value=18, max_value=100, value=30)
    ingresos = st.number_input("Ingresos mensuales Netos (€)", min_value=0.0, format="%.2f")
    ahorro_mensual = st.number_input("Cantidad que puedes ahorrar/invertir mensualmente (€)", min_value=0.0, format="%.2f")

    st.subheader("Tolerancia al Riesgo")
    riesgo_cualitativo = st.selectbox("¿Cómo describirías tu actitud frente a las fluctuaciones del mercado?", 
                                     ["Muy conservador (prefiero seguridad y poca volatilidad)", 
                                      "Conservador (priorizo la preservación del capital)", 
                                      "Moderado (busco un equilibrio entre riesgo y rentabilidad)", 
                                      "Agresivo (dispuesto a asumir riesgos altos por mayores retornos)",
                                      "Muy agresivo (busco maximizar retornos, incluso con alta volatilidad)"])
    
    # Mapeo simple del riesgo cualitativo a una categoría de riesgo
    if "Muy conservador" in riesgo_cualitativo:
        riesgo_perfil_categoria = "Conservador"
    elif "Conservador" in riesgo_cualitativo:
        riesgo_perfil_categoria = "Conservador"
    elif "Moderado" in riesgo_cualitativo:
        riesgo_perfil_categoria = "Moderado"
    elif "Agresivo" in riesgo_cualitativo:
        riesgo_perfil_categoria = "Agresivo"
    else: # Muy agresivo
        riesgo_perfil_categoria = "Agresivo"

    st.session_state['riesgo_perfil_categoria'] = riesgo_perfil_categoria # Guarda el resultado del mapeo

    # Cuestionario de perfil de riesgo más detallado
    st.markdown("### Cuestionario Adicional de Perfil de Riesgo")
    respuestas_riesgo = {}
    for i, q_data in enumerate(get_risk_profile_questions()):
        respuestas_riesgo[f"q{i+1}"] = st.radio(q_data["pregunta"], q_data["opciones"], key=f"risk_q_{i}")
    
    horizonte = st.selectbox("Horizonte temporal principal de tu inversión", 
                             ["Corto plazo (menos de 3 años)", 
                              "Medio plazo (3 a 7 años)", 
                              "Largo plazo (más de 7 años)"])

    st.session_state['edad'] = edad
    st.session_state['ingresos'] = ingresos
    st.session_state['ahorro_mensual'] = ahorro_mensual
    st.session_state['horizonte'] = horizonte
    st.session_state['respuestas_riesgo'] = respuestas_riesgo


# Página 3: Resultados y Recomendaciones
elif st.session_state['current_page'] == 3:
    st.header(PAGES[3])
    
    # Asegúrate de que los datos necesarios estén en session_state
    if 'patrimonio_total' not in st.session_state or st.session_state['patrimonio_total'] is None:
        st.warning("Por favor, completa la sección de 'Tu Patrimonio' primero.")
        st.session_state['current_page'] = 1
        st.rerun()

    patrimonio_total = st.session_state['patrimonio_total']
    riesgo_perfil_categoria = st.session_state.get('riesgo_perfil_categoria', 'Moderado')
    horizonte = st.session_state.get('horizonte', 'Medio plazo')
    activos_actuales = st.session_state.get('assets', {})

    st.subheader("Análisis de Tu Patrimonio Actual")
    
    # Gráfico de tu patrimonio actual
    labels_actual = [k.replace('_', ' ').title() for k in activos_actuales.keys()]
    values_actual = list(activos_actuales.values())
    
    # Filtrar valores cero para el gráfico de pastel
    filtered_labels_actual = [labels_actual[i] for i, val in enumerate(values_actual) if val > 0]
    filtered_values_actual = [val for val in values_actual if val > 0]

    if filtered_values_actual:
        fig_actual, ax_actual = plt.subplots()
        ax_actual.pie(filtered_values_actual, labels=filtered_labels_actual, autopct='%1.1f%%', startangle=90)
        ax_actual.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig_actual, use_container_width=True)
    else:
        st.info("No hay activos para mostrar en tu patrimonio actual.")

    # Evaluación de diversificación más inteligente
    if activos_actuales.get('inmuebles', 0) > 0.6 * patrimonio_total and patrimonio_total > 0:
        st.warning("🚨 **Riesgo de Concentración:** Tu patrimonio está muy concentrado en bienes inmuebles. Aunque los inmuebles son una inversión estable, una excesiva concentración puede limitar la liquidez y exponer tu patrimonio a riesgos específicos del sector.")
        st.info("Considera diversificar hacia otras clases de activos para reducir este riesgo y mejorar tu liquidez.")
    
    st.subheader("Recomendación de Diversificación Personalizada")
    
    porcentajes_recomendados = assign_asset_allocation(st.session_state['edad'], riesgo_perfil_categoria, horizonte)
    etiquetas_recomendadas = list(porcentajes_recomendados.keys())
    valores_recomendados = [round((p/100) * patrimonio_total, 2) for p in porcentajes_recomendados.values()]

    # Mostrar gráfico de recomendación
    fig_rec, ax_rec = plt.subplots()
    ax_rec.pie(porcentajes_recomendados.values(), labels=etiquetas_recomendadas, autopct='%1.1f%%', startangle=90)
    ax_rec.axis('equal')
    st.pyplot(fig_rec, use_container_width=True)

    st.write("### Desglose de la Recomendación:")
    for e, p, v in zip(etiquetas_recomendadas, porcentajes_recomendados.values(), valores_recomendados):
        st.write(f"- **{e}**: {p:.1f}% ({v:,.2f} €)")
        
        # Añadir pequeña descripción de cada clase de activo
        if e == "Acciones":
            st.markdown("  _Representan propiedad en empresas, con potencial de alto crecimiento a largo plazo, pero también mayor volatilidad._")
        elif e == "Bonos":
            st.markdown("  _Préstamos a gobiernos o empresas, generalmente más estables que las acciones, proporcionan ingresos fijos._")
        elif e == "Liquidez":
            st.markdown("  _Fondos fácilmente accesibles para emergencias y oportunidades. Es crucial tener un fondo de emergencia._")
        elif e == "Cripto":
            st.markdown("  _Activos digitales descentralizados, de muy alta volatilidad y riesgo. Solo para perfiles agresivos y una pequeña porción._")
        elif e == "Commodities":
            st.markdown("  _Materias primas como oro, petróleo, etc. Pueden servir como cobertura contra la inflación._")
        elif e == "Inversiones alternativas":
            st.markdown("  _Incluye capital privado, fondos de cobertura, bienes raíces no tradicionales. Requieren mayor sofisticación._")
        elif e == "ETFs temáticos":
            st.markdown("  _Fondos que invierten en tendencias específicas (ej. tecnología verde, inteligencia artificial). Pueden ser volátiles._")
    
    st.markdown("---")
    st.subheader("Próximos Pasos Sugeridos")
    st.info(f"""
    Basado en tu perfil {riesgo_perfil_categoria} y tu horizonte de {horizonte}, aquí tienes algunas consideraciones adicionales:
    * **Fondo de Emergencia:** Asegúrate de tener al menos 3-6 meses de gastos en liquidez.
    * **Educación Financiera:** Aprende más sobre cada clase de activo antes de invertir.
    * **Revisión Periódica:** Revisa tu plan financiero al menos una vez al año o ante cambios significativos en tu vida.
    """)


# Página 4: Evaluación y Cierre
elif st.session_state['current_page'] == 4:
    st.header(PAGES[4])
    st.subheader("Tu Opinión es Importante")
    satisfaccion = st.slider("¿Qué tan útil te resultó esta herramienta?", 1, 10, value=7)
    comentarios = st.text_area("¿Tienes algún comentario o sugerencia para mejorar el asesor?")

    end_time = time.time()
    duration = round(end_time - st.session_state['start_time'], 2)
    st.success(f"¡Análisis Completado! Has finalizado el proceso en **{duration} segundos**.")
    st.balloons() # Pequeña animación para la finalización

    st.write("Gracias por usar nuestro Asesor Financiero Virtual. Esperamos que te haya sido de gran ayuda para comprender mejor tu patrimonio.")
    st.info("Recuerda que este es un punto de partida. La planificación financiera es un viaje continuo.")
