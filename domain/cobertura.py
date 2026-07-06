"""Cobertura de auditoría: % de tiendas activas auditadas a tiempo."""
from dataclasses import dataclass, field
from typing import Optional
import pandas as pd

from config.umbrales import COBERTURA_DIAS_CORTO, COBERTURA_DIAS_LARGO


@dataclass
class Cobertura:
    n_activas: int
    n_auditadas_90d: int
    n_auditadas_180d: int
    pct_90d: float
    pct_180d: float
    pendientes_90d: pd.DataFrame = field(default_factory=pd.DataFrame)


def calcular_cobertura(
    dias_sin_auditar_por_tienda: pd.Series,
    dias_corto: int = COBERTURA_DIAS_CORTO,
    dias_largo: int = COBERTURA_DIAS_LARGO,
) -> Cobertura:
    """A partir de una Serie [tienda -> días sin auditar] (tiendas activas
    únicamente), calcula cuántas están dentro de los umbrales de 90/180 días.

    >>> import pandas as pd
    >>> s = pd.Series([10, 95, 200, 30], index=["A", "B", "C", "D"])
    >>> c = calcular_cobertura(s)
    >>> c.n_activas, c.n_auditadas_90d, c.n_auditadas_180d
    (4, 2, 3)
    >>> c.pct_90d
    50.0
    """
    n_tot = len(dias_sin_auditar_por_tienda)
    n_90 = int((dias_sin_auditar_por_tienda <= dias_corto).sum())
    n_180 = int((dias_sin_auditar_por_tienda <= dias_largo).sum())
    return Cobertura(
        n_activas=n_tot,
        n_auditadas_90d=n_90,
        n_auditadas_180d=n_180,
        pct_90d=(n_90 / n_tot * 100) if n_tot else 0.0,
        pct_180d=(n_180 / n_tot * 100) if n_tot else 0.0,
    )
