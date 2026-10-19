extends Node

signal roster_updated
signal aether_changed(new_amount: int)
signal log_added(category: String, message: String)
signal hospital_updated

var roster: Array = []
var aether_energy: int = 150
var hospital_beds_max: int = 4
var logs: Array = []

var gacha_system: GachaSystem
var combat_system: CombatSystem

var unit_templates: Dictionary = {}
var traits_catalog: Array = []

var hostile_names: Array = [
	"Sombra Hostil Alfa", "Gólem Corrupto", "Acechador del Velo",
	"Bruto de Ceniza", "Lanzaósea", "Cultista Hueco"
]

func _ready():
	_load_database()
	gacha_system = GachaSystem.new(unit_templates, traits_catalog)
	combat_system = CombatSystem.new()
	_initialize_starter_squad()
	log_event("SYSTEM", "Santuario inicializado en Godot Engine.")

func _load_database():
	unit_templates = _load_json("res://data/unit_templates.json")
	var traits_raw = _load_json("res://data/traits.json")
	if traits_raw is Array:
		traits_catalog = traits_raw
	else:
		traits_catalog = []

func _load_json(path: String) -> Variant:
	if not FileAccess.file_exists(path):
		push_error("No se encontró el archivo: " + path)
		return {}
	var file = FileAccess.open(path, FileAccess.READ)
	var text = file.get_as_text()
	var json = JSON.new()
	var error = json.parse(text)
	if error == OK:
		return json.data
	push_error("Error parseando JSON: " + path)
	return {}

func _initialize_starter_squad():
	var u1 = gacha_system.recruit_unit("Aiden Rompefilos")
	var u2 = gacha_system.recruit_unit("Kaelen Luz de Plata")
	roster.append(u1)
	roster.append(u2)
	log_event("SANCTUARY", "%s fue acuartelado en el Santuario." % u1.name)
	log_event("SANCTUARY", "%s fue acuartelado en el Santuario." % u2.name)
	roster_updated.emit()

func recruit(catalyst_bonus: float = 0.0) -> Unit:
	if aether_energy < 50:
		log_event("GACHA", "Éter insuficiente para invocar (requiere 50).")
		return null
		
	aether_energy -= 50
	aether_changed.emit(aether_energy)
	
	var unit = gacha_system.recruit_unit("", catalyst_bonus)
	roster.append(unit)
	log_event("GACHA", "¡Nueva invocación: %s [%s %s] con LDR %d/%d!" % [
		unit.name, unit.rarity, unit.unit_class.capitalize(), unit.ldr, unit.ldr_cap
	])
	roster_updated.emit()
	return unit

func advance_cycle():
	# Generar Éter
	var gained_aether = randi_range(15, 30)
	aether_energy += gained_aether
	aether_changed.emit(aether_energy)
	log_event("SANCTUARY", "Ciclo avanzado (+%d Éter). Éter total: %d." % [gained_aether, aether_energy])
	
	# Entrenar unidades activas en LDR
	for u in roster:
		if u.status == "ACTIVE" and u.ldr < u.ldr_cap:
			if randf() < 0.65:
				u.modify_ldr(1)
				log_event("SANCTUARY", "%s mejoró su LDR (+1) -> %d/%d." % [u.name, u.ldr, u.ldr_cap])
	
	# Procesar hospital
	var discharged_any = false
	for u in roster:
		if u.status == "HOSPITALIZED":
			u.recovery_cycles -= 1
			if u.recovery_cycles <= 0:
				u.status = "ACTIVE"
				u.current_hp = int(u.max_hp * 0.75)
				u.injury_severity = "NONE"
				log_event("HOSPITAL", "%s ha recibido el alta médica y vuelve al servicio activo." % u.name)
				discharged_any = true
				
	hospital_updated.emit()
	roster_updated.emit()

func admit_to_hospital(unit: Unit) -> bool:
	var hospitalized_count = get_hospitalized_units().size()
	if hospitalized_count < hospital_beds_max:
		unit.mark_incapacitated("SEVERE")
		log_event("HOSPITAL", "%s ingresó a camilla de cuidados intensivos." % unit.name)
		hospital_updated.emit()
		roster_updated.emit()
		return true
	else:
		log_event("HOSPITAL", "¡Hospital colapsado! No hay camillas libres para %s." % unit.name)
		return false

func fast_heal_hospital(unit: Unit) -> bool:
	if aether_energy >= 30 and unit.status == "HOSPITALIZED":
		aether_energy -= 30
		aether_changed.emit(aether_energy)
		unit.status = "ACTIVE"
		unit.current_hp = unit.max_hp
		unit.recovery_cycles = 0
		unit.injury_severity = "NONE"
		log_event("HOSPITAL", "Tratamiento de Éter aplicado a %s. ¡Recuperación inmediata!" % unit.name)
		hospital_updated.emit()
		roster_updated.emit()
		return true
	return false

func get_active_combat_units() -> Array:
	return roster.filter(func(u): return u.is_combat_ready())

func get_hospitalized_units() -> Array:
	return roster.filter(func(u): return u.status == "HOSPITALIZED")

func create_hostiles(count: int) -> Array:
	var hostiles = []
	for i in range(count):
		var h_name = hostile_names[i % hostile_names.size()]
		var unit = gacha_system.recruit_unit(h_name)
		hostiles.append(unit)
	return hostiles

func log_event(category: String, message: String):
	var entry = {
		"time": Time.get_time_string_from_system(),
		"category": category,
		"message": message
	}
	logs.append(entry)
	if logs.size() > 100:
		logs.pop_front()
	log_added.emit(category, message)
	print("[%s][%s] %s" % [entry["time"], category, message])
