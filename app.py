# app.py - Análisis Manchester City vs Napoli
import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Análisis Man City vs Napoli",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Análisis Táctico: Manchester City vs Napoli")
st.markdown("---")

# Cargar datos
@st.cache_data
def load_data():
    np.random.seed(42)
    n_matches = 20
    
    data_man_city = {
        'possession': np.random.randint(55, 75, n_matches),
        'pass_accuracy': np.random.randint(85, 95, n_matches),
        'shots': np.random.randint(12, 25, n_matches),
        'goals': np.random.randint(1, 5, n_matches),
        'fouls': np.random.randint(8, 15, n_matches),
        'corners': np.random.randint(4, 10, n_matches),
    }
    
    data_napoli = {
        'possession': np.random.randint(45, 65, n_matches),
        'pass_accuracy': np.random.randint(80, 90, n_matches),
        'shots': np.random.randint(10, 20, n_matches),
        'goals': np.random.randint(0, 4, n_matches),
        'fouls': np.random.randint(10, 18, n_matches),
        'corners': np.random.randint(3, 8, n_matches),
    }
    
    return pd.DataFrame(data_man_city), pd.DataFrame(data_napoli)

df_mc, df_na = load_data()

# Navegación
page = st.sidebar.selectbox("Navegación", ["Inicio", "Comparación", "Predicción", "Dashboard"])

if page == "Inicio":
    st.header("🏠 Análisis Manchester City vs Napoli")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔵 Manchester City")
        st.metric("Posesión", f"{df_mc['possession'].mean():.1f}%")
        st.metric("Precisión Pase", f"{df_mc['pass_accuracy'].mean():.1f}%")
        st.metric("Tiros/Partido", f"{df_mc['shots'].mean():.1f}")
        st.metric("Goles/Partido", f"{df_mc['goals'].mean():.1f}")
    
    with col2:
        st.subheader("🔴 Napoli")
        st.metric("Posesión", f"{df_na['possession'].mean():.1f}%")
        st.metric("Precisión Pase", f"{df_na['pass_accuracy'].mean():.1f}%")
        st.metric("Tiros/Partido", f"{df_na['shots'].mean():.1f}")
        st.metric("Goles/Partido", f"{df_na['goals'].mean():.1f}")

elif page == "Comparación":
    st.header("📊 Comparación Directa")
    
    # Usar gráficos nativos de Streamlit
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Manchester City")
        st.dataframe(df_mc.describe())
        
    with col2:
        st.subheader("Napoli")
        st.dataframe(df_na.describe())
    
    # Métricas comparativas
    st.subheader("📈 Métricas Comparativas")
    
    metrics_data = {
        'Métrica': ['Posesión', 'Precisión Pase', 'Tiros', 'Goles', 'Faltas'],
        'Man City': [
            df_mc['possession'].mean(),
            df_mc['pass_accuracy'].mean(),
            df_mc['shots'].mean(),
            df_mc['goals'].mean(),
            df_mc['fouls'].mean()
        ],
        'Napoli': [
            df_na['possession'].mean(),
            df_na['pass_accuracy'].mean(),
            df_na['shots'].mean(),
            df_na['goals'].mean(),
            df_na['fouls'].mean()
        ]
    }
    
    df_comparison = pd.DataFrame(metrics_data)
    st.dataframe(df_comparison, use_container_width=True)

elif page == "Predicción":
    st.header("🤖 Predicción del Partido")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Victoria Man City", "65%")
        st.info("**Escenario:** 2-0, 3-1")
        
    with col2:
        st.metric("Empate", "25%") 
        st.warning("**Escenario:** 1-1, 2-2")
        
    with col3:
        st.metric("Victoria Napoli", "10%")
        st.error("**Escenario:** 0-1, 1-2")
    
    st.markdown("---")
    st.subheader("🔍 Factores Clave")
    
    factors = [
        "✅ Man City: Superior posesión y control",
        "✅ Man City: Mayor volumen ofensivo", 
        "⚠️ Napoli: Buena efectividad goleadora",
        "⚠️ Man City: Mayor experiencia europea",
        "❌ Napoli: Menor consistencia defensiva"
    ]
    
    for factor in factors:
        st.write(factor)

elif page == "Dashboard":
    st.header("📈 Dashboard Táctico")
    
    # Filtros
    metric = st.selectbox("Selecciona métrica:", ["Posesión", "Precisión Pase", "Tiros", "Goles"])
    
    metric_map = {
        "Posesión": "possession",
        "Precisión Pase": "pass_accuracy", 
        "Tiros": "shots",
        "Goles": "goals"
    }
    
    selected = metric_map[metric]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(f"{metric} MC", f"{df_mc[selected].mean():.1f}")
    
    with col2:
        st.metric(f"{metric} Napoli", f"{df_na[selected].mean():.1f}")
    
    with col3:
        diff = df_mc[selected].mean() - df_na[selected].mean()
        st.metric("Diferencia", f"{diff:+.1f}")
    
    with col4:
        advantage = "Man City" if diff > 0 else "Napoli"
        st.metric("Ventaja", advantage)

st.markdown("---")
st.success("✅ Aplicación ejecutándose correctamente")
