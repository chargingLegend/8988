import pytest

from wizard import Wizard
from entities.monster import (RavenSwarm, Rat, Bat, Goblin, Wolf,
                               Skeleton, Spider, CaveTroll, Wraith, TrollKing)
from inventory import Inventory
from location import (Location, Town, Vardeth, FreeHollow,
                      Cave, DrevsCave, CrystalGrotta, Shadowhollow,
                      Forest, SylasForest, MireWood, WhisperGrove,
                      Mountain, FrostpeakMountain, StormridgeMountain, AshenPeak,
                      Ruins, OrathsRuins, ForgottenTemple, CollapsingCitadel)
from items import (Item, Consumable, Equipment, HPPotion, ManaPotion,
                   ManabdaPotion, PassRune, ExceptVial, FinallyFlask,
                   Cloak, Staff, Rod, Scepter)
from spawn import EnemySpawner
from entities.humanoid import DesperateTraveler, Enforcer, TitheCollector


# ── LOCATION HIERARCHY ───────────────────────────────────────

def test_location_is_grandparent():
  assert issubclass(Town, Location)
  assert issubclass(Cave, Location)
  assert issubclass(Forest, Location)
  assert issubclass(Mountain, Location)
  assert issubclass(Ruins, Location)

def test_vardeth_inherits_from_town():
  assert issubclass(Vardeth, Town)
  assert issubclass(Vardeth, Location)

def test_drevscave_inherits_from_cave():
  assert issubclass(DrevsCave, Cave)
  assert issubclass(DrevsCave, Location)

def test_sylasforest_inherits_from_forest():
  assert issubclass(SylasForest, Forest)
  assert issubclass(SylasForest, Location)

def test_frostpeak_inherits_from_mountain():
  assert issubclass(FrostpeakMountain, Mountain)
  assert issubclass(FrostpeakMountain, Location)

def test_orathsruins_inherits_from_ruins():
  assert issubclass(OrathsRuins, Ruins)
  assert issubclass(OrathsRuins, Location)


# ── LOCATION DEFAULTS ────────────────────────────────────────

def test_location_grandparent_defaults():
  assert Location.level_cap == 0
  assert Location.boss is None
  assert Location.enemy_table == []
  assert Location.common == []
  assert Location.uncommon == []
  assert Location.rare == []

def test_town_defaults():
  assert Town.vendors == []
  assert Town.requires_tithe == False
  assert Town.grind_available == False

def test_cave_defaults():
  assert Cave.grind_available == True
  assert Cave.boss is None
  assert Cave.enemy_table == []
  assert Cave.level_cap == 0


# ── VARDETH ──────────────────────────────────────────────────

def test_vardeth_level_cap():
  assert Vardeth.level_cap == 4

def test_vardeth_requires_tithe():
  assert Vardeth.requires_tithe == True

def test_vardeth_grind_available():
  assert Vardeth.grind_available == True

def test_vardeth_has_vendor():
  assert "Maren" in Vardeth.vendors

def test_vardeth_has_enemy_table():
  assert len(Vardeth.enemy_table) > 0

def test_vardeth_common_items():
  assert "broken_pavement" in Vardeth.common
  assert "paper_scrap" in Vardeth.common
  assert "empty_bottle" in Vardeth.common

def test_vardeth_uncommon_items():
  assert "silver_pendant" in Vardeth.uncommon
  assert "half_filled_ink_bottle" in Vardeth.uncommon

def test_vardeth_rare_items():
  assert "enforcer_badge" in Vardeth.rare
  assert "collectors_ledger" in Vardeth.rare

def test_vardeth_enemy_weights_sum_to_100():
  weights = [w for _, w in Vardeth.enemy_table]
  assert sum(weights) == 100


# ── DREVS CAVE ───────────────────────────────────────────────

def test_drevscave_level_cap():
  assert DrevsCave.level_cap == 6

def test_drevscave_boss():
  assert DrevsCave.boss == "Cave Troll"

def test_drevscave_has_vendor():
  assert "Drev" in DrevsCave.vendors

def test_drevscave_common_items():
  assert "rock" in DrevsCave.common
  assert "mushroom" in DrevsCave.common
  assert "bat_wing" in DrevsCave.common
  assert "dust" in DrevsCave.common

def test_drevscave_uncommon_items():
  assert "crystal_shard" in DrevsCave.uncommon
  assert "glowing_moss" in DrevsCave.uncommon

def test_drevscave_rare_items():
  assert "troll_blood_vial" in DrevsCave.rare
  assert "cave_pearl" in DrevsCave.rare

def test_drevscave_enemy_weights_sum_to_100():
  weights = [w for _, w in DrevsCave.enemy_table]
  assert sum(weights) == 100


# ── SYLAS FOREST ─────────────────────────────────────────────

def test_sylasforest_level_cap():
  assert SylasForest.level_cap == 10

def test_sylasforest_boss():
  assert SylasForest.boss == "Troll King"

def test_sylasforest_has_vendor():
  assert "Syla" in SylasForest.vendors

def test_sylasforest_rare_items():
  assert "ancient_root" in SylasForest.rare
  assert "glowspore" in SylasForest.rare

def test_sylasforest_enemy_weights_sum_to_100():
  weights = [w for _, w in SylasForest.enemy_table]
  assert sum(weights) == 100


# ── FROSTPEAK MOUNTAIN ───────────────────────────────────────

def test_frostpeak_level_cap():
  assert FrostpeakMountain.level_cap == 8

def test_frostpeak_boss():
  assert FrostpeakMountain.boss == "Wraith"

def test_frostpeak_common_items():
  assert "stone" in FrostpeakMountain.common
  assert "snow" in FrostpeakMountain.common
  assert "goat_hair" in FrostpeakMountain.common

def test_frostpeak_rare_items():
  assert "wraith_essence" in FrostpeakMountain.rare
  assert "ancient_ore" in FrostpeakMountain.rare

def test_frostpeak_enemy_weights_sum_to_100():
  weights = [w for _, w in FrostpeakMountain.enemy_table]
  assert sum(weights) == 100


# ── ORATHS RUINS ─────────────────────────────────────────────

def test_orathsruins_level_cap():
  assert OrathsRuins.level_cap == 12

def test_orathsruins_boss():
  assert OrathsRuins.boss == "Lich"

def test_orathsruins_has_vendor():
  assert "Orath" in OrathsRuins.vendors

def test_orathsruins_rare_items():
  assert "lich_fragment" in OrathsRuins.rare
  assert "forgotten_spellscroll" in OrathsRuins.rare

def test_orathsruins_enemy_weights_sum_to_100():
  weights = [w for _, w in OrathsRuins.enemy_table]
  assert sum(weights) == 100


# ── ALL LOCATIONS HAVE 3 ITEM TIERS ──────────────────────────

@pytest.mark.parametrize("loc", [
  DrevsCave, CrystalGrotta, Shadowhollow,
  SylasForest, MireWood, WhisperGrove,
  FrostpeakMountain, StormridgeMountain, AshenPeak,
  OrathsRuins, ForgottenTemple, CollapsingCitadel,
  Vardeth, FreeHollow
])
def test_all_locations_have_three_tiers(loc):
  assert len(loc.common) > 0
  assert len(loc.uncommon) > 0
  assert len(loc.rare) > 0

@pytest.mark.parametrize("loc", [
  DrevsCave, CrystalGrotta, Shadowhollow,
  SylasForest, MireWood, WhisperGrove,
  FrostpeakMountain, StormridgeMountain, AshenPeak,
  OrathsRuins, ForgottenTemple, CollapsingCitadel,
  Vardeth, FreeHollow
])
def test_all_locations_have_level_cap(loc):
  assert loc.level_cap > 0

@pytest.mark.parametrize("loc", [
  DrevsCave, CrystalGrotta, Shadowhollow,
  SylasForest, MireWood, WhisperGrove,
  FrostpeakMountain, StormridgeMountain, AshenPeak,
  OrathsRuins, ForgottenTemple, CollapsingCitadel,
  Vardeth, FreeHollow
])
def test_all_locations_have_boss(loc):
  assert loc.boss is not None

@pytest.mark.parametrize("loc", [
  DrevsCave, CrystalGrotta, Shadowhollow,
  SylasForest, MireWood, WhisperGrove,
  FrostpeakMountain, StormridgeMountain, AshenPeak,
  OrathsRuins, ForgottenTemple, CollapsingCitadel,
  Vardeth, FreeHollow
])
def test_all_locations_have_enemy_table(loc):
  assert len(loc.enemy_table) > 0


# ── SPAWN ────────────────────────────────────────────────────

def test_spawner_returns_enemy_below_level_cap():
  spawner = EnemySpawner(DrevsCave)
  enemy, is_boss = spawner.spawn(player_level=1)
  assert enemy is not None
  assert is_boss == False
  assert enemy.is_alive()

def test_spawner_returns_boss_at_level_cap():
  spawner = EnemySpawner(DrevsCave)
  enemy, is_boss = spawner.spawn(player_level=DrevsCave.level_cap)
  assert is_boss == True
  assert enemy.name == "Cave Troll"

def test_spawner_boss_is_alive():
  spawner = EnemySpawner(DrevsCave)
  enemy, is_boss = spawner.spawn(player_level=DrevsCave.level_cap)
  assert enemy.is_alive()

def test_spawner_forest_boss():
  spawner = EnemySpawner(SylasForest)
  enemy, is_boss = spawner.spawn(player_level=SylasForest.level_cap)
  assert is_boss == True
  assert enemy.name == "Troll King"

def test_spawner_mountain_boss():
  spawner = EnemySpawner(FrostpeakMountain)
  enemy, is_boss = spawner.spawn(player_level=FrostpeakMountain.level_cap)
  assert is_boss == True
  assert enemy.name == "Wraith"


# ── WIZARD EXISTING TESTS (preserved) ───────────────────────

def test_raven_swarm_inherits_from_monster():
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

@pytest.mark.parametrize("school", [
  "Pyromancy", "Cryomancy", "Chronomancy", "Necromancy",
  "Enhancement", "Illusion", "Conjuration", "Shadow", "Transmutation"
])
def test_valid_schools(school):
  wizard = Wizard("Test", school=school)
  assert wizard.school == school

def test_inventory_add_item():
  inv = Inventory()
  inv.add("Sword")
  assert len(inv.items) == 1
  assert "Sword" in inv.items

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

def test_except_vial_doesnt_exceed_max_hp():
  player = Wizard("Test", hp=100)
  player.hp = 90
  vial = ExceptVial()
  vial.use(player)
  assert player.hp == 100

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

# ── GRIND ────────────────────────────────────────────────────

from unittest.mock import patch, MagicMock
from systems.grind import grind

def make_player(level=1):
  p = Wizard(name="Test", level=level, school="Pyromancy")
  p.gold = 0
  p.flags = {}
  p.spells = ["Ignite"]
  return p

def test_grind_blocked_if_not_available():
  p = make_player()

  class NoGrind:
    grind_available = False
    level_cap = 4

  grind(p, NoGrind)  # should just return, no error

def test_grind_stops_at_grind_cap():
  p = make_player(level=6)  # DrevsCave cap is 6, grind_cap = 8
  with patch('builtins.input', return_value='y'):
    with patch('systems.grind.simple_combat') as mock_combat:
      grind(p, DrevsCave)
      mock_combat.assert_not_called()

def test_grind_player_gains_exp():
  p = make_player(level=1)
  starting_exp = p.exp
  with patch('builtins.input', side_effect=['n']):
    with patch('systems.grind.simple_combat') as mock_combat:
      def kill_enemy(player, enemy):
        enemy.hp = 0

      mock_combat.side_effect = kill_enemy
      grind(p, DrevsCave)
  assert p.exp > starting_exp

def test_grind_player_gains_gold():
  p = make_player(level=1)
  with patch('builtins.input', side_effect=['n']):
    with patch('systems.grind.simple_combat') as mock_combat:
      def kill_enemy(player, enemy):
        enemy.hp = 0

      mock_combat.side_effect = kill_enemy
      grind(p, DrevsCave)
  assert p.gold > 0

def test_grind_stops_if_player_dies():
  p = make_player(level=1)
  with patch('systems.grind.simple_combat') as mock_combat:
    def kill_player(player, enemy):
      player.hp = 0

    mock_combat.side_effect = kill_player
    grind(p, DrevsCave)
  assert not p.is_alive()

# ── HUMANOID COMBAT ──────────────────────────────────────────

from entities.humanoid import DesperateTraveler, Enforcer, TitheCollector

def test_desperate_traveler_attack_damages_target():
  traveler = DesperateTraveler()
  target = Wizard(name="Test", level=1, school="Pyromancy")
  starting_hp = target.hp
  traveler.attack(target)
  assert target.hp < starting_hp

def test_desperate_traveler_attack_melee_damages_target():
  traveler = DesperateTraveler()
  traveler.mana = 0  # force melee branch
  target = Wizard(name="Test", level=1, school="Pyromancy")
  starting_hp = target.hp
  traveler.attack(target)
  assert target.hp < starting_hp

def test_enforcer_attack_damages_target():
  enforcer = Enforcer()
  target = Wizard(name="Test", level=1, school="Pyromancy")
  starting_hp = target.hp
  enforcer.attack(target)
  assert target.hp < starting_hp

def test_enforcer_melee_damages_target():
  enforcer = Enforcer()
  enforcer.mana = 0
  target = Wizard(name="Test", level=1, school="Pyromancy")
  starting_hp = target.hp
  enforcer.attack(target)
  assert target.hp < starting_hp

def test_tithe_collector_attack_damages_target():
  collector = TitheCollector()
  target = Wizard(name="Test", level=1, school="Pyromancy")
  starting_hp = target.hp
  collector.attack(target)
  assert target.hp < starting_hp

def test_tithe_collector_melee_damages_target():
  collector = TitheCollector()
  collector.mana = 0
  target = Wizard(name="Test", level=1, school="Pyromancy")
  starting_hp = target.hp
  collector.attack(target)
  assert target.hp < starting_hp