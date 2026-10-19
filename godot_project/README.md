# 🎮 Proyecto Santuario - Cliente Godot Engine (Godot 4.x)

Este directorio contiene la implementación del videojuego en **Godot Engine 4**, integrando todas las mecánicas desarrolladas en el proyecto (Gacha, Liderazgo LDR, Permadeath vs Hospital, Gestión del Santuario y Combate por turnos táctico).

---

## 🏛️ Estructura del Proyecto Godot

```text
godot_project/
├── project.godot               # Configuración del proyecto Godot 4
├── icon.svg                    # Icono del juego
├── data/                       # Bases de datos sincronizadas
│   ├── unit_templates.json     # Clases, stats y probabilidades de invocación
│   └── traits.json             # Rasgos de nacimiento (Cuna de Noble, etc.)
├── scripts/
│   ├── autoload/
│   │   └── game_manager.gd     # Singleton global de estado, éter, hospital y bitácora
│   ├── models/
│   │   └── unit.gd             # Clase de entidad Unit (stats, LDR tier, estados vitales)
│   ├── systems/
│   │   ├── gacha_system.gd     # Invocación, rates, anomalías UR y traits
│   │   └── combat_system.gd    # Simulación de escaramuzas y resolución de fatalidad
│   └── ui/
│       ├── main_menu.gd        # Controlador principal de interfaz y pestañas
│       └── unit_card.gd        # Componente visual interactivo para tarjetas de unidades
└── scenes/
    ├── main_menu.tscn          # Escena principal (Tabs: Santuario, Reclutar, Combate, etc.)
    └── components/
        └── unit_card.tscn      # Escena reutilizable de tarjeta de tropa
```

---

## ⚡ Características Implementadas en Godot

1. **Gestión del Santuario y Éter**:
   - Visualización de todas las tropas acuarteladas.
   - Botón **"Avanzar Ciclo"** para generar Éter pasivo y entrenar el liderazgo (**LDR**) de las tropas activas.

2. **Invocador Gacha & Detección de Anomalías**:
   - Invocación estándar (50 Éter) con tasas N, R, SR, SSR y UR.
   - Opción con **Catalizador** (+5% de anomalía trascendente).
   - Tarjeta animada con color dinámico según rareza.

3. **Escaramuza Táctica (Combate 2D)**:
   - Despliegue de escuadra aliada vs hostiles procedurales.
   - Ejecución ronda a ronda basada en velocidad y ataque.
   - Resolución de bajas: caída a la **Enfermería/Hospital** o **Permadeath**.

4. **Hospital y Camillas Médicas**:
   - Control de 4 camillas de cuidados intensivos.
   - Conteo regresivo de ciclos de convalecencia.
   - Opción de **Tratamiento Rápido con Éter** (30 Éter).

5. **Cámara de Evaluación (Inspector)**:
   - Selección de cualquier unidad para inspeccionar su LDR Tier (Tropa Ciega hasta Mariscal Absoluto), % de obediencia táctica, atributos y pasivas.

6. **Bitácora en Tiempo Real**:
   - Registro de todos los eventos del juego categorizados (SYSTEM, GACHA, COMBAT, HOSPITAL, SANCTUARY).

---

## 🚀 Cómo Abrir y Ejecutar el Juego en Godot

### Opción 1: Desde el Editor de Godot (Recomendado)
1. Descarga o abre **Godot 4.x** (disponible gratis y portable en [godotengine.org](https://godotengine.org)).
2. En el Administrador de Proyectos de Godot, haz clic en **Importar** (Import).
3. Selecciona el archivo:
   `c:/xampp/htdocs/Proyectos Propios/JuegoGacha/godot_project/project.godot`
4. Pulsa **Importar y Editar** (Import & Edit).
5. Presiona **F5** (o el botón Play ▶️ en la esquina superior derecha) para ejecutar el juego.

### Opción 2: Desde la Terminal (CLI)
Si tienes el ejecutable de Godot en tu sistema:
```powershell
godot --path "c:\xampp\htdocs\Proyectos Propios\JuegoGacha\godot_project"
```
