"""Regras de negócio da consulta de regime tributário por CNPJ.

Fica separado da interface (app.py) para poder ser testado com pytest.
"""

import re

import requests

URL_API = "https://api.opencnpj.org/{cnpj}"
TIMEOUT_SEGUNDOS = 10


class CNPJInvalidoError(ValueError):
    """O CNPJ informado não tem formato ou dígitos verificadores válidos."""


class CNPJNaoEncontradoError(LookupError):
    """A API não encontrou nenhuma empresa com o CNPJ informado."""


class ErroConsultaAPI(RuntimeError):
    """Falha de comunicação com a API (fora do ar, lenta ou resposta inesperada)."""


def limpar_cnpj(cnpj: str) -> str:
    """Remove pontos, barras, traços e espaços: '12.345.678/0001-95' -> '12345678000195'."""
    return re.sub(r"\D", "", cnpj or "")


def _digito_verificador(numeros: str, pesos: list[int]) -> str:
    soma = sum(int(n) * p for n, p in zip(numeros, pesos))
    resto = soma % 11
    return "0" if resto < 2 else str(11 - resto)


def cnpj_valido(cnpj: str) -> bool:
    """Confere se o CNPJ tem 14 dígitos e se os dígitos verificadores batem."""
    numeros = limpar_cnpj(cnpj)
    if len(numeros) != 14 or numeros == numeros[0] * 14:
        return False
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6] + pesos1
    dv1 = _digito_verificador(numeros[:12], pesos1)
    dv2 = _digito_verificador(numeros[:12] + dv1, pesos2)
    return numeros[-2:] == dv1 + dv2


def formatar_cnpj(cnpj: str) -> str:
    """'12345678000195' -> '12.345.678/0001-95'."""
    n = limpar_cnpj(cnpj)
    return f"{n[:2]}.{n[2:5]}.{n[5:8]}/{n[8:12]}-{n[12:]}"


def determinar_regime(opcao_simples: str | None, opcao_mei: str | None) -> str:
    """Define o regime a partir das opções do Simples Nacional e do MEI.

    'S' significa que a empresa é optante. Quem não é optante do Simples
    está no regime normal (Lucro Presumido ou Lucro Real).
    """
    simples = (opcao_simples or "").strip().upper() == "S"
    mei = (opcao_mei or "").strip().upper() == "S"
    if simples and mei:
        return "MEI"
    if simples:
        return "SIMPLES NACIONAL"
    return "REGIME NORMAL"


def consultar_cnpj(cnpj: str, sessao=requests) -> dict:
    """Consulta a API OpenCNPJ e devolve os dados principais da empresa.

    Lança CNPJInvalidoError, CNPJNaoEncontradoError ou ErroConsultaAPI.
    """
    numeros = limpar_cnpj(cnpj)
    if not cnpj_valido(numeros):
        raise CNPJInvalidoError("CNPJ inválido. Confira os 14 dígitos.")

    try:
        resposta = sessao.get(URL_API.format(cnpj=numeros), timeout=TIMEOUT_SEGUNDOS)
    except requests.RequestException as erro:
        raise ErroConsultaAPI("Não foi possível conectar à API. Tente novamente.") from erro

    if resposta.status_code == 404:
        raise CNPJNaoEncontradoError("CNPJ não encontrado na base da Receita.")
    if resposta.status_code != 200:
        raise ErroConsultaAPI(f"A API respondeu com erro {resposta.status_code}. Tente novamente.")

    try:
        dados = resposta.json()
    except ValueError as erro:
        raise ErroConsultaAPI("A API devolveu uma resposta inválida.") from erro

    return {
        "cnpj": formatar_cnpj(numeros),
        "razao_social": dados.get("razao_social") or "Não informado",
        "nome_fantasia": dados.get("nome_fantasia") or "Não informado",
        "situacao_cadastral": dados.get("situacao_cadastral") or "Não informado",
        "porte_empresa": dados.get("porte_empresa") or "Não informado",
        "regime_tributario": determinar_regime(dados.get("opcao_simples"), dados.get("opcao_mei")),
    }
