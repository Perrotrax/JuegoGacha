"""
Generador de eventos para la Bitácora del Santuario.
Registra eventos del juego, auditorías de reclutamiento, incidentes del hospital y crónicas de batalla.
"""
from datetime import datetime
from typing import List, Dict, Any, Optional


class SanctuaryLogger:
    def __init__(self, max_entries: int = 500):
        self.max_entries = max_entries
        self.log_history: List[Dict[str, Any]] = []

    def log_event(self, category: str, message: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Registra un evento clasificado en la bitácora.
        Categorías típicas: 'GACHA', 'COMBAT', 'HOSPITAL', 'SANCTUARY', 'SYSTEM', 'TACTIC'.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "category": category.upper(),
            "message": message,
            "metadata": metadata or {}
        }
        self.log_history.append(entry)
        if len(self.log_history) > self.max_entries:
            self.log_history.pop(0)
        
        # También imprimir en consola en formato legible
        print(f"[{entry['timestamp']}][{entry['category']}] {message}")
        return entry

    def get_logs(self, category: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Devuelve los últimos eventos registrados, opcionalmente filtrados por categoría."""
        if category:
            filtered = [e for e in self.log_history if e["category"] == category.upper()]
            return filtered[-limit:]
        return self.log_history[-limit:]

    def clear(self) -> None:
        """Limpia los registros de la bitácora."""
        self.log_history.clear()


# Instancia singleton para fácil acceso entre sistemas
sanctuary_logger = SanctuaryLogger()
