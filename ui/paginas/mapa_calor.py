"""Página 04 — Mapa de Calor.

Primera pestaña migrada al patrón `render(dff)`: recibe el DataFrame ya
filtrado por el sidebar (zona/línea/auditor/riesgo/fechas) y dibuja toda
la página. No depende de ninguna variable global de app.py — todo lo que
necesita entra por parámetro o se importa explícitamente.

Este archivo es la prueba de concepto de cómo quedarían las otras 9
páginas si se completa la migración.
"""
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from config.columnas import (
    COL_ALMACEN, COL_ZONA, COL_LINEA, COL_TOTAL_INVENTARIO_COSTO,
    COL_SCORE, COL_RIESGO_NORM, COL_RESULT_A_COBRAR_COSTO,
)
from config.estilos import C_RED
from config.umbrales import HEATMAP_UMBRAL_ROJO_DEFAULT, HEATMAP_PASO_SEMAFORO_DEFAULT
from domain.formato import fmt_money
from ui.componentes import titulo_seccion
from ui.exportar import download_button_excel


def render(dff: pd.DataFrame) -> None:
    titulo_seccion("Mapa de Calor — Todas las Tiendas")

    heat_col0, heat_col1, heat_col2, heat_col3 = st.columns([1.3, 1, 1, 2])
    with heat_col0:
        metrica_color = st.selectbox(
            "Colorear por", ["A Cobrar (Costo)", "Score de Riesgo"],
            help="Cambia qué variable define el color de cada tienda en el mapa"
        )
    with heat_col1:
        rango_min = st.number_input("Umbral rojo (desde)", value=HEATMAP_UMBRAL_ROJO_DEFAULT, step=500,
                                     help="Valores menores a este umbral se marcan en rojo")
    with heat_col2:
        rango_step = st.number_input("Paso semáforo ($)", value=HEATMAP_PASO_SEMAFORO_DEFAULT,
                                      min_value=100, step=100,
                                      help="Intervalo entre verde, amarillo y rojo")
    with heat_col3:
        st.markdown(f"""<div style="font-size:11px;color:#666;margin-top:28px;">
          🟢 ≥ {fmt_money(0)} &nbsp;·&nbsp;
          🟡 {fmt_money(rango_min + rango_step)} a {fmt_money(0)} &nbsp;·&nbsp;
          🔴 &lt; {fmt_money(rango_min)}
        </div>""", unsafe_allow_html=True)

    heat_df = dff.copy()
    heat_df["COBRAR_COSTO"] = pd.to_numeric(heat_df.get(COL_RESULT_A_COBRAR_COSTO, 0), errors="coerce").fillna(0)
    heat_df["SCORE_NUM"]    = pd.to_numeric(heat_df.get(COL_SCORE, 0), errors="coerce").fillna(0)

    if metrica_color == "A Cobrar (Costo)":
        color_col, color_scale, color_mid, color_titulo = (
            "COBRAR_COSTO", ["#E24B4A", "#EF9F27", "#FFFF88", "#639922"], rango_min / 2, "A Cobrar Costo")
    else:
        color_col, color_scale, color_mid, color_titulo = (
            "SCORE_NUM", ["#639922", "#FFFF88", "#EF9F27", "#E24B4A"], 50, "Score de Riesgo")

    fig = px.treemap(heat_df, path=[px.Constant("Todas"), COL_ZONA, COL_LINEA, COL_ALMACEN],
                      values=COL_TOTAL_INVENTARIO_COSTO,
                      color=color_col,
                      color_continuous_scale=color_scale,
                      color_continuous_midpoint=color_mid,
                      hover_data={"COBRAR_COSTO": ":$,.2f", COL_SCORE: ":.1f"})
    fig.update_layout(height=420, margin=dict(l=0, r=0, t=10, b=0),
                       coloraxis_colorbar=dict(title=color_titulo,
                                                tickprefix="$" if color_col == "COBRAR_COSTO" else ""))
    st.plotly_chart(fig, use_container_width=True)

    # Foco rápido: las 5 tiendas más críticas del período, para lectura gerencial directa
    top_criticas = heat_df.nsmallest(5, "COBRAR_COSTO")[[COL_ALMACEN, COL_ZONA, "COBRAR_COSTO", "SCORE_NUM"]]
    if len(top_criticas) > 0 and top_criticas["COBRAR_COSTO"].min() < 0:
        titulo_seccion("🔴 Focos Rojos — Top 5 del Período")
        cols_focos = st.columns(len(top_criticas))
        for i, (_, r) in enumerate(top_criticas.iterrows()):
            with cols_focos[i]:
                st.markdown(f"""<div class="kpi-card" style="border-top-color:{C_RED};padding:10px">
                  <div style="font-size:11px;font-weight:600;color:#1a1a2e">{r[COL_ALMACEN][:22]}</div>
                  <div style="font-size:10px;color:#999">{r[COL_ZONA]}</div>
                  <div style="font-size:15px;font-weight:700;color:{C_RED};margin-top:4px">{fmt_money(r['COBRAR_COSTO'])}</div>
                  <div style="font-size:10px;color:#999">Score {r['SCORE_NUM']:.0f}</div>
                </div>""", unsafe_allow_html=True)

    tabla_heat = heat_df[[COL_ALMACEN, COL_ZONA, COL_LINEA, "COBRAR_COSTO",
                           COL_TOTAL_INVENTARIO_COSTO, COL_SCORE, COL_RIESGO_NORM]].copy()
    tabla_heat = tabla_heat.rename(columns={
        "COBRAR_COSTO": "A Cobrar Costo",
        COL_TOTAL_INVENTARIO_COSTO: "Inventario Costo",
        COL_SCORE: "Score", COL_RIESGO_NORM: "Riesgo",
    })

    umbral_rojo = rango_min
    umbral_amarillo = rango_min + rango_step

    def color_costo(val):
        try:
            v = float(val)
            if v < umbral_rojo:
                return "background-color:#FFCCCC"
            elif v < umbral_amarillo:
                return "background-color:#FFE5CC"
            elif v < 0:
                return "background-color:#FFFACC"
            return "background-color:#D5F5E3"
        except (TypeError, ValueError):
            return ""

    tot_h = pd.DataFrame([{COL_ALMACEN: "TOTAL", COL_ZONA: "—", COL_LINEA: "—",
        "A Cobrar Costo": heat_df["COBRAR_COSTO"].sum(),
        "Inventario Costo": heat_df[COL_TOTAL_INVENTARIO_COSTO].sum(),
        "Score": round(heat_df[COL_SCORE].mean(), 1), "Riesgo": "—"}])
    tabla_heat_full = pd.concat([tabla_heat, tot_h], ignore_index=True)

    st.dataframe(
        tabla_heat_full.style
            .map(color_costo, subset=["A Cobrar Costo"])
            .format({"A Cobrar Costo": "${:,.2f}", "Inventario Costo": "${:,.2f}", "Score": "{:.1f}"}),
        use_container_width=True, hide_index=True,
    )
    download_button_excel(tabla_heat_full, f"mapa_calor_{datetime.today().strftime('%Y%m%d')}.xlsx",
                           "⬇ Exportar tabla tiendas", money_cols=["A Cobrar Costo", "Inventario Costo"])
