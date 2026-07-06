"""Tests de domain/reportes.py — subtotales de reportes jerárquicos.

Un subtotal mal sumado en un reporte de auditoría no es un bug visual,
es un error de auditoría. Por eso esto tiene su propia suite.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import pytest

from domain.reportes import (
    construir_tabla_jerarquica, TIPO_DETALLE, TIPO_SUBTOTAL,
    TIPO_TOTAL_GRUPO, TIPO_TOTAL_GENERAL,
)

COLS_DETALLE = ["Auditor", "Línea", "Tienda", "Monto"]
COLS_VALOR = ["Monto"]


def _df_ejemplo():
    return pd.DataFrame([
        {"Auditor": "Ana",  "Línea": "TCL",  "Tienda": "TCL Batán", "Monto": -100},
        {"Auditor": "Ana",  "Línea": "TCL",  "Tienda": "TCL Rio",   "Monto": -50},
        {"Auditor": "Ana",  "Línea": "Bike", "Tienda": "Bike A",    "Monto": -30},
        {"Auditor": "Luis", "Línea": "TCL",  "Tienda": "TCL Manta", "Monto": -20},
    ])


class TestTablaJerarquica:
    def test_estructura_de_filas(self):
        resultado = construir_tabla_jerarquica(_df_ejemplo(), "Auditor", "Línea", COLS_VALOR, COLS_DETALLE)
        tipos = resultado["_tipo_fila"].tolist()
        # 4 detalle + 2 subtotal (TCL-Ana, Bike-Ana, TCL-Luis = 3 en realidad) + 2 total_grupo + 1 total_general
        assert tipos.count(TIPO_DETALLE) == 4
        assert tipos.count(TIPO_SUBTOTAL) == 3       # TCL(Ana), Bike(Ana), TCL(Luis)
        assert tipos.count(TIPO_TOTAL_GRUPO) == 2    # Total Ana, Total Luis
        assert tipos.count(TIPO_TOTAL_GENERAL) == 1

    def test_subtotal_suma_correctamente(self):
        resultado = construir_tabla_jerarquica(_df_ejemplo(), "Auditor", "Línea", COLS_VALOR, COLS_DETALLE)
        subtotal_tcl_ana = resultado[
            (resultado["_tipo_fila"] == TIPO_SUBTOTAL) & (resultado["Línea"] == "Subtotal — TCL")
        ]
        assert subtotal_tcl_ana.iloc[0]["Monto"] == -150

    def test_total_por_auditor(self):
        resultado = construir_tabla_jerarquica(_df_ejemplo(), "Auditor", "Línea", COLS_VALOR, COLS_DETALLE)
        total_ana = resultado[resultado["Auditor"] == "Total Ana"]
        assert total_ana.iloc[0]["Monto"] == -180  # -100-50-30

    def test_total_general(self):
        resultado = construir_tabla_jerarquica(_df_ejemplo(), "Auditor", "Línea", COLS_VALOR, COLS_DETALLE)
        total_general = resultado[resultado["_tipo_fila"] == TIPO_TOTAL_GENERAL]
        assert total_general.iloc[0]["Monto"] == -200  # -180 + -20

    def test_valores_de_grupo_repetidos_quedan_en_blanco(self):
        resultado = construir_tabla_jerarquica(_df_ejemplo(), "Auditor", "Línea", COLS_VALOR, COLS_DETALLE)
        detalle = resultado[resultado["_tipo_fila"] == TIPO_DETALLE]
        # El orden real (alfabético por Auditor, luego Línea) es:
        # Ana/Bike/Bike A, Ana/TCL/TCL Batán, Ana/TCL/TCL Rio, Luis/TCL/TCL Manta
        fila_bike_a = detalle[detalle["Tienda"] == "Bike A"].iloc[0]
        assert fila_bike_a["Auditor"] == "Ana"   # primera fila de Ana -> sí trae el nombre
        assert fila_bike_a["Línea"] == "Bike"    # primera fila de este grupo Línea -> sí trae el nombre

        fila_tcl_rio = detalle[detalle["Tienda"] == "TCL Rio"].iloc[0]
        assert fila_tcl_rio["Auditor"] == ""     # mismo auditor que la fila anterior -> en blanco
        assert fila_tcl_rio["Línea"] == ""       # misma línea que la fila anterior -> en blanco

        fila_tcl_batan = detalle[detalle["Tienda"] == "TCL Batán"].iloc[0]
        assert fila_tcl_batan["Auditor"] == ""   # sigue siendo Ana -> en blanco
        assert fila_tcl_batan["Línea"] == "TCL"  # primera fila del NUEVO grupo Línea -> sí trae el nombre

        fila_manta = detalle[detalle["Tienda"] == "TCL Manta"].iloc[0]
        assert fila_manta["Auditor"] == "Luis"   # nuevo auditor -> sí trae el nombre
        assert fila_manta["Línea"] == "TCL"      # nuevo auditor implica nuevo grupo línea -> sí trae el nombre

    def test_df_vacio_devuelve_solo_total_en_cero(self):
        vacio = pd.DataFrame(columns=COLS_DETALLE)
        resultado = construir_tabla_jerarquica(vacio, "Auditor", "Línea", COLS_VALOR, COLS_DETALLE)
        assert len(resultado) == 1
        assert resultado.iloc[0]["_tipo_fila"] == TIPO_TOTAL_GENERAL
        assert resultado.iloc[0]["Monto"] == 0

    def test_un_solo_auditor_un_solo_grupo(self):
        df = pd.DataFrame([
            {"Auditor": "Ana", "Línea": "TCL", "Tienda": "X", "Monto": 10},
        ])
        resultado = construir_tabla_jerarquica(df, "Auditor", "Línea", COLS_VALOR, COLS_DETALLE)
        tipos = resultado["_tipo_fila"].tolist()
        assert tipos == [TIPO_DETALLE, TIPO_SUBTOTAL, TIPO_TOTAL_GRUPO, TIPO_TOTAL_GENERAL]
