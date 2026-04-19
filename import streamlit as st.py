import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime

st.title("Sistema de Previsão de Medicamentos")

# -------------------------
# 📊 DADOS (exemplo simples)
# -------------------------
dados = {
    "mes": [1, 2, 3, 4, 5, 6],
    "consumo": [100, 120, 130, 150, 170, 200]
}

df = pd.DataFrame(dados)

# -------------------------
# 🤖 TREINAMENTO DO MODELO
# -------------------------
X = df[["mes"]]
y = df["consumo"]

modelo = LinearRegression()
modelo.fit(X, y)

# -------------------------
# 📥 ENTRADA DO USUÁRIO
# -------------------------
mes_futuro = st.number_input("Digite o mês para previsão (1 a 12):", min_value=1, max_value=12)
validade = st.date_input("Data de validade do medicamento")
