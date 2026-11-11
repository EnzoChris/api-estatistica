import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.main import estatisticas_metricas
from app.schema.metricas_schema import MetricasInput


def test_metricas_amostrais_e_correlacao_positiva():
    result = estatisticas_metricas(
        MetricasInput(base_dados_um=[1, 2, 3], base_dados_dois=[2, 4, 6])
    )
    assert result["variancia_base_um"] == pytest.approx(1)
    assert result["variancia_base_dois"] == pytest.approx(4)
    assert result["desvio_padrao_um"] == pytest.approx(1)
    assert result["desvio_padrao_dois"] == pytest.approx(2)
    assert result["covariancia e classificao"] == "2.0 - positivo"
    assert result["correlacao e classificao"] == "1.0 - positivo"


def test_correlacao_negativa():
    result = estatisticas_metricas(
        MetricasInput(base_dados_um=[1, 2, 3], base_dados_dois=[3, 2, 1])
    )
    assert result["correlacao e classificao"] == "-1.0 - negativo"


def test_correlacao_zero():
    result = estatisticas_metricas(
        MetricasInput(base_dados_um=[-1, 0, 1], base_dados_dois=[1, -2, 1])
    )
    assert result["correlacao e classificao"] == "0.0 - estável"


@pytest.mark.parametrize(
    "primeira, segunda",
    [
        ([], []),
        ([1], [2]),
        ([1, 2], [1, 2, 3]),
        ([1, 1], [1, 2]),
        ([1, 2], [3, 3]),
        ([1, "abc"], [1, 2]),
        ([1, "NaN"], [1, 2]),
        ([1, "Infinity"], [1, 2]),
    ],
)
def test_entradas_invalidas(primeira, segunda):
    with pytest.raises(ValidationError):
        MetricasInput(base_dados_um=primeira, base_dados_dois=segunda)


def test_resultados_nao_finitos_sao_rejeitados():
    entrada = MetricasInput(base_dados_um=[1e308, -1e308], base_dados_dois=[1, 2])
    with pytest.raises(HTTPException) as erro:
        estatisticas_metricas(entrada)
    assert erro.value.status_code == 422
