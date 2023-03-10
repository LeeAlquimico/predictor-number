import numpy as np
import pandas as pd
import streamlit as st
from sklearn.neural_network import MLPClassifier

st.set_page_config(page_title="BUDAPrototype", page_icon="🌀")

# Define o título do aplicativo
st.title("Prevendo números da Lotofácil")

# carrega os dados de treinamento
dados_treinamento = pd.read_csv('sequencias.csv')

# extrai as sequências e os rótulos
X = dados_treinamento.values[:, :-1]
y = dados_treinamento.values[:, -1]

# cria o modelo MLP
model = MLPClassifier(hidden_layer_sizes=(30, 20, 10), max_iter=1000)

# treina o modelo
model.fit(X, y)

# solicita que o usuário insira a sequência a ser prevista
nova_sequencia_str = st.text_input("Digite os 15 números da sequência a ser prevista, separados por vírgula (ex: 1,2,3,...,15): ")

# adiciona um botão para prever os números
if st.button("Prever"):
    if nova_sequencia_str:
        nova_sequencia = list(map(int, nova_sequencia_str.split(',')))
        if len(nova_sequencia) != 15:
            st.error("A sequência deve conter exatamente 15 números!")
        elif not all(1 <= numero <= 25 for numero in nova_sequencia):
            st.error("A sequência deve conter apenas números no intervalo de 1 a 25!")
        else:
            # obtém os índices das posições em ordem decrescente de probabilidade
            probabilidades = model.predict_proba([nova_sequencia])[0]
            indices_previstos = np.argsort(probabilidades)[::-1]

            # seleciona os 15 números com maior probabilidade no intervalo de 1 a 25
            numeros_previstos = []
            for indice in indices_previstos:
                numero_previsto = indice + 1
                if numero_previsto not in numeros_previstos and numero_previsto <= 25:
                    numeros_previstos.append(numero_previsto)
                if len(numeros_previstos) == 15:
                    break

            # ordena os números previstos na ordem crescente
            numeros_previstos = sorted(numeros_previstos)

            # exibe os números previstos em um retângulo com bordas arredondadas
            st.markdown(
                f"""
                        <div style="background-color:white; border-radius: 20px; padding: 10px; width: 750px; display: flex; justify-content: center; align-items: center;">
                            <div style="display: flex; justify-content: flex-end; align-items: center; margin-left: 10px;">
                                {" ".join([f'<div style="background-color:green; color:white; font-size: 20px; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center;">{num}</div><div style="width: 10px;"></div>' for num in numeros_previstos])}
                            </div>
                        </div>
                        """,
                unsafe_allow_html=True
            )
