"""
Entry point y bucle principal (Game Loop) del juego.
Integra todos los subsistemas mecánicos, estados y modos de simulación.
"""
from typing import List, Optional
from ..entities.base_unit import BaseUnit
from ..systems.gacha.gacha_system import GachaSystem
from ..systems.combat.combat_system import CombatSystem
from ..systems.hospital.hospital_system import HospitalSystem
from ..systems.sanctuary.sanctuary_system import SanctuarySystem
from ..systems.inventory.inventory_system import InventorySystem
from ..systems.progression.progression_system import ProgressionSystem
from ..systems.tactics.tactics_system import TacticsSystem
from ..core.game_state import GameStateManager, GameState
from ..core.mode_manager import ModeManager
from ..ui.camera_eval import EvaluationCameraUI
from ..ui.log_viewer import LogViewerUI
from ..utils.logger import sanctuary_logger


class GameApp:
    def __init__(self):
        # Inicialización de subsistemas
        self.hospital = HospitalSystem(total_beds=4)
        self.mode_manager = ModeManager()
        self.progression = ProgressionSystem()
        self.combat = CombatSystem(hospital_system=self.hospital, mode_manager=self.mode_manager, progression_system=self.progression)
        self.gacha = GachaSystem()
        self.sanctuary = SanctuarySystem()
        self.inventory = InventorySystem()
        self.tactics = TacticsSystem(sanctuary_system=self.sanctuary, hospital_system=self.hospital)

        # Estados y gestión de modos
        self.state_manager = GameStateManager(GameState.MAIN_MENU)

        # Colección de unidades del jugador
        self.roster: List[BaseUnit] = []
        self.is_running = True

    def initialize_starter_squad(self) -> None:
        """Crea una escuadra inicial para que el jugador pueda interactuar de inmediato."""
        sanctuary_logger.log_event("SYSTEM", "Inicializando escuadra de bienvenida del Santuario...")
        u1 = self.gacha.recruit_unit(custom_name="Aiden Rompefilos")
        u2 = self.gacha.recruit_unit(custom_name="Kaelen Luz de Plata")
        self.roster.extend([u1, u2])
        self.sanctuary.station_unit(u1)
        self.sanctuary.station_unit(u2)

    def recruit(self, catalyst_bonus: float = 0.0) -> BaseUnit:
        """Invoca una nueva unidad mediante el sistema de gacha."""
        unit = self.gacha.recruit_unit(catalyst_bonus=catalyst_bonus)
        self.roster.append(unit)
        self.sanctuary.station_unit(unit)
        return unit

    def run_battle_demo(self):
        """Ejecuta una batalla de demostración entre la escuadra y una partida enemiga generada."""
        self.state_manager.change_state(GameState.BATTLE_SIMULATION)
        sanctuary_logger.log_event("COMBAT", "Iniciando escaramuza de entrenamiento...")

        # Asegurar unidades aliadas vivas
        allies = [u for u in self.roster if u.is_alive and not u.is_in_hospital]
        if not allies:
            sanctuary_logger.log_event("COMBAT", "No hay unidades aliadas disponibles (todas hospitalizadas o caídas).")
            return None

        # Generar enemigos de prueba
        e1 = self.gacha.recruit_unit(custom_name="Sombra Hostil Alfa")
        e2 = self.gacha.recruit_unit(custom_name="Gólem Corrupto")
        enemies = [e1, e2]

        result = self.combat.simulate_clash(allies, enemies, max_rounds=6)
        sanctuary_logger.log_event("COMBAT", f"Fin del encuentro. Ganador: {result['winner']}.")
        return result

    def advance_time(self, hours: float = 1.0) -> None:
        """Avanza el tiempo del santuario (recupera pacientes y entrena liderazgo)."""
        # Simulación del santuario
        self.sanctuary.simulate_tick(delta_hours=hours)
        # Procesamiento del hospital
        self.hospital.process_cycle()

    def show_camera_eval(self, unit_index: int = 0) -> str:
        """Muestra la pantalla de evaluación para una unidad del roster."""
        if 0 <= unit_index < len(self.roster):
            return EvaluationCameraUI.render_inspection(self.roster[unit_index])
        return "Unidad no encontrada en el roster."

    def show_logs(self, category: Optional[str] = None, limit: int = 15) -> str:
        """Retorna la bitácora formateada."""
        return LogViewerUI.render_logs(category=category, limit=limit)
