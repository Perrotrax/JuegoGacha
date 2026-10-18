"""
Entidades especiales: Héroes de alto rango, comandantes legendarios y jefes sometidos/tameados.
"""
from typing import List, Optional
from .base_unit import BaseUnit
from .traits import Trait


class HeroUnit(BaseUnit):
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
        boss_title: Optional[str] = None,
        traits: Optional[List[Trait]] = None
    ):
        super().__init__(
            name=name,
            unit_class=unit_class,
            rarity=rarity,
            max_hp=max_hp,
            atk=atk,
            defense=defense,
            speed=speed,
            base_ldr=base_ldr,
            ldr_cap=ldr_cap,
            traits=traits
        )
        self.boss_title = boss_title
        self.aura_buff_value: int = 10
        self.tamed: bool = boss_title is not None

    def trigger_aura_shout(self, allies: List[BaseUnit]) -> str:
        """Emite un grito de mando que incrementa temporalmente el LDR de aliados cercanos."""
        boosted_count = 0
        for ally in allies:
            if ally.is_alive and ally.id != self.id:
                ally.leadership.modify_base(self.aura_buff_value)
                boosted_count += 1
        return f"{self.name} activó Rugido de Comandante, inspirando a {boosted_count} unidades (+{self.aura_buff_value} LDR)."
