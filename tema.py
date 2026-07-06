"""Tema visual central del dashboard.

Un solo lugar que define cómo se ven TODOS los gráficos de Plotly:
tipografía, colores de fondo, líneas de grilla, y esquinas redondeadas
en barras. Se registra una vez al arrancar la app (`aplicar_tema()`) y
Plotly lo aplica automáticamente a cada gráfico nuevo — no hace falta
tocar cada uno de los +40 `go.Figure`/`px.bar` del dashboard uno por uno.

Antes: cada gráfico definía su propio `plot_bgcolor`, fuente y grilla
a mano, con pequeñas inconsistencias entre pestañas. Ahora: un tema,
aplicado en todos lados por igual.
"""
import plotly.graph_objects as go
import plotly.io as pio

from config.estilos import (
    C_RED, C_AMBER, C_GREEN, C_BLUE, C_NAVY, C_TEAL, C_PURPLE,
)

# Superficie de los gráficos: un blanco cálido apenas distinto del fondo
# de la página (#F4F6F9), para que el gráfico "flote" sutilmente sobre
# el card sin un corte duro de color.
SURFACE = "#FFFFFF"
GRIDLINE = "#E7ECF3"
AXISLINE = "#C9D3E0"
INK = "#2C3E50"
INK_MUTED = "#7C8A9C"

FONT_FAMILY = "'Inter', 'Segoe UI', -apple-system, sans-serif"

# Paleta categórica (para gráficos con varias series/líneas de negocio):
# se prioriza contraste y que cada color siga significando lo mismo en
# toda la app (no es una paleta "arcoíris" genérica).
COLORWAY = [C_BLUE, C_TEAL, C_AMBER, C_PURPLE, C_RED, C_GREEN, "#8E5B3F", "#5B6470", "#B0578D"]


def aplicar_tema() -> None:
    """Registra el template 'auditoria' y lo deja como default de Plotly.

    Llamar una sola vez, al arrancar app.py, antes de crear cualquier
    figura.
    """
    template = go.layout.Template(
        layout=go.Layout(
            font=dict(family=FONT_FAMILY, size=12, color=INK),
            title=dict(font=dict(family=FONT_FAMILY, size=13, color=C_NAVY)),
            paper_bgcolor=SURFACE,
            plot_bgcolor=SURFACE,
            colorway=COLORWAY,
            xaxis=dict(
                gridcolor=GRIDLINE, zerolinecolor=GRIDLINE,
                showline=True, linecolor=AXISLINE, linewidth=1,
                tickfont=dict(color=INK_MUTED, size=11),
            ),
            yaxis=dict(
                gridcolor=GRIDLINE, zerolinecolor=GRIDLINE,
                showline=False, tickfont=dict(color=INK_MUTED, size=11),
            ),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11, color=INK_MUTED)),
            hoverlabel=dict(
                bgcolor=C_NAVY, font=dict(family=FONT_FAMILY, color="white", size=12),
                bordercolor=C_NAVY,
            ),
            margin=dict(t=20),
        ),
        data=dict(
            # Esquinas redondeadas en TODAS las barras del dashboard, sin
            # tener que tocar cada llamada a go.Bar()/px.bar() una por una.
            bar=[go.Bar(marker=dict(cornerradius=4))],
            scatter=[go.Scatter(line=dict(width=2.5))],
        ),
    )
    pio.templates["auditoria"] = template
    pio.templates.default = "auditoria"
