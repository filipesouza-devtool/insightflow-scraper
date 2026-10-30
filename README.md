# InsightFlow Analytics

Projeto de estudo em Python dividido em duas partes: um **motor de extração** que coleta dados da web e uma **vitrine** em Streamlit que transforma o CSV em um painel de análise.

> Desenvolvido 100% pelo celular, no pyramIDE.

## Como funciona

1. **`Scrape.py`** percorre as páginas de [quotes.toscrape.com](https://quotes.toscrape.com) (site feito para praticar scraping), extrai autor, texto e tags de cada citação e salva tudo em CSV.
2. **`app.py`** lê o CSV (upload ou arquivo local) e exibe métricas, destaques e a tabela de dados.

## Recursos

- Paginação automática, parando quando não há mais botão "next"
- Pausa entre requisições para não sobrecarregar o servidor
- Remoção de duplicatas e CSV com acentos corretos no Excel
- Painel com total de citações, autores e tags mais frequentes
- Seleção de colunas e upload de outros CSVs
- Leitura com fallback de encoding (utf-8 / latin1)

## Tecnologias

Python · requests · BeautifulSoup · pandas · Streamlit

## Como executar

```bash
pip install requests beautifulsoup4 pandas streamlit
python Scrape.py          # gera o CSV
streamlit run app.py      # abre o painel
```

O painel espera o arquivo `dados_raspados.csv` na mesma pasta (ou use o upload na barra lateral).

## Estrutura

```
├── Scrape.py   # motor de extração
├── app.py      # painel Streamlit
└── README.md
```

## Próximos passos

- Busca por texto e filtro por autor
- Gráficos de frequência
- Botão para atualizar os dados dentro do painel

## Aviso

Projeto com fins educacionais, usando um site criado para prática de scraping.
