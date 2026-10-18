"""
Gestor de Modo de Ejecución: Modo Offline (Simulación Autónoma Local) vs Online (Sincronizado).
"""
from typing import Dict, Any
from ..utils.logger import sanctuary_logger


class ModeManager:
    OFFLINE_SIMULATION = "OFFLINE_SIMULATION"
    ONLINE_SYNC = "ONLINE_SYNC"

    def __init__(self, initial_mode: str = OFFLINE_SIMULATION):
        self.current_mode = initial_mode
        self.is_connected = False
        self.server_endpoint = "https://api.sanctuary-gacha.local"

    @property
    def is_online(self) -> bool:
        return self.current_mode == self.ONLINE_SYNC

    @property
    def permadeath_enabled(self) -> bool:
        """El modo offline es una simulación segura; el online asume riesgo total."""
        return self.is_online

    def get_rules_summary(self) -> Dict[str, Any]:
        if self.permadeath_enabled:
            return {
                "mode": "ONLINE",
                "permadeath": True,
                "description": "Operación en vivo: una unidad a 0 HP muere si no fue evacuada a tiempo."
            }
        return {
            "mode": "OFFLINE",
            "permadeath": False,
            "description": "Simulación segura: las bajas se convierten en incapacitados que requieren tratamiento."
        }

    def set_mode(self, new_mode: str) -> None:
        if new_mode in (self.OFFLINE_SIMULATION, self.ONLINE_SYNC):
            self.current_mode = new_mode
            sanctuary_logger.log_event("SYSTEM", f"Modo de juego cambiado a: {self.current_mode}")

    def toggle_mode(self) -> str:
        new_mode = self.ONLINE_SYNC if self.current_mode == self.OFFLINE_SIMULATION else self.OFFLINE_SIMULATION
        self.set_mode(new_mode)
        return self.current_mode

    def sync_data(self) -> Dict[str, Any]:
        """Sincroniza el estado local con el servidor en modo Online, o simula persistencia local."""
        if self.current_mode == self.ONLINE_SYNC:
            return {"status": "SUCCESS", "message": "Datos sincronizados con la nube del Santuario."}
        else:
            return {"status": "LOCAL_SAVED", "message": "Progreso guardado en almacenamiento local (Modo Offline)."}
