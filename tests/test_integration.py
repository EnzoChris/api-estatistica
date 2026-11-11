from fastapi.testclient import TestClient

from app.main import app


def test_requisicao_http_valida():
    with TestClient(app) as client:
        resposta = client.post(
            "/criar-metricas-estatisticas",
            json={"base_dados_um": [1, 2, 3], "base_dados_dois": [2, 4, 6]},
        )
    assert resposta.status_code == 200
    assert resposta.json()["variancia_base_um"] == 1.0
    assert resposta.json()["correlacao e classificao"] == "1.0 - positivo"


def test_requisicao_http_invalida():
    with TestClient(app) as client:
        resposta = client.post(
            "/criar-metricas-estatisticas",
            json={"base_dados_um": [1, 2], "base_dados_dois": [1]},
        )
    assert resposta.status_code == 422
