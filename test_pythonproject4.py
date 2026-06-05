import pytest

from wizard import Wizard
from entities.monster import RavenSwarm
from inventory import Inventory
from location import Location
from items import (Item, Consumable, Equipment, HPPotion, ManaPotion,
                   ManabdaPotion, PassRune, ExceptVial, FinallyFlask,
                   Cloak, Staff, Rod, Scepter)

def test_Raven_Swarm_inherits_from_monster():
  swarm = RavenSwarm()
  assert swarm.hp == 15
  assert swarm.name == "Raven Swarm"
  assert swarm.exp_value == 50
  assert swarm.is_alive() == True

def test_inventory_starts_empty():
  inv = Inventory()
  assert len(inv.items) == 0
  assert str(inv) == "Inventory is empty."

def test_learn_sort_unlocks_spell():
  player = Wizard(name="TestWizard")
  result = player.learn_spell_sort()
  assert "sort" in player.spells
  assert "rune" in result.lower()


@pytest.mark.parametrize("school", ["Pyromancy", "Cryomancy","Chronomancy", "Necromancy", "Enhancement",
                                    "Illusion", "Conjuration", "Shadow", "Transmutation"])
def test_valid_schools(school):
    wizard = Wizard("Test", school=school)
    assert wizard.school == school



def test_inventory_add_item():
  inv = Inventory()
  inv.add("Sword")
  assert len(inv.items) == 1
  assert "Sword" in inv.items

def test_location_is_a_location():
  assert Location.MOUNTAIN in Location.LOCATIONS

@pytest.mark.parametrize("location", [
    Location.CAVE,
    Location.MOUNTAIN,
    Location.FOREST,
])
def test_valid_locations(location):
    assert location in Location.LOCATIONS


def test_cave_common_items():
  common = Location.LOCATIONS[Location.CAVE]["common"]
  assert "rock" in common
  assert "mushroom" in common
  assert "bat_wing" in common
  assert "dust" in common






def test_map_fire_costs_manabda():
  wizard = Wizard("Test", school="Pyromancy", manabda=8)
  target = RavenSwarm()
  initial_manabda = wizard.manabda
  wizard.map_fire([target])
  assert wizard.manabda == initial_manabda - 3

def test_map_fire_deals_damage():
  wizard = Wizard("Test", school="Pyromancy", manabda=8)
  target = RavenSwarm()
  initial_hp = target.hp
  wizard.map_fire([target])
  assert target.hp < initial_hp

def test_reduce_ash_costs_manabda():
  wizard = Wizard("Test", school="Pyromancy", manabda=8)
  target = RavenSwarm()
  initial_manabda = wizard.manabda
  wizard.reduce_ash(target)
  assert wizard.manabda == initial_manabda - 5

def test_reduce_ash_kills_weak_target():
  wizard = Wizard("Test", school="Pyromancy", manabda=8)
  target = RavenSwarm()
  target.hp = 5
  wizard.reduce_ash(target)
  assert target.hp == 0

def test_pass_rune_returns_negated():
  rune = PassRune()
  player = Wizard("Test")
  result = rune.use(player)
  assert result == "negated"

def test_hp_potion_restores_hp():
  player = Wizard("Test", hp=100)
  player.hp = 50
  potion = HPPotion("I")
  potion.use(player)
  assert player.hp == 65

def test_hp_potion_does_not_exceed_max():
  player = Wizard("Test", hp=100)
  player.hp = 95
  potion = HPPotion("I")
  potion.use(player)
  assert player.hp == 100

def test_mana_potion_restores_mana():
  player = Wizard("Test")
  player.mana = 0
  potion = ManaPotion("I")
  potion.use(player)
  assert player.mana == 10

def test_finally_flask_fully_restores():
  player = Wizard("Test", hp=100)
  player.hp = 0
  flask = FinallyFlask()
  result = flask.use(player)
  assert player.hp == player.max_hp
  assert player.mana == player.max_mana
  assert player.manabda == 8
  assert result == "resurrected"

def test_except_vial_restores_quarter_hp():
  player = Wizard("Test", hp=100)
  player.hp = 10
  vial = ExceptVial()
  vial.use(player)
  assert player.hp == 35

def test_cloak_adds_defense():
  player = Wizard("Test")
  cloak = Cloak()
  cloak.equip(player)
  assert player.defense == 2

def test_cloak_removes_defense_on_unequip():
  player = Wizard("Test")
  cloak = Cloak()
  cloak.equip(player)
  cloak.unequip(player)
  assert player.defense == 0

def test_manabda_potion_does_not_exceed_max():
  player = Wizard("Test")
  player.manabda = 7
  potion = ManabdaPotion("I")
  potion.use(player)
  assert player.manabda == 8


def test_except_vial_restores_quarter_hp():
  player = Wizard("Test", hp=100)
  player.hp = 10
  vial = ExceptVial()
  vial.use(player)
  assert player.hp == 35


def test_except_vial_doesnt_exceed_max_hp():
  player = Wizard("Test", hp=100)
  player.hp = 90
  vial = ExceptVial()
  vial.use(player)
  assert player.hp == 100