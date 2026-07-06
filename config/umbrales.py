# ═══════════════════════════════════════════════════════════════════════
# UMBRALES Y CONSTANTES DE NEGOCIO
# ═══════════════════════════════════════════════════════════════════════
# Cualquier número que representa una REGLA DE NEGOCIO (una meta, un
# umbral de riesgo, un peso de fórmula) vive aquí — nunca como un número
# suelto ("mágico") dentro de una fórmula en medio del código de una
# pestaña. Si gerencia decide mañana que la meta ya no es 12 auditorías
# sino 15, se cambia UNA línea, no se busca en 2,000 líneas de código.
# ═══════════════════════════════════════════════════════════════════════

# ── KPI Auditores: ciclo de evaluación y meta mensual ──
CICLO_DIA_INICIO           = 26   # el ciclo de evaluación arranca el día 26...
CICLO_DIA_FIN              = 25   # ...y cierra el 25 del mes siguiente
META_AUDITORIAS_RETAIL     = 12   # auditorías/mes esperadas, solo aplica a Retail

# Semáforo de % de cumplimiento de meta (KPI Auditores)
CUMPLIMIENTO_UMBRAL_ROJO   = 50   # < 50%  -> rojo
CUMPLIMIENTO_UMBRAL_VERDE  = 90   # >= 90% -> verde (entre medio: amarillo)

# ── Mapa de Calor: semáforo de "A Cobrar (Costo)" por tienda ──
HEATMAP_UMBRAL_ROJO_DEFAULT = -5000   # valor por defecto del filtro (editable en pantalla)
HEATMAP_PASO_SEMAFORO_DEFAULT = 1000

# ── Score de prioridad de auditoría (Prioridades IA) ──
# PRIORIDAD_SCORE = DÍAS_SIN_AUDITAR * PESO_DIAS
#                  + SCORE_RIESGO    * PESO_SCORE
#                  + |A_COBRAR_COSTO| * PESO_MONTO
PRIORIDAD_PESO_DIAS   = 0.4
PRIORIDAD_PESO_SCORE  = 1.5
PRIORIDAD_PESO_MONTO  = 0.015

PRIORIDAD_UMBRAL_URGENTE = 150
PRIORIDAD_UMBRAL_ALTA    = 80
PRIORIDAD_UMBRAL_MEDIA   = 40

# ── Reincidencia: ventana de análisis ──
REINCIDENCIA_VENTANA_DIAS = 365   # "reincidencia en los últimos 12 meses"

# ── Cobertura de auditoría: umbrales de días sin auditar ──
COBERTURA_DIAS_CORTO  = 90    # % de tiendas activas auditadas en <= 90 días
COBERTURA_DIAS_LARGO  = 180   # % de tiendas activas auditadas en <= 180 días
COBERTURA_PCT_VERDE_90D   = 80
COBERTURA_PCT_AMBAR_90D   = 50
COBERTURA_PCT_VERDE_180D  = 90
COBERTURA_PCT_AMBAR_180D  = 70

# ── Aging del cobro pendiente (Gestión de Cobro) ──
AGING_BUCKETS_DIAS = [0, 30, 60, 90]   # bordes de los buckets 0-30/31-60/61-90/+90
AGING_ETIQUETAS    = ["0-30 días", "31-60 días", "61-90 días", "+90 días"]

# ── Gestión de Cobro: año desde el que existe el indicador ──
COBRO_ANIO_INICIO_INDICADOR = 2026
