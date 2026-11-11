from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, FiniteFloat, model_validator


class MetricasInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    base_dados_um: Annotated[list[FiniteFloat], Field(min_length=2)]
    base_dados_dois: Annotated[list[FiniteFloat], Field(min_length=2)]

    @model_validator(mode="after")
    def validar_bases(self):
        if len(self.base_dados_um) != len(self.base_dados_dois):
            raise ValueError("As bases devem ter o mesmo número de elementos")
        if len(set(self.base_dados_um)) < 2 or len(set(self.base_dados_dois)) < 2:
            raise ValueError(
                "Cada base deve ter pelo menos dois valores distintos para calcular a correlação"
            )
        return self


class VarianciaOutput(BaseModel):
    variancia_base_um: float
    variancia_base_dois: float


class DesvioPadraoOutput(BaseModel):
    desvio_padrao_base_um: float
    desvio_padrao_base_dois: float


class CovarianciaOutput(BaseModel):
    cov_base: float


class CorrelacaoOutput(BaseModel):
    corr_base: float


class ClassificacaoOutput(BaseModel):
    cov_avaliacao: str
    corr_avaliacao: str
