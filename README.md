# API de estatísticas

Calcula variância e desvio padrão amostrais, covariância amostral e correlação de Pearson para duas séries de observações pareadas. A classificação indica o sinal da covariância e da correlação; zero é apresentado como `estável`.

## Executar

Requer Python 3.14 ou superior.

```bash
pip install ".[dev]"
uvicorn app.main:app --reload
```

A documentação interativa fica em http://127.0.0.1:8000/docs. Para executar os testes: `python -m pytest`.

Também é possível executar com Docker:

```bash
docker build -t api-estatistica .
docker run --rm -p 8000:8000 api-estatistica
```

## Requisição

`POST /criar-metricas-estatisticas` aceita duas listas numéricas de mesmo tamanho, com pelo menos duas observações e pelo menos dois valores distintos em cada lista. Os valores devem ser finitos. A correlação não é definida para uma série constante. Dados inválidos ou resultados que excedam a precisão numérica retornam HTTP 422.

```json
{"base_dados_um": [1, 2, 3], "base_dados_dois": [2, 4, 6]}
```

```json
{
  "variancia_base_um": 1.0,
  "variancia_base_dois": 4.0,
  "desvio_padrao_um": 1.0,
  "desvio_padrao_dois": 2.0,
  "covariancia e classificao": "2.0 - positivo",
  "correlacao e classificao": "1.0 - positivo"
}
```

Os nomes existentes dos campos de resposta são mantidos por compatibilidade. Variância, desvio padrão e covariância usam divisor `n - 1`.
