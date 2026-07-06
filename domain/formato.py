"""Formateo de moneda y conversión texto<->número.

Estas dos funciones son el punto único de verdad de cómo se ve un monto
en pantalla ("$-1,234.56") y cómo se revierte a número real al exportar
a Excel. Antes de este refactor, exportar mal el signo negativo
("$-1,234.56" leído como positivo) fue un bug real que llegó a producción.
"""


def fmt_money(v) -> str:
    """Formatea un número como moneda: 2 decimales, signo antes del $.

    >>> fmt_money(1234.5)
    '$1,234.50'
    >>> fmt_money(-1234.5)
    '-$1,234.50'
    """
    try:
        v = float(v)
        return f"${v:,.2f}" if v >= 0 else f"-${abs(v):,.2f}"
    except (TypeError, ValueError):
        return str(v)


def texto_a_numero(v):
    """Convierte '$-1,234.56' -> -1234.56. Deja pasar valores ya numéricos.

    FIX histórico: fmt_money produce el signo DESPUÉS del símbolo $
    ("$-1,234.56"), así que hay que quitar "$" y "," primero y recién ahí
    revisar el signo — revisarlo antes de quitar el $ siempre daba False.

    >>> texto_a_numero("$-1,234.56")
    -1234.56
    >>> texto_a_numero("$500.00")
    500.0
    >>> texto_a_numero(42)
    42
    """
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return v
    s = str(v).strip()
    if s in ("", "—", "-", "nan", "None"):
        return None
    s = s.replace("$", "").replace(",", "").strip()
    neg = s.startswith("-")
    s = s.lstrip("-").strip()
    try:
        val = float(s)
        return -val if neg else val
    except ValueError:
        return v
