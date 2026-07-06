"""Ciclos de evaluación de auditores: del día 26 al 25 de cada mes."""
import pandas as pd

MESES_ES = {1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
            7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"}


def generar_ciclos_26_25(inicio_rango, fin_rango, dia_inicio=26, dia_fin=25):
    """Genera tuplas (inicio, fin) de ciclos que cubren el rango dado.

    >>> ciclos = generar_ciclos_26_25("2026-01-01", "2026-03-01")
    >>> [(i.strftime('%Y-%m-%d'), f.strftime('%Y-%m-%d')) for i, f in ciclos]
    [('2025-12-26', '2026-01-25'), ('2026-01-26', '2026-02-25'), ('2026-02-26', '2026-03-25')]
    """
    ciclos = []
    cursor = pd.Timestamp(inicio_rango)
    ini = (cursor.replace(day=dia_inicio) if cursor.day >= dia_inicio
           else (cursor - pd.DateOffset(months=1)).replace(day=dia_inicio))
    fin_rango_ts = pd.Timestamp(fin_rango)
    while ini <= fin_rango_ts:
        fin = (ini + pd.DateOffset(months=1)).replace(day=dia_fin)
        ciclos.append((ini, fin))
        ini = ini + pd.DateOffset(months=1)
    return ciclos


def label_ciclo(ini, fin) -> str:
    """Etiqueta legible de un ciclo.

    >>> label_ciclo(pd.Timestamp('2026-05-26'), pd.Timestamp('2026-06-25'))
    '26 May – 25 Jun 2026'
    """
    return f"{ini.day} {MESES_ES[ini.month]} – {fin.day} {MESES_ES[fin.month]} {fin.year}"
