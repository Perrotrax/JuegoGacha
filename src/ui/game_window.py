"""Interfaz gráfica de escritorio para Proyecto Santuario."""
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Optional

# Permite abrir este archivo directamente desde VS Code o PowerShell, además de
# usarlo como módulo mediante ``python main.py --gui``.
if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from src.core.app import GameApp
    from src.core.game_state import GameState
    from src.entities.base_unit import BaseUnit
    from src.utils.logger import sanctuary_logger
else:
    from ..core.app import GameApp
    from ..core.game_state import GameState
    from ..entities.base_unit import BaseUnit
    from ..utils.logger import sanctuary_logger


class SanctuaryGameWindow:
    """Presenta los sistemas del juego mediante una interfaz Tkinter."""

    COLORS = {"bg": "#10141f", "panel": "#1b2233", "head": "#252f45", "accent": "#6c8cff",
              "gold": "#f4c95d", "text": "#edf2ff", "muted": "#aebbd3"}

    def __init__(self, app: Optional[GameApp] = None):
        self.app = app or GameApp()
        if not self.app.roster:
            self.app.initialize_starter_squad()
        self.app.state_manager.change_state(GameState.SANCTUARY_BASE)
        self.selected_index: Optional[int] = None
        self.root = tk.Tk()
        self.root.title("Proyecto Santuario · Gacha RPG")
        self.root.geometry("1180x720")
        self.root.minsize(960, 620)
        self.root.configure(bg=self.COLORS["bg"])
        self._build_layout()
        self.refresh()

    def _build_layout(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Roster.Treeview", background=self.COLORS["panel"], fieldbackground=self.COLORS["panel"], foreground=self.COLORS["text"], rowheight=30, borderwidth=0)
        style.configure("Roster.Treeview.Heading", background=self.COLORS["head"], foreground=self.COLORS["text"], relief="flat")
        style.map("Roster.Treeview", background=[("selected", self.COLORS["accent"])])

        header = tk.Frame(self.root, bg=self.COLORS["bg"], padx=24, pady=18)
        header.pack(fill="x")
        tk.Label(header, text="PROYECTO SANTUARIO", font=("Segoe UI", 22, "bold"), bg=self.COLORS["bg"], fg=self.COLORS["gold"]).pack(side="left")
        self.status_label = tk.Label(header, font=("Segoe UI", 10), bg=self.COLORS["bg"], fg=self.COLORS["muted"])
        self.status_label.pack(side="right")
        actions = tk.Frame(self.root, bg=self.COLORS["bg"], padx=24)
        actions.pack(fill="x")
        for text, command, color in (("Reclutar", self.recruit, self.COLORS["accent"]), ("Simular batalla", self.battle, "#d75e71"), ("Avanzar 1 hora", self.advance_time, "#467fbc"), ("Escudo de sangre", self.apply_shield, "#8e5bc5")):
            tk.Button(actions, text=text, command=command, bg=color, fg="white", activebackground=color, activeforeground="white", relief="flat", padx=15, pady=9, font=("Segoe UI", 10, "bold"), cursor="hand2").pack(side="left", padx=(0, 9))

        body = tk.Frame(self.root, bg=self.COLORS["bg"], padx=24, pady=18)
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=3); body.grid_columnconfigure(1, weight=2); body.grid_rowconfigure(0, weight=1)
        left = self._panel(body, "ROSTER DEL SANTUARIO"); left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        columns = ("name", "class", "rarity", "hp", "ldr", "status")
        self.roster = ttk.Treeview(left, columns=columns, show="headings", style="Roster.Treeview", selectmode="browse")
        for column, label, width in zip(columns, ("Unidad", "Clase", "Rareza", "HP", "LDR", "Estado"), (190, 100, 90, 90, 90, 100)):
            self.roster.heading(column, text=label); self.roster.column(column, width=width, anchor="center")
        self.roster.column("name", anchor="w")
        self.roster.pack(fill="both", expand=True, padx=12, pady=(4, 12)); self.roster.bind("<<TreeviewSelect>>", self._on_select)

        right = tk.Frame(body, bg=self.COLORS["bg"]); right.grid(row=0, column=1, sticky="nsew"); right.grid_rowconfigure(1, weight=1)
        details = self._panel(right, "CÁMARA DE EVALUACIÓN"); details.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.detail_text = tk.Label(details, justify="left", anchor="nw", wraplength=360, bg=self.COLORS["panel"], fg=self.COLORS["text"], font=("Segoe UI", 10))
        self.detail_text.pack(fill="x", padx=16, pady=(2, 16))
        logs = self._panel(right, "BITÁCORA DEL SANTUARIO"); logs.grid(row=1, column=0, sticky="nsew")
        self.log_text = tk.Text(logs, height=14, wrap="word", bg=self.COLORS["panel"], fg=self.COLORS["muted"], insertbackground="white", relief="flat", font=("Consolas", 9), state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=12, pady=(4, 12))

    def _panel(self, parent, title: str) -> tk.Frame:
        panel = tk.Frame(parent, bg=self.COLORS["panel"], highlightbackground="#33415d", highlightthickness=1)
        tk.Label(panel, text=title, bg=self.COLORS["head"], fg=self.COLORS["gold"], font=("Segoe UI", 10, "bold"), anchor="w", padx=14, pady=8).pack(fill="x")
        return panel

    def _on_select(self, _event=None) -> None:
        selected = self.roster.selection(); self.selected_index = int(selected[0]) if selected else None; self._render_selected_unit()

    def _selected_unit(self) -> Optional[BaseUnit]:
        return self.app.roster[self.selected_index] if self.selected_index is not None and 0 <= self.selected_index < len(self.app.roster) else None

    def _render_selected_unit(self) -> None:
        unit = self._selected_unit()
        if not unit:
            self.detail_text.config(text="Selecciona una unidad para consultar sus estadísticas y rasgos."); return
        traits = "\n".join(f"• {trait.name}" for trait in unit.traits) or "• Sin rasgos"
        tier, tier_name = unit.leadership.get_tier()
        self.detail_text.config(text=(f"{unit.name}\n{unit.rarity} · {unit.unit_class}\n\nEstado: {unit.status}\nHP: {unit.current_hp}/{unit.max_hp}\nATK {unit.atk}   DEF {unit.defense}   SPD {unit.speed}\nLDR: {unit.leadership.value}/{unit.leadership.cap} · Tier {tier}: {tier_name}\n\nRASGOS\n{traits}"))

    def refresh(self) -> None:
        current = self.selected_index; self.roster.delete(*self.roster.get_children())
        for index, unit in enumerate(self.app.roster):
            self.roster.insert("", "end", iid=str(index), values=(unit.name, unit.unit_class, unit.rarity, f"{unit.current_hp}/{unit.max_hp}", f"{unit.leadership.value}/{unit.leadership.cap}", unit.status))
        if current is not None and current < len(self.app.roster): self.roster.selection_set(str(current)); self.roster.focus(str(current))
        self._render_selected_unit()
        self.status_label.config(text=f"Éter: {self.app.sanctuary.aether_energy}   ·   Hospital: {len(self.app.hospital.patients)}/{self.app.hospital.total_beds}")
        entries = sanctuary_logger.get_logs(limit=12); formatted = "\n".join(f"[{entry['timestamp'][11:19]}] {entry['category']}: {entry['message']}" for entry in entries)
        self.log_text.config(state="normal"); self.log_text.delete("1.0", "end"); self.log_text.insert("1.0", formatted or "Sin eventos registrados."); self.log_text.config(state="disabled")

    def recruit(self) -> None:
        unit = self.app.recruit(); self.selected_index = len(self.app.roster) - 1; self.refresh(); messagebox.showinfo("Reclutamiento completado", f"{unit.name}\n{unit.rarity} {unit.unit_class}")

    def battle(self) -> None:
        result = self.app.run_battle_demo(); self.refresh()
        if result: messagebox.showinfo("Escaramuza finalizada", f"Ganador: {result['winner']}\nRondas: {result['rounds_executed']}")
        else: messagebox.showwarning("Sin escuadra", "No hay unidades disponibles para combatir.")

    def advance_time(self) -> None:
        self.app.advance_time(1.0); self.refresh()

    def apply_shield(self) -> None:
        unit = self._selected_unit()
        if not unit: messagebox.showwarning("Selecciona una unidad", "Elige una unidad antes de usar una táctica."); return
        if self.app.inventory.get_quantity("blood_vessel_crystal") < 1: messagebox.showwarning("Sin cristales", "No quedan cristales de sangre primordial."); return
        success, message = self.app.tactics.cast_blood_shield(unit, 1)
        if success: self.app.inventory.use_item("blood_vessel_crystal")
        self.refresh(); messagebox.showinfo("Táctica", message)

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    SanctuaryGameWindow().run()
