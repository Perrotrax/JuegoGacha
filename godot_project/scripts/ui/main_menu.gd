extends Control

@onready var aether_label = $MainContainer/TopBar/AetherCounter/AetherLabel
@onready var units_count_label = $MainContainer/TopBar/InfoContainer/UnitsLabel
@onready var hospital_label = $MainContainer/TopBar/InfoContainer/HospitalLabel
@onready var tab_container = $MainContainer/TabContainer

# Vistas
@onready var sanctuary_grid = $MainContainer/TabContainer/Santuario/ScrollContainer/UnitsGrid
@onready var hospital_grid = $MainContainer/TabContainer/Hospital/ScrollContainer/BedsGrid
@onready var log_text_edit = $MainContainer/TabContainer/Bitacora/LogTextEdit

# Gacha UI
@onready var gacha_result_panel = $MainContainer/TabContainer/Reclutar/VBox/ResultCard
@onready var gacha_name = $MainContainer/TabContainer/Reclutar/VBox/ResultCard/Margin/VBox/NameLabel
@onready var gacha_details = $MainContainer/TabContainer/Reclutar/VBox/ResultCard/Margin/VBox/DetailsLabel
@onready var gacha_stats = $MainContainer/TabContainer/Reclutar/VBox/ResultCard/Margin/VBox/StatsLabel

# Combate UI
@onready var ally_container = $MainContainer/TabContainer/Escaramuza/VBox/Arena/AllySquad
@onready var enemy_container = $MainContainer/TabContainer/Escaramuza/VBox/Arena/EnemySquad
@onready var combat_log_label = $MainContainer/TabContainer/Escaramuza/VBox/CombatLog
@onready var combat_status_label = $MainContainer/TabContainer/Escaramuza/VBox/StatusLabel
@onready var btn_next_round = $MainContainer/TabContainer/Escaramuza/VBox/Actions/BtnNextRound
@onready var btn_start_combat = $MainContainer/TabContainer/Escaramuza/VBox/Actions/BtnStartCombat

# Cámara de Evaluación UI
@onready var eval_unit_option = $MainContainer/TabContainer/Evaluacion/VBox/TopSelect/UnitOptionButton
@onready var eval_name_label = $MainContainer/TabContainer/Evaluacion/VBox/Details/Info/NameLabel
@onready var eval_class_label = $MainContainer/TabContainer/Evaluacion/VBox/Details/Info/ClassLabel
@onready var eval_stats_label = $MainContainer/TabContainer/Evaluacion/VBox/Details/Info/StatsLabel
@onready var eval_traits_label = $MainContainer/TabContainer/Evaluacion/VBox/Details/Info/TraitsLabel
@onready var eval_ldr_label = $MainContainer/TabContainer/Evaluacion/VBox/Details/Info/LDRLabel

var unit_card_scene = preload("res://scenes/components/unit_card.tscn")
var current_combat_allies: Array = []
var current_combat_enemies: Array = []

func _ready():
	GameManager.aether_changed.connect(_on_aether_changed)
	GameManager.roster_updated.connect(_on_roster_updated)
	GameManager.hospital_updated.connect(_on_hospital_updated)
	GameManager.log_added.connect(_on_log_added)
	
	_on_aether_changed(GameManager.aether_energy)
	_on_roster_updated()
	_on_hospital_updated()
	_refresh_logs()

func _on_aether_changed(new_amount: int):
	aether_label.text = "Éter: %d" % new_amount

func _on_roster_updated():
	var total = GameManager.roster.size()
	var active = GameManager.get_active_combat_units().size()
	units_count_label.text = "Tropas: %d (%d listas)" % [total, active]
	
	# Repoblar Santuario
	for child in sanctuary_grid.get_children():
		child.queue_free()
	
	for unit in GameManager.roster:
		var card = unit_card_scene.instantiate()
		sanctuary_grid.add_child(card)
		card.setup(unit)
		card.unit_selected.connect(_on_unit_selected_for_eval)
	
	_update_eval_options()

func _on_hospital_updated():
	var hospitalized = GameManager.get_hospitalized_units()
	hospital_label.text = "Hospital: %d/%d" % [hospitalized.size(), GameManager.hospital_beds_max]
	
	for child in hospital_grid.get_children():
		child.queue_free()
	
	for i in range(GameManager.hospital_beds_max):
		var panel = PanelContainer.new()
		panel.custom_minimum_size = Vector2(240, 140)
		var vbox = VBoxContainer.new()
		vbox.add_theme_constant_override("separation", 8)
		panel.add_child(vbox)
		
		var title = Label.new()
		title.text = "Camilla #%d" % (i + 1)
		title.add_theme_font_size_override("font_size", 14)
		vbox.add_child(title)
		
		if i < hospitalized.size():
			var p: Unit = hospitalized[i]
			var desc = Label.new()
			desc.text = "%s (%s)\nCiclos restantes: %d\nGravedad: %s" % [
				p.name, p.rarity, p.recovery_cycles, p.injury_severity
			]
			desc.add_theme_color_override("font_color", Color(1.0, 0.6, 0.3))
			vbox.add_child(desc)
			
			var btn_heal = Button.new()
			btn_heal.text = "Tratamiento Éter (30)"
			btn_heal.pressed.connect(func(): GameManager.fast_heal_hospital(p))
			vbox.add_child(btn_heal)
		else:
			var empty_lbl = Label.new()
			empty_lbl.text = "[Desocupada / Disponible]"
			empty_lbl.add_theme_color_override("font_color", Color(0.5, 0.7, 0.5))
			vbox.add_child(empty_lbl)
			
		hospital_grid.add_child(panel)

func _on_log_added(_category: String, _message: String):
	_refresh_logs()

func _refresh_logs():
	var full_text = ""
	for entry in GameManager.logs:
		full_text += "[%s][%s] %s\n" % [entry["time"], entry["category"], entry["message"]]
	log_text_edit.text = full_text
	log_text_edit.scroll_vertical = 99999

# --- ACCIONES DE GACHA ---
func _on_btn_recruit_pressed():
	var unit = GameManager.recruit(0.0)
	if unit != null:
		_show_gacha_result(unit)

func _on_btn_recruit_catalyst_pressed():
	var unit = GameManager.recruit(0.05)
	if unit != null:
		_show_gacha_result(unit)

func _show_gacha_result(unit: Unit):
	gacha_result_panel.visible = true
	gacha_name.text = "¡%s!" % unit.name
	gacha_name.modulate = unit.get_rarity_color()
	gacha_details.text = "Rareza: %s | Clase: %s | Rol: %s" % [
		unit.rarity, unit.unit_class.capitalize(), unit.get_ldr_tier()["name"]
	]
	gacha_stats.text = "HP: %d | ATK: %d | DEF: %d | LDR: %d/%d" % [
		unit.max_hp, unit.atk, unit.def_stat, unit.ldr, unit.ldr_cap
	]

# --- AVANCE DEL CICLO (SANTUARIO) ---
func _on_btn_advance_cycle_pressed():
	GameManager.advance_cycle()

# --- COMBATE / ESCARAMUZA ---
func _on_btn_start_combat_pressed():
	current_combat_allies = GameManager.get_active_combat_units().slice(0, 3)
	if current_combat_allies.is_empty():
		combat_status_label.text = "No hay unidades listas para el combate (hospitalizadas o caídas)."
		return
	
	current_combat_enemies = GameManager.create_hostiles(current_combat_allies.size())
	_render_combat_arenas()
	
	combat_status_label.text = "Escaramuza iniciada: %d Aliados vs %d Hostiles." % [
		current_combat_allies.size(), current_combat_enemies.size()
	]
	combat_log_label.text = "La batalla ha comenzado...\n"
	btn_next_round.disabled = false

func _on_btn_next_round_pressed():
	if current_combat_allies.is_empty() or current_combat_enemies.is_empty():
		return
		
	var round_result = GameManager.combat_system.simulate_round(current_combat_allies, current_combat_enemies)
	
	var log_str = ""
	for action in round_result["log"]:
		log_str += "%s ataca a %s causando %d daño (HP restante: %d).\n" % [
			action["attacker"], action["defender"], action["damage"], action["defender_hp"]
		]
		if action["fatal"]:
			if action["fate"] == "HOSPITAL":
				log_str += " -> ¡%s ha caído inconsciente y es trasladado a la enfermería!\n" % action["defender"]
			else:
				log_str += " -> ¡%s ha sufrido PERMADEATH!\n" % action["defender"]
				
	combat_log_label.text = log_str + "\n" + combat_log_label.text
	_render_combat_arenas()
	
	if round_result["finished"]:
		btn_next_round.disabled = true
		combat_status_label.text = "Fin del encuentro. Ganador: %s" % round_result["winner"]
		GameManager.log_event("COMBAT", "Fin de escaramuza. Ganador: %s." % round_result["winner"])
		# Actualizar hospital si hubo bajas aliadas
		for ally in current_combat_allies:
			if ally.status == "HOSPITALIZED":
				GameManager.admit_to_hospital(ally)
		GameManager.roster_updated.emit()

func _render_combat_arenas():
	for c in ally_container.get_children():
		c.queue_free()
	for c in enemy_container.get_children():
		c.queue_free()
		
	for u in current_combat_allies:
		var card = unit_card_scene.instantiate()
		ally_container.add_child(card)
		card.setup(u)
		
	for u in current_combat_enemies:
		var card = unit_card_scene.instantiate()
		enemy_container.add_child(card)
		card.setup(u)

# --- CÁMARA DE EVALUACIÓN ---
func _update_eval_options():
	eval_unit_option.clear()
	for i in range(GameManager.roster.size()):
		var u: Unit = GameManager.roster[i]
		eval_unit_option.add_item("%s (%s)" % [u.name, u.rarity], i)
	if GameManager.roster.size() > 0:
		_show_unit_eval(GameManager.roster[0])

func _on_unit_option_selected(index: int):
	if index >= 0 and index < GameManager.roster.size():
		_show_unit_eval(GameManager.roster[index])

func _on_unit_selected_for_eval(unit: Unit):
	tab_container.current_tab = 4 # Tab de Evaluación
	_show_unit_eval(unit)

func _show_unit_eval(unit: Unit):
	eval_name_label.text = unit.name
	eval_name_label.modulate = unit.get_rarity_color()
	eval_class_label.text = "Clase: %s | Rareza: %s | Estado: %s" % [
		unit.unit_class.capitalize(), unit.rarity, unit.status
	]
	eval_stats_label.text = "HP Máx: %d | Ataque: %d | Defensa: %d | Velocidad: %d" % [
		unit.max_hp, unit.atk, unit.def_stat, unit.speed
	]
	
	var tier_info = unit.get_ldr_tier()
	eval_ldr_label.text = "Liderazgo (LDR): %d / %d\nTier: %s (Tier %d)\nObediencia táctica: %d%%" % [
		unit.ldr, unit.ldr_cap, tier_info["name"], tier_info["num"],
		int((0.25 + (float(unit.ldr)/100.0) * 0.75) * 100)
	]
	
	var traits_str = "Rasgos de Nacimiento:\n"
	if unit.traits.is_empty():
		traits_str += " - Sin rasgos especiales reconocidos."
	else:
		for t in unit.traits:
			traits_str += " • %s: %s\n" % [t.get("name", "Rasgo"), t.get("description", "")]
	eval_traits_label.text = traits_str
