"""Score de prioridad de auditoría y normalización de riesgo."""
from config.umbrales import (
    PRIORIDAD_PESO_DIAS, PRIORIDAD_PESO_SCORE, PRIORIDAD_PESO_MONTO,
    PRIORIDAD_UMBRAL_URGENTE, PRIORIDAD_UMBRAL_ALTA, PRIORIDAD_UMBRAL_MEDIA,
)


def calcular_prioridad_score(
    dias_sin_auditar: float,
    score_riesgo: float,
    monto_a_cobrar_costo: float,
    peso_dias: float = PRIORIDAD_PESO_DIAS,
    peso_score: float = PRIORIDAD_PESO_SCORE,
    peso_monto: float = PRIORIDAD_PESO_MONTO,
) -> float:
    """Score que prioriza qué tienda auditar primero.

    >>> round(calcular_prioridad_score(dias_sin_auditar=100, score_riesgo=20, monto_a_cobrar_costo=-1000), 2)
    85.0
    """
    return (
        dias_sin_auditar * peso_dias
        + score_riesgo * peso_score
        + abs(monto_a_cobrar_costo) * peso_monto
    )


def clasificar_recomendacion(score: float) -> str:
    """Traduce el score de prioridad a una etiqueta accionable.

    >>> clasificar_recomendacion(200)
    'URGENTE'
    >>> clasificar_recomendacion(10)
    'NORMAL'
    """
    if score > PRIORIDAD_UMBRAL_URGENTE:
        return "URGENTE"
    if score > PRIORIDAD_UMBRAL_ALTA:
        return "ALTA"
    if score > PRIORIDAD_UMBRAL_MEDIA:
        return "MEDIA"
    return "NORMAL"


def normalizar_riesgo(valor: str) -> str:
    """El Excel a veces trae 'RIESGO' en vez de 'MEDIO' para el nivel medio.

    >>> normalizar_riesgo("RIESGO")
    'MEDIO'
    >>> normalizar_riesgo("alto")
    'ALTO'
    """
    v = str(valor).upper().strip()
    return "MEDIO" if v == "RIESGO" else v
