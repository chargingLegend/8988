import json
import os

CHECKPOINT_FILE = "checkpoint.json"


def save_checkpoint(player):
  data = {
    "name": player.name,
    "level": player.level,
    "hp": player.hp,
    "max_hp": player.max_hp,
    "mana": player.mana,
    "max_mana": player.max_mana,
    "manabda": player.manabda,
    "school": player.school,
    "spells": player.spells,
    "spell_data": player.spell_data,
    "ability_data": player.ability_data,
    "spell_upgrades": player.spell_upgrades,
    "ability_upgrades": player.ability_upgrades,
    "abilities": player.abilities,
    "exp": player.exp,
    "exp_to_next": player.exp_to_next,
    "defense": player.defense,
    "gold": player.gold,
    "flags": player.flags,
    "corruption": player.corruption,
    "sort_acquired_by": player.sort_acquired_by,
    "last_killed": player.last_killed,
    "inventory": [item.name for item in player.inventory.items],
  }
  with open(CHECKPOINT_FILE, "w") as f:
    json.dump(data, f, indent=2)
  print("\nThe path behind you solidifies.")
  print("This moment is recorded.")


def load_checkpoint():
  if not os.path.exists(CHECKPOINT_FILE):
    return None
  with open(CHECKPOINT_FILE, "r") as f:
    return json.load(f)


def checkpoint_exists():
  return os.path.exists(CHECKPOINT_FILE)


def apply_checkpoint(player, data):
  player.name = data["name"]
  player.level = data["level"]
  player.hp = data["max_hp"]
  player.max_hp = data["max_hp"]
  player.mana = data["max_mana"]
  player.max_mana = data["max_mana"]
  player.manabda = data["manabda"]
  player.school = data["school"]
  player.spells = data["spells"]
  player.spell_data = data["spell_data"]
  player.ability_data = data["ability_data"]
  player.spell_upgrades = data["spell_upgrades"]
  player.ability_upgrades = data["ability_upgrades"]
  player.abilities = data["abilities"]
  player.exp = data["exp"]
  player.exp_to_next = data["exp_to_next"]
  player.defense = data["defense"]
  player.gold = data["gold"]
  player.flags = data["flags"]
  player.corruption = data["corruption"]
  player.sort_acquired_by = data["sort_acquired_by"]
  player.last_killed = data["last_killed"]
  player.status_effects = []