extends PanelContainer

signal unit_selected(unit: Unit)

@onready var name_label = $Margin/VBox/Header/NameLabel
@onready var rarity_label = $Margin/VBox/Header/RarityLabel
@onready var class_label = $Margin/VBox/ClassLabel
@onready var hp_bar = $Margin/VBox/HPContainer/HPBar
@onready var hp_label = $Margin/VBox/HPContainer/HPLabel
@onready var ldr_bar = $Margin/VBox/LDRContainer/LDRBar
@onready var ldr_label = $Margin/VBox/LDRContainer/LDRLabel
@onready var status_badge = $Margin/VBox/StatusBadge

var current_unit: Unit = null

func setup(unit: Unit):
	current_unit = unit
	name_label.text = unit.name
	rarity_label.text = unit.rarity
	rarity_label.modulate = unit.get_rarity_color()
	class_label.text = "%s - %s" % [unit.unit_class.capitalize(), unit.get_ldr_tier()["name"]]
	
	hp_bar.max_value = unit.max_hp
	hp_bar.value = unit.current_hp
	hp_label.text = "HP: %d/%d" % [unit.current_hp, unit.max_hp]
	
	ldr_bar.max_value = unit.ldr_cap
	ldr_bar.value = unit.ldr
	ldr_label.text = "LDR: %d/%d" % [unit.ldr, unit.ldr_cap]
	
	match unit.status:
		"ACTIVE":
			status_badge.text = "[ACTIVO]"
			status_badge.modulate = Color(0.3, 0.9, 0.4)
		"HOSPITALIZED":
			status_badge.text = "[HOSPITAL: %d ciclos]" % unit.recovery_cycles
			status_badge.modulate = Color(1.0, 0.6, 0.2)
		"DEAD":
			status_badge.text = "[CAÍDO]"
			status_badge.modulate = Color(0.9, 0.2, 0.2)

func _on_gui_input(event: InputEvent):
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		if current_unit != null:
			unit_selected.emit(current_unit)
