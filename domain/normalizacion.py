"""Normalización de nombres de auditores y tiendas.

Funciones puras: no dependen de Streamlit ni leen archivos. Reciben un
string y devuelven un string. Esto es lo que hace posible probarlas con
pytest sin levantar el dashboard.
"""
import re
import unicodedata

# Alias de usuarios técnicos (ej. nombres de usuario de SAP) a nombre real.
ALIAS_AUDITORES = {
    "jremacher":   "Joshué Remache",
    "equinga":     "Eliana Quinga",
    "jyuquilima":  "José Yuquilima",
    "palvarado":   "Pablo Alvarado",
}

# Variantes de mayúsculas/tildes conocidas -> forma canónica.
MAPEO_AUDITORES = {
    "JOSHUE REMACHE": "Joshué Remache",
    "JOSHUÉ REMACHE": "Joshué Remache",
    "JOSHUÈ REMACHE": "Joshué Remache",
    "JOSHUE REMACHE PABLO ALVARADO": "Joshué Remache",
    "ELIANA QUINGA":  "Eliana Quinga",
    "PABLO ALVARADO": "Pablo Alvarado",
    "JOSE YUQUILIMA": "José Yuquilima",
    "JOSÉ YUQUILIMA": "José Yuquilima",
    "JOEL CONTRERAS": "Joel Contreras",
    "MILTON BUESTAN": "Milton Buestan",
    "JOSE LUIS ROSERO": "José Luis Rosero",
}

# Auditores/valores que en realidad son referencias de informe mal
# extraídas y nunca deben tratarse como un auditor real.
AUDITORES_EXCLUIR = {"sin-referencia", "005-001", "BIKE SHOP DAULE V1"}


def normalizar_auditor(nombre) -> str:
    """Unifica variantes del mismo nombre de auditor.

    >>> normalizar_auditor("JOSHUE REMACHE")
    'Joshué Remache'
    >>> normalizar_auditor("jremacher")
    'Joshué Remache'
    >>> normalizar_auditor("")
    'Sin asignar'
    """
    if not nombre or str(nombre).strip() == "":
        return "Sin asignar"
    n = str(nombre).strip()
    if n.lower() in ALIAS_AUDITORES:
        return ALIAS_AUDITORES[n.lower()]
    upper = n.upper().strip()
    for k, v in MAPEO_AUDITORES.items():
        if upper == k.upper():
            return v
    # Fallback: si viene todo en mayúsculas, convertir a Title Case.
    if n == n.upper():
        return n.title()
    return n


def normalizar_clave_tienda(nombre) -> str:
    """Clave de comparación de tiendas: sin espacios, tildes ni mayúsculas.

    Existe porque el histórico usa "BIKE SHOP CUMBAYA" y el config de
    tiendas usa "BIKESHOP CUMBAYA" — sin esta normalización, un `.isin()`
    exacto descarta tiendas activas en silencio.

    >>> normalizar_clave_tienda("BIKE SHOP CUMBAYA") == normalizar_clave_tienda("BIKESHOP CUMBAYA")
    True
    """
    if nombre is None:
        return ""
    s = str(nombre).upper().strip()
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    s = re.sub(r"[^A-Z0-9]", "", s)
    return s
