"""
Gestión de módulos de la base / Santuario y simulación autónoma de recursos y progresión.
"""
import random
from typing import Dict, Any, List
from ...entities.base_unit import BaseUnit
from ...utils.logger import sanctuary_logger
from ...utils.RNG import RNGManager


class SanctuarySystem:
    def __init__(self):
        self.modules: Dict[str, Dict[str, Any]] = {
            "altar_of_summoning": {"level": 1, "name": "Altar de Reclutamiento", "bonus": 0.0},
            "training_grounds": {"level": 1, "name": "Campo de Entrenamiento Táctico", "ldr_bonus": 1},
            "infirmary_wing": {"level": 1, "name": "Ala Médica Avanzada", "recovery_speed": 1.0},
            "aether_refinery": {"level": 1, "name": "Refinería de Éter", "rate": 10},
            "military_academy": {"level": 1, "name": "Academia Militar", "ldr_training": 1.0},
            "alchemy_lab": {"level": 1, "name": "Laboratorio de Alquimia", "potion_quality": 1.0},
            "tavern": {"level": 1, "name": "Taberna del Santuario", "social_bonus": 1.0}
        }
        self.aether_energy: int = 150
        self.stationed_units: List[BaseUnit] = []

    def station_unit(self, unit: BaseUnit) -> None:
        """Asigna una unidad a descansar/entrenar en el Santuario."""
        if unit not in self.stationed_units:
            self.stationed_units.append(unit)
            sanctuary_logger.log_event("SANCTUARY", f"{unit.name} fue acuartelado en el Santuario.")

    def unstation_unit(self, unit: BaseUnit) -> None:
        if unit in self.stationed_units:
            self.stationed_units.remove(unit)

    def simulate_tick(self, delta_hours: float = 1.0) -> Dict[str, Any]:
        """
        Simulación autónoma / offline:
        - Generación pasiva de recursos (Éter)
        - Crecimiento de LDR de las unidades acuarteladas según su LDR Cap
        """
        refinery_level = self.modules["aether_refinery"]["level"]
        generated_aether = int(10 * refinery_level * delta_hours)
        self.aether_energy += generated_aether

        ldr_growth_events = []
        academy_level = self.modules["military_academy"]["level"]
        for unit in self.stationed_units:
            if unit.is_alive and not unit.is_in_hospital:
                gained_ldr = RNGManager.calculate_ldr_growth(
                    unit.leadership.value,
                    unit.leadership.cap,
                    growth_potential=(1.2 * self.modules["training_grounds"]["level"] * academy_level * unit.ldr_growth_multiplier)
                )
                if gained_ldr > 0:
                    unit.leadership.modify_base(gained_ldr)
                    ldr_growth_events.append(f"{unit.name} mejoró su LDR (+{gained_ldr}) -> {unit.leadership.value}/{unit.leadership.cap}.")

        if ldr_growth_events:
            for ev in ldr_growth_events:
                sanctuary_logger.log_event("SANCTUARY", ev)

        social_updates = self._simulate_social_life()

        return {
            "aether_produced": generated_aether,
            "total_aether": self.aether_energy,
            "ldr_updates": ldr_growth_events,
            "social_updates": social_updates
        }

    def _simulate_social_life(self) -> List[str]:
        """Genera vínculos de baja frecuencia entre habitantes disponibles del Santuario."""
        candidates = [unit for unit in self.stationed_units if unit.is_alive and not unit.is_in_hospital]
        if len(candidates) < 2 or random.random() >= 0.35:
            return []
        first, second = random.sample(candidates, 2)
        change = random.choice((-1, 1, 1)) * self.modules["tavern"]["level"]
        first.relationships[second.id] = first.relationships.get(second.id, 0) + change
        second.relationships[first.id] = second.relationships.get(first.id, 0) + change
        relation = "fortalecieron su amistad" if change > 0 else "tuvieron una rivalidad en la taberna"
        event = f"{first.name} y {second.name} {relation}."
        sanctuary_logger.log_event("SOCIAL", event, {"first": first.id, "second": second.id, "change": change})
        return [event]

    def upgrade_module(self, module_key: str) -> bool:
        """Sube de nivel una instalación del Santuario si hay suficiente Éter."""
        if module_key not in self.modules:
            return False
        
        mod = self.modules[module_key]
        cost = mod["level"] * 75
        if self.aether_energy >= cost:
            self.aether_energy -= cost
            mod["level"] += 1
            sanctuary_logger.log_event(
                "SANCTUARY",
                f"Módulo '{mod['name']}' mejorado al nivel {mod['level']}.",
                {"module": module_key, "level": mod["level"]}
            )
            return True
        return False
