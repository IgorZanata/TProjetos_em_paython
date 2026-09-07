import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# ==========================================================
# CONFIGURAR O SITE DO STREAMLIT
# ==========================================================
st.set_page_config(
    page_title="Aprendizado em maquina",
    page_icon="💊"
)
st.title("💊 Previsão de Consumo de Medicamentos utilizando Machine Learning")

# ==========================================================
# CARREGAR E LIMPAR OS DADOS DO ARQUIVO CSV
# ==========================================================
try:
    dados = pd.read_csv("medicamentos.csv")
except FileNotFoundError:
    st.error("Erro: O arquivo medicamentos.csv não foi encontrado.")
    st.stop()


dados = dados.drop_duplicates()
dados = dados.dropna()

dados["validade"] = pd.to_datetime(dados["validade"], 
                    format="%d/%m/%Y", errors="coerce")


hoje = pd.Timestamp.today().normalize() #armazenar data atual

dados["dias_validade"] = (dados["validade"] - hoje).dt.days 

dados["tempo"] = pd.to_numeric(dados["tempo"],errors="coerce")
dados["quantidade"] = pd.to_numeric(dados["quantidade"],errors="coerce")
dados["consumo"] = pd.to_numeric(dados["consumo"],errors="coerce")

dados = dados.dropna()


# ==========================================================
# VARIÁVEIS DO MODELO
# ==========================================================

X = dados[[
    "tempo",
    "quantidade",
    "dias_validade"
]]

y = dados["consumo"]


# ==========================================================
# DIVISÃO DOS DADOS EM TREINAMENTO E TESTE
# ==========================================================

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ==========================================================
# TREINAMENTO DO MODELO
# ==========================================================

modelo = LinearRegression()

modelo.fit(
    X_treino,
    y_treino
)

# ==========================================================
# PREVISÕES E AVALIAÇÃO DO MODELO
# ==========================================================

previsoes_teste = modelo.predict(X_teste)

mae = mean_absolute_error(
    y_teste, previsoes_teste
)

rmse = mean_squared_error(
    y_teste,previsoes_teste
) ** 0.5

r2 = r2_score(
    y_teste, previsoes_teste
)


# ==========================================================
# INTERFACE DE SELEÇÃO DO MEDICAMENTO
# ==========================================================

st.header("Selecione o Medicamento")

lista_remedios = sorted(
    dados["medicamento"].unique()
)

remedio_escolhido = st.selectbox(
    "Escolha um remédio:",
    lista_remedios
)


# ==========================================================
# BUSCAR DADOS DO MEDICAMENTO
# ==========================================================

linha_do_remedio = dados[
    dados["medicamento"] == remedio_escolhido
].iloc[0]


codigo = linha_do_remedio["cod_medicamento"]

tempo = linha_do_remedio["tempo"]

quantidade = linha_do_remedio["quantidade"]

dias_validade = linha_do_remedio["dias_validade"]

data_validade = linha_do_remedio[
    "validade"
].strftime("%d/%m/%Y")


# ==========================================================
# CALCULAR PREVISÃO
# ==========================================================

if st.button("Calcular Previsão"):

# ==========================================================
# DADOS CADASTRADOS
# ==========================================================

    st.subheader("Dados Cadastrados")

    st.write(f"Código:{codigo}")

    st.write(
        f"Quantidade no estoque: "
        f"{quantidade:.0f} unidades"
    )

    st.write(
        f"Validade: {data_validade} "
        f"(faltam {dias_validade:.0f} dias)"
    )

    st.write(
        f"Tempo de consumo: "
        f"{tempo:.0f} dias"
    )


 # ==========================================================
# PREPARAR DADOS PARA A PREVISÃO
 # ==========================================================
 
    dados_para_prever = pd.DataFrame(
        [[
            tempo,
            quantidade,
            dias_validade
        ]],
        columns=["tempo", "quantidade", "dias_validade"])

# ==========================================================
# PREVISÃO DO CONSUMO
# ==========================================================

    consumo_previsto = modelo.predict(
        dados_para_prever
    )[0]

    if consumo_previsto < 0: # Impedir valor negativo
        consumo_previsto = 0

    consumo_previsto = round(consumo_previsto )

    sobra = (quantidade - consumo_previsto
    
        if consumo_previsto < quantidade
        else 0
    )
    porcentagem_perda = ((sobra / quantidade) * 100
        if quantidade > 0
        else 0
    )



  # ======================================================
# CLASSIFICAÇÃO DE RISCO
  # ======================================================

    if (dias_validade <= 30 or porcentagem_perda >= 30):
        risco = "CRÍTICO"

    elif (dias_validade <= 60 or porcentagem_perda >= 15):
        risco = "ALERTA"

    elif (dias_validade <= 90 or sobra > 0):
        risco = "ATENÇÃO"
    
    else:
        risco = "NORMAL"

    # ======================================================
    # EXIBIÇÃO DOS RESULTADOS
    # ======================================================
    st.subheader("Resultado")

    st.metric(
        "Consumo Previsto",
        f"{consumo_previsto:.0f} unidades")
    
    st.write(
        f"**Risco de Vencimento:** {risco}")

    # ======================================================
    # ALERTA DE SOBRA
    # ======================================================

    if sobra > 0:

        st.warning(
            f"Alerta de Perda: "
            f"Estima-se uma sobra não consumida de "
            f"{sobra:.0f} unidades antes do vencimento.")

    else:

        st.success(
            "Estoque Seguro: "
            "O consumo previsto cobre a quantidade "
            "em estoque.")

    # ======================================================
    # MÉTRICAS DE AVALIAÇÃO
    # ======================================================

    st.subheader("Qualidade do Modelo")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Erro Médio (MAE)",
        f"{mae:.2f}")

    col2.metric(
        "Erro RMSE",
        f"{rmse:.2f}")

    col3.metric(
        "Precisão (R²)",
        f"{r2:.2f}")


# ==========================================================
# TABELA COMPLETA
# ==========================================================

with st.expander(
    "Ver tabela de dados completa"
):

    st.dataframe(dados)