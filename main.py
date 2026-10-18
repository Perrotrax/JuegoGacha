"""
Script ejecutor principal del juego (JuegoGacha / Sanctuary Gacha Project).
"""
import sys
from pathlib import Path

# Asegurar que el directorio raíz esté en el PYTHONPATH
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.app import GameApp
from src.core.game_state import GameState
from src.ui.game_window import SanctuaryGameWindow


if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def print_banner():
    print("""
======================================================================
                   PROYECTO SANTUARIO - GACHA RPG                    
         Simulación Autónoma • Permadeath • LDR Leadership           
======================================================================
""")


def main():
    if "--gui" in sys.argv:
        SanctuaryGameWindow().run()
        return

    print_banner()
    app = GameApp()
    app.initialize_starter_squad()
    app.state_manager.change_state(GameState.SANCTUARY_BASE)

    # Si se ejecuta sin interactividad o en modo script demo rápido
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        print("\n--- [EJECUTANDO DEMO AUTOMÁTICA DE TODOS LOS SISTEMAS] ---")
        
        # 1. Gacha recruit
        print("\n>> 1. Reclutamiento de prueba:")
        new_unit = app.recruit(catalyst_bonus=0.05)
        
        # 2. Cámara de evaluación
        print("\n>> 2. Inspección en Cámara de Evaluación:")
        print(app.show_camera_eval(len(app.roster) - 1))
        
        # 3. Batalla y Permadeath vs Herida
        print("\n>> 3. Simulación de Combate:")
        app.run_battle_demo()
        
        # 4. Avance de tiempo (Santuario + Hospital)
        print("\n>> 4. Avance del ciclo en el Santuario y Hospital:")
        app.advance_time(hours=2.0)
        
        # 5. Bitácora final
        print("\n>> 5. Bitácora del Santuario:")
        print(app.show_logs(limit=10))
        
        print("\n[DEMO FINALIZADA CON ÉXITO]\n")
        return

    # Loop interactivo en consola
    while app.is_running:
        print("\n--- MENÚ DEL SANTUARIO ---")
        print("1. Reclutar unidad (Gacha / Anomalía)")
        print("2. Inspeccionar unidad en Cámara de Evaluación")
        print("3. Iniciar Escaramuza de Batalla (Permadeath / Heridas)")
        print("4. Gestionar Hospital y Camillas")
        print("5. Avanzar ciclo en Santuario (Entrenamiento LDR y Éter)")
        print("6. Ver Bitácora del Santuario")
        print("7. Salir")

        try:
            choice = input("\nSeleccione una opción (1-7, o 'q' para salir): ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if choice in ("7", "q", "exit"):
            print("Cerrando sesión del Santuario...")
            break
        elif choice == "1":
            unit = app.recruit()
            print(f"\n¡Has invocado a {unit.name} ({unit.rarity} {unit.unit_class})!")
        elif choice == "2":
            if not app.roster:
                print("No hay unidades en el roster.")
                continue
            print("\nUnidades disponibles:")
            for idx, u in enumerate(app.roster):
                print(f"[{idx}] {u.name} - {u.rarity} {u.unit_class} ({u.status})")
            try:
                u_idx = int(input("Ingrese el índice de la unidad a evaluar: "))
                print(app.show_camera_eval(u_idx))
            except ValueError:
                print("Índice no válido.")
        elif choice == "3":
            app.run_battle_demo()
        elif choice == "4":
            print(f"\nEstado del Hospital: {len(app.hospital.patients)}/{app.hospital.total_beds} camillas ocupadas.")
            for p in app.hospital.patients:
                print(f" - {p.name}: {p.hospital_time_remaining} ciclos para el alta.")
        elif choice == "5":
            app.advance_time(1.0)
            print(f"\nCiclo avanzado. Éter actual: {app.sanctuary.aether_energy}")
        elif choice == "6":
            print(app.show_logs())
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
