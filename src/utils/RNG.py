"""
Generador probabilístico y RNG con porcentajes para LDR Cap, Anomalías y tiradas de gacha.
"""
import random
from typing import Dict, Any, List, Optional


class RNGManager:
    @staticmethod
    def roll_percentage() -> float:
        """Devuelve un número flotante entre 0.0 y 1.0."""
        return random.random()

    @staticmethod
    def roll_chance(chance: float) -> bool:
        """Determina si un evento con probabilidad `chance` (0.0 a 1.0) tiene éxito."""
        return random.random() < chance

    @staticmethod
    def weighted_choice(choices: Dict[str, float]) -> str:
        """
        Selecciona una clave basada en pesos/porcentajes.
        choices: {'Common': 0.60, 'Rare': 0.28, 'Epic': 0.09, 'Legendary': 0.025, 'Anomaly': 0.005}
        """
        keys = list(choices.keys())
        weights = list(choices.values())
        return random.choices(keys, weights=weights, k=1)[0]

    @staticmethod
    def generate_ldr_cap() -> int:
        """Genera el potencial de mando según la curva punitiva del diseño.

        La rareza de combate no interviene en esta tirada: un recluta Normal
        puede convertirse en un gran comandante y una unidad UR puede no tener
        ninguna aptitud táctica.
        """
        roll = random.random() * 100
        if roll < 98.49:
            return random.randint(0, 10)
        if roll < 99.49:
            return random.randint(11, 49)
        if roll < 99.99:
            return random.randint(50, 74)
        if roll < 99.999:
            return random.randint(75, 89)
        return random.randint(90, 100)

    @staticmethod
    def calculate_ldr_growth(current_ldr: int, ldr_cap: int, growth_potential: float = 1.0) -> int:
        """
        Calcula el incremento de LDR considerando la proximidad al cap.
        A mayor proximidad al cap, menor la probabilidad de aumentar.
        """
        if ldr_cap <= 0 or current_ldr >= ldr_cap:
            return 0
        
        remaining_gap = ldr_cap - current_ldr
        prob = min(0.9, (remaining_gap / ldr_cap) * growth_potential)
        
        if random.random() < prob:
            increment = random.randint(1, max(1, int(remaining_gap * 0.15)))
            return min(ldr_cap - current_ldr, increment)
        return 0

    @staticmethod
    def roll_anomaly_mutation(base_rate: float = 0.01, catalyst_bonus: float = 0.0) -> bool:
        """Determina si ocurre una anomalía genética/mágica."""
        final_rate = min(0.5, base_rate + catalyst_bonus)
        return random.random() < final_rate
