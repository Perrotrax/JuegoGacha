"""
UI y Visor para la "Bitácora del Santuario".
Muestra la cronología de eventos históricos, bajas, cirugías e invocaciones.
"""
from typing import Optional
from ..utils.logger import sanctuary_logger


class LogViewerUI:
    @staticmethod
    def render_logs(category: Optional[str] = None, limit: int = 15) -> str:
        logs = sanctuary_logger.get_logs(category=category, limit=limit)
        category_header = f"[{category.upper()}]" if category else "[TODAS LAS CATEGORÍAS]"
        
        output = [
            f"╔════════════════════════════════════════════════════════════════════╗",
            f"║              BITÁCORA OFICIAL DEL SANTUARIO {category_header.center(22)} ║",
            f"╚════════════════════════════════════════════════════════════════════╝"
        ]

        if not logs:
            output.append("  (No hay entradas registradas en esta categoría)")
        else:
            for entry in logs:
                ts = entry["timestamp"].split("T")[-1][:8]
                cat = entry["category"].ljust(9)
                msg = entry["message"]
                output.append(f"  [{ts}] [{cat}] {msg}")

        output.append("╚════════════════════════════════════════════════════════════════════╝")
        return "\n".join(output)
