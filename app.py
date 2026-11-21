"""Interface web (Streamlit) da consulta de regime tributário por CNPJ."""

import streamlit as st

from cnpj import (
    CNPJInvalidoError,
    CNPJNaoEncontradoError,
    ErroConsultaAPI,
    consultar_cnpj,
)

st.set_page_config(page_title="Consulta de Regime Tributário", page_icon="🧾")

st.header("🧾 Consulta de Regime Tributário por CNPJ")
st.caption("Descubra se uma empresa é MEI, optante do Simples Nacional ou do regime normal.")

with st.form("consulta"):
    cnpj = st.text_input("CNPJ", placeholder="00.000.000/0000-00 (com ou sem pontuação)")
    pesquisar = st.form_submit_button("Pesquisar")

if pesquisar:
    try:
        with st.spinner("Consultando..."):
            empresa = consultar_cnpj(cnpj)
    except CNPJInvalidoError as erro:
        st.warning(str(erro))
    except CNPJNaoEncontradoError as erro:
        st.error(str(erro))
    except ErroConsultaAPI as erro:
        st.error(str(erro))
    else:
        st.success(f"Regime tributário: **{empresa['regime_tributario']}**")
        st.markdown(
            f"""
- **CNPJ:** {empresa['cnpj']}
- **Razão Social:** {empresa['razao_social']}
- **Nome Fantasia:** {empresa['nome_fantasia']}
- **Situação Cadastral:** {empresa['situacao_cadastral']}
- **Porte da Empresa:** {empresa['porte_empresa']}
"""
        )
        if empresa["regime_tributario"] == "REGIME NORMAL":
            st.info("Regime normal = Lucro Presumido ou Lucro Real. A API pública não informa qual dos dois.")

st.divider()
st.caption("Dados da [OpenCNPJ](https://opencnpj.org), com base nos dados abertos da Receita Federal.")
