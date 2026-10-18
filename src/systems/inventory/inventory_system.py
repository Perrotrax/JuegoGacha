"""
Sistema de Inventario, consumibles, catalizadores y materiales.
"""
from typing import Dict, Any, Optional
from ...entities.base_unit import BaseUnit
from ...utils.logger import sanctuary_logger


class InventorySystem:
    def __init__(self):
        # item_id -> {"name": str, "quantity": int, "type": str, "data": dict}
        self.items: Dict[str, Dict[str, Any]] = {
            "healing_salve": {"name": "Bálsamo Curativo", "quantity": 5, "type": "consumable", "data": {"heal": 50}},
            "blood_vessel_crystal": {"name": "Cristal de Sangre Primordial", "quantity": 2, "type": "catalyst", "data": {"tactical_power": 100}}
        }

    def add_item(self, item_id: str, name: str, item_type: str, quantity: int = 1, data: Optional[Dict[str, Any]] = None) -> None:
        """Agrega items al inventario."""
        if item_id in self.items:
            self.items[item_id]["quantity"] += quantity
        else:
            self.items[item_id] = {
                "name": name,
                "quantity": quantity,
                "type": item_type,
                "data": data or {}
            }
        sanctuary_logger.log_event("SYSTEM", f"Obtenido: {quantity}x {name}.")

    def use_item(self, item_id: str, target_unit: Optional[BaseUnit] = None) -> bool:
        """Aplica el efecto de un item y decrementa su cantidad."""
        if item_id not in self.items or self.items[item_id]["quantity"] <= 0:
            return False

        item_entry = self.items[item_id]
        item_data = item_entry["data"]

        if item_entry["type"] == "consumable" and target_unit:
            if "heal" in item_data:
                healed = target_unit.heal(item_data["heal"])
                sanctuary_logger.log_event("SYSTEM", f"{target_unit.name} fue curado por {healed} HP con {item_entry['name']}.")
        
        item_entry["quantity"] -= 1
        if item_entry["quantity"] == 0:
            del self.items[item_id]
        return True

    def get_quantity(self, item_id: str) -> int:
        return self.items.get(item_id, {}).get("quantity", 0)

    def to_dict(self) -> Dict[str, Any]:
        return self.items
