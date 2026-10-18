"""Pruebas de admisión y validaciones del hospital."""
import unittest

from src.entities.base_unit import BaseUnit
from src.systems.hospital.hospital_system import HospitalSystem


class TestHospital(unittest.TestCase):
    def setUp(self):
        self.hospital = HospitalSystem(total_beds=1)
        self.unit = BaseUnit("Paciente", "Guardian", "Common", 100, 10, 0, 10, 10, 30)
        self.unit.status = "CRITICAL"

    def test_admitting_same_unit_does_not_consume_another_bed(self):
        self.assertTrue(self.hospital.admit_patient(self.unit))
        self.assertTrue(self.hospital.admit_patient(self.unit))
        self.assertEqual(len(self.hospital.patients), 1)

    def test_invalid_staff_and_bed_changes_are_rejected(self):
        with self.assertRaises(ValueError):
            self.hospital.upgrade_beds(0)
        with self.assertRaises(ValueError):
            self.hospital.assign_surgeon(0)


if __name__ == "__main__":
    unittest.main()
