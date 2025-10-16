# app.py - CON matplotlib (ejecutar después de que la básica funcione)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Análisis Fútbol", page_icon="⚽", layout="wide")
st.title("⚽ Análisis Man City vs Napoli")

@st.cache_data
def load_data():
    np.random.seed(42)
    n_matches = 20
    
    mc_data = {
        'possession': np.random.randint(55, 75, n_matches),
        'pass_accuracy': np.random.randint(85, 95, n_matches),
        'shots': np.random.randint(12, 25, n_matches),
        'goals': np.random.randint(1, 5, n_matches),
    }
    
    na_data = {
        'possession': np.random.randint(45, 65, n_matches),
        'pass_accuracy': np.random.randint(80, 90, n_matches),
        'shots': np.random.randint(10, 20, n_matches),
        'goals': np.random.randint(0, 4, n_matches),
    }
    
    return pd.DataFrame(mc_data), pd.DataFrame(na_data)

df_mc, df_na = load_data()

page = st.sidebar.selectbox("Navegación", ["Inicio", "Gráficos"])

if page == "Inicio":
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("🔵 Manchester City")
        st.metric("Posesión", f"{df_mc['possession'].mean():.1f}%")
        st.metric("Precisión", f"{df_mc['pass_accuracy'].mean():.1f}%")
    
    with col2:
        st.header("🔴 Napoli") 
        st.metric("Posesión", f"{df_na['possession'].mean():.1f}%")
        st.metric("Precisión", f"{df_na['pass_accuracy'].mean():.1f}%")

elif page == "Gráficos":
    st.header("📊 Gráficos Comparativos")
    
    # Gráfico de barras simple
    fig, ax = plt.subplots(figsize=(10, 6))
    
    metrics = ['Posesión', 'Precisión', 'Tiros', 'Goles']
    mc_vals = [df_mc['possession'].mean(), df_mc['pass_accuracy'].mean(), 
               df_mc['shots'].mean(), df_mc['goals'].mean()]
    na_vals = [df_na['possession'].mean(), df_na['pass_accuracy'].mean(),
               df_na['shots'].mean(), df_na['goals'].mean()]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    ax.bar(x - width/2, mc_vals, width, label='Man City', color='blue')
    ax.bar(x + width/2, na_vals, width, label='Napoli', color='red')
    
    ax.set_xlabel('Métricas')
    ax.set_ylabel('Valores')
    ax.set_title('Comparación Man City vs Napoli')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend()
    
    st.pyplot(fig)

st.markdown("---")
st.success("🚀 Aplicación con gráficos funcionando")
