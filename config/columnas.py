# ═══════════════════════════════════════════════════════════════════════
# CONSTANTES DE COLUMNAS
# ═══════════════════════════════════════════════════════════════════════
# Un solo lugar con el nombre exacto de cada columna tal como aparece en
# los archivos Excel de origen (o tal como se genera internamente).
#
# Por qué existe este archivo: antes del refactor, strings como
# "RESULT. A COBRAR COSTO" estaban escritos a mano 37 veces en app.py.
# Un typo, un acento faltante o un cambio de encabezado en el Excel
# rompía silenciosamente algún cálculo en un lugar aleatorio del código
# (ej. un `.get("...", 0)` que devuelve 0 en vez de fallar visiblemente).
#
# Regla de uso: en el resto del proyecto, NUNCA se escribe el nombre de
# una columna como string suelto — siempre se importa la constante de
# este archivo. Si el Excel cambia un encabezado, se corrige en un
# solo lugar.
# ═══════════════════════════════════════════════════════════════════════

# ───────────────────────────────────────────────
# Hoja "Registro_Auditorias" — columnas de origen
# ───────────────────────────────────────────────
COL_NUMERO               = "No."
COL_ALMACEN              = "ALMACÉN"
COL_SOCIEDAD             = "SOCIEDAD"
COL_LINEA                = "LÍNEA"
COL_ZONA                 = "ZONA"
COL_CENTRO_SAP           = "CE."
COL_AUDITOR              = "AUDITOR"
COL_TIPO_AUDITORIA       = "TIPO AUDITORÍA"
COL_REF_INFORME          = "REF. INFORME"
COL_FECHA_AUDITORIA      = "FECHA AUDITORÍA"
COL_FECHA_ENVIO          = "FECHA ENVÍO"
COL_VERSION              = "VERSIÓN"

COL_TOTAL_INVENTARIO_COSTO      = "TOTAL INVENTARIO COSTO"
COL_SOBRANTES_PVP               = "SOBRANTES PVP"
COL_FALTANTES_PVP               = "FALTANTES PVP"
COL_DIF_CRUCES_PVP              = "DIF. CRUCES PVP"
COL_MAL_ESTADO_CADUCADOS_PVP    = "MAL ESTADO CADUCADOS PVP"
COL_DEFECTOS_FABRICA_PVP        = "DEFECTOS FÁBRICA PVP"
COL_OTROS_PVP                   = "OTROS PVP"
COL_RESULT_NETO_PVP             = "RESULT. NETO PVP"
COL_RESULT_A_COBRAR_PVP         = "RESULT. A COBRAR PVP"
COL_RESULT_A_COBRAR_COSTO       = "RESULT. A COBRAR COSTO"
COL_AJUSTE_EGRESO_COSTO         = "AJUSTE EGRESO COSTO"
COL_AJUSTE_EGRESO_MAL_ESTADO    = "AJUSTE EGRESO MAL ESTADO"
COL_AJUSTE_EGRESO_DEFECTO_FAB   = "AJUSTE EGRESO DEFECTO FAB."
COL_AJUSTE_INGRESO_COSTO        = "AJUSTE INGRESO COSTO"
COL_TOTAL_COSTO_NETO            = "TOTAL COSTO NETO"

COL_RIESGO               = "RIESGO"
COL_SCORE                = "SCORE (0/100)"
COL_PEND_FACTURAR_COSTO  = "PEND. FACTURAR COSTO"
COL_ESTADO_REGISTRO      = "ESTADO REGISTRO"
COL_AJUSTE_SI_NO         = "Ajuste (Si/No)"
COL_OBSERVACIONES        = "OBSERVACIONES"
COL_VALOR_COBRADO        = "VALOR COBRADO"
COL_PCT_COBRO_VS_COSTO   = "% COBRO VS A COBRAR COSTO"
COL_ESTADO_COBRO         = "ESTADO COBRO"

# ───────────────────────────────────────────────
# Derivadas — calculadas en data/loader.py, no existen en el Excel
# ───────────────────────────────────────────────
COL_MES                  = "MES"
COL_MES_LABEL            = "MES_LABEL"
COL_DIAS_RESPUESTA       = "DÍAS RESPUESTA"
COL_FALTANTE_COSTO       = "FALTANTE COSTO"
COL_SOBRANTE_COSTO       = "SOBRANTE COSTO"
COL_MAL_ESTADO_COSTO     = "MAL ESTADO COSTO"
COL_DEFECTOS_COSTO       = "DEFECTOS COSTO"
COL_TIPO_AUDITOR         = "TIPO_AUDITOR"
COL_RIESGO_NORM          = "RIESGO_NORM"
COL_DIAS_SIN_AUDITAR     = "DÍAS SIN AUDITAR"
COL_PRIORIDAD_SCORE      = "PRIORIDAD_SCORE"
COL_REINCIDENCIA_12M     = "REINCIDENCIA_12M"

# ───────────────────────────────────────────────
# Hoja "Detalle_SKUs"
# ───────────────────────────────────────────────
COL_TIPO_HALLAZGO        = "TIPO HALLAZGO"
COL_MATERIAL_SKU         = "MATERIAL (SKU)"
COL_DESCRIPCION          = "DESCRIPCIÓN"
COL_CANTIDAD             = "CANTIDAD"
COL_COSTO_UNITARIO       = "COSTO UNITARIO"
COL_COSTO_TOTAL          = "COSTO TOTAL"
COL_PVP_UNITARIO         = "PVP UNITARIO"
COL_PVP_TOTAL            = "PVP TOTAL"

# ───────────────────────────────────────────────
# Hoja "Tiendas" (config de tiendas activas/cerradas)
# ───────────────────────────────────────────────
COL_CFG_CENTRO           = "Centro"
COL_CFG_NOMBRE_TIENDA    = "Nombre tienda"
COL_CFG_LINEA            = "Línea"
COL_CFG_EMPRESA          = "EMPRESA"
COL_CFG_AUDITOR_RESP     = "Auditor responsable"
COL_CFG_ZONA             = "Zona"
COL_CFG_ESTADO           = "Estado"
COL_CFG_FECHA            = "Fecha"
COL_CFG_CLAVE_TIENDA     = "_CLAVE_TIENDA"   # clave normalizada interna, no viene del Excel

# ───────────────────────────────────────────────
# Hoja "Correos auditores"
# ───────────────────────────────────────────────
COL_CFG_TIPO_AUDITOR     = "Tipo auditor"
COL_CFG_CORREO           = "Correo"
