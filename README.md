# Proyecto Santuario — Gacha RPG en Godot 4

RPG gacha táctico con mecánicas de liderazgo (**LDR**), gestión de base (Santuario), sistema de hospital y resolución dinámica de **Permadeath vs Herida Crítica**. Desarrollado en **Godot Engine 4** con **GDScript**.

---

## 🏛️ Estructura del Proyecto

```text
├── godot_project/              # Proyecto Godot 4 (fuente principal del juego)
│   ├── project.godot           # Configuración del proyecto
│   ├── data/                   # Plantillas de unidades, rarezas y rasgos
│   │   ├── unit_templates.json
│   │   └── traits.json
│   ├── scripts/
│   │   ├── autoload/
│   │   │   └── game_manager.gd # Singleton global: Roster, Éter, Hospital, Logs
│   │   ├── models/
│   │   │   └── unit.gd         # Clase Unit (stats, LDR tiers, estados vitales)
│   │   ├── systems/
│   │   │   ├── gacha_system.gd # Invocación y detección de anomalías UR
│   │   │   └── combat_system.gd# Combate por rondas y resolución de fatalidad
│   │   └── ui/
│   │       ├── main_menu.gd    # Controlador de navegación por pestañas
│   │       └── unit_card.gd    # Tarjeta visual de unidad
│   └── scenes/
│       ├── main_menu.tscn      # Escena principal del juego
│       └── components/
│           └── unit_card.tscn  # Componente reutilizable de tarjeta
├── run_godot.bat               # Ejecuta el juego directamente
├── run_godot_editor.bat        # Abre el editor de Godot en el proyecto
└── .vscode/
    └── launch.json             # Configuración de debug con la extensión godot-tools
```

---

## ⚡ Mecánicas del Juego

1. **Invocación Gacha**: Tasas N/R/SR/SSR/UR con posibilidad de anomalía UR trascendente.
2. **Liderazgo (LDR)**: Cada unidad tiene un LDR actual y un cap biológico. Define su tier táctico: desde *Tropa Ciega* hasta *Mariscal Absoluto*.
3. **Combate por rondas**: Escaramuzas por velocidad, daño con variación ±15%.
4. **Permadeath vs Hospital**: Al caer a 0 HP, se resuelve supervivencia o muerte definitiva según el LDR del personaje.
5. **Santuario (Ciclos)**: Genera Éter pasivo y entrena LDR de las tropas acuarteladas.
6. **Hospital**: Hasta 4 camillas de cuidados intensivos con ciclos de convalecencia o cura rápida con Éter.

---

## 🚀 Cómo Ejecutar

### Opción 1: Lanzadores de script
```bat
:: Ejecutar el juego directamente
run_godot.bat

:: Abrir el editor visual de Godot
run_godot_editor.bat
```

### Opción 2: Desde VS Code / Cursor (F5)
1. Presiona `Ctrl + Shift + D`.
2. Selecciona **"GDScript: Ejecutar Proyecto Santuario (Godot 4)"**.
3. Presiona **F5**.

### Opción 3: Importar manualmente en Godot
1. Abre **Godot Engine 4**.
2. Haz clic en **Importar** y selecciona `godot_project/project.godot`.
3. Presiona **F5** dentro del editor.

---

## 🛠️ Requisitos

- **Godot Engine 4.7.x** (instalado en `%LOCALAPPDATA%\Microsoft\WinGet\Packages\` vía winget)
- **Extensión VS Code**: `geequlim.godot-tools` v2.7.1 (ya instalada)
