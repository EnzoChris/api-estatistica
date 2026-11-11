import math

from fastapi import FastAPI, HTTPException

from app.schema.metricas_schema import MetricasInput
from app.service.metricas_service import (
    calcular_correlacao,
    calcular_covariancia,
    calcular_desvio_padrao,
    calcular_variancia,
    classificacao_cov_e_corr,
    to_dataframe,
)

app = FastAPI()


@app.post("/criar-metricas-estatisticas")
def estatisticas_metricas(base_dados: MetricasInput):
    df = to_dataframe(base_dados)
    var = calcular_variancia(df)
    dp = calcular_desvio_padrao(df)
    cov = calcular_covariancia(df)
    corr = calcular_correlacao(df)
    valores = (
        var.variancia_base_um,
        var.variancia_base_dois,
        dp.desvio_padrao_base_um,
        dp.desvio_padrao_base_dois,
        cov.cov_base,
        corr.corr_base,
    )
    if not all(math.isfinite(valor) for valor in valores):
        raise HTTPException(
            status_code=422,
            detail="Não foi possível calcular métricas finitas para os valores informados",
        )
    classificacao = classificacao_cov_e_corr(cov, corr)

    return {
        "variancia_base_um": var.variancia_base_um,
        "variancia_base_dois": var.variancia_base_dois,
        "desvio_padrao_um": dp.desvio_padrao_base_um,
        "desvio_padrao_dois": dp.desvio_padrao_base_dois,
        "covariancia e classificao": f"{cov.cov_base} - {classificacao.cov_avaliacao}",
        "correlacao e classificao": f"{corr.corr_base} - {classificacao.corr_avaliacao}",
    }
