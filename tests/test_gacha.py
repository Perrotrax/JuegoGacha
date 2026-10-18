"""Pruebas unitarias para el sistema de Gacha y Reclutamiento."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from src.systems.gacha.gacha_system import GachaSystem
from src.entities.base_unit import BaseUnit


class TestGacha(unittest.TestCase):
    def setUp(self):
        self.gacha = GachaSystem()

    def test_recruitment_generates_valid_unit(self):
        unit = self.gacha.recruit_unit()
        self.assertIsInstance(unit, BaseUnit)
        self.assertTrue(unit.max_hp > 0)
        self.assertTrue(unit.atk > 0)
        self.assertTrue(unit.leadership.cap > 0)
        self.assertIn(unit.rarity, ["Common", "Rare", "Epic", "Legendary", "Anomaly"])
        self.assertIn(unit.unit_class, ["Guardian", "Vanguard", "Arcanist", "Medic"])

    def test_missing_data_files_raise_clear_error(self):
        with TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                GachaSystem(data_path=Path(directory))


if __name__ == "__main__":
    unittest.main()
