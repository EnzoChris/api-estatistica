import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_criar_metricas_por_http():
    response = client.post(
        "/criar-metricas-estatisticas",
        json={"base_dados_um": [1, 2, 3], "base_dados_dois": [2, 4, 6]},
    )

    assert response.status_code == 200
    assert response.json() == {
        "variancia_base_um": 1.0,
        "variancia_base_dois": 4.0,
        "desvio_padrao_um": 1.0,
        "desvio_padrao_dois": 2.0,
        "covariancia e classificao": "2.0 - positivo",
        "correlacao e classificao": "1.0 - positivo",
    }


@pytest.mark.parametrize(
    "dados",
    [
        {"base_dados_um": [1, 2], "base_dados_dois": [1, 2, 3]},
        {"base_dados_um": [1, 1], "base_dados_dois": [1, 2]},
        {"base_dados_um": [1, 2]},
        {"base_dados_um": [1, 2], "base_dados_dois": [1, 2], "extra": 1},
    ],
)
def test_dados_invalidos_retornam_422_por_http(dados):
    response = client.post("/criar-metricas-estatisticas", json=dados)

    assert response.status_code == 422


def test_metricas_nao_finitas_retornam_422_por_http():
    response = client.post(
        "/criar-metricas-estatisticas",
        json={"base_dados_um": [1e308, -1e308], "base_dados_dois": [1, 2]},
    )

    assert response.status_code == 422
    assert "métricas finitas" in response.json()["detail"]
