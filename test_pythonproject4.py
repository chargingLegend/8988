import pytest

from characters import Wizard
from entities.monster import RavenSwarm
from Inventory import Inventory
from location import Location

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