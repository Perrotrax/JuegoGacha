"""
Lógica de Autonomía de NPCs en Combate según Rangos de LDR.
Determina la estrategia y la acción de cada unidad en base a su nivel de liderazgo.
"""
from typing import Dict, Any, List
from ..entities.base_unit import BaseUnit
from .behavior_tree import NodeStatus, Selector, Sequence, ConditionNode, ActionNode


class TacticalDecider:
    @staticmethod
    def decide_action(unit: BaseUnit, allies: List[BaseUnit], enemies: List[BaseUnit]) -> Dict[str, Any]:
        """
        Retorna la intención táctica de la unidad según su LDR:
        - 0-10:   Caótico / Pánico (ataque errático o parálisis)
        - 11-49:  Soldado Básico (ataca al enemigo más cercano o de menor defensa)
        - 50-79:  Oficial Autónomo (prioriza supervivencia de escuadra o retaguardia)
        - 80+:    Comandante Estratega (foco táctico en soportes/mágicos y sinergias)
        """
        ldr_value = unit.leadership.value
        alive_enemies = [e for e in enemies if e.is_alive]
        
        if not alive_enemies:
            return {"action": "IDLE", "target": None, "strategy": "No hay amenazas"}

        # Rango 0-10: Caótico / Pánico
        if ldr_value <= 10:
            if unit.current_hp < unit.max_hp * 0.4:
                return {
                    "action": "PANIC_RETREAT",
                    "target": None,
                    "strategy": "Pánico ciego: intentando huir desordenadamente."
                }
            import random
            target = random.choice(alive_enemies)
            return {
                "action": "ERRATIC_ATTACK",
                "target": target,
                "strategy": "Ataque errático sin cálculo de amenaza."
            }

        # Rango 11-49: Soldado Disciplinado
        elif ldr_value <= 49:
            # Ataca al enemigo con menor HP restante
            target = min(alive_enemies, key=lambda e: e.current_hp)
            return {
                "action": "STANDARD_ATTACK",
                "target": target,
                "strategy": "Foco básico en el enemigo más vulnerable."
            }

        # Rango 50-79: Suboficial Autónomo
        elif ldr_value <= 79:
            # Si un aliado está en estado crítico, prioriza defenderlo o cubrir retirada
            critical_allies = [a for a in allies if a.is_alive and a.status in ("CRITICAL", "WOUNDED")]
            if critical_allies and unit.current_hp > unit.max_hp * 0.5:
                return {
                    "action": "DEFENSIVE_STANCE",
                    "target": critical_allies[0],
                    "strategy": "Postura defensiva para escoltar aliado herido."
                }
            # De lo contrario ataca al de mayor daño
            target = max(alive_enemies, key=lambda e: e.atk)
            return {
                "action": "INTERCEPT_ATTACK",
                "target": target,
                "strategy": "Intercepción contra el mayor daño rival."
            }

        # Rango 80+: Comandante / Anomalía Trascendente
        else:
            # Prioriza neutralizar soportes/médicos enemigos o el comandante enemigo
            priority_targets = [e for e in alive_enemies if e.unit_class.lower() in ("medic", "arcanist")]
            target = priority_targets[0] if priority_targets else min(alive_enemies, key=lambda e: e.current_hp)
            return {
                "action": "COMMANDER_BURST",
                "target": target,
                "strategy": "Optimización táctica: Foco coordinado en el objetivo de alto valor."
            }
