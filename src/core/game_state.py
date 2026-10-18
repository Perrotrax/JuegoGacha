"""
Manejo de Estados del Juego (FSM: Base, Batalla, Menú, Cámara de Evaluación, Hospital).
"""
from enum import Enum
from typing import Optional
from ..utils.logger import sanctuary_logger


class GameState(Enum):
    MAIN_MENU = "MAIN_MENU"
    SANCTUARY_BASE = "SANCTUARY_BASE"
    EVALUATION_CHAMBER = "EVALUATION_CHAMBER"
    BATTLE_SIMULATION = "BATTLE_SIMULATION"
    HOSPITAL_VIEW = "HOSPITAL_VIEW"
    LOG_VIEWER = "LOG_VIEWER"


class GameStateManager:
    def __init__(self, initial_state: GameState = GameState.MAIN_MENU):
        self.current_state = initial_state
        self.previous_state: Optional[GameState] = None

    def change_state(self, new_state: GameState) -> None:
        if new_state != self.current_state:
            self.previous_state = self.current_state
            self.current_state = new_state
            sanctuary_logger.log_event("SYSTEM", f"Transición de estado: {self.previous_state.name} -> {self.current_state.name}")

    def revert_state(self) -> None:
        if self.previous_state:
            self.change_state(self.previous_state)
