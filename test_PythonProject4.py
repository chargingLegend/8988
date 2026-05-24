import pytest
from main import RavenSwarm, Inventory, Wizard, Mountain

def test_Raven_Swarm_inherits_from_monster():
    swarm = RavenSwarm()
    assert swarm.hp == 15
    assert swarm.name == "RavenSwarm"
    assert swarm.exo_value == 50
    assert swarm.is_alive() == True

def test_inventory_starts_empty():
    inv = Inventory()
    assert len(inv.items) == 0
    assert str(inv) == "Inventory empty."

def test_inventory_add_item():
    inv = Inventory()
    result = inv.add("Rock")
    assert "Rock" in inv.items
    assert len(inv.items) == 1
    assert result == "Added Rock to inventory."

def test_inventory_full_raises_error():
    inv = Inventory()
    inv.max_size = 2
    inv.add("Rock")
    inv.add("Stick")
    with pytest.raises(Exception, match="Inventory full"):
        inv.add("Snow")

def test_inventory_remove_item():
    inv = Inventory()
    inv.add("Rock")
    result = inv.remove("Rock")
    assert "Rock" not in inv.items
    assert result == "Used Rock."

def test_inventory_remove_missing_raises_error():
    inv = Inventory()
    with pytest.raises(ValueError, match="Ancient Coin not in inventory"):
        inv.remove("Ancient Coin")

def test_sort_locked_by_default():
    player = Wizard(name="TestWizard")
    with pytest.raises(AttributeError, match="trace the rune"):
        player.sort(Mountain)

def test_learn_sort_unlocks_spell():
    player = Wizard(name="TestWizard")
    result = player.learn_spell_sort()
    assert "sort" in player.known_spells
    assert "rune" in result.lower()

def test_sort_finds_items_after_unlock():
    player = Wizard(name="TestWizard")
    player.learn_spell_sort()
    found = player.sort(Mountain)
    assert len(found) >= 2
    assert len(player.inventory.items) >= 2
    assert all(item in Mountain["common"] + Mountain["uncommon"] for item in found)

def test_sort_uncommon_chance():
    player = Wizard(name="TestWizard")
    player.learn_spell_sort()
    uncommon_count = 0
    for _ in range(100):
        player.inventory.items = []
        found = player.sort(Mountain)
        if "Mountain Herb" in found:
            uncommon_count += 1
    assert 3 <= uncommon_count <= 20

def test_wizard_starts_with_inventory():
    player = Wizard(name="TestWizard")
    assert player.inventory is not None
    assert len(player.inventory.items) == 0


