import streamlit as st
import requests

def consultar_cnpj(cnpj):

    URL_API = f"https://api.opencnpj.org/{cnpj}"

    response = requests.get(URL_API)

    status_requisicao = response.status_code

    if status_requisicao == 200:
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
    else:
        st.error(f"Erro {status_requisicao} | Conexão Mal Sucedida❌ | CNPJ não encontrado.")

titulo = st.header("Consulta de Regime Tributário por CNPJ")

cnpj = st.text_input("Insira o CNPJ:")

pesquisar = st.button("Pesquisar")

if pesquisar:
    consultar_cnpj(cnpj)
