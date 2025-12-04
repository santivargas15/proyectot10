import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Vehicle Data EDA", layout="wide")

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

DATA_PATH = "vehicles_us .csv"

data = load_data(DATA_PATH)

st.header("Datos del conjunto de vehículos")

# Identificar columnas numéricas y categóricas
num_cols = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
cat_cols = data.select_dtypes(include=['object']).columns.tolist()

if not num_cols:
    st.warning("No numerical columns found in the dataset.")

# --- EXPLORACIÓN ----
with st.expander('Vista previa de datos', expanded=True):
    st.dataframe(data.head(50), use_container_width=True)

# --- HISTOGRAMA ----
st.subheader('Histograma')
col_hist = st.selectbox('Selecciona una columna numérica para el histograma:', num_cols)
bins = st.slider('Número de bins:', min_value=5, max_value=100, value=30)
show_hist = st.checkbox('Mostrar Histograma', value=True)

# --- SCATTER ----
st.subheader('Gráfico de dispersión')

if len(num_cols) >= 2:
    default_x = num_cols[0]
    default_y = num_cols[1]
else:
    default_x = default_y = num_cols[0] if num_cols else None

x_scatter = st.selectbox(
    'Selecciona la columna X:',
    num_cols,
    index=num_cols.index(default_x) if default_x in num_cols else 0
)

y_scatter = st.selectbox(
    'Selecciona la columna Y:',
    num_cols,
    index=num_cols.index(default_y) if default_y in num_cols else 0
)

show_scatter = st.checkbox('Mostrar Gráfico de Dispersión', value=True)

# --- PLOTS ----
if show_hist and col_hist:
    fig_hist = px.histogram(data, x=col_hist, nbins=bins, title=f'Histograma de {col_hist}')
    st.plotly_chart(fig_hist, use_container_width=True)

if show_scatter and x_scatter and y_scatter:
    fig_scatter = px.scatter(
        data,
        x=x_scatter, y=y_scatter,
        title=f'Gráfico de Dispersión: {y_scatter} vs {x_scatter}'
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")
st.markdown("Developed by Santiago")
