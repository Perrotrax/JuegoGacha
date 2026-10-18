"""Componentes visuales del HUD (Botones, Barras de Vida, Paneles)."""
from typing import Dict, Any


class HealthBarRenderer:
    @staticmethod
    def render(current_hp: int, max_hp: int, length: int = 20) -> str:
        """Renderiza una barra de vida estilo ASCII/UI moderna."""
        ratio = max(0.0, min(1.0, current_hp / max_hp))
        filled = int(length * ratio)
        empty = length - filled
        bar = "█" * filled + "░" * empty
        pct = int(ratio * 100)
        return f"[{bar}] {current_hp}/{max_hp} ({pct}%)"


class StatusBadgeRenderer:
    @staticmethod
    def render(status: str) -> str:
        badges = {
            "HEALTHY": "🟢 SALUDABLE",
            "WOUNDED": "🟡 HERIDO",
            "CRITICAL": "🔴 CRÍTICO",
            "DEAD": "💀 PERMADEATH"
        }
        return badges.get(status.upper(), f"⚪ {status}")


class LeadershipGaugeRenderer:
    @staticmethod
    def render(current_ldr: int, cap_ldr: int, tier_name: str) -> str:
        ratio = max(0.0, min(1.0, current_ldr / cap_ldr))
        filled = int(15 * ratio)
        empty = 15 - filled
        bar = "◆" * filled + "◇" * empty
        return f"LDR: [{bar}] {current_ldr}/{cap_ldr} | Rango: {tier_name}"
