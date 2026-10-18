"""
Lógica de intervención en vivo del jugador (Portal de Evacuación, Escudo de Sangre).
Considera obediencia y LDR de la unidad para el éxito de la intervención táctica.
"""
from typing import Dict, Any, Tuple
from ...entities.base_unit import BaseUnit
from ...utils.logger import sanctuary_logger
from ...utils.RNG import RNGManager


class TacticsSystem:
    def __init__(self, sanctuary_system=None, hospital_system=None):
        self.sanctuary = sanctuary_system
        self.hospital = hospital_system

    def cast_blood_shield(self, target: BaseUnit, blood_crystals_available: int) -> Tuple[bool, str]:
        """
        Activa un Escudo de Sangre que absorbe daño y mitiga permadeath temporalmente.
        Requiere 1 Cristal de Sangre.
        """
        if blood_crystals_available < 1:
            return False, "Cristales de sangre insuficientes."

        # Incrementa la resistencia al permadeath
        target.permadeath_resistance += 0.35
        # Añade un extra de armadura temporal
        target.defense += 15

        msg = f"Escudo de Sangre invocado sobre {target.name}. Defensa y resistencia a la muerte reforzadas."
        sanctuary_logger.log_event("TACTIC", msg, {"target": target.name, "action": "BLOOD_SHIELD"})
        return True, msg

    def open_emergency_portal(self, target: BaseUnit) -> Tuple[bool, str]:
        """
        Abre un Portal de Evacuación en vivo para retirar a una unidad herida del combate.
        Depende de la obediencia táctica de la unidad (LDR).
        """
        if not target.is_alive:
            return False, f"{target.name} ya ha perecido. El portal no puede rescatar almas perdidas."

        obedience = target.leadership.get_tactical_obedience()
        obeyed = RNGManager.roll_chance(obedience)

        if not obeyed:
            msg = f"¡FALLO DE RETIRADA! {target.name} desobedeció la orden del Portal y se rehúsa a abandonar la línea de fuego."
            sanctuary_logger.log_event("TACTIC", msg, {"target": target.name, "obedience_rolled": False})
            return False, msg

        if self.hospital:
            admitted = self.hospital.admit_patient(target)
            if admitted:
                target.status = "WOUNDED"
                msg = f"¡Evacuación exitosa! {target.name} cruzó el Portal de Emergencia y está a salvo en la Enfermería."
                sanctuary_logger.log_event("TACTIC", msg, {"target": target.name, "result": "EVACUATED"})
                return True, msg

        return False, "No hay camillas disponibles en el hospital para recibir la evacuación."
