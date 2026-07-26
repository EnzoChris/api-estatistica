from pydantic import BaseModel

class MetricasInput(BaseModel):
    base_dados_um: list[float|int]
    base_dados_dois: list[float|int]

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
    
