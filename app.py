import streamlit as st
import matplotlib.pyplot as plt
import time

# --- Configuración Inicial y Estado de Sesión ---
# Reiniciar el estado de la sesión si el usuario pulsa "Volver a Empezar"
if 'restart_app' in st.session_state and st.session_state['restart_app']:
    for key in st.session_state.keys():
        del st.session_state[key]
    st.session_state['restart_app'] = False # Resetea la bandera

if 'start_time' not in st.session_state:
    st.session_state['start_time'] = time.time()
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 0

PAGES = ["Bienvenida y Consentimiento", "Tu Patrimonio", "Tu Perfil de Inversor",
         "Resultados y Recomendaciones", "Evaluación y Cierre"]

# --- Funciones de Utilidad ---
def update_progress_bar(page_index):
    progress = int((page_index / (len(PAGES) - 1)) * 100)
    st.sidebar.progress(progress) # La barra de progreso ahora estará en la barra lateral

def calculate_net_worth(assets, liabilities):
    return sum(assets.values()) - sum(liabilities.values())

def get_risk_profile_questions():
    return [
        {"pregunta": "¿Cómo reaccionarías si tus inversiones cayeran un 20% en un mes?",
         "opciones": ["Entraría en pánico y vendería todo", "Me preocuparía, pero mantendría la calma", "Lo vería como una oportunidad para comprar más"]},
        {"pregunta": "¿Cuál es tu experiencia previa invirtiendo?",
         "opciones": ["Ninguna", "Poca, solo algunas acciones", "Moderada, he invertido en diferentes instrumentos", "Mucha, soy un inversor experimentado"]},
    ]

def assign_asset_allocation(edad, riesgo_perfil, horizonte_temporal):
    allocation = {}
    if riesgo_perfil == "Conservador":
        allocation = {"Acciones": 10, "Bonos": 50, "Liquidez": 30, "Inversiones alternativas": 5, "ETFs temáticos": 5}
    elif riesgo_perfil == "Moderado":
        allocation = {"Acciones": 30, "Bonos": 30, "Liquidez": 20, "Cripto": 5, "Commodities": 5, "Inversiones alternativas": 5, "ETFs temáticos": 5}
    else:  # Agresivo
        allocation = {"Acciones": 50, "Bonos": 10, "Liquidez": 10, "Cripto": 10, "Commodities": 5, "Inversiones alternativas": 10, "ETFs temáticos": 5}

    if edad < 40 and horizonte_temporal == "Largo plazo":
        allocation["Acciones"] = min(allocation.get("Acciones", 0) + 10, 70)
        allocation["Bonos"] = max(allocation.get("Bonos", 0) - 10, 0)
    elif edad > 60 and horizonte_temporal == "Corto plazo":
        allocation["Acciones"] = max(allocation.get("Acciones", 0) - 15, 0)
        allocation["Bonos"] = min(allocation.get("Bonos", 0) + 15, 70)
    
    total_percent = sum(allocation.values())
    if total_percent != 100:
        factor = 100 / total_percent
        allocation = {k: v * factor for k, v in allocation.items()}

    return allocation

# --- Contenido de la Aplicación ---
st.title("Asesor Financiero Personalizado 📈")
st.write("Bienvenido. Esta herramienta avanzada te ayudará a comprender y optimizar la diversificación de tu patrimonio.")

# La barra de progreso ahora está en la barra lateral
st.sidebar.header("Progreso del Análisis")
progress_text = st.sidebar.empty() # Placeholder para el texto de progreso
progress_bar = st.sidebar.progress(0) # Placeholder para la barra

# Actualizar la barra y el texto de progreso
progress_value = int((st.session_state['current_page'] / (len(PAGES) - 1)) * 100) if len(PAGES) > 1 else 100
progress_bar.progress(progress_value)
progress_text.write(f"Paso {st.session_state['current_page'] + 1} de {len(PAGES)}: {PAGES[st.session_state['current_page']]} ({progress_value}%)")


# --- Navegación entre Páginas ---
st.markdown("---") # Separador visual para la navegación
col1, col2 = st.columns([1, 1])
with col1:
    if st.session_state['current_page'] > 0:
        if st.button("⬅️ Anterior"):
            st.session_state['current_page'] -= 1
            st.rerun()
with col2:
    if st.session_state['current_page'] < len(PAGES) - 1:
        # Deshabilitar el botón "Siguiente" si la validación falla en la página actual
        disable_next = False
        if st.session_state['current_page'] == 0 and not st.session_state.get('consent_given', False):
            disable_next = True
        elif st.session_state['current_page'] == 1 and (st.session_state.get('patrimonio_total', 0) <= 0 and sum(st.session_state.get('assets', {}).values()) > 0): # Asegúrate de haber introducido algún activo
            disable_next = True # Deshabilitar si el patrimonio es <= 0 y hay activos introducidos
        elif st.session_state['current_page'] == 1 and sum(st.session_state.get('assets', {}).values()) == 0 and sum(st.session_state.get('liabilities', {}).values()) == 0 :
             st.info("Por favor, introduce al menos un activo o pasivo para calcular tu patrimonio.")
             disable_next = True

        if st.button("Siguiente ➡️", disabled=disable_next):
            st.session_state['current_page'] += 1
            st.rerun()

st.markdown("---") # Otro separador

# --- Páginas del Asesor ---

# Página 0: Bienvenida y Consentimiento
if st.session_state['current_page'] == 0:
    st.header(PAGES[0])
    st.markdown("""
    Este simulador está diseñado con **fines exclusivamente educativos** y no debe considerarse como asesoramiento financiero profesional, personalizado o vinculante.
    Las recomendaciones generadas se basan en algoritmos predefinidos y no tienen en cuenta tu situación fiscal individual ni tus objetivos específicos más allá de los introducidos.
    Para una planificación financiera completa, siempre consulta con un asesor financiero certificado.
    """)
    consent_checkbox = st.checkbox("Entiendo y acepto las condiciones.", key="consent_checkbox")
    st.session_state['consent_given'] = consent_checkbox
    if not consent_checkbox:
        st.info("Debes aceptar las condiciones para continuar.")


# Página 1: Tu Patrimonio
elif st.session_state['current_page'] == 1:
    st.header(PAGES[1])
    st.subheader("Tus Activos")
    assets = {
        "efectivo": st.number_input("Efectivo y Depósitos (€)", min_value=0.0, value=st.session_state.get('assets', {}).get('efectivo', 0.0), format="%.2f"),
        "inmuebles": st.number_input("Bienes Inmuebles (Valor de mercado estimado) (€)", min_value=0.0, value=st.session_state.get('assets', {}).get('inmuebles', 0.0), format="%.2f"),
        "vehiculos": st.number_input("Vehículos y Otros Bienes de Alto Valor (€)", min_value=0.0, value=st.session_state.get('assets', {}).get('vehiculos', 0.0), format="%.2f"),
        "bolsa": st.number_input("Inversiones en Bolsa (Acciones, Fondos, ETFs) (€)", min_value=0.0, value=st.session_state.get('assets', {}).get('bolsa', 0.0), format="%.2f"),
        "otros_activos": st.number_input("Otros Activos (Joyas, Colecciones, etc.) (€)", min_value=0.0, value=st.session_state.get('assets', {}).get('otros_activos', 0.0), format="%.2f")
    }

    st.subheader("Tus Pasivos (Deudas)")
    liabilities = {
        "hipoteca": st.number_input("Deuda Hipotecaria Pendiente (€)", min_value=0.0, value=st.session_state.get('liabilities', {}).get('hipoteca', 0.0), format="%.2f"),
        "prestamos": st.number_input("Préstamos Personales o de Coche (€)", min_value=0.0, value=st.session_state.get('liabilities', {}).get('prestamos', 0.0), format="%.2f"),
        "tarjetas": st.number_input("Deuda de Tarjetas de Crédito (€)", min_value=0.0, value=st.session_state.get('liabilities', {}).get('tarjetas', 0.0), format="%.2f"),
        "otras_deudas": st.number_input("Otras Deudas (€)", min_value=0.0, value=st.session_state.get('liabilities', {}).get('otras_deudas', 0.0), format="%.2f")
    }

    st.session_state['assets'] = assets
    st.session_state['liabilities'] = liabilities
    
    patrimonio_total = calculate_net_worth(assets, liabilities)
    st.session_state['patrimonio_total'] = patrimonio_total

    if patrimonio_total < 0:
        st.error(f"Tu patrimonio neto es negativo: €{patrimonio_total:,.2f}. Esto indica que tus deudas superan tus activos.")
    elif patrimonio_total == 0:
        st.warning("Tu patrimonio neto es cero. Es importante empezar a construir activos y reducir deudas.")
    else:
        st.success(f"Tu Patrimonio Neto Total es de: €{patrimonio_total:,.2f}")
    
    # Validación más clara para el usuario
    if patrimonio_total <= 0 and sum(assets.values()) == 0 and sum(liabilities.values()) == 0:
        st.info("Para continuar, por favor introduce al menos un valor en tus activos o pasivos.")


# Página 2: Tu Perfil de Inversor
elif st.session_state['current_page'] == 2:
    st.header(PAGES[2])
    
    st.subheader("Información Personal")
    edad = st.slider("Edad", min_value=18, max_value=100, value=st.session_state.get('edad', 30))
    ingresos = st.number_input("Ingresos mensuales Netos (€)", min_value=0.0, value=st.session_state.get('ingresos', 0.0), format="%.2f")
    ahorro_mensual = st.number_input("Cantidad que puedes ahorrar/invertir mensualmente (€)", min_value=0.0, value=st.session_state.get('ahorro_mensual', 0.0), format="%.2f")

    st.subheader("Tolerancia al Riesgo")
    riesgo_opciones = ["Muy conservador (prefiero seguridad y poca volatilidad)",
                       "Conservador (priorizo la preservación del capital)",
                       "Moderado (busco un equilibrio entre riesgo y rentabilidad)",
                       "Agresivo (dispuesto a asumir riesgos altos por mayores retornos)",
                       "Muy agresivo (busco maximizar retornos, incluso con alta volatilidad)"]
    riesgo_cualitativo = st.selectbox("¿Cómo describirías tu actitud frente a las fluctuaciones del mercado?",
                                     riesgo_opciones, index=riesgo_opciones.index(st.session_state.get('riesgo_cualitativo', riesgo_opciones[2])))

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

    st.session_state['riesgo_perfil_categoria'] = riesgo_perfil_categoria
    st.session_state['riesgo_cualitativo'] = riesgo_cualitativo

    st.markdown("### Cuestionario Adicional de Perfil de Riesgo")
    respuestas_riesgo = {}
    for i, q_data in enumerate(get_risk_profile_questions()):
        # Pre-seleccionar la opción si ya se ha respondido antes
        default_index = q_data["opciones"].index(st.session_state.get('respuestas_riesgo', {}).get(f"q{i+1}", q_data["opciones"][0]))
        respuestas_riesgo[f"q{i+1}"] = st.radio(q_data["pregunta"], q_data["opciones"], key=f"risk_q_{i}", index=default_index)
    
    horizonte_opciones = ["Corto plazo (menos de 3 años)", "Medio plazo (3 a 7 años)", "Largo plazo (más de 7 años)"]
    horizonte = st.selectbox("Horizonte temporal principal de tu inversión",
                             horizonte_opciones, index=horizonte_opciones.index(st.session_state.get('horizonte', horizonte_opciones[1])))

    st.session_state['edad'] = edad
    st.session_state['ingresos'] = ingresos
    st.session_state['ahorro_mensual'] = ahorro_mensual
    st.session_state['horizonte'] = horizonte
    st.session_state['respuestas_riesgo'] = respuestas_riesgo


# Página 3: Resultados y Recomendaciones
elif st.session_state['current_page'] == 3:
    st.header(PAGES[3])
    
    if 'patrimonio_total' not in st.session_state or st.session_state['patrimonio_total'] is None or st.session_state['patrimonio_total'] <= 0:
        st.warning("Por favor, completa la sección de 'Tu Patrimonio' con valores válidos y un patrimonio neto positivo para ver las recomendaciones.")
        st.session_state['current_page'] = 1
        st.rerun()

    patrimonio_total = st.session_state['patrimonio_total']
    riesgo_perfil_categoria = st.session_state.get('riesgo_perfil_categoria', 'Moderado')
    horizonte = st.session_state.get('horizonte', 'Medio plazo')
    activos_actuales = st.session_state.get('assets', {})

    st.subheader("Análisis de Tu Patrimonio Actual")
    
    labels_actual = [k.replace('_', ' ').title() for k in activos_actuales.keys()]
    values_actual = list(activos_actuales.values())
    
    filtered_labels_actual = [labels_actual[i] for i, val in enumerate(values_actual) if val > 0]
    filtered_values_actual = [val for val in values_actual if val > 0]

    if filtered_values_actual:
        fig_actual, ax_actual = plt.subplots()
        ax_actual.pie(filtered_values_actual, labels=filtered_labels_actual, autopct='%1.1f%%', startangle=90)
        ax_actual.axis('equal')
        st.pyplot(fig_actual, use_container_width=True)
    else:
        st.info("No hay activos para mostrar en tu patrimonio actual.")

    if activos_actuales.get('inmuebles', 0) > 0.6 * patrimonio_total and patrimonio_total > 0:
        st.warning("🚨 **Riesgo de Concentración:** Tu patrimonio está muy concentrado en bienes inmuebles. Aunque los inmuebles son una inversión estable, una excesiva concentración puede limitar la liquidez y exponer tu patrimonio a riesgos específicos del sector.")
        st.info("Considera diversificar hacia otras clases de activos para reducir este riesgo y mejorar tu liquidez.")
    
    st.subheader("Recomendación de Diversificación Personalizada")
    
    porcentajes_recomendados = assign_asset_allocation(st.session_state['edad'], riesgo_perfil_categoria, horizonte)
    etiquetas_recomendadas = list(porcentajes_recomendados.keys())
    valores_recomendados = [round((p/100) * patrimonio_total, 2) for p in porcentajes_recomendados.values()]

    fig_rec, ax_rec = plt.subplots()
    ax_rec.pie(porcentajes_recomendados.values(), labels=etiquetas_recomendadas, autopct='%1.1f%%', startangle=90)
    ax_rec.axis('equal')
    st.pyplot(fig_rec, use_container_width=True)

    st.write("### Desglose de la Recomendación:")
    for e, p, v in zip(etiquetas_recomendadas, porcentajes_recomendados.values(), valores_recomendados):
        st.write(f"- **{e}**: {p:.1f}% ({v:,.2f} €)")
        
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
    Basado en tu perfil **{riesgo_perfil_categoria}** y tu horizonte de **{horizonte}**, aquí tienes algunas consideraciones adicionales:
    * **Fondo de Emergencia:** Asegúrate de tener al menos 3-6 meses de gastos en liquidez.
    * **Educación Financiera:** Aprende más sobre cada clase de activo antes de invertir.
    * **Revisión Periódica:** Revisa tu plan financiero al menos una vez al año o ante cambios significativos en tu vida.
    """)


# Página 4: Evaluación y Cierre
elif st.session_state['current_page'] == 4:
    st.header(PAGES[4])
    st.subheader("Tu Opinión es Importante")
    satisfaccion = st.slider("¿Qué tan útil te resultó esta herramienta?", 1, 10, value=st.session_state.get('satisfaccion', 7))
    comentarios = st.text_area("¿Tienes algún comentario o sugerencia para mejorar el asesor?", value=st.session_state.get('comentarios', ''))

    st.session_state['satisfaccion'] = satisfaccion
    st.session_state['comentarios'] = comentarios

    end_time = time.time()
    duration = round(end_time - st.session_state['start_time'], 2)
    st.success(f"¡Análisis Completado! Has finalizado el proceso en **{duration} segundos**.")
    st.balloons() # Pequeña animación para la finalización

    st.write("Gracias por usar nuestro Asesor Financiero Virtual. Esperamos que te haya sido de gran ayuda para comprender mejor tu patrimonio.")
    st.info("Recuerda que este es un punto de partida. La planificación financiera es un viaje continuo.")
    
    # Botón para reiniciar la aplicación
    if st.button("🔄 Volver a Empezar el Análisis"):
        st.session_state['restart_app'] = True
        st.rerun() # Esto hará que la aplicación se recargue y limpie el estado
