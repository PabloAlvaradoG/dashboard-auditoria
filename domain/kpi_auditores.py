"""Cálculo de cumplimiento de meta mensual de auditores.

Aislado del resto del dashboard a propósito: esta es la lógica que
evalúa el desempeño de personas reales, así que necesita poder probarse
con casos conocidos (12/12 = 100%, 6/12 = 50%, 0 auditorías = 0%) sin
tener que levantar Streamlit ni cargar un Excel.
"""
from dataclasses import dataclass
from typing import Optional

from config.umbrales import META_AUDITORIAS_RETAIL
from config.valores import VAL_TIPO_RETAIL


@dataclass
class Cumplimiento:
    auditor: str
    tipo_auditor: str
    realizadas: int
    meta: Optional[int]
    cumplimiento_real: Optional[float]        # % sobre la meta, con lo ya realizado
    proyeccion_cierre: Optional[float]        # auditorías proyectadas al cierre del ciclo
    cumplimiento_proyectado: Optional[float]  # % sobre la meta, al ritmo actual


def calcular_meta(tipo_auditor: str, meta_retail: int = META_AUDITORIAS_RETAIL) -> Optional[int]:
    """La meta de auditorías/mes solo aplica a auditores tipo Retail.

    >>> calcular_meta("Retail")
    12
    >>> calcular_meta("Coral") is None
    True
    """
    return meta_retail if tipo_auditor == VAL_TIPO_RETAIL else None


def calcular_cumplimiento(
    auditor: str,
    tipo_auditor: str,
    realizadas: int,
    dias_transcurridos: int,
    dias_totales_ciclo: int,
    meta_retail: int = META_AUDITORIAS_RETAIL,
) -> Cumplimiento:
    """Calcula el cumplimiento real y proyectado de un auditor en un ciclo.

    - `cumplimiento_real`  = realizadas / meta * 100 (tal cual va el ciclo)
    - `proyeccion_cierre`  = al ritmo actual, cuántas haría si el ciclo
      completara sus días totales
    - `cumplimiento_proyectado` = proyección / meta * 100

    >>> c = calcular_cumplimiento("X", "Retail", realizadas=6, dias_transcurridos=15, dias_totales_ciclo=30)
    >>> c.cumplimiento_real
    50.0
    >>> c.proyeccion_cierre
    12.0
    >>> c.cumplimiento_proyectado
    100.0

    >>> c2 = calcular_cumplimiento("Y", "Coral", realizadas=5, dias_transcurridos=15, dias_totales_ciclo=30)
    >>> c2.meta is None and c2.cumplimiento_real is None
    True

    >>> c3 = calcular_cumplimiento("Z", "Retail", realizadas=0, dias_transcurridos=10, dias_totales_ciclo=30)
    >>> c3.cumplimiento_real
    0.0
    """
    meta = calcular_meta(tipo_auditor, meta_retail)
    dias_transcurridos = max(dias_transcurridos, 1)  # evitar división por cero

    cumplimiento_real = (realizadas / meta * 100) if meta else None
    proyeccion_cierre = realizadas / dias_transcurridos * dias_totales_ciclo
    cumplimiento_proyectado = (proyeccion_cierre / meta * 100) if meta else None

    return Cumplimiento(
        auditor=auditor,
        tipo_auditor=tipo_auditor,
        realizadas=realizadas,
        meta=meta,
        cumplimiento_real=cumplimiento_real,
        proyeccion_cierre=proyeccion_cierre,
        cumplimiento_proyectado=cumplimiento_proyectado,
    )


def clasificar_semaforo(pct: Optional[float], umbral_rojo: float, umbral_verde: float) -> str:
    """Clasifica un % de cumplimiento en 'rojo' / 'amarillo' / 'verde' / 'no_aplica'.

    >>> clasificar_semaforo(None, 50, 90)
    'no_aplica'
    >>> clasificar_semaforo(40, 50, 90)
    'rojo'
    >>> clasificar_semaforo(70, 50, 90)
    'amarillo'
    >>> clasificar_semaforo(95, 50, 90)
    'verde'
    """
    if pct is None:
        return "no_aplica"
    if pct < umbral_rojo:
        return "rojo"
    if pct < umbral_verde:
        return "amarillo"
    return "verde"
