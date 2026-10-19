class_name CombatSystem
extends RefCounted

signal attack_occurred(action_info: Dictionary)
signal unit_fallen(unit: Unit, fate: String)
signal combat_finished(winner: String, details: Dictionary)

var permadeath_enabled: bool = false # Si es seguro (simulador) o modo hardcore

func simulate_round(squad_a: Array, squad_b: Array) -> Dictionary:
	var active_a = squad_a.filter(func(u): return u.is_combat_ready())
	var active_b = squad_b.filter(func(u): return u.is_combat_ready())
	
	if active_a.is_empty() or active_b.is_empty():
		return {"finished": true, "winner": "Ninguno", "log": []}
	
	# Ordenar por velocidad
	var all_units = []
	for u in active_a:
		all_units.append({"unit": u, "team": "A"})
	for u in active_b:
		all_units.append({"unit": u, "team": "B"})
	
	all_units.sort_custom(func(x, y): return x["unit"].speed > y["unit"].speed)
	
	var round_logs: Array = []
	
	for participant in all_units:
		var attacker: Unit = participant["unit"]
		var team: String = participant["team"]
		
		if not attacker.is_combat_ready():
			continue
			
		var opponents = active_b if team == "A" else active_a
		var valid_opponents = opponents.filter(func(u): return u.is_combat_ready())
		
		if valid_opponents.is_empty():
			break
			
		var defender: Unit = valid_opponents[randi() % valid_opponents.size()]
		var raw_dmg = int(attacker.atk * randf_range(0.85, 1.15))
		var dealt = defender.take_damage(raw_dmg)
		
		var log_entry = {
			"attacker": attacker.name,
			"team": team,
			"defender": defender.name,
			"damage": dealt,
			"defender_hp": defender.current_hp,
			"fatal": false,
			"fate": ""
		}
		
		if defender.current_hp == 0:
			log_entry["fatal"] = true
			var fate = _resolve_fatality(defender)
			log_entry["fate"] = fate
			unit_fallen.emit(defender, fate)
			
		round_logs.append(log_entry)
		attack_occurred.emit(log_entry)
	
	var remaining_a = squad_a.filter(func(u): return u.is_combat_ready()).size()
	var remaining_b = squad_b.filter(func(u): return u.is_combat_ready()).size()
	
	var finished = (remaining_a == 0 or remaining_b == 0)
	var winner = "En curso"
	if finished:
		if remaining_a > 0 and remaining_b == 0:
			winner = "Tu Escuadra"
		elif remaining_b > 0 and remaining_a == 0:
			winner = "Hostiles"
		else:
			winner = "Empate"
	
	var result = {
		"finished": finished,
		"winner": winner,
		"remaining_a": remaining_a,
		"remaining_b": remaining_b,
		"log": round_logs
	}
	
	if finished:
		combat_finished.emit(winner, result)
		
	return result

func _resolve_fatality(unit: Unit) -> String:
	if not permadeath_enabled:
		unit.mark_incapacitated("SEVERE")
		return "HOSPITAL"
	
	# Cálculo de probabilidad de sobrevivir con herida crítica vs muerte definitiva
	var base_survival: float = 0.50
	var ldr_bonus: float = (float(unit.ldr) / 100.0) * 0.20
	var total_chance: float = clampf(base_survival + ldr_bonus, 0.05, 0.95)
	
	if randf() < total_chance:
		unit.mark_incapacitated("SEVERE")
		return "HOSPITAL"
	else:
		unit.mark_dead()
		return "PERMADEATH"
