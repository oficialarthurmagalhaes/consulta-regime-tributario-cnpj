import streamlit as st
import requests

# def consultar_cnpj(cnpj):
    
#     ULR_API = f'https://api.opencnpj.org/{cnpj}'

#     response = requests.get(ULR_API)

#     if response.status_code == 200:
#         print("--------------------\nConexão bem sucedida✅\n")

#         dados = response.json()
#         razao_social = dados['razao_social']
#         porte_empresa = dados['porte_empresa']
#         simples_nacional = dados['opcao_simples']
#         mei = dados['opcao_mei']
#         regime_tributario = ''

#         #REGIME TRIBUTARIO
#         if((simples_nacional == "S") and (mei == "S")):
#             regime_tributario = "MEI"
#         elif((simples_nacional == "S") and (mei == "N")):
#             regime_tributario = "SIMPLES NACIONAL"
#         else:
#             regime_tributario = "REGIME NORMAL"

#         print(f"CNPJ: {cnpj}\nRazão Social: {razao_social}\nPorte da Empresa: {porte_empresa}\nRegime Tributário: {regime_tributario}")

#     else:
#         dados = response.json()
#         print("--------------------\nConexão mal sucedida❌\n",dados)

def consultar_cnpj(cnpj):

    URL_API = f"https://api.opencnpj.org/{cnpj}"

    response = requests.get(URL_API)

    if response.status_code == 200:
        st.success("Conexão bem sucedida✅")

        dados = response.json()

        razao_social = dados['razao_social']
        nome_fantasia = dados['nome_fantasia']
        situacao_cadastral = dados['situacao_cadastral']
        porte_empresa = dados['porte_empresa']
        simples_nacional = dados['opcao_simples']
        mei = dados['opcao_mei']
        regime_tributario = ''

        #REGIME TRIBUTARIO
        if((simples_nacional == "S") and (mei == "S")):
            regime_tributario = "MEI"
        elif((simples_nacional == "S") and (mei == "N")):
            regime_tributario = "SIMPLES NACIONAL"
        else:
            regime_tributario = "REGIME NORMAL"

        st.markdown(f"""
        - **CNPJ:** {cnpj}  
        - **Razão Social:** {razao_social}  
        - **Nome Fantasia:** {nome_fantasia}
        - **Situação Cadastral:** {situacao_cadastral}
        - **Porte Empresa:** {porte_empresa}
        - **Regime Tributário:** {regime_tributario}
        """)

titulo = st.header("Consulta de Regime Tributário por CNPJ")

cnpj = st.text_input("Insira o CNPJ:")

pesquisar = st.button("Pesquisar")

if pesquisar:
    consultar_cnpj(cnpj)
