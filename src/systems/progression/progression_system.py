"""Promoción de tropas por hitos reales, no por gasto de recursos."""
from typing import Dict, Tuple

from ...entities.base_unit import BaseUnit
from ...utils.logger import sanctuary_logger


class ProgressionSystem:
    """Aplica la escalera N → R → SR → SSR y registra la historia de la unidad."""

    RARITY_ORDER = ("N", "R", "SR", "SSR")
    REQUIRED_FEATS: Dict[str, int] = {"N": 1, "R": 3, "SR": 6}
    STAT_MULTIPLIERS: Dict[str, float] = {"N": 1.0, "R": 1.25, "SR": 1.55, "SSR": 2.0, "UR": 2.5}

    def register_feat(self, unit: BaseUnit, feat: str) -> Tuple[bool, str]:
        """Registra una hazaña y promueve si la unidad ya probó su mérito."""
        if not unit.add_feat(feat):
            return False, f"La hazaña '{feat}' ya constaba en el historial de {unit.name}."

        sanctuary_logger.log_event("PROGRESSION", f"{unit.name} logró la hazaña: {feat}.", {"unit": unit.name, "feat": feat})
        promoted = self._promote_if_eligible(unit)
        if promoted:
            return True, f"{unit.name} ascendió a rareza {unit.rarity} gracias a sus hazañas."
        return True, f"Hazaña registrada para {unit.name} ({len(unit.feats)} acumuladas)."

    def _promote_if_eligible(self, unit: BaseUnit) -> bool:
        if unit.rarity not in self.REQUIRED_FEATS:
            return False
        needed = self.REQUIRED_FEATS[unit.rarity]
        if len(unit.feats) < needed:
            return False

        current_index = self.RARITY_ORDER.index(unit.rarity)
        next_rarity = self.RARITY_ORDER[current_index + 1]
        scale = self.STAT_MULTIPLIERS[next_rarity] / self.STAT_MULTIPLIERS[unit.rarity]
        unit.max_hp = max(1, int(unit.max_hp * scale))
        unit.current_hp = min(unit.max_hp, max(1, int(unit.current_hp * scale)))
        unit.atk = max(1, int(unit.atk * scale))
        unit.defense = max(0, int(unit.defense * scale))
        previous = unit.rarity
        unit.rarity = next_rarity
        sanctuary_logger.log_event("PROGRESSION", f"Promoción por hazaña: {unit.name} {previous} → {next_rarity}.", {"unit": unit.name, "from": previous, "to": next_rarity})
        return True

    def trigger_system_anomaly(self, unit: BaseUnit) -> Tuple[bool, str]:
        """Convierte una tropa N en UR ante una hazaña excepcional validada por el juego."""
        if unit.rarity != "N" or len(unit.feats) < 6:
            return False, "La Anomalía del Sistema solo responde a una tropa N con una hazaña extraordinaria."
        scale = self.STAT_MULTIPLIERS["UR"] / self.STAT_MULTIPLIERS["N"]
        unit.max_hp = int(unit.max_hp * scale)
        unit.current_hp = min(unit.max_hp, max(1, int(unit.current_hp * scale)))
        unit.atk = int(unit.atk * scale)
        unit.defense = int(unit.defense * scale)
        unit.rarity = "UR"
        sanctuary_logger.log_event("PROGRESSION", f"¡ANOMALÍA DEL SISTEMA! {unit.name} se transformó en una unidad UR única.", {"unit": unit.name, "rarity": "UR"})
        return True, f"{unit.name} rompió la matriz y despertó como UR."
