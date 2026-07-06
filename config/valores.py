# ═══════════════════════════════════════════════════════════════════════
# CONSTANTES DE VALORES CATEGÓRICOS
# ═══════════════════════════════════════════════════════════════════════
# Los valores que puede tomar una columna categórica (Estado, Riesgo,
# Tipo de auditor...). Centralizarlos evita, por ejemplo, comparar
# "Retail" en un lugar y "RETAIL" en otro sin que nadie lo note.
# ═══════════════════════════════════════════════════════════════════════

# Estado de tienda (hoja "Tiendas") — se normalizan siempre a MAYÚSCULAS
VAL_TIENDA_ACTIVA   = "ACTIVA"
VAL_TIENDA_CERRADA  = "CERRADA"

# Riesgo normalizado (RIESGO_NORM)
VAL_RIESGO_CRITICO  = "CRÍTICO"
VAL_RIESGO_ALTO     = "ALTO"
VAL_RIESGO_MEDIO    = "MEDIO"
VAL_RIESGO_BAJO     = "BAJO"
RIESGOS_ORDENADOS   = [VAL_RIESGO_CRITICO, VAL_RIESGO_ALTO, VAL_RIESGO_MEDIO, VAL_RIESGO_BAJO]

# Valor crudo que a veces trae la columna RIESGO cuando no trae calificador
# (ej. "🟡 RIESGO" sin "MEDIO/ALTO/BAJO" después) — se interpreta como MEDIO.
# Es un VALOR de celda, no debe confundirse con el nombre de columna "RIESGO".
VAL_RIESGO_SIN_CALIFICAR = "RIESGO"

# Tipo de auditor (hoja "Correos auditores")
VAL_TIPO_RETAIL         = "Retail"
VAL_TIPO_CORAL          = "Coral"
VAL_TIPO_SIN_CLASIFICAR = "Sin clasificar"

# Estado de cobro (columna ESTADO COBRO)
VAL_COBRO_PENDIENTE  = "Pendiente"
VAL_COBRO_NO_APLICA  = "No Aplica"

# Estado de registro (columna ESTADO REGISTRO)
VAL_REGISTRO_AUTOMATICO   = "Registro automático"
VAL_REGISTRO_PROCESADO    = "Procesado - Cobrado"
VAL_REGISTRO_RRHH         = "Pasado a RRHH para cobro"
VAL_REGISTRO_EN_APROBACION = "En proceso de aprobación de ajustes"

# Ajuste (Si/No)
VAL_AJUSTE_SI = "Si"
VAL_AJUSTE_NO = "No"
