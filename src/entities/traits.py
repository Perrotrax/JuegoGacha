"""
Sistema de Rasgos Pasivos (Traits).
Define la estructura de los rasgos genéticos o de nacimiento y cómo modifican los atributos.
"""
from typing import Dict, Any, List


class Trait:
    def __init__(self, trait_id: str, name: str, description: str, effects: Dict[str, Any]):
        self.id = trait_id
        self.name = name
        self.description = description
        self.effects = effects

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "effects": self.effects
        }


class TraitManager:
    @staticmethod
    def apply_traits(unit: Any, traits: List[Trait]) -> None:
        """Aplica los efectos acumulativos de una lista de traits a una unidad."""
        for trait in traits:
            for effect_name, value in trait.effects.items():
                if effect_name == "ldr_bonus" and hasattr(unit, "leadership"):
                    unit.leadership.modify_base(int(value))
                elif effect_name == "attack_power_mult":
                    unit.atk = int(unit.atk * value)
                elif effect_name == "permadeath_resist":
                    unit.permadeath_resistance = getattr(unit, "permadeath_resistance", 0.0) + value
                elif effect_name == "autonomy_rebellion_chance":
                    unit.rebellion_chance = getattr(unit, "rebellion_chance", 0.0) + value
                elif effect_name == "ldr_cap_bonus" and hasattr(unit, "leadership"):
                    unit.leadership.increase_cap(int(value))
                elif effect_name == "ldr_gain_multiplier":
                    unit.ldr_growth_multiplier = getattr(unit, "ldr_growth_multiplier", 1.0) * float(value)
