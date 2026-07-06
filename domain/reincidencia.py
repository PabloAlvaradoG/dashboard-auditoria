"""Reincidencia: cuántas veces una tienda cayó en riesgo alto en 12 meses."""
import pandas as pd

from config.valores import VAL_RIESGO_ALTO, VAL_RIESGO_CRITICO
from config.umbrales import REINCIDENCIA_VENTANA_DIAS


def calcular_reincidencia(df: pd.DataFrame, col_almacen: str, col_fecha: str,
                           col_riesgo_norm: str, hoy: pd.Timestamp,
                           ventana_dias: int = REINCIDENCIA_VENTANA_DIAS) -> pd.Series:
    """Cuenta, por tienda, cuántas auditorías cayeron en riesgo ALTO/CRÍTICO
    dentro de la ventana de tiempo (por defecto, últimos 12 meses).

    Devuelve una Serie indexada por nombre de tienda -> conteo (int).
    Tiendas sin reincidencia no aparecen en el resultado (se debe hacer
    `.reindex(..., fill_value=0)` si se necesita el 0 explícito).
    """
    ventana = df[
        (df[col_fecha] >= hoy - pd.Timedelta(days=ventana_dias)) &
        (df[col_riesgo_norm].isin([VAL_RIESGO_ALTO, VAL_RIESGO_CRITICO]))
    ]
    return ventana.groupby(col_almacen).size()
