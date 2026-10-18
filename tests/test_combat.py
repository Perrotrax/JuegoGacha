"""Pruebas unitarias para el combate y cálculo de permadeath vs herida."""
import unittest
from src.entities.base_unit import BaseUnit
from src.systems.combat.combat_system import CombatSystem
from src.systems.hospital.hospital_system import HospitalSystem


class TestCombat(unittest.TestCase):
    def setUp(self):
        self.hospital = HospitalSystem(total_beds=2)
        self.combat = CombatSystem(hospital_system=self.hospital)

    def test_damage_and_fatality_resolution(self):
        attacker = BaseUnit(
            name="Guerrero", unit_class="Vanguard", rarity="Common",
            max_hp=100, atk=50, defense=0, speed=10, base_ldr=20, ldr_cap=40
        )
        defender = BaseUnit(
            name="Defensor", unit_class="Guardian", rarity="Common",
            max_hp=20, atk=10, defense=0, speed=5, base_ldr=10, ldr_cap=30
        )

        res = self.combat.execute_attack(attacker, defender)
        self.assertEqual(defender.current_hp, 0)
        self.assertIn("fatal_resolution", res)
        self.assertIn(res["fatal_resolution"], ["PERMADEATH", "WOUNDED_CRITICAL"])

    def test_zero_rounds_returns_valid_result(self):
        unit_a = BaseUnit("A", "Vanguard", "Common", 100, 10, 0, 10, 10, 30)
        unit_b = BaseUnit("B", "Guardian", "Common", 100, 10, 0, 10, 10, 30)

        result = self.combat.simulate_clash([unit_a], [unit_b], max_rounds=0)

        self.assertEqual(result["rounds_executed"], 0)
        self.assertEqual(result["combat_log"], [])

    def test_negative_damage_is_rejected(self):
        unit = BaseUnit("Defensor", "Guardian", "Common", 100, 10, 0, 10, 10, 30)
        with self.assertRaises(ValueError):
            unit.take_damage(-1)


if __name__ == "__main__":
    unittest.main()
