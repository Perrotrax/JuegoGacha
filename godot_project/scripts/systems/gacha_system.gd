class_name GachaSystem
extends RefCounted

var unit_templates: Dictionary = {}
var traits_catalog: Array = []

var first_names: Array = [
	"Aiden", "Kaelen", "Lyra", "Vaelen", "Seraphina", "Darius", "Morrigan",
	"Ignis", "Sylas", "Rowan", "Elira", "Thorne", "Valeria", "Gideon", "Cassian"
]

var epithets: Array = [
	"Rompefilos", "Luz de Plata", "Alba Radiante", "Guardián de Ceniza",
	"Hijo del Trueno", "Manto Sombrío", "Ojo de Halcón", "Inquebrantable",
	"Hoja Carmesí", "del Velo Eterno", "Furia de Acero", "Susurro Fugaz"
]

func _init(templates: Dictionary, traits: Array):
	unit_templates = templates
	traits_catalog = traits

func recruit_unit(custom_name: String = "", catalyst_bonus: float = 0.0) -> Unit:
	var rarity_multipliers: Dictionary = unit_templates.get("rarity_multipliers", {})
	var classes: Dictionary = unit_templates.get("classes", {})
	
	# Determinar rareza
	var chosen_rarity: String = "N"
	var is_anomaly: bool = randf() < (0.0001 + catalyst_bonus)
	
	if is_anomaly:
		chosen_rarity = "UR"
	else:
		chosen_rarity = _roll_weighted_rarity(rarity_multipliers)
	
	# Seleccionar clase al azar
	var class_keys = classes.keys()
	var chosen_class = class_keys[randi() % class_keys.size()]
	var class_data: Dictionary = classes[chosen_class]
	var rarity_data: Dictionary = rarity_multipliers.get(chosen_rarity, {"stat_mult": 1.0, "max_traits": 1})
	
	# Generar nombre
	var final_name = custom_name
	if final_name == "":
		final_name = "%s %s" % [first_names[randi() % first_names.size()], epithets[randi() % epithets.size()]]
	
	var unit = Unit.new(final_name, chosen_class, chosen_rarity)
	
	# Escalar estadísticas con multiplicador de rareza
	var mult: float = float(rarity_data.get("stat_mult", 1.0))
	unit.max_hp = int(class_data.get("base_hp", 100) * mult)
	unit.current_hp = unit.max_hp
	unit.atk = int(class_data.get("base_atk", 15) * mult)
	unit.def_stat = int(class_data.get("base_def", 10) * mult)
	unit.speed = int(class_data.get("speed", 10))
	
	var base_ldr = int(class_data.get("base_ldr", 30))
	unit.ldr_cap = int(base_ldr * mult + randi_range(5, 20))
	unit.ldr = randi_range(int(base_ldr * 0.3), unit.ldr_cap)
	
	# Asignar rasgos
	var max_traits: int = int(rarity_data.get("max_traits", 1))
	if traits_catalog.size() > 0 and max_traits > 0:
		var shuffled_traits = traits_catalog.duplicate()
		shuffled_traits.shuffle()
		var num_traits = randi_range(1, mini(max_traits, shuffled_traits.size()))
		for i in range(num_traits):
			unit.traits.append(shuffled_traits[i])
	
	return unit

func _roll_weighted_rarity(rarities: Dictionary) -> String:
	var roll = randf()
	var cumulative: float = 0.0
	# Orden típico N, R, SR, SSR, UR
	for r in ["UR", "SSR", "SR", "R", "N"]:
		if rarities.has(r):
			var rate = float(rarities[r].get("pull_rate", 0.0))
			cumulative += rate
			if roll <= cumulative:
				return r
	return "N"
