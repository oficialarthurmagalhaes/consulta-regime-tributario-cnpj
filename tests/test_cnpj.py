import pytest
import requests

from cnpj import (
    CNPJInvalidoError,
    CNPJNaoEncontradoError,
    ErroConsultaAPI,
    cnpj_valido,
    consultar_cnpj,
    determinar_regime,
    formatar_cnpj,
    limpar_cnpj,
)

CNPJ_VALIDO = "11222333000181"


# ---------- Funções puras ----------

def test_limpar_cnpj_remove_pontuacao():
    assert limpar_cnpj("11.222.333/0001-81") == CNPJ_VALIDO
    assert limpar_cnpj(" 11 222 333 0001 81 ") == CNPJ_VALIDO


@pytest.mark.parametrize("cnpj", ["11.222.333/0001-81", CNPJ_VALIDO])
def test_cnpj_valido(cnpj):
    assert cnpj_valido(cnpj)


@pytest.mark.parametrize("cnpj", ["", "123", "11222333000180", "00000000000000", "1122233300018100"])
def test_cnpj_invalido(cnpj):
    assert not cnpj_valido(cnpj)


def test_formatar_cnpj():
    assert formatar_cnpj(CNPJ_VALIDO) == "11.222.333/0001-81"


@pytest.mark.parametrize(
    "simples, mei, esperado",
    [
        ("S", "S", "MEI"),
        ("S", "N", "SIMPLES NACIONAL"),
        ("N", "N", "REGIME NORMAL"),
        (None, None, "REGIME NORMAL"),
        ("s", "n", "SIMPLES NACIONAL"),
    ],
)
def test_determinar_regime(simples, mei, esperado):
    assert determinar_regime(simples, mei) == esperado


# ---------- Consulta à API (com respostas simuladas) ----------

class RespostaFalsa:
    def __init__(self, status_code, dados=None):
        self.status_code = status_code
        self._dados = dados

    def json(self):
        if self._dados is None:
            raise ValueError("sem JSON")
        return self._dados


class SessaoFalsa:
    def __init__(self, resposta=None, erro=None):
        self.resposta = resposta
        self.erro = erro
        self.chamadas = []

    def get(self, url, timeout):
        self.chamadas.append((url, timeout))
        if self.erro:
            raise self.erro
        return self.resposta


def test_consulta_sucesso():
    dados = {
        "razao_social": "EMPRESA TESTE LTDA",
        "nome_fantasia": "",
        "situacao_cadastral": "Ativa",
        "porte_empresa": "Microempresa",
        "opcao_simples": "S",
        "opcao_mei": "N",
    }
    sessao = SessaoFalsa(RespostaFalsa(200, dados))

    empresa = consultar_cnpj("11.222.333/0001-81", sessao=sessao)

    assert empresa["regime_tributario"] == "SIMPLES NACIONAL"
    assert empresa["cnpj"] == "11.222.333/0001-81"
    assert empresa["nome_fantasia"] == "Não informado"
    url, timeout = sessao.chamadas[0]
    assert url.endswith(CNPJ_VALIDO)
    assert timeout > 0


def test_consulta_cnpj_invalido_nao_chama_api():
    sessao = SessaoFalsa()
    with pytest.raises(CNPJInvalidoError):
        consultar_cnpj("123", sessao=sessao)
    assert sessao.chamadas == []


def test_consulta_nao_encontrado():
    with pytest.raises(CNPJNaoEncontradoError):
        consultar_cnpj(CNPJ_VALIDO, sessao=SessaoFalsa(RespostaFalsa(404)))


def test_consulta_erro_servidor():
    with pytest.raises(ErroConsultaAPI):
        consultar_cnpj(CNPJ_VALIDO, sessao=SessaoFalsa(RespostaFalsa(500)))


def test_consulta_falha_de_rede():
    with pytest.raises(ErroConsultaAPI):
        consultar_cnpj(CNPJ_VALIDO, sessao=SessaoFalsa(erro=requests.Timeout()))


def test_consulta_resposta_invalida():
    with pytest.raises(ErroConsultaAPI):
        consultar_cnpj(CNPJ_VALIDO, sessao=SessaoFalsa(RespostaFalsa(200, None)))
