"""
Pantalla de la "Cámara de Evaluación".
Permite inspeccionar a fondo a reclutas, anomalías o prisioneros de guerra, analizando LDR, rasgos y condición médica.
"""
from typing import Dict, Any
from ..entities.base_unit import BaseUnit
from .components.hud_elements import HealthBarRenderer, StatusBadgeRenderer, LeadershipGaugeRenderer


class EvaluationCameraUI:
    @staticmethod
    def render_inspection(unit: BaseUnit) -> str:
        """Genera un reporte detallado visual de la unidad evaluada."""
        tier_num, tier_name = unit.leadership.get_tier()
        health_display = HealthBarRenderer.render(unit.current_hp, unit.max_hp)
        status_badge = StatusBadgeRenderer.render(unit.status)
        ldr_display = LeadershipGaugeRenderer.render(unit.leadership.value, unit.leadership.cap, tier_name)

        traits_str = "\n".join([f"    - {t.name}: {t.description}" for t in unit.traits]) or "    (Ninguno)"

        report = f"""
╔════════════════════════════════════════════════════════════════════╗
║             CÁMARA DE EVALUACIÓN TÁCTICA DEL SANTUARIO             ║
╚════════════════════════════════════════════════════════════════════╝
  ID UNIDAD : #{unit.id}
  NOMBRE    : {unit.name}
  CLASE     : {unit.unit_class} | RAREZA: [{unit.rarity}]
  ESTADO    : {status_badge}
  SALUD     : {health_display}
  --------------------------------------------------------------------
  ESTADÍSTICAS DE COMBATE:
    ATK : {unit.atk}  |  DEF : {unit.defense}  |  SPD : {unit.speed}
  --------------------------------------------------------------------
  AUDITORÍA DE MANDO (LDR):
    {ldr_display}
    Obediencia Táctica Manual: {int(unit.leadership.get_tactical_obedience() * 100)}%
  --------------------------------------------------------------------
  RASGOS GENÉTICOS Y DE NACIMIENTO:
{traits_str}
╚════════════════════════════════════════════════════════════════════╝
"""
        return report
