"""
Lógica del stat LDR (Leadership), LDR Cap y determinación de tiers de autonomía táctica.
Rangos de LDR:
- 0-10:   Caótico / Pánico fácil / Desobediencia alta
- 11-49:  Soldado disciplinado básico / Ejecuta órdenes simples
- 50-79:  Suboficial / Toma decisiones autónomas sensatas (retirada, cobertura)
- 80-100: Comandante Táctico / Optimización de cooldowns, foco coordinado y sinergias
- >100:   Anomalía Trascendente / Control del campo de batalla
"""
from typing import Tuple


class Leadership:
    def __init__(self, current_value: int, cap_value: int):
        # El documento de diseño permite NPCs sin potencial de mando (LDR Cap = 0).
        self.cap: int = max(0, cap_value)
        self.value: int = max(0, min(current_value, self.cap))

    def modify_base(self, amount: int) -> None:
        """Modifica el valor actual respetando el límite (cap)."""
        self.value = max(0, min(self.cap, self.value + amount))

    def increase_cap(self, amount: int) -> None:
        """Aumenta el límite máximo de liderazgo (mediante entrenamiento o santuario)."""
        self.cap += amount
        self.value = min(self.cap, self.value)

    def get_tier(self) -> Tuple[int, str]:
        """
        Retorna (tier_num, tier_label) basado en el valor actual de LDR.
        """
        if self.value <= 10:
            return 1, "Tropa Ciega"
        elif self.value <= 49:
            return 2, "Sargento de Guardia"
        elif self.value <= 74:
            return 3, "Oficial Táctico"
        elif self.value <= 89:
            return 4, "General de Campo"
        return 5, "Mariscal Absoluto"

    def get_tactical_obedience(self) -> float:
        """Probabilidad de obedecer directamente una orden manual de emergencia (0.0 a 1.0)."""
        return min(1.0, 0.25 + (self.value / 100.0) * 0.75)

    def to_dict(self) -> dict:
        tier_num, tier_name = self.get_tier()
        return {
            "current": self.value,
            "cap": self.cap,
            "tier_num": tier_num,
            "tier_name": tier_name,
            "tactical_obedience": self.get_tactical_obedience()
        }
