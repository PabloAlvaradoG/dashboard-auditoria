"""Reportes jerárquicos con subtotales — estilo papel de trabajo de auditoría.

Construye tablas tipo "Auditor > Línea > Tienda" con una fila de subtotal
al cierre de cada grupo intermedio y un total general al final. Es lógica
pura de pandas (sin Streamlit) para poder probarla con pytest — un reporte
que suma mal un subtotal es un error de auditoría, no solo un bug visual.
"""
from dataclasses import dataclass, field

import pandas as pd

TIPO_DETALLE = "detalle"
TIPO_SUBTOTAL = "subtotal"
TIPO_TOTAL_GRUPO = "total_grupo"
TIPO_TOTAL_GENERAL = "total_general"


def construir_tabla_jerarquica(
    df: pd.DataFrame,
    col_grupo1: str,
    col_grupo2: str,
    cols_valor: list,
    cols_detalle: list,
    etiqueta_total_general: str = "TOTAL GENERAL",
    orden_extra: list | None = None,
) -> pd.DataFrame:
    """Agrupa `df` por `col_grupo1` (ej. Auditor) y, dentro de cada uno,
    por `col_grupo2` (ej. Línea), insertando:

    - una fila de subtotal al cierre de cada grupo2 (suma de `cols_valor`)
    - una fila de total al cierre de cada grupo1 (suma de todo el grupo1)
    - una fila de total general al final (suma de todo `df`)

    `cols_detalle` son las columnas que se muestran en las filas de detalle
    (deben incluir `col_grupo1`, `col_grupo2` y `cols_valor`). `orden_extra`
    son columnas adicionales para ordenar DENTRO de cada grupo2 (ej. nombre
    de tienda o fecha) — el orden es estable, así que si no se especifica
    se respeta el orden original de `df`. El resultado trae una columna
    extra `_tipo_fila` (detalle/subtotal/total_grupo/total_general) para
    que la capa de presentación decida cómo pintarla, sin tener que volver
    a inferir la lógica de agrupación.

    Los valores de `col_grupo1`/`col_grupo2` se dejan en blanco ("") en las
    filas de detalle que repiten el mismo grupo que la fila anterior —
    el patrón clásico de un papel de trabajo, para no repetir "Pablo
    Alvarado" en cada una de sus 80 filas.

    Si `df` está vacío, devuelve una tabla con solo la fila de total general
    en cero (nunca una tabla vacía sin fila de total).
    """
    columnas_salida = cols_detalle + ["_tipo_fila"]

    if len(df) == 0:
        fila_vacia = {c: (0 if c in cols_valor else "") for c in cols_detalle}
        fila_vacia[col_grupo1] = etiqueta_total_general
        fila_vacia["_tipo_fila"] = TIPO_TOTAL_GENERAL
        return pd.DataFrame([fila_vacia])[columnas_salida]

    claves_orden = [col_grupo1, col_grupo2] + (orden_extra or [])
    df = df.sort_values(claves_orden, kind="stable").reset_index(drop=True)

    filas = []
    grupo1_anterior = None
    grupo2_anterior = None

    def _fila_agregada(valores_grupo, etiqueta, col_etiqueta, tipo):
        fila = {c: "" for c in cols_detalle}
        fila[col_etiqueta] = etiqueta
        for c in cols_valor:
            fila[c] = valores_grupo[c].sum()
        fila["_tipo_fila"] = tipo
        return fila

    buffer_grupo2 = []
    buffer_grupo1 = []

    def _cerrar_grupo2():
        if buffer_grupo2:
            sub_df = pd.DataFrame(buffer_grupo2)
            filas.append(_fila_agregada(sub_df, f"Subtotal — {grupo2_anterior}", col_grupo2, TIPO_SUBTOTAL))

    def _cerrar_grupo1():
        _cerrar_grupo2()
        if buffer_grupo1:
            tot_df = pd.DataFrame(buffer_grupo1)
            filas.append(_fila_agregada(tot_df, f"Total {grupo1_anterior}", col_grupo1, TIPO_TOTAL_GRUPO))

    for _, row in df.iterrows():
        g1, g2 = row[col_grupo1], row[col_grupo2]

        if grupo1_anterior is not None and g1 != grupo1_anterior:
            _cerrar_grupo1()
            buffer_grupo1 = []
            buffer_grupo2 = []
            grupo2_anterior = None
        elif grupo2_anterior is not None and g2 != grupo2_anterior:
            _cerrar_grupo2()
            buffer_grupo2 = []

        fila_detalle = {c: row.get(c, "") for c in cols_detalle}
        fila_detalle[col_grupo1] = g1 if g1 != grupo1_anterior else ""
        fila_detalle[col_grupo2] = g2 if g2 != grupo2_anterior else ""
        fila_detalle["_tipo_fila"] = TIPO_DETALLE
        filas.append(fila_detalle)

        buffer_grupo1.append(row)
        buffer_grupo2.append(row)
        grupo1_anterior, grupo2_anterior = g1, g2

    _cerrar_grupo1()

    fila_total_general = _fila_agregada(df, etiqueta_total_general, col_grupo1, TIPO_TOTAL_GENERAL)
    filas.append(fila_total_general)

    return pd.DataFrame(filas)[columnas_salida]
