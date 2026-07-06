"""Componentes de UI reutilizables.

Antes de este archivo, la tarjeta `<div class="kpi-card">...` estaba
copiada a mano 47 veces en app.py, cada una con ligeras variaciones.
Cambiar el diseño de las tarjetas significaba editar 47 lugares — y de
hecho ya vimos bugs de copy-paste en este proyecto por ese patrón
(la fila TOTAL con llaves de diccionario que no coincidían).
"""
import streamlit as st


def tarjeta_kpi(contenedor, titulo: str, valor, color_borde: str,
                 subtitulo: str = "", clase_valor: str = "neu",
                 color_valor: str | None = None) -> None:
    """Dibuja una tarjeta KPI estándar dentro de `contenedor`.

    - `contenedor`: el objeto de columna de Streamlit (ej. `c1`) o `st` mismo.
    - `clase_valor`: "neu" (neutro), "pos" (positivo/verde) o "neg" (negativo/rojo)
      — controla el color por CSS. Se ignora si se pasa `color_valor`.
    - `color_valor`: color explícito para el valor (ej. un semáforo dinámico
      que no es simplemente pos/neg/neu).

    Ejemplo — antes:
        c1.markdown(f'<div class="kpi-card" style="border-top-color:{C_BLUE}">'
                     f'<div class="kpi-label">Auditorías</div>'
                     f'<div class="kpi-value neu">{n_aud}</div>'
                     f'<div class="kpi-sub">Período seleccionado</div></div>',
                     unsafe_allow_html=True)

    Ahora:
        tarjeta_kpi(c1, "Auditorías", n_aud, C_BLUE, "Período seleccionado")
    """
    estilo_valor = f' style="color:{color_valor}"' if color_valor else ""
    contenedor.markdown(
        f'<div class="kpi-card" style="border-top-color:{color_borde}">'
        f'<div class="kpi-label">{titulo}</div>'
        f'<div class="kpi-value {clase_valor}"{estilo_valor}>{valor}</div>'
        f'<div class="kpi-sub">{subtitulo}</div></div>',
        unsafe_allow_html=True,
    )


def titulo_seccion(texto: str) -> None:
    """Encabezado de sección estándar (antes: 51 `st.markdown` idénticos)."""
    st.markdown(f'<div class="section-title">{texto}</div>', unsafe_allow_html=True)


def tabla_con_fila_total(df, fila_total: dict, **kwargs_dataframe):
    """Concatena una fila TOTAL a un DataFrame ya formateado y lo muestra.

    `fila_total` debe tener EXACTAMENTE las mismas llaves que las columnas
    de `df` — si no coinciden, pandas las agrega como columnas nuevas con
    NaN en vez de fallar, que es exactamente el bug que ya tuvimos en las
    tablas de Auditores y Líneas de Negocio. Por eso esta función valida
    las llaves antes de concatenar.
    """
    import pandas as pd

    columnas_df = set(df.columns)
    columnas_total = set(fila_total.keys())
    if columnas_df != columnas_total:
        faltan = columnas_df - columnas_total
        sobran = columnas_total - columnas_df
        raise ValueError(
            f"fila_total no coincide con las columnas de df. "
            f"Faltan en fila_total: {faltan}. Sobran en fila_total: {sobran}."
        )
    df_full = pd.concat([df, pd.DataFrame([fila_total])], ignore_index=True)
    st.dataframe(df_full, use_container_width=True, hide_index=True, **kwargs_dataframe)
    return df_full
