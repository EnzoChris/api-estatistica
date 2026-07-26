#dentro desse arquivo será exposto as rotas e será chamado os services correspondentes a cada rota
from fastapi import FastAPI
from app.schema.metricas_schema import MetricasInput
from app.service.metricas_service import to_dataframe, calcular_correlacao, calcular_covariancia, calcular_desvio_padrao, classificacao_cov_e_corr, calcular_variancia

app = FastAPI()

#criando rota para apresentar os dados estatísticos
@app.post("/criar-metricas-estatisticas")
def estatisticas_metricas(base_dados: MetricasInput):
    df = to_dataframe(base_dados)
    var = calcular_variancia(df)
    dp = calcular_desvio_padrao(df)
    cov = calcular_covariancia(df)
    corr = calcular_correlacao(df)
    classificacao = classificacao_cov_e_corr(cov, corr)

    return {
        "variancia_base_um":var.variancia_base_um,
        "variancia_base_dois":var.variancia_base_dois,
        "desvio_padrao_um":dp.desvio_padrao_base_um,
        "desvio_padrao_dois":dp.desvio_padrao_base_dois,
        "covariancia e classificao":f"{cov.cov_base} - {classificacao.cov_avaliacao}",
        "correlacao e classificao":f"{corr.corr_base} - {classificacao.corr_avaliacao}"
    }