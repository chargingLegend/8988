import pytest
from characters import Wizard
from entities.monster import RavenSwarm
from Inventory import Inventory
from main import Mountain

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

def test_inventory_add_item():
  inv = Inventory()
  inv.add("Sword")
  assert len(inv.items) == 1
  assert "Sword" in inv.items



def test_wizard_starts_with_no_spells():
  wizard = Wizard("Gandalf")
  assert len(wizard.spells) == 0