import pandas as pd

from app.schema.metricas_schema import (
    ClassificacaoOutput,
    CorrelacaoOutput,
    CovarianciaOutput,
    DesvioPadraoOutput,
    MetricasInput,
    VarianciaOutput,
)


def to_dataframe(base_dados: MetricasInput) -> pd.DataFrame:
    return pd.DataFrame(
        {"base_um": base_dados.base_dados_um, "base_dois": base_dados.base_dados_dois}
    )


def calcular_variancia(base_dados: pd.DataFrame) -> VarianciaOutput:
    return VarianciaOutput(
        variancia_base_um=base_dados.base_um.var(),
        variancia_base_dois=base_dados.base_dois.var(),
    )


def calcular_desvio_padrao(base_dados: pd.DataFrame) -> DesvioPadraoOutput:
    return DesvioPadraoOutput(
        desvio_padrao_base_um=base_dados.base_um.std(),
        desvio_padrao_base_dois=base_dados.base_dois.std(),
    )


def calcular_covariancia(base_dados: pd.DataFrame) -> CovarianciaOutput:
    return CovarianciaOutput(
        cov_base=base_dados[["base_um", "base_dois"]].cov().iloc[0, 1],
    )


def calcular_correlacao(base_dados: pd.DataFrame) -> CorrelacaoOutput:
    return CorrelacaoOutput(
        corr_base=base_dados[["base_um", "base_dois"]].corr().iloc[0, 1],
    )


def classificacao_cov_e_corr(
    cov: CovarianciaOutput, corr: CorrelacaoOutput
) -> ClassificacaoOutput:
    cov_avaliacao = ""
    corr_avaliacao = ""

    if cov.cov_base < 0:
        cov_avaliacao = "negativo"
    elif cov.cov_base > 0:
        cov_avaliacao = "positivo"
    else:
        cov_avaliacao = "estável"

    if corr.corr_base > 0:
        corr_avaliacao = "positivo"
    elif corr.corr_base < 0:
        corr_avaliacao = "negativo"
    else:
        corr_avaliacao = "estável"

    return ClassificacaoOutput(
        cov_avaliacao=cov_avaliacao, corr_avaliacao=corr_avaliacao
    )
