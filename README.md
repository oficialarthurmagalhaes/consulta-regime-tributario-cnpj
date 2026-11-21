# 🧾 Consulta de Regime Tributário por CNPJ

[![Testes](https://github.com/oficialarthurmagalhaes/consulta-regime-tributario-cnpj/actions/workflows/testes.yml/badge.svg)](https://github.com/oficialarthurmagalhaes/consulta-regime-tributario-cnpj/actions/workflows/testes.yml)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)

Aplicação web que informa, a partir de um CNPJ, se a empresa é **MEI**, optante do **Simples Nacional** ou do **regime normal** (Lucro Presumido/Real), além da razão social, nome fantasia, situação cadastral e porte.

O projeto nasceu de uma necessidade real do trabalho: conferir rapidamente o regime tributário de empresas sem precisar entrar no site da Receita uma a uma.

## ✨ Funcionalidades

- Aceita o CNPJ **com ou sem pontuação** (`11.222.333/0001-81` ou `11222333000181`)
- **Valida os dígitos verificadores** antes de consultar, sem gastar requisição com CNPJ errado
- Mensagens claras para CNPJ inválido, não encontrado ou API fora do ar
- Consulta com **timeout**, para a tela não travar se a API demorar

## ▶️ Como rodar

```bash
git clone https://github.com/oficialarthurmagalhaes/consulta-regime-tributario-cnpj.git
cd consulta-regime-tributario-cnpj
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

O app abre em `http://localhost:8501`.

## 🧪 Testes

A lógica fica em `cnpj.py`, separada da interface, e é coberta por testes com `pytest`. As chamadas à API são simuladas, então os testes rodam sem internet:

```bash
pip install -r requirements-dev.txt
pytest -v
```

Os testes também rodam automaticamente no **GitHub Actions** a cada push.

## 🗂️ Estrutura

```
├── app.py                 # interface (Streamlit)
├── cnpj.py                # validação do CNPJ, consulta à API e regra do regime
├── tests/test_cnpj.py     # testes automatizados
├── requirements.txt       # dependências do app
├── requirements-dev.txt   # dependências de desenvolvimento (pytest)
└── .github/workflows/     # CI com GitHub Actions
```

## 📡 Fonte dos dados

[OpenCNPJ](https://opencnpj.org), API gratuita baseada nos dados abertos da Receita Federal.

> A API pública não diferencia Lucro Presumido de Lucro Real, por isso os dois aparecem como "Regime Normal".
