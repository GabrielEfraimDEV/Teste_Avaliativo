import streamlit as st
import pandas as pd
import plotly.express as px
from db import load_sales_data


# ---------------------------
# Configuração da página
# ---------------------------
st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide"
)


# ---------------------------
# Carregamento de dados
# ---------------------------
@st.cache_data(show_spinner="Carregando dados de vendas...")
def load_data():
    df = load_sales_data()

    # Garantia de tipos
    df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')

    # Remove possíveis registros inválidos
    df = df.dropna(subset=['OrderDate', 'TotalDue'])

    return df


# ---------------------------
# Execução principal
# ---------------------------
try:
    df = load_data()
except Exception as e:
    st.error("Erro ao carregar os dados do banco.")
    st.stop()
