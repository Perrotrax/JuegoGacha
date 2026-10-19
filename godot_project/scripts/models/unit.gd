class_name Unit
extends RefCounted

signal hp_changed(new_hp: int, max_hp: int)
signal status_changed(new_status: String)

enum Status {
	ACTIVE,
	HOSPITALIZED,
	DEAD
}

@export var id: String = ""
@export var name: String = ""
@export var unit_class: String = "guardian"
@export var rarity: String = "N"

# Estadísticas de Combate
@export var max_hp: int = 100
@export var current_hp: int = 100
@export var atk: int = 15
@export var def_stat: int = 10
@export var speed: int = 10

# Liderazgo (LDR)
@export var ldr: int = 20
@export var ldr_cap: int = 50

# Estado vital y médico
@export var status: String = "ACTIVE"
@export var injury_severity: String = "NONE" # NONE, MILD, SEVERE, FATAL
@export var recovery_cycles: int = 0

# Rasgos (Traits)
@export var traits: Array = []

func _init(p_name: String = "Soldado", p_class: String = "guardian", p_rarity: String = "N"):
	id = "unit_%d_%d" % [Time.get_ticks_msec(), randi() % 9999]
	name = p_name
	unit_class = p_class
	rarity = p_rarity

func is_combat_ready() -> bool:
	return status == "ACTIVE" and current_hp > 0

func take_damage(raw_damage: int) -> int:
	var effective_damage = maxi(1, raw_damage - def_stat)
	current_hp = maxi(0, current_hp - effective_damage)
	hp_changed.emit(current_hp, max_hp)
	return effective_damage

func heal(amount: int) -> void:
	current_hp = mini(max_hp, current_hp + amount)
	hp_changed.emit(current_hp, max_hp)

func mark_incapacitated(severity: String = "SEVERE") -> void:
	status = "HOSPITALIZED"
	injury_severity = severity
	recovery_cycles = 5
	status_changed.emit(status)

func mark_dead() -> void:
	status = "DEAD"
	injury_severity = "FATAL"
	current_hp = 0
	status_changed.emit(status)

func modify_ldr(amount: int) -> void:
	ldr = clamp(ldr + amount, 0, ldr_cap)

func get_ldr_tier() -> Dictionary:
	if ldr <= 10:
		return {"num": 1, "name": "Tropa Ciega", "color": Color(0.7, 0.7, 0.7)}
	elif ldr <= 49:
		return {"num": 2, "name": "Sargento de Guardia", "color": Color(0.3, 0.8, 0.4)}
	elif ldr <= 74:
		return {"num": 3, "name": "Oficial Táctico", "color": Color(0.3, 0.6, 1.0)}
	elif ldr <= 89:
		return {"num": 4, "name": "General de Campo", "color": Color(0.8, 0.4, 1.0)}
	return {"num": 5, "name": "Mariscal Absoluto", "color": Color(1.0, 0.8, 0.2)}

func get_rarity_color() -> Color:
	match rarity:
		"N":
			return Color(0.75, 0.75, 0.75)
		"R":
			return Color(0.2, 0.6, 1.0)
		"SR":
			return Color(0.7, 0.3, 0.95)
		"SSR":
			return Color(1.0, 0.75, 0.2)
		"UR":
			return Color(1.0, 0.25, 0.35)
		_:
			return Color.WHITE

func to_dict() -> Dictionary:
	return {
		"id": id,
		"name": name,
		"unit_class": unit_class,
		"rarity": rarity,
		"max_hp": max_hp,
		"current_hp": current_hp,
		"atk": atk,
		"def": def_stat,
		"speed": speed,
		"ldr": ldr,
		"ldr_cap": ldr_cap,
		"status": status,
		"injury_severity": injury_severity,
		"recovery_cycles": recovery_cycles,
		"traits": traits
	}

static func from_dict(data: Dictionary) -> Unit:
	var u = Unit.new(data.get("name", "Soldado"), data.get("unit_class", "guardian"), data.get("rarity", "N"))
	u.id = data.get("id", u.id)
	u.max_hp = data.get("max_hp", 100)
	u.current_hp = data.get("current_hp", u.max_hp)
	u.atk = data.get("atk", 15)
	u.def_stat = data.get("def", 10)
	u.speed = data.get("speed", 10)
	u.ldr = data.get("ldr", 20)
	u.ldr_cap = data.get("ldr_cap", 50)
	u.status = data.get("status", "ACTIVE")
	u.injury_severity = data.get("injury_severity", "NONE")
	u.recovery_cycles = data.get("recovery_cycles", 0)
	u.traits = data.get("traits", [])
	return u
