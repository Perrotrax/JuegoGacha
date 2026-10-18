"""
Clase base para unidades del juego (NPCs y tropas).
Maneja atributos de combate, estado de salud (Vivo, Herido, Crítico, Muerto), rareza y traits.
"""
import uuid
from typing import List, Dict, Any, Optional
from .leadership import Leadership
from .traits import Trait, TraitManager


class BaseUnit:
    def __init__(
        self,
        name: str,
        unit_class: str,
        rarity: str,
        max_hp: int,
        atk: int,
        defense: int,
        speed: int,
        base_ldr: int,
        ldr_cap: int,
        traits: Optional[List[Trait]] = None
    ):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.unit_class = unit_class
        self.rarity = rarity
        
        # Atributos de combate
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.atk = atk
        self.defense = defense
        self.speed = speed
        
        # Sistema de Liderazgo
        self.leadership = Leadership(current_value=base_ldr, cap_value=ldr_cap)
        
        # Rasgos y modificadores
        self.traits: List[Trait] = traits or []
        self.permadeath_resistance: float = 0.0
        self.rebellion_chance: float = 0.0
        self.ldr_growth_multiplier: float = 1.0
        self.feats: List[str] = []
        self.relationships: Dict[str, int] = {}
        
        # Estados: 'HEALTHY', 'WOUNDED', 'INCAPACITATED', 'DEAD'
        self.status: str = "HEALTHY"
        self.injury_severity: str = "NONE"
        self.is_in_hospital: bool = False
        self.hospital_time_remaining: int = 0
        
        # Aplicar modificaciones iniciales de rasgos
        TraitManager.apply_traits(self, self.traits)

    @property
    def is_alive(self) -> bool:
        return self.status != "DEAD"

    @property
    def is_combat_ready(self) -> bool:
        return self.is_alive and self.current_hp > 0 and not self.is_in_hospital and self.status != "INCAPACITATED"

    def take_damage(self, amount: int) -> int:
        """Aplica daño mitigado por la defensa."""
        if amount < 0:
            raise ValueError("El daño no puede ser negativo.")
        if not self.is_alive:
            return 0
        mitigated = max(1, amount - (self.defense // 2))
        self.current_hp = max(0, self.current_hp - mitigated)
        if self.current_hp == 0:
            self.mark_incapacitated("SEVERE")
        elif self.current_hp <= self.max_hp * 0.3:
            self.status = "WOUNDED"
            self.injury_severity = "LIGHT"
        return mitigated

    def heal(self, amount: int) -> int:
        """Cura salud sin sobrepasar el máximo."""
        if amount < 0:
            raise ValueError("La curación no puede ser negativa.")
        if not self.is_alive:
            return 0
        healed = min(self.max_hp - self.current_hp, amount)
        self.current_hp += healed
        if self.current_hp > self.max_hp * 0.3:
            self.status = "HEALTHY"
            self.injury_severity = "NONE"
        return healed

    def mark_incapacitated(self, severity: str = "SEVERE") -> None:
        """Marca a la unidad fuera de combate sin convertirla en una baja definitiva."""
        self.status = "INCAPACITATED"
        self.injury_severity = severity

    def add_feat(self, feat: str) -> bool:
        """Registra una hazaña única que puede habilitar promociones de rareza."""
        if feat in self.feats:
            return False
        self.feats.append(feat)
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "unit_class": self.unit_class,
            "rarity": self.rarity,
            "hp": f"{self.current_hp}/{self.max_hp}",
            "atk": self.atk,
            "defense": self.defense,
            "speed": self.speed,
            "status": self.status,
            "injury_severity": self.injury_severity,
            "leadership": self.leadership.to_dict(),
            "feats": list(self.feats),
            "traits": [t.to_dict() for t in self.traits]
        }
