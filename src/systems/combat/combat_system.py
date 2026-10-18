"""
Sistema de Combate y Resolución de Permadeath vs Herida Crítica.
"""
import random
from typing import List, Dict, Any, Tuple
from ...entities.base_unit import BaseUnit
from ...utils.logger import sanctuary_logger
from ...utils.RNG import RNGManager


class CombatSystem:
    def __init__(self, hospital_system=None, mode_manager=None, progression_system=None):
        self.hospital = hospital_system
        self.mode_manager = mode_manager
        self.progression = progression_system

    def execute_attack(self, attacker: BaseUnit, defender: BaseUnit) -> Dict[str, Any]:
        """Calcula y aplica el ataque directo de una unidad a otra."""
        if not attacker.is_combat_ready or not defender.is_combat_ready:
            return {"damage": 0, "status": "NO_OP"}

        # Variación aleatoria de ±15% de ataque
        raw_damage = int(attacker.atk * random.uniform(0.85, 1.15))
        actual_damage = defender.take_damage(raw_damage)

        result = {
            "attacker": attacker.name,
            "defender": defender.name,
            "damage": actual_damage,
            "defender_hp_left": defender.current_hp,
            "defender_status": defender.status
        }

        if defender.current_hp == 0:
            fate, fate_detail = self.resolve_fatality(defender)
            result["fatal_resolution"] = fate
            result["fatal_detail"] = fate_detail
            if fate == "PERMADEATH" and self.progression:
                self.progression.register_feat(attacker, f"Victoria sobre {defender.name} ({defender.id})")

        return result

    def resolve_fatality(self, unit: BaseUnit) -> Tuple[str, str]:
        """
        Determina si una unidad en 0 HP sufre Permadeath o sobrevive con Herida Crítica.
        Factores:
        - Resistencia base al permadeath (traits, etc.)
        - Rango de Liderazgo (mayor LDR = mayor instinto de supervivencia)
        - Rareza de la unidad
        """
        if self.mode_manager is not None:
            if not self.mode_manager.permadeath_enabled:
                unit.mark_incapacitated("SEVERE")
                admitted = self.hospital.admit_patient(unit) if self.hospital else False
                location = " y fue trasladado a la Enfermería." if admitted else " y espera atención médica."
                msg = f"{unit.name} cayó en la simulación segura; quedó incapacitado{location}"
                sanctuary_logger.log_event("COMBAT", msg, {"unit": unit.name, "mode": "OFFLINE", "admitted": admitted})
                return "INCAPACITATED", msg

            unit.status = "DEAD"
            unit.injury_severity = "FATAL"
            msg = f"{unit.name} sufrió PERMADEATH durante una operación online."
            sanctuary_logger.log_event("COMBAT", msg, {"unit": unit.name, "mode": "ONLINE", "event": "PERMADEATH"})
            return "PERMADEATH", msg

        # Compatibilidad para usos independientes del sistema de combate.
        base_survival_rate = 0.50
        ldr_bonus = (unit.leadership.value / 100.0) * 0.20
        trait_bonus = getattr(unit, "permadeath_resistance", 0.0)
        
        final_survival_chance = min(0.95, max(0.05, base_survival_rate + ldr_bonus + trait_bonus))
        
        survived = RNGManager.roll_chance(final_survival_chance)
        
        if survived:
            unit.mark_incapacitated("SEVERE")
            msg = f"{unit.name} cayó en combate pero sobrevivió milagrosamente (Herida Crítica)."
            sanctuary_logger.log_event("COMBAT", msg, {"unit": unit.name, "survival_chance": final_survival_chance})
            if self.hospital:
                admitted = self.hospital.admit_patient(unit)
                if not admitted:
                    msg += " No hay camilla disponible; requiere atención inmediata."
            return "WOUNDED_CRITICAL", msg
        else:
            unit.status = "DEAD"
            msg = f"{unit.name} sufrió PERMADEATH y ha perecido definitivamente en batalla."
            sanctuary_logger.log_event("COMBAT", msg, {"unit": unit.name, "event": "PERMADEATH"})
            return "PERMADEATH", msg

    def simulate_clash(self, squad_a: List[BaseUnit], squad_b: List[BaseUnit], max_rounds: int = 10) -> Dict[str, Any]:
        """Simulación automática por rondas entre dos escuadras."""
        round_log = []
        rounds_executed = 0
        for round_idx in range(1, max_rounds + 1):
            alive_a = [u for u in squad_a if u.is_combat_ready]
            alive_b = [u for u in squad_b if u.is_combat_ready]
            if not alive_a or not alive_b:
                break
            rounds_executed = round_idx

            # Turno de squad A
            for attacker in sorted(alive_a, key=lambda unit: unit.speed, reverse=True):
                targets = [u for u in squad_b if u.is_combat_ready]
                if not targets:
                    break
                target = random.choice(targets)
                res = self.execute_attack(attacker, target)
                round_log.append(f"Ronda {round_idx}: {res['attacker']} atacó a {res['defender']} ({res['damage']} daño).")

            # Turno de squad B
            active_b = [u for u in squad_b if u.is_combat_ready]
            for attacker in sorted(active_b, key=lambda unit: unit.speed, reverse=True):
                targets = [u for u in squad_a if u.is_combat_ready]
                if not targets:
                    break
                target = random.choice(targets)
                res = self.execute_attack(attacker, target)
                round_log.append(f"Ronda {round_idx}: {res['attacker']} atacó a {res['defender']} ({res['damage']} daño).")

        survivors_a = len([u for u in squad_a if u.is_combat_ready])
        survivors_b = len([u for u in squad_b if u.is_combat_ready])
        winner = "Squad A" if survivors_a > survivors_b else ("Squad B" if survivors_b > survivors_a else "Empate")

        return {
            "winner": winner,
            "rounds_executed": rounds_executed,
            "survivors_a": survivors_a,
            "survivors_b": survivors_b,
            "combat_log": round_log
        }
