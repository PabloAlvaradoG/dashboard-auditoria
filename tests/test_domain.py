"""Tests de la lógica de negocio pura (domain/).

Correr con: pytest tests/ -v
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import pytest

from domain.normalizacion import normalizar_auditor, normalizar_clave_tienda
from domain.formato import fmt_money, texto_a_numero
from domain.ciclos import generar_ciclos_26_25, label_ciclo
from domain.kpi_auditores import calcular_meta, calcular_cumplimiento, clasificar_semaforo
from domain.scoring import calcular_prioridad_score, clasificar_recomendacion, normalizar_riesgo
from domain.reincidencia import calcular_reincidencia
from domain.cobertura import calcular_cobertura
from domain.aging import clasificar_aging


# ── normalizacion ──
class TestNormalizacion:
    def test_variantes_mismo_auditor(self):
        variantes = ["JOSHUE REMACHE", "Joshué Remache", "JOSHUÉ REMACHE", "jremacher"]
        resultados = {normalizar_auditor(v) for v in variantes}
        assert resultados == {"Joshué Remache"}

    def test_auditor_vacio(self):
        assert normalizar_auditor("") == "Sin asignar"
        assert normalizar_auditor(None) == "Sin asignar"

    def test_auditor_desconocido_todo_mayus_se_titulariza(self):
        assert normalizar_auditor("JUAN PEREZ") == "Juan Perez"

    def test_auditor_desconocido_mixto_queda_igual(self):
        assert normalizar_auditor("Juan Pérez") == "Juan Pérez"

    def test_clave_tienda_ignora_espacios_tildes_mayusculas(self):
        assert normalizar_clave_tienda("BIKE SHOP CUMBAYA") == normalizar_clave_tienda("BIKESHOP CUMBAYA")
        assert normalizar_clave_tienda("Motoshop Monay") == normalizar_clave_tienda("MOTOSHOP  MONAY")

    def test_clave_tienda_distingue_tiendas_distintas(self):
        assert normalizar_clave_tienda("TCL BATAN") != normalizar_clave_tienda("TCL RIO")


# ── formato ──
class TestFormato:
    @pytest.mark.parametrize("valor,esperado", [
        (1234.5, "$1,234.50"),
        (-1234.5, "-$1,234.50"),
        (0, "$0.00"),
    ])
    def test_fmt_money(self, valor, esperado):
        assert fmt_money(valor) == esperado

    def test_texto_a_numero_negativo_con_signo_despues_del_simbolo(self):
        # Caso real que causó un bug en producción: el signo va DESPUÉS del $
        assert texto_a_numero("$-1,234.56") == -1234.56

    def test_texto_a_numero_positivo(self):
        assert texto_a_numero("$500.00") == 500.0

    def test_texto_a_numero_ya_numerico_pasa_igual(self):
        assert texto_a_numero(42) == 42
        assert texto_a_numero(-3.5) == -3.5

    def test_texto_a_numero_vacio_o_guion(self):
        assert texto_a_numero("—") is None
        assert texto_a_numero("") is None


# ── ciclos ──
class TestCiclos:
    def test_genera_ciclo_que_contiene_fecha_dada(self):
        ciclos = generar_ciclos_26_25("2026-06-10", "2026-06-10")
        assert len(ciclos) == 1
        ini, fin = ciclos[0]
        assert ini == pd.Timestamp("2026-05-26")
        assert fin == pd.Timestamp("2026-06-25")

    def test_genera_multiples_ciclos_consecutivos(self):
        ciclos = generar_ciclos_26_25("2026-01-01", "2026-03-15")
        assert len(ciclos) == 3

    def test_label_ciclo(self):
        assert label_ciclo(pd.Timestamp("2026-05-26"), pd.Timestamp("2026-06-25")) == "26 May – 25 Jun 2026"


# ── kpi_auditores: el más sensible, evalúa desempeño real de personas ──
class TestKPIAuditores:
    def test_meta_solo_aplica_a_retail(self):
        assert calcular_meta("Retail") == 12
        assert calcular_meta("Coral") is None
        assert calcular_meta("Sin clasificar") is None

    def test_cumplimiento_100_por_ciento(self):
        c = calcular_cumplimiento("X", "Retail", realizadas=12, dias_transcurridos=30, dias_totales_ciclo=30)
        assert c.cumplimiento_real == 100.0

    def test_cumplimiento_50_por_ciento(self):
        c = calcular_cumplimiento("X", "Retail", realizadas=6, dias_transcurridos=30, dias_totales_ciclo=30)
        assert c.cumplimiento_real == 50.0

    def test_cero_auditorias_es_cero_no_error(self):
        c = calcular_cumplimiento("X", "Retail", realizadas=0, dias_transcurridos=15, dias_totales_ciclo=30)
        assert c.cumplimiento_real == 0.0
        assert c.cumplimiento_proyectado == 0.0

    def test_coral_no_tiene_meta_ni_cumplimiento(self):
        c = calcular_cumplimiento("X", "Coral", realizadas=5, dias_transcurridos=15, dias_totales_ciclo=30)
        assert c.meta is None
        assert c.cumplimiento_real is None
        assert c.cumplimiento_proyectado is None

    def test_proyeccion_al_ritmo_actual(self):
        # 6 auditorías en 15 días de un ciclo de 30 -> ritmo de 12 al cierre
        c = calcular_cumplimiento("X", "Retail", realizadas=6, dias_transcurridos=15, dias_totales_ciclo=30)
        assert c.proyeccion_cierre == 12.0
        assert c.cumplimiento_proyectado == 100.0

    def test_dias_transcurridos_cero_no_divide_por_cero(self):
        c = calcular_cumplimiento("X", "Retail", realizadas=0, dias_transcurridos=0, dias_totales_ciclo=30)
        assert c.proyeccion_cierre == 0.0

    @pytest.mark.parametrize("pct,esperado", [
        (None, "no_aplica"),
        (10, "rojo"),
        (49.9, "rojo"),
        (50, "amarillo"),
        (89.9, "amarillo"),
        (90, "verde"),
        (150, "verde"),
    ])
    def test_semaforo(self, pct, esperado):
        assert clasificar_semaforo(pct, umbral_rojo=50, umbral_verde=90) == esperado


# ── scoring ──
class TestScoring:
    def test_prioridad_score_combina_los_tres_factores(self):
        score = calcular_prioridad_score(dias_sin_auditar=100, score_riesgo=20, monto_a_cobrar_costo=-1000)
        assert score == pytest.approx(100 * 0.4 + 20 * 1.5 + 1000 * 0.015)

    def test_prioridad_score_usa_valor_absoluto_del_monto(self):
        # Un monto a favor (positivo) también debe sumar prioridad, no restar
        score_negativo = calcular_prioridad_score(0, 0, -1000)
        score_positivo = calcular_prioridad_score(0, 0, 1000)
        assert score_negativo == score_positivo

    @pytest.mark.parametrize("score,esperado", [
        (200, "URGENTE"), (100, "ALTA"), (50, "MEDIA"), (10, "NORMAL"),
    ])
    def test_clasificar_recomendacion(self, score, esperado):
        assert clasificar_recomendacion(score) == esperado

    def test_normalizar_riesgo_traduce_riesgo_a_medio(self):
        assert normalizar_riesgo("RIESGO") == "MEDIO"
        assert normalizar_riesgo("alto") == "ALTO"


# ── reincidencia ──
class TestReincidencia:
    def test_cuenta_solo_dentro_de_la_ventana_y_en_riesgo_alto(self):
        hoy = pd.Timestamp("2026-07-01")
        df = pd.DataFrame({
            "ALMACEN": ["A", "A", "A", "B"],
            "FECHA": [hoy - pd.Timedelta(days=10), hoy - pd.Timedelta(days=400), hoy - pd.Timedelta(days=20), hoy],
            "RIESGO": ["ALTO", "CRÍTICO", "BAJO", "ALTO"],
        })
        resultado = calcular_reincidencia(df, "ALMACEN", "FECHA", "RIESGO", hoy)
        # Tienda A: solo la de hace 10 días cuenta (la de 400 días está fuera de ventana,
        # la de 20 días es BAJO y no cuenta)
        assert resultado.get("A", 0) == 1
        assert resultado.get("B", 0) == 1


# ── cobertura ──
class TestCobertura:
    def test_cobertura_basica(self):
        dias = pd.Series([10, 95, 200, 30])
        c = calcular_cobertura(dias)
        assert c.n_activas == 4
        assert c.n_auditadas_90d == 2
        assert c.n_auditadas_180d == 3
        assert c.pct_90d == 50.0

    def test_cobertura_sin_tiendas_no_falla(self):
        c = calcular_cobertura(pd.Series([], dtype=float))
        assert c.n_activas == 0
        assert c.pct_90d == 0.0


# ── aging ──
class TestAging:
    def test_buckets_correctos(self):
        dias = pd.Series([5, 45, 75, 120])
        buckets = clasificar_aging(dias)
        assert list(buckets) == ["0-30 días", "31-60 días", "61-90 días", "+90 días"]

    def test_dia_cero_cae_en_primer_bucket(self):
        assert clasificar_aging(pd.Series([0]))[0] == "0-30 días"
