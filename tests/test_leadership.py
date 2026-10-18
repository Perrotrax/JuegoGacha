"""Pruebas unitarias para el sistema de Liderazgo (LDR)."""
import unittest
from src.entities.leadership import Leadership


class TestLeadership(unittest.TestCase):
    def test_cap_and_boundaries(self):
        ldr = Leadership(current_value=40, cap_value=50)
        self.assertEqual(ldr.value, 40)
        self.assertEqual(ldr.cap, 50)

        # Modificación respetando el cap
        ldr.modify_base(20)
        self.assertEqual(ldr.value, 50)

        # Modificación respetando el piso
        ldr.modify_base(-100)
        self.assertEqual(ldr.value, 0)

    def test_tiers(self):
        ldr = Leadership(current_value=5, cap_value=100)
        tier_num, tier_label = ldr.get_tier()
        self.assertEqual(tier_num, 1)

        ldr.modify_base(25)  # 30 LDR
        tier_num, _ = ldr.get_tier()
        self.assertEqual(tier_num, 2)

        ldr.modify_base(30)  # 60 LDR
        tier_num, _ = ldr.get_tier()
        self.assertEqual(tier_num, 3)

        ldr.modify_base(30)  # 90 LDR
        tier_num, _ = ldr.get_tier()
        self.assertEqual(tier_num, 4)

        ldr.increase_cap(30)
        ldr.modify_base(25)  # 115 LDR
        tier_num, _ = ldr.get_tier()
        self.assertEqual(tier_num, 5)


if __name__ == "__main__":
    unittest.main()
