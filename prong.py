import streamlit as st
import pandas as pd

# --- Configuración de la página ---
st.set_page_config(
    page_title="Optimización de Redes",
    page_icon="🌐",
    layout="centered"
)

# --- Título y descripción ---
st.title("🌐 Optimización de Redes (Modo Colapsado)")
st.markdown("""
Satura la ruta más económica (Ruta A) antes de asignar el remanente a la ruta secundaria (Ruta B).
""")

# --- Sidebar para controles de entrada ---
st.sidebar.header("⚙️ Parámetros de la Red")

demanda_total = st.sidebar.slider(
    "Demanda Total (Mbps)", 
    min_value=0.0, 
    max_value=200.0, 
    value=120.0, 
    step=5.0
)

st.sidebar.subheader("Ruta A (Económica)")
cap_A = st.sidebar.number_input("Capacidad Máxima A (Mbps)", min_value=0.0, value=90.0, step=0.5)
costo_A = st.sidebar.number_input("Costo A (por Mbps)", min_value=0.0, value=2.0, step=0.05)

st.sidebar.subheader("Ruta B (Secundaria)")
cap_B = st.sidebar.number_input("Capacidad Máxima B (Mbps)", min_value=0.0, value=60.0, step=0.5)
costo_B = st.sidebar.number_input("Costo B (por Mbps)", min_value=0.0, value=5.0, step=0.05)

# --- Inicialización del Estado de la Sesión ---
if 'ejecutado' not in st.session_state:
    st.session_state.ejecutado = False
    st.session_state.flujo_A = 0.0
    st.session_state.flujo_B = 0.0
    st.session_state.costo_total = 0.0
    st.session_state.capacidad_total_red = 0.0

# --- Botón de Ejecución y Lógica del Algoritmo ---
if st.button("ejecutar optimizacion"):
    if demanda_total <= cap_A:
        st.session_state.flujo_A = demanda_total
        st.session_state.flujo_B = 0.0
    else:
        st.session_state.flujo_A = cap_A
        st.session_state.flujo_B = demanda_total - cap_A
    
    # Validación si el remanente supera la capacidad física de la Ruta B
    if st.session_state.flujo_B > cap_B:
        st.session_state.flujo_B = cap_B

    st.session_state.costo_total = (st.session_state.flujo_A * costo_A) + (st.session_state.flujo_B * costo_B)
    st.session_state.capacidad_total_red = cap_A + cap_B
    st.session_state.ejecutado = True

# --- Despliegue de Resultados (Solo si se ha presionado el botón) ---
if st.session_state.ejecutado:
    
    # --- Métricas Principales ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Flujo Ruta A", value=f"{st.session_state.flujo_A:.2f} Mbps")
    with col2:
        st.metric(label="Flujo Ruta B", value=f"{st.session_state.flujo_B:.2f} Mbps")
    with col3:
        st.metric(label="Costo Total", value=f"${st.session_state.costo_total:.2f}")

    # --- Alertas de Capacidad ---
    if demanda_total > st.session_state.capacidad_total_red:
        st.error(f"⚠️ **Déficit de capacidad:** La demanda ({demanda_total:.2f} Mbps) supera la capacidad total de la red ({st.session_state.capacidad_total_red:.2f} Mbps). Se han colapsado ambas rutas a su límite máximo.")
    elif st.session_state.flujo_A == cap_A and st.session_state.flujo_B > 0:
        st.warning("⚠️ **Ruta A saturada:** El tráfico excedente se desvió a la Ruta B.")
    else:
        st.success("✅ **Red optimizada:** Toda la demanda se procesa de forma eficiente.")

    # --- Visualización Gráfica ---
    st.subheader("📊 Distribución del Tráfico")

    # Creamos un DataFrame para los datos del gráfico
    datos_grafico = pd.DataFrame({
        'Ruta': ['Ruta A', 'Ruta B'],
        'Tráfico Asignado (Mbps)': [st.session_state.flujo_A, st.session_state.flujo_B],
        'Capacidad Máxima (Mbps)': [cap_A, cap_B]
    }).set_index('Ruta')

    # Gráfico de barras nativo de Streamlit
    st.bar_chart(datos_grafico['Tráfico Asignado (Mbps)'])

    # --- Tabla de Resumen ---
    st.subheader("📋 Resumen de Datos")
    st.dataframe(datos_grafico)
else:
    st.info("💡 Haz clic en el botón **'ejecutar optimizacion'** para ver los resultados.")
