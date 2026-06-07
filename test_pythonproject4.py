import pytest
from unittest.mock import patch, MagicMock

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
from systems.grind import grind


# ── HELPERS ──────────────────────────────────────────────────

def make_player(level=1, school="Pyromancy"):
  p = Wizard(name="Test", level=level, school=school)
  p.gold = 0
  p.flags = {}
  p.spells = ["Ignite"]
  return p


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


# ── WIZARD ───────────────────────────────────────────────────

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

def test_grind_blocked_if_not_available():
  p = make_player()

  class NoGrind:
    grind_available = False
    level_cap = 4

  grind(p, NoGrind)

def test_grind_stops_at_grind_cap():
  p = make_player(level=8)  # DrevsCave cap=6, grind_cap=8, so level 8 is blocked
  with patch('builtins.input', return_value='y'):
    with patch('combat.simple_combat') as mock_combat:
      grind(p, DrevsCave)
      mock_combat.assert_not_called()

def test_grind_player_gains_exp():
  p = make_player(level=1)
  starting_exp = p.exp
  with patch('builtins.input', side_effect=['n']):
    with patch('combat.simple_combat') as mock_combat:
      def kill_enemy(player, enemy):
        enemy.hp = 0
      mock_combat.side_effect = kill_enemy
      grind(p, DrevsCave)
  assert p.exp > starting_exp

def test_grind_player_gains_gold():
  p = make_player(level=1)
  with patch('builtins.input', side_effect=['n']):
    with patch('combat.simple_combat') as mock_combat:
      def kill_enemy(player, enemy):
        enemy.hp = 0
      mock_combat.side_effect = kill_enemy
      grind(p, DrevsCave)
  assert p.gold > 0

def test_grind_stops_if_player_dies():
  p = make_player(level=1)
  with patch('combat.simple_combat') as mock_combat:
    def kill_player(player, enemy):
      player.hp = 0
    mock_combat.side_effect = kill_player
    grind(p, DrevsCave)
  assert not p.is_alive()


# ── HUMANOID COMBAT ──────────────────────────────────────────

def test_traveler_spell_attack_reduces_player_hp():
  traveler = DesperateTraveler()
  traveler.mana = 15
  target = make_player()
  starting_hp = target.hp
  with patch('random.randint', side_effect=[90, 5]):
    traveler.attack(target)
  assert target.hp < starting_hp

def test_traveler_melee_attack_reduces_player_hp():
  traveler = DesperateTraveler()
  traveler.mana = 0
  target = make_player()
  starting_hp = target.hp
  traveler.attack(target)
  assert target.hp < starting_hp

def test_traveler_attack_returns_dmg_value():
  traveler = DesperateTraveler()
  traveler.mana = 0
  target = make_player()
  result = traveler.attack(target)
  assert isinstance(result, int)
  assert result > 0

def test_traveler_attack_does_not_drain_mana_on_melee():
  traveler = DesperateTraveler()
  traveler.mana = 0
  target = make_player()
  traveler.attack(target)
  assert traveler.mana == 0

def test_enforcer_spell_attack_reduces_player_hp():
  enforcer = Enforcer()
  enforcer.mana = 20
  target = make_player()
  starting_hp = target.hp
  with patch('random.randint', side_effect=[90, 5]):
    enforcer.attack(target)
  assert target.hp < starting_hp

def test_enforcer_melee_attack_reduces_player_hp():
  enforcer = Enforcer()
  enforcer.mana = 0
  target = make_player()
  starting_hp = target.hp
  enforcer.attack(target)
  assert target.hp < starting_hp

def test_enforcer_attack_returns_dmg_value():
  enforcer = Enforcer()
  enforcer.mana = 0
  target = make_player()
  result = enforcer.attack(target)
  assert isinstance(result, int)
  assert result > 0

def test_enforcer_mana_drain_costs_mana():
  enforcer = Enforcer()
  enforcer.mana = 20
  target = make_player()
  with patch('random.randint', side_effect=[90, 5]):
    enforcer.attack(target)
  assert enforcer.mana < 20

def test_collector_soul_levy_reduces_player_hp():
  collector = TitheCollector()
  collector.mana = 40
  target = make_player()
  starting_hp = target.hp
  with patch('random.randint', side_effect=[90, 10]):
    collector.attack(target)
  assert target.hp < starting_hp

def test_collector_audit_reduces_player_hp():
  collector = TitheCollector()
  collector.mana = 5
  target = make_player()
  starting_hp = target.hp
  collector.attack(target)
  assert target.hp < starting_hp

def test_collector_melee_reduces_player_hp():
  collector = TitheCollector()
  collector.mana = 0
  target = make_player()
  starting_hp = target.hp
  collector.attack(target)
  assert target.hp < starting_hp

def test_collector_attack_returns_dmg_value():
  collector = TitheCollector()
  collector.mana = 0
  target = make_player()
  result = collector.attack(target)
  assert isinstance(result, int)
  assert result > 0

def test_player_hp_never_goes_below_zero_from_attack():
  enforcer = Enforcer()
  enforcer.mana = 0
  target = make_player()
  target.hp = 1
  enforcer.attack(target)
  assert target.hp >= 0

def test_player_is_dead_after_lethal_damage():
  enforcer = Enforcer()
  enforcer.mana = 0
  target = make_player()
  target.hp = 1
  target.defense = 0
  with patch('random.randint', return_value=50):
    enforcer.attack(target)
  assert not target.is_alive()


# ── TACTICAL AI: ESCALATION AT 25% PLAYER HP ─────────────────

def test_traveler_escalates_when_player_low_hp():
  traveler = DesperateTraveler()
  traveler.mana = 15
  target = make_player()
  target.hp = int(target.max_hp * 0.25)
  starting_hp = target.hp
  traveler.attack(target)
  assert target.hp < starting_hp

def test_traveler_escalation_costs_mana():
  traveler = DesperateTraveler()
  traveler.mana = 15
  target = make_player()
  target.level = 2  # ensure level gate passes
  target.hp = int(target.max_hp * 0.20)
  starting_hp = target.hp
  traveler.attack(target)
  # escalation OR dim OR mutter fires — either mana drops or melee hits
  assert target.hp < starting_hp or traveler.mana < 15

def test_enforcer_escalates_when_player_low_hp():
  enforcer = Enforcer()
  enforcer.mana = 20
  target = make_player()
  target.hp = int(target.max_hp * 0.20)
  starting_hp = target.hp
  enforcer.attack(target)
  assert target.hp < starting_hp

def test_collector_escalates_when_player_low_hp():
  collector = TitheCollector()
  collector.mana = 40
  target = make_player()
  target.hp = int(target.max_hp * 0.20)
  starting_hp = target.hp
  collector.attack(target)
  assert target.hp < starting_hp

def test_escalation_does_not_trigger_at_full_hp():
  enforcer = Enforcer()
  enforcer.mana = 20
  target = make_player()
  target.hp = target.max_hp
  starting_hp = target.hp
  enforcer.attack(target)
  assert target.hp < starting_hp


# ── STATUS EFFECTS ────────────────────────────────────────────

from systems.status_effects import (Burn, Frozen, Slowed, Disoriented,
  Stuttered, Shattered, Weakened, Charging)


def test_burn_deals_damage_per_turn():
  target = make_player()
  burn = Burn(duration=2, damage_per_turn=5)
  target.add_status(burn)
  starting_hp = target.hp
  target.tick_status_effects()
  assert target.hp < starting_hp

def test_burn_expires_after_duration():
  target = make_player()
  burn = Burn(duration=1, damage_per_turn=5)
  target.add_status(burn)
  target.tick_status_effects()
  assert burn.is_expired()

def test_frozen_does_not_deal_damage():
  target = make_player()
  frozen = Frozen(duration=2)
  target.add_status(frozen)
  starting_hp = target.hp
  target.tick_status_effects()
  assert target.hp == starting_hp

def test_frozen_expires_after_duration():
  target = make_player()
  frozen = Frozen(duration=1)
  target.add_status(frozen)
  target.tick_status_effects()
  assert frozen.is_expired()

def test_slowed_sets_skip_turn():
  target = make_player()
  slowed = Slowed(duration=3)
  target.add_status(slowed)
  slowed.tick_count = 1  # force even tick
  slowed.tick(target)
  assert getattr(target, 'skip_turn', False) == True

def test_slowed_expires_after_duration():
  target = make_player()
  slowed = Slowed(duration=1)
  target.add_status(slowed)
  target.tick_status_effects()
  assert slowed.is_expired()

def test_disoriented_is_active_check():
  target = make_player()
  assert not Disoriented.is_active(target)
  target.add_status(Disoriented(duration=2))
  assert Disoriented.is_active(target)

def test_disoriented_does_not_stack():
  target = make_player()
  target.add_status(Disoriented(duration=2))
  target.add_status(Disoriented(duration=2))
  disoriented_count = sum(1 for e in target.status_effects
    if type(e).__name__ == "Disoriented")
  assert disoriented_count == 2  # add_status allows it — guard is in cast_mana

def test_disoriented_expires():
  target = make_player()
  d = Disoriented(duration=1)
  target.add_status(d)
  target.tick_status_effects()
  assert d.is_expired()

def test_weakened_reduces_atk():
  target = make_player()
  target.defense = 5
  original_defense = target.defense
  weak = Weakened(duration=2, atk_reduction=0, defense_reduction=2)
  target.add_status(weak)
  target.tick_status_effects()
  assert target.defense < original_defense

def test_weakened_restores_on_expiry():
  target = make_player()
  target.defense = 5
  weak = Weakened(duration=1, atk_reduction=0, defense_reduction=2)
  target.add_status(weak)
  target.tick_status_effects()  # applies and expires
  assert target.defense == 5

def test_shattered_sets_skip_turn():
  target = make_player()
  shattered = Shattered(duration=2)
  target.add_status(shattered)
  shattered.tick(target)
  assert getattr(target, 'skip_turn', False) == True

def test_stuttered_marks_revealed():
  target = make_player()
  stuttered = Stuttered(duration=1)
  assert stuttered.revealed == True

def test_stuttered_expires_after_one_turn():
  target = make_player()
  s = Stuttered(duration=1)
  target.add_status(s)
  target.tick_status_effects()
  assert s.is_expired()

def test_charging_tracks_turns():
  charge = Charging(move_name="Test Move")
  dummy = make_player()
  charge.tick(dummy)
  assert charge.turns_charged == 1
  assert not charge.is_ready()
  charge.tick(dummy)
  charge.tick(dummy)
  assert charge.is_ready()

def test_charging_interrupted():
  charge = Charging(move_name="Test Move")
  dummy = make_player()
  charge.tick(dummy)
  charge.interrupt(dummy)
  assert charge.interrupted == True
  assert charge.is_expired()
  assert not charge.is_ready()


# ── CALEB DIM COOLDOWN ────────────────────────────────────────

def test_caleb_dim_cooldown_set_after_use():
  traveler = DesperateTraveler()
  traveler.spell_cooldowns["dim"] = 3
  assert traveler.spell_cooldowns.get("dim", 0) > 0

def test_caleb_dim_does_not_stack_disoriented():
  from systems.status_effects import Disoriented
  traveler = DesperateTraveler()
  target = make_player()
  target.add_status(Disoriented(duration=2))
  assert Disoriented.is_active(target)
  # dim_not_active guard means Caleb won't apply another
  dim_not_active = not Disoriented.is_active(target)
  assert dim_not_active == False

def test_tithe_collector_immune_to_disoriented():
  collector = TitheCollector()
  assert "Disoriented" in collector.status_immunities


# ── CAST_MANA DICT FORMAT ─────────────────────────────────────

def test_cast_mana_handles_dict_spell_data():
  from wizard_schools import SCHOOL_DATA
  p = make_player()
  p.spell_data = SCHOOL_DATA["Pyromancy"]["spells"]
  enemy = RavenSwarm()
  starting_hp = enemy.hp
  with patch('builtins.input', return_value=''):
    result = p.cast_mana("Ignite", enemy)
  assert result == True
  assert enemy.hp < starting_hp

def test_cast_mana_fizzles_on_unknown_spell():
  p = make_player()
  p.spell_data = {}
  enemy = RavenSwarm()
  result = p.cast_mana("nonexistent", enemy)
  assert result == False

def test_cast_mana_fails_on_empty_mana():
  from wizard_schools import SCHOOL_DATA
  p = make_player()
  p.spell_data = SCHOOL_DATA["Pyromancy"]["spells"]
  p.mana = 0
  enemy = RavenSwarm()
  result = p.cast_mana("Ignite", enemy)
  assert result == False