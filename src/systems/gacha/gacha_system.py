"""
Sistema de Gacha, Invocación y Detección de Anomalías.
Carga plantillas y rasgos para generar instancias únicas de BaseUnit.
"""
import json
import random
from pathlib import Path
from typing import Dict, Any, List, Optional
from ...entities.base_unit import BaseUnit
from ...entities.traits import Trait
from ...utils.logger import sanctuary_logger
from ...utils.RNG import RNGManager


class GachaSystem:
    def __init__(self, data_path: Optional[Path] = None):
        if data_path is None:
            # Buscar en el directorio data/ por defecto
            self.data_path = Path(__file__).resolve().parents[3] / "data"
        else:
            self.data_path = data_path

        self.unit_templates = self._load_json(self.data_path / "unit_templates.json")
        self.traits_catalog = self._load_json(self.data_path / "traits.json")

    def _load_json(self, path: Path) -> Dict[str, Any]:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError) as exc:
                raise ValueError(f"No se pudo cargar el archivo de datos: {path}") from exc
        raise FileNotFoundError(f"No se encontró el archivo de datos requerido: {path}")

    def recruit_unit(self, custom_name: Optional[str] = None, catalyst_bonus: float = 0.0) -> BaseUnit:
        """
        Invoca una unidad tirando por rareza, clase, stats escalados y traits.
        """
        rarity_rates = {
            r: info["pull_rate"]
            for r, info in self.unit_templates.get("rarity_multipliers", {}).items()
            if info.get("pull_rate", 0) > 0
        }
        classes = self.unit_templates.get("classes", {})
        if not rarity_rates or not classes:
            raise ValueError("Los datos de gacha deben definir rarezas con pull_rate y al menos una clase.")

        # Chequeo de Anomalía especial
        is_anomaly = RNGManager.roll_anomaly_mutation(base_rate=0.00001, catalyst_bonus=catalyst_bonus)
        chosen_rarity = "UR" if is_anomaly else RNGManager.weighted_choice(rarity_rates)

        # Selección de clase
        chosen_class_name = random.choice(list(classes.keys()))
        class_data = classes[chosen_class_name]
        rarity_data = self.unit_templates.get("rarity_multipliers", {}).get(chosen_rarity, {
            "stat_mult": 1.0, "max_traits": 1
        })

        stat_mult = rarity_data["stat_mult"]
        max_traits = rarity_data.get("max_traits", 1)
        ldr_cap = RNGManager.generate_ldr_cap()

        # Generar rasgos asignados
        available_traits = self.traits_catalog if isinstance(self.traits_catalog, list) else []
        selected_traits: List[Trait] = []
        if available_traits:
            sample_count = min(len(available_traits), random.randint(1, max_traits))
            raw_traits = random.sample(available_traits, sample_count)
            for t in raw_traits:
                selected_traits.append(
                    Trait(t["id"], t["name"], t["description"], t["effects"])
                )

        # Nombres generados aleatorios si no se suministra uno
        first_names = ["Kael", "Lyra", "Vane", "Seraph", "Morgath", "Aurelius", "Zarek", "Elysia"]
        titles = ["el Implacable", "del Vacío", "Espada Negra", "Alba Radiante", "el Silente"]
        unit_name = custom_name or f"{random.choice(first_names)} {random.choice(titles)}"

        unit = BaseUnit(
            name=unit_name,
            unit_class=chosen_class_name.capitalize(),
            rarity=chosen_rarity,
            max_hp=int(class_data["base_hp"] * stat_mult),
            atk=int(class_data["base_atk"] * stat_mult),
            defense=int(class_data["base_def"] * stat_mult),
            speed=class_data["speed"],
            # Todos parten de LDR 0; los rasgos de nacimiento son la excepción.
            base_ldr=0,
            ldr_cap=ldr_cap,
            traits=selected_traits
        )

        sanctuary_logger.log_event(
            "GACHA",
            f"Nueva invocación: {unit.name} [{unit.rarity} {unit.unit_class}] con LDR {unit.leadership.value}/{unit.leadership.cap}.",
            {"unit_id": unit.id, "rarity": unit.rarity}
        )

        return unit
