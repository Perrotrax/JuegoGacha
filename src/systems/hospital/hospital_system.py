"""
Gestión del Hospital / Enfermería: camillas, asignación de cirujanos y recuperación de traumatismos.
"""
from typing import List, Dict, Any, Optional
from ...entities.base_unit import BaseUnit
from ...utils.logger import sanctuary_logger


class HospitalSystem:
    def __init__(self, total_beds: int = 4):
        self.total_beds = total_beds
        self.patients: List[BaseUnit] = []
        self.assigned_surgeons: int = 1

    @property
    def available_beds(self) -> int:
        return max(0, self.total_beds - len(self.patients))

    def admit_patient(self, unit: BaseUnit) -> bool:
        """Admite a una unidad herida o en estado crítico en una camilla si hay espacio."""
        if not unit.is_alive:
            return False
        if unit in self.patients:
            return True
        if self.available_beds <= 0:
            sanctuary_logger.log_event(
                "HOSPITAL",
                f"ALERTA: Hospital saturado. No hay camilla para {unit.name}.",
                {"unit": unit.name}
            )
            return False

        unit.is_in_hospital = True
        recovery_by_severity = {"LIGHT": 2, "SEVERE": 5, "TRAUMATIC": 10}
        base_recovery_turns = recovery_by_severity.get(unit.injury_severity, 2)
        reduction = max(1, self.assigned_surgeons)
        unit.hospital_time_remaining = max(1, base_recovery_turns - (reduction // 2))
        self.patients.append(unit)

        sanctuary_logger.log_event(
            "HOSPITAL",
            f"{unit.name} ingresó a camilla de cuidados intensivos ({unit.hospital_time_remaining} ciclos restantes).",
            {"unit": unit.name, "beds_left": self.available_beds}
        )
        return True

    def process_cycle(self) -> List[str]:
        """Procesa un ciclo de tiempo médico para todos los pacientes ingresados."""
        discharged = []
        for patient in list(self.patients):
            patient.hospital_time_remaining -= 1
            # Curación gradual
            heal_amount = int(patient.max_hp * 0.25 * (1 + self.assigned_surgeons * 0.1))
            patient.heal(heal_amount)

            if patient.hospital_time_remaining <= 0:
                patient.is_in_hospital = False
                patient.status = "HEALTHY"
                patient.injury_severity = "NONE"
                patient.current_hp = patient.max_hp
                self.patients.remove(patient)
                msg = f"{patient.name} ha recibido el alta médica y vuelve al servicio activo."
                discharged.append(msg)
                sanctuary_logger.log_event("HOSPITAL", msg, {"unit": patient.name})

        return discharged

    def upgrade_beds(self, amount: int = 1) -> int:
        """Expande el número de camillas disponibles."""
        if amount < 1:
            raise ValueError("La ampliación debe añadir al menos una camilla.")
        self.total_beds += amount
        sanctuary_logger.log_event("HOSPITAL", f"Ampliación completada: Ahora hay {self.total_beds} camillas.")
        return self.total_beds

    def assign_surgeon(self, count: int = 1) -> int:
        """Asigna más cirujanos al hospital."""
        if count < 1:
            raise ValueError("Debe asignarse al menos un cirujano.")
        self.assigned_surgeons += count
        return self.assigned_surgeons
