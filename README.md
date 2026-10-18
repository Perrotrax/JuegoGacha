# Proyecto Santuario - Gacha RPG & Simulación Autónoma

Un sistema RPG gacha con simulación táctica, mecánicas de liderazgo (**LDR**), gestión de santuario y resolución dinámica de **Permadeath vs Herida Crítica**.

---

## 🏛️ Estructura del Proyecto

```text
├── assets/                  # Recursos multimedia
│   ├── audio/ (music, sfx)
│   ├── fonts/
│   └── sprites/ (environment, UI, units)
├── data/                    # Bases de datos y configuraciones JSON
│   ├── items/items.json
│   ├── traits.json          # Rasgos de nacimiento (Cuna de Noble, Mente Prodigiosa, etc.)
│   └── unit_templates.json  # Clases, rarezas, multiplicadores de stats y pull rates
├── src/                     # Código fuente
│   ├── core/                # Loop principal, control de estados (FSM) y modo offline/online
│   │   ├── app.py
│   │   ├── game_state.py
│   │   └── mode_manager.py
│   ├── entities/            # Entidades y estadísticas
│   │   ├── base_unit.py     # Clase base de combatientes y estados vitales
│   │   ├── leadership.py    # Lógica de stat LDR, LDR Cap y tiers tácticos
│   │   ├── traits.py        # Pasivos y rasgos de nacimiento
│   │   └── hero.py          # Héroes legendarios y jefes sometidos
│   ├── systems/             # Subsistemas mecánicos
│   │   ├── combat/          # Daño, enfrentamientos y cálculo de permadeath vs herida
│   │   ├── gacha/           # Invocación de tropas, rarezas y anomalías
│   │   ├── hospital/        # Enfermería, camillas y cirujanos
│   │   ├── inventory/       # Items, pociones y catalizadores
│   │   ├── sanctuary/       # Módulos de la base y progresión autónoma offline
│   │   └── tactics/         # Intervención en vivo (Escudo de Sangre, Portal de Evacuación)
│   ├── ai/                  # Árbol de comportamiento y lógica por LDR
│   │   ├── behavior_tree.py
│   │   └── autonomy_logic.py
│   ├── ui/                  # HUD y pantallas de visualización
│   │   ├── components/      # Barras de vida, gauges de LDR y badges
│   │   ├── camera_eval.py   # Pantalla de la "Cámara de Evaluación"
│   │   └── log_viewer.py    # Bitácora oficial del Santuario
│   └── utils/               # Loggers y generadores probabilísticos
│       ├── logger.py
│       └── RNG.py
├── tests/                   # Pruebas unitarias de sistemas
├── main.py                  # Script ejecutor del juego
└── README.md
```

---

## ⚡ Características Principales

1. **Liderazgo (LDR) & LDR Cap**:
   - Cada unidad posee un límite biológico/mágico (`ldr_cap`) y un nivel de liderazgo actual (`ldr`).
   - Define el nivel de autonomía táctica y la probabilidad de acatar órdenes en combate manual o huir en pánico.

2. **Permadeath vs Herida Crítica**:
   - Cuando una unidad llega a 0 HP, se calcula su destino según su resistencia, rango de LDR y azar:
     - **Herida Crítica**: La unidad sobrevive inconsciente y es trasladada al Hospital.
     - **Permadeath**: La unidad muere definitivamente y se registra en la bitácora.

3. **Hospital y Cirugías**:
   - Camillas limitadas, asignación de cirujanos y turnos de convalecencia.

4. **Santuario y Progresión Autónoma (Offline)**:
   - Acuartela unidades para que entrenen su LDR de forma pasiva mientras se genera Éter para mejorar las instalaciones.

5. **Intervención en Vivo (Tácticas)**:
   - Habilidades de intervención en tiempo real como el **Portal de Evacuación** o el **Escudo de Sangre**.

---

## 🚀 Cómo Ejecutar

### Interfaz gráfica de escritorio
```bash
python main.py --gui
```

Permite reclutar, consultar el roster, simular combates, avanzar el tiempo, usar tácticas y revisar la bitácora desde una ventana.

### 1. Ejecutar la demo automática completa de todos los sistemas:
```bash
python main.py --demo
```

### 2. Ejecutar el menú interactivo:
```bash
python main.py
```

### 3. Ejecutar las pruebas unitarias:
```bash
python -m unittest discover tests
```
