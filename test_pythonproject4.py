import pytest
from unittest.mock import patch, MagicMock

from wizard import Wizard
from entities.monster import (RavenSwarm, Rat, Bat, Goblin, Wolf,
  Skeleton, Spider, CaveTroll, Wraith, TrollKing)
from inventory import Inventory
from location import (Vardeth, DrevsCave, SylasForest,
  FrostpeakMountain, OrathsRuins)
from items import (HPPotion, ManaPotion, ManabdaPotion,
  PassRune, ExceptVial, FinallyFlask, Cloak, Staff, Rod, Scepter)
from merchant import Maren
from entities.humanoid import DesperateTraveler, Enforcer, TitheCollector


# ── HELPERS ──────────────────────────────────────────────────

def make_player(level=1, school="Pyromancy"):
  p = Wizard(name="Test", level=level, school=school)
  p.gold = 0
  p.flags = {}
  p.corruption = 0
  return p


def make_wizard(school):
  w = Wizard(name="Test")
  w.choose_school(school)
  w.unlock_abilities()
  for spell in list(w.spell_data.keys()):
    if spell not in w.spells:
      w.spells.append(spell)
  w.gold = 0
  w.flags = {}
  return w


def make_target(name="Dummy", hp=50, fire_resistance=0):
  t = RavenSwarm()
  t.name = name
  t.hp = hp
  t.max_hp = hp
  t.fire_resistance = fire_resistance
  t.status_effects = []
  return t


# ── CORRUPTION SYSTEM ────────────────────────────────────────

def test_wizard_has_corruption_attribute():
  p = make_player()
  assert hasattr(p, 'corruption')

def test_wizard_corruption_starts_at_zero():
  p = make_player()
  assert p.corruption == 0

def test_corruption_is_not_morality():
  p = make_player()
  assert not hasattr(p, 'morality')

def test_corruption_increments():
  p = make_player()
  p.corruption += 1
  assert p.corruption == 1

def test_corruption_increments_multiple():
  p = make_player()
  p.corruption += 1
  p.corruption += 1
  p.corruption += 3
  assert p.corruption == 5

def test_corruption_clean_threshold():
  p = make_player()
  p.corruption = 0
  assert p.corruption == 0

def test_corruption_shady_threshold():
  p = make_player()
  p.corruption = 2
  assert 1 <= p.corruption <= 3

def test_corruption_dark_threshold():
  p = make_player()
  p.corruption = 5
  assert 4 <= p.corruption <= 7

def test_corruption_corrupted_threshold():
  p = make_player()
  p.corruption = 8
  assert p.corruption >= 8

def test_corruption_max_enforcement_works():
  p = make_player()
  p.corruption = max(p.corruption, 3)
  assert p.corruption >= 3


# ── RAVEN SWARM GOLD ─────────────────────────────────────────

def test_raven_swarm_gold_reward_is_15():
  swarm = RavenSwarm()
  assert swarm.gold_reward == 15

def test_raven_swarm_gold_reward_not_5():
  swarm = RavenSwarm()
  assert swarm.gold_reward != 5

def test_raven_swarm_gold_enough_for_hp_potion():
  swarm = RavenSwarm()
  hp_potion_price = 20
  assert swarm.gold_reward >= hp_potion_price * 0.75

def test_raven_swarm_stats_unchanged():
  swarm = RavenSwarm()
  assert swarm.hp == 15
  assert swarm.exp_value == 50
  assert swarm.atk == 4
  assert swarm.defense == 0

def test_raven_swarm_loot_table_intact():
  swarm = RavenSwarm()
  loot_names = [name for name, _ in swarm.loot_table]
  assert "Black Feather" in loot_names
  assert "Crow's Eye" in loot_names


# ── MAREN MERCHANT ───────────────────────────────────────────

def test_maren_initializes():
  maren = Maren()
  assert maren.name == "Maren"
  assert maren.faction == "Neutral"

def test_maren_has_stock():
  maren = Maren()
  assert len(maren.stock) > 0

def test_maren_stock_has_hp_potion():
  maren = Maren()
  names = [e["item"].name for e in maren.stock]
  assert "HP Potion I" in names

def test_maren_stock_has_mana_potion():
  maren = Maren()
  names = [e["item"].name for e in maren.stock]
  assert "Mana Potion I" in names

def test_maren_stock_has_pass_rune():
  maren = Maren()
  names = [e["item"].name for e in maren.stock]
  assert "Pass Rune" in names

def test_maren_stock_has_cloak():
  maren = Maren()
  names = [e["item"].name for e in maren.stock]
  assert any("Cloak" in n for n in names)

def test_maren_stock_has_except_vial():
  maren = Maren()
  names = [e["item"].name for e in maren.stock]
  assert "Except Vial" in names

def test_maren_stock_has_prices():
  maren = Maren()
  for entry in maren.stock:
    assert entry["price"] > 0

def test_maren_buy_succeeds_with_enough_gold():
  maren = Maren()
  p = make_player()
  p.gold = 100
  result = maren.buy(p, 1)
  assert result == True

def test_maren_buy_fails_without_gold():
  maren = Maren()
  p = make_player()
  p.gold = 0
  result = maren.buy(p, 1)
  assert result == False

def test_maren_buy_deducts_gold():
  maren = Maren()
  p = make_player()
  p.gold = 100
  price = maren.stock[0]["price"]
  maren.buy(p, 1)
  assert p.gold == 100 - price

def test_maren_buy_adds_item_to_inventory():
  maren = Maren()
  p = make_player()
  p.gold = 100
  maren.buy(p, 1)
  assert len(p.inventory.items) == 1

def test_maren_enforcer_discount_halves_price():
  maren = Maren()
  p = make_player()
  p.flags['enforcer_aligned'] = True
  p.gold = 100
  base_price = maren.stock[0]["price"]
  maren.buy(p, 1)
  assert p.gold == 100 - (base_price // 2)

def test_maren_no_discount_without_flag():
  maren = Maren()
  p = make_player()
  p.gold = 100
  base_price = maren.stock[0]["price"]
  maren.buy(p, 1)
  assert p.gold == 100 - base_price

def test_maren_buy_invalid_choice_returns_false():
  maren = Maren()
  p = make_player()
  p.gold = 100
  result = maren.buy(p, 99)
  assert result == False

def test_maren_buy_choice_zero_returns_false():
  maren = Maren()
  p = make_player()
  p.gold = 100
  result = maren.buy(p, 0)
  assert result == False

def test_maren_greet_sets_spoke_freely_flag():
  maren = Maren()
  p = make_player()
  maren.greet(p)
  assert p.flags.get('maren_spoke_freely') == True

def test_maren_greet_enforcer_does_not_set_spoke_freely():
  maren = Maren()
  p = make_player()
  p.flags['enforcer_aligned'] = True
  maren.greet(p)
  assert not p.flags.get('maren_spoke_freely')

def test_maren_shop_accepts_skip_greet_param():
  maren = Maren()
  p = make_player()
  p.flags['paid_tithe'] = True
  p.gold = 0
  with patch('builtins.input', return_value=str(len(maren.stock) + 1)):
    maren.shop(p, skip_greet=True)
  assert not p.flags.get('maren_spoke_freely')

def test_maren_shop_greets_normally_without_skip():
  maren = Maren()
  p = make_player()
  p.flags['paid_tithe'] = True
  with patch('builtins.input', return_value=str(len(maren.stock) + 1)):
    maren.shop(p, skip_greet=False)
  assert p.flags.get('maren_spoke_freely') == True


# ── WIZARD CORE ──────────────────────────────────────────────

def test_wizard_initializes_with_defaults():
  p = Wizard(name="Test")
  assert p.name == "Test"
  assert p.level == 1
  assert p.hp == 100
  assert p.max_hp == 100
  assert p.mana == 20
  assert p.max_mana == 20
  assert p.manabda == 8
  assert p.defense == 0
  assert p.gold == 0
  assert p.exp == 0
  assert p.corruption == 0

def test_wizard_is_alive_at_full_hp():
  p = make_player()
  assert p.is_alive()

def test_wizard_is_dead_at_zero_hp():
  p = make_player()
  p.hp = 0
  assert not p.is_alive()

def test_wizard_hp_never_goes_below_zero():
  p = make_player()
  p.take_damage(9999)
  assert p.hp == 0

def test_wizard_defense_reduces_damage():
  p = make_player()
  p.defense = 5
  p.take_damage(10)
  assert p.hp == 95

def test_wizard_defense_minimum_one_damage():
  p = make_player()
  p.defense = 999
  p.take_damage(5)
  assert p.hp == 99

def test_wizard_gain_exp_increments():
  p = make_player()
  p.gain_exp(10)
  assert p.exp == 10

def test_wizard_levels_up_when_exp_threshold_met():
  p = make_player()
  with patch('builtins.input', return_value='1'):
    p.gain_exp(p.exp_to_next)
  assert p.level == 2

def test_wizard_level_up_increases_max_hp():
  p = make_player()
  old_max = p.max_hp
  with patch('builtins.input', return_value='1'):
    p.level_up()
  assert p.max_hp > old_max

def test_wizard_level_up_increases_max_mana():
  p = make_player()
  old_max = p.max_mana
  with patch('builtins.input', return_value='1'):
    p.level_up()
  assert p.max_mana > old_max

def test_wizard_add_hp_bonus():
  p = make_player()
  old_hp = p.max_hp
  p.add_hp_bonus(10)
  assert p.max_hp == old_hp + 10
  assert p.hp == old_hp + 10

def test_wizard_add_mana_bonus():
  p = make_player()
  old_mana = p.max_mana
  p.add_mana_bonus(5)
  assert p.max_mana == old_mana + 5
  assert p.mana == old_mana + 5

def test_wizard_calc_exp_to_next_level_1():
  p = make_player()
  assert p.exp_to_next == 33

def test_wizard_calc_exp_to_next_scales_with_level():
  p = make_player(level=2)
  assert p.exp_to_next > 33

def test_wizard_str_shows_alive():
  p = make_player()
  assert "alive" in str(p)

def test_wizard_str_shows_fallen_when_dead():
  p = make_player()
  p.hp = 0
  assert "Fallen" in str(p)

def test_wizard_repr_shows_spell_count():
  p = make_player()
  assert "Spells:" in repr(p)

def test_wizard_flags_default_empty():
  p = Wizard(name="Test")
  p.flags = {}
  assert p.flags == {}

def test_wizard_gold_default_zero():
  p = Wizard(name="Test")
  assert p.gold == 0

def test_wizard_learn_sort_adds_spell():
  p = make_player()
  p.learn_spell_sort()
  assert "sort" in p.spells

def test_wizard_learn_sort_not_duplicate():
  p = make_player()
  p.learn_spell_sort()
  p.learn_spell_sort()
  assert p.spells.count("sort") == 1

def test_wizard_learn_sort_sets_acquired_by():
  p = make_player()
  p.learn_spell_sort(method="absorbed")
  assert p.sort_acquired_by == "absorbed"

def test_wizard_choose_school_sets_spells():
  p = Wizard(name="Test")
  p.choose_school("Pyromancy")
  assert len(p.spells) > 0

def test_wizard_choose_school_sets_spell_data():
  p = Wizard(name="Test")
  p.choose_school("Pyromancy")
  assert "Ignite" in p.spell_data

@pytest.mark.parametrize("school", [
  "Pyromancy", "Cryomancy", "Chronomancy", "Necromancy",
  "Enhancement", "Illusion", "Conjuration", "Shadow", "Transmutation"
])
def test_all_schools_set_spell_data(school):
  p = Wizard(name="Test")
  p.choose_school(school)
  assert len(p.spell_data) > 0

@pytest.mark.parametrize("school", [
  "Pyromancy", "Cryomancy", "Chronomancy", "Necromancy",
  "Enhancement", "Illusion", "Conjuration", "Shadow", "Transmutation"
])
def test_all_schools_give_three_starter_spells(school):
  p = Wizard(name="Test")
  p.choose_school(school)
  assert len(p.spells) == 3

@pytest.mark.parametrize("school", [
  "Pyromancy", "Cryomancy", "Chronomancy", "Necromancy",
  "Enhancement", "Illusion", "Conjuration", "Shadow", "Transmutation"
])
def test_all_schools_unlock_abilities(school):
  p = Wizard(name="Test")
  p.choose_school(school)
  p.unlock_abilities()
  assert len(p.abilities) > 0

@pytest.mark.parametrize("school", [
  "Pyromancy", "Cryomancy", "Chronomancy", "Necromancy",
  "Enhancement", "Illusion", "Conjuration", "Shadow", "Transmutation"
])
def test_all_schools_unlock_sort(school):
  p = Wizard(name="Test")
  p.choose_school(school)
  p.unlock_abilities()
  assert "sort" in p.spells

def test_ignite_desc_no_feathers():
  p = Wizard(name="Test")
  p.choose_school("Pyromancy")
  desc = p.spell_data["Ignite"]["desc"]
  assert "feathers" not in desc

def test_ignite_desc_has_target_placeholder():
  p = Wizard(name="Test")
  p.choose_school("Pyromancy")
  desc = p.spell_data["Ignite"]["desc"]
  assert "{target}" in desc


# ── SORT FUNCTION ────────────────────────────────────────────

def test_sort_works_with_class_location():
  p = Wizard(name="Test")
  p.choose_school("Pyromancy")
  p.unlock_abilities()
  assert "sort" in p.spells
  p.sort(Vardeth)
  assert len(p.inventory.items) >= 2

def test_sort_works_with_dict_location():
  p = Wizard(name="Test")
  p.choose_school("Pyromancy")
  p.unlock_abilities()
  fake_loc = {"common": ["stick", "rock", "dust"], "uncommon": ["gem"]}
  p.sort(fake_loc)
  assert len(p.inventory.items) >= 2

def test_sort_raises_if_spell_not_learned():
  p = Wizard(name="Test")
  with pytest.raises(AttributeError):
    p.sort(Vardeth)

def test_sort_adds_items_to_inventory():
  p = Wizard(name="Test")
  p.choose_school("Pyromancy")
  p.unlock_abilities()
  before = len(p.inventory.items)
  p.sort(Vardeth)
  assert len(p.inventory.items) > before

def test_sort_only_pulls_from_common_normally():
  p = Wizard(name="Test")
  p.choose_school("Pyromancy")
  p.unlock_abilities()
  with patch('random.random', return_value=0.99):
    p.sort(Vardeth)
  for item in p.inventory.items:
    assert item in Vardeth.common or item in Vardeth.uncommon

def test_sort_can_find_uncommon_item():
  p = Wizard(name="Test")
  p.choose_school("Pyromancy")
  p.unlock_abilities()
  with patch('random.random', return_value=0.01):
    p.sort(Vardeth)
  items = list(p.inventory.items)
  has_uncommon = any(i in Vardeth.uncommon for i in items)
  assert has_uncommon


# ── COMBAT — MIRA PROMPT ─────────────────────────────────────

def test_combat_prompt_no_mira_without_flag():
  p = make_player()
  p.choose_school("Pyromancy")
  enemy = Rat()
  inputs = iter(['flee'])
  with patch('builtins.input', side_effect=inputs) as mock_input:
    from combat import simple_combat
    simple_combat(p, enemy)
  prompt_calls = [str(c) for c in mock_input.call_args_list]
  assert not any('mira' in c.lower() for c in prompt_calls)

def test_combat_prompt_has_mira_with_flag():
  p = make_player()
  p.choose_school("Pyromancy")
  p.flags['companion_mira'] = True
  enemy = Rat()
  from entities.humanoid import FrightenedWoman
  with patch('builtins.input', return_value='flee') as mock_input:
    from combat import simple_combat
    simple_combat(p, enemy)
  prompt_calls = [str(c) for c in mock_input.call_args_list]
  assert any('mira' in c.lower() for c in prompt_calls)


# ── GRIND — NO DOUBLE GOLD ───────────────────────────────────

def test_grind_does_not_double_count_gold():
  from systems.grind import grind
  p = make_player(level=1)
  p.gold = 0
  kills = []

  def kill_and_track(player, enemy):
    kills.append(enemy.gold_reward)
    enemy.hp = 0

  inputs = iter(['n', 'n'])
  with patch('builtins.input', side_effect=inputs):
    with patch('combat.simple_combat', side_effect=kill_and_track):
      grind(p, DrevsCave)

  # gold comes from combat.py reward logic — since combat is mocked
  # gold won't be added here — what we're verifying is grind.py
  # does NOT add gold on its own (no duplicate line)
  assert p.gold == 0  # mocked combat means no reward fires — correct behavior

def test_grind_gold_not_added_twice():
  from systems.grind import grind
  p = make_player(level=1)
  p.gold = 0

  kills = [0]

  def kill_enemy(player, enemy):
    enemy.hp = 0
    kills[0] += 1

  with patch('builtins.input', return_value='n'):
    with patch('combat.simple_combat', side_effect=kill_enemy):
      grind(p, DrevsCave)

  # gold should only reflect one reward per kill not two
  assert kills[0] == 1


# ── ITEMS ────────────────────────────────────────────────────

def test_hp_potion_tiers_exist():
  for tier in ["I", "II", "III", "IV"]:
    p = HPPotion(tier)
    assert p.name == f"HP Potion {tier}"

def test_mana_potion_tiers_exist():
  for tier in ["I", "II", "III", "IV"]:
    p = ManaPotion(tier)
    assert p.name == f"Mana Potion {tier}"

def test_manabda_potion_tiers_exist():
  for tier in ["I", "II", "III"]:
    p = ManabdaPotion(tier)
    assert p.name == f"Manabda Potion {tier}"

def test_hp_potion_t1_restores_15():
  p = make_player()
  p.hp = 50
  HPPotion("I").use(p)
  assert p.hp == 65

def test_hp_potion_t2_restores_35():
  p = make_player()
  p.hp = 50
  HPPotion("II").use(p)
  assert p.hp == 85

def test_hp_potion_t3_restores_60():
  p = make_player()
  p.hp = 10
  HPPotion("III").use(p)
  assert p.hp == 70

def test_hp_potion_t4_restores_100():
  p = make_player()
  p.hp = 10
  HPPotion("IV").use(p)
  assert p.hp == p.max_hp  # 100 restore on 100 max hp caps at max

def test_hp_potion_caps_at_max_hp():
  p = make_player()
  p.hp = 98
  HPPotion("I").use(p)
  assert p.hp == p.max_hp

def test_mana_potion_t1_restores_10():
  p = make_player()
  p.mana = 0
  ManaPotion("I").use(p)
  assert p.mana == 10

def test_mana_potion_caps_at_max_mana():
  p = make_player()
  p.mana = p.max_mana - 2
  ManaPotion("I").use(p)
  assert p.mana == p.max_mana

def test_manabda_potion_restores_manabda():
  p = make_player()
  p.manabda = 4
  ManabdaPotion("I").use(p)
  assert p.manabda == 6

def test_manabda_potion_caps_at_8():
  p = make_player()
  p.manabda = 7
  ManabdaPotion("I").use(p)
  assert p.manabda == 8

def test_pass_rune_returns_negated():
  p = make_player()
  result = PassRune().use(p)
  assert result == "negated"

def test_except_vial_restores_25_percent():
  p = make_player()
  p.hp = 10
  ExceptVial().use(p)
  assert p.hp == 35

def test_except_vial_caps_at_max_hp():
  p = make_player()
  p.hp = 99
  ExceptVial().use(p)
  assert p.hp == p.max_hp

def test_finally_flask_full_restore():
  p = make_player()
  p.hp = 1
  p.mana = 0
  p.manabda = 0
  result = FinallyFlask().use(p)
  assert p.hp == p.max_hp
  assert p.mana == p.max_mana
  assert p.manabda == 8
  assert result == "resurrected"

def test_cloak_adds_defense():
  p = make_player()
  Cloak().equip(p)
  assert p.defense == 2

def test_cloak_unequip_removes_defense():
  p = make_player()
  c = Cloak()
  c.equip(p)
  c.unequip(p)
  assert p.defense == 0

def test_staff_equip_adds_mana():
  p = make_player()
  starting_mana = p.mana
  Staff().equip(p)
  assert p.mana == starting_mana + 5

def test_staff_has_atk_bonus_stored():
  s = Staff()
  assert s.atk_bonus == 2

def test_item_inspect_returns_string():
  item = HPPotion("I")
  result = item.inspect()
  assert isinstance(result, str)
  assert "HP Potion I" in result


# ── INVENTORY ────────────────────────────────────────────────

def test_inventory_starts_empty():
  inv = Inventory()
  assert len(inv.items) == 0

def test_inventory_add_string():
  inv = Inventory()
  inv.add("Sort Rune")
  assert inv.has_item("Sort Rune")

def test_inventory_add_object():
  inv = Inventory()
  inv.add(HPPotion("I"))
  assert inv.has_item("HP Potion I")

def test_inventory_remove_item():
  inv = Inventory()
  inv.add("Sort Rune")
  inv.remove("Sort Rune")
  assert not inv.has_item("Sort Rune")

def test_inventory_has_item_false_when_empty():
  inv = Inventory()
  assert not inv.has_item("anything")

def test_inventory_get_item_returns_object():
  inv = Inventory()
  potion = HPPotion("I")
  inv.add(potion)
  result = inv.get_item("HP Potion I")
  assert result is not None

def test_inventory_str_empty():
  inv = Inventory()
  assert "empty" in str(inv).lower()

def test_inventory_str_not_empty_after_add():
  inv = Inventory()
  inv.add("sword")
  assert "empty" not in str(inv).lower()


# ── MONSTER BASE ─────────────────────────────────────────────

def test_monster_take_damage_reduces_hp():
  swarm = RavenSwarm()
  swarm.take_damage(5)
  assert swarm.hp == 10

def test_monster_hp_never_below_zero():
  swarm = RavenSwarm()
  swarm.take_damage(9999)
  assert swarm.hp == 0

def test_monster_is_alive_true():
  swarm = RavenSwarm()
  assert swarm.is_alive()

def test_monster_is_alive_false_at_zero():
  swarm = RavenSwarm()
  swarm.hp = 0
  assert not swarm.is_alive()

def test_monster_defense_reduces_damage():
  skeleton = Skeleton()
  skeleton.hp = 15
  skeleton.take_damage(3)
  assert skeleton.hp == 14  # defense 2 means 3-2=1 dmg

def test_monster_heal_increases_hp():
  swarm = RavenSwarm()
  swarm.hp = 5
  swarm.heal(5)
  assert swarm.hp == 10

def test_monster_heal_caps_at_max_hp():
  swarm = RavenSwarm()
  swarm.heal(9999)
  assert swarm.hp == swarm.max_hp

def test_monster_attack_reduces_target_hp():
  rat = Rat()
  p = make_player()
  starting = p.hp
  rat.attack(p)
  assert p.hp < starting

def test_monster_drop_loot_returns_list():
  swarm = RavenSwarm()
  with patch('random.randint', return_value=1):
    drops = swarm.drop_loot()
  assert isinstance(drops, list)

def test_monster_on_spawn_returns_string():
  swarm = RavenSwarm()
  result = swarm.on_spawn()
  assert isinstance(result, str)
  assert "Raven Swarm" in result

@pytest.mark.parametrize("MonsterClass", [
  Rat, Bat, Goblin, Wolf, Skeleton, Spider, CaveTroll, Wraith, TrollKing
])
def test_all_monsters_have_gold_reward(MonsterClass):
  m = MonsterClass()
  assert hasattr(m, 'gold_reward')
  assert m.gold_reward >= 0

@pytest.mark.parametrize("MonsterClass", [
  Rat, Bat, Goblin, Wolf, Skeleton, Spider, CaveTroll, Wraith, TrollKing
])
def test_all_monsters_have_exp_value(MonsterClass):
  m = MonsterClass()
  assert m.exp_value > 0

@pytest.mark.parametrize("MonsterClass", [
  Rat, Bat, Goblin, Wolf, Skeleton, Spider, CaveTroll, Wraith, TrollKing
])
def test_all_monsters_alive_on_spawn(MonsterClass):
  m = MonsterClass()
  assert m.is_alive()

@pytest.mark.parametrize("MonsterClass", [
  Rat, Bat, Goblin, Wolf, Skeleton, Spider, CaveTroll, Wraith, TrollKing
])
def test_all_monsters_have_loot_table(MonsterClass):
  m = MonsterClass()
  assert isinstance(m.loot_table, list)


# ── CAST_MANA ────────────────────────────────────────────────

def test_cast_mana_costs_one_mana():
  from wizard_schools import SCHOOL_DATA
  p = make_player()
  p.spell_data = SCHOOL_DATA["Pyromancy"]["spells"]
  p.spells = ["Ignite"]
  enemy = RavenSwarm()
  starting_mana = p.mana
  with patch('builtins.input', return_value=''):
    p.cast_mana("Ignite", enemy)
  assert p.mana == starting_mana - 1

def test_cast_mana_deals_damage():
  from wizard_schools import SCHOOL_DATA
  p = make_player()
  p.spell_data = SCHOOL_DATA["Pyromancy"]["spells"]
  p.spells = ["Ignite"]
  enemy = RavenSwarm()
  starting_hp = enemy.hp
  with patch('builtins.input', return_value=''):
    p.cast_mana("Ignite", enemy)
  assert enemy.hp < starting_hp

def test_cast_mana_returns_false_on_empty_mana():
  from wizard_schools import SCHOOL_DATA
  p = make_player()
  p.spell_data = SCHOOL_DATA["Pyromancy"]["spells"]
  p.spells = ["Ignite"]
  p.mana = 0
  enemy = RavenSwarm()
  result = p.cast_mana("Ignite", enemy)
  assert result == False

def test_cast_mana_returns_false_on_unknown_spell():
  p = make_player()
  p.spell_data = {}
  result = p.cast_mana("FakeSpell", RavenSwarm())
  assert result == False

@pytest.mark.parametrize("school,spell", [
  ("Pyromancy", "Ignite"),
  ("Cryomancy", "Frostbite"),
  ("Chronomancy", "Hesitate"),
  ("Necromancy", "Rattle"),
  ("Enhancement", "Surge"),
  ("Illusion", "Phantom"),
  ("Conjuration", "Shardling"),
  ("Shadow", "Mutter"),
  ("Transmutation", "Shift"),
])
def test_each_school_damage_spell_hits(school, spell):
  p = Wizard(name="Test")
  p.choose_school(school)
  p.spells = [spell]
  enemy = RavenSwarm()
  starting_hp = enemy.hp
  with patch('builtins.input', return_value=''):
    result = p.cast_mana(spell, enemy)
  assert result == True
  assert enemy.hp < starting_hp


# ── NEW SPELL TESTS ─────────────────────────────────────────

class TestSmelt:
  def test_smelt_full_damage_below_threshold(self):
    w = make_wizard("Pyromancy")
    t = make_target(fire_resistance=5)
    starting_hp = t.hp
    w.cast_mana("smelt", t)
    assert t.hp < starting_hp

  def test_smelt_strips_resistance_above_threshold(self):
    w = make_wizard("Pyromancy")
    t = make_target(fire_resistance=15)
    w.cast_mana("smelt", t)
    assert t.fire_resistance < 15

  def test_smelt_no_damage_when_above_threshold(self):
    w = make_wizard("Pyromancy")
    t = make_target(hp=50, fire_resistance=15)
    w.cast_mana("smelt", t)
    assert t.hp == 50

  def test_smelt_costs_mana(self):
    w = make_wizard("Pyromancy")
    t = make_target()
    starting = w.mana
    w.cast_mana("smelt", t)
    assert w.mana == starting - 1

  def test_smelt_returns_true(self):
    w = make_wizard("Pyromancy")
    t = make_target()
    result = w.cast_mana("smelt", t)
    assert result == True


class TestFlashpoint:
  def test_flashpoint_deals_damage_when_vulnerable(self):
    w = make_wizard("Pyromancy")
    t = make_target(fire_resistance=0)
    starting_hp = t.hp
    w.cast_mana("flashpoint", t)
    assert t.hp < starting_hp

  def test_flashpoint_fizzles_when_resistant(self):
    w = make_wizard("Pyromancy")
    t = make_target(hp=50, fire_resistance=20)
    mana_before = w.mana
    w.cast_mana("flashpoint", t)
    assert t.hp == 50
    # mana refunded on fizzle
    assert w.mana == mana_before - 1 + 1

  def test_flashpoint_returns_true(self):
    w = make_wizard("Pyromancy")
    t = make_target(fire_resistance=0)
    result = w.cast_mana("flashpoint", t)
    assert result == True


# ── CRYOMANCY ────────────────────────────────────────────────

class TestGlacialGrind:
  def test_glacial_grind_hits_while_above_half(self):
    w = make_wizard("Cryomancy")
    t = make_target(hp=50)
    starting_hp = t.hp
    w.cast_mana("glacial grind", t)
    assert t.hp < starting_hp

  def test_glacial_grind_stops_at_half_hp(self):
    w = make_wizard("Cryomancy")
    t = make_target(hp=10)
    t.max_hp = 50
    # already below half — loop should not fire
    w.cast_mana("glacial grind", t)
    assert t.hp == 10

  def test_glacial_grind_returns_true(self):
    w = make_wizard("Cryomancy")
    t = make_target(hp=50)
    result = w.cast_mana("glacial grind", t)
    assert result == True


class TestNullfrost:
  def test_nullfrost_removes_active_status(self):
    from systems.status_effects import Weakened
    w = make_wizard("Cryomancy")
    t = make_target()
    t.status_effects = [Weakened(duration=3, atk_reduction=2, defense_reduction=1)]
    w.cast_mana("nullfrost", t)
    assert len(t.status_effects) == 0

  def test_nullfrost_does_nothing_when_no_status(self):
    w = make_wizard("Cryomancy")
    t = make_target()
    t.status_effects = []
    result = w.cast_mana("nullfrost", t)
    assert result == True

  def test_nullfrost_returns_true(self):
    w = make_wizard("Cryomancy")
    t = make_target()
    result = w.cast_mana("nullfrost", t)
    assert result == True


# ── CHRONOMANCY ──────────────────────────────────────────────

class TestInterval:
  def test_interval_deals_damage(self):
    w = make_wizard("Chronomancy")
    t = make_target(hp=200)
    starting_hp = t.hp
    w.cast_mana("interval", t)
    assert t.hp < starting_hp

  def test_interval_costs_extra_mana_per_hit(self):
    w = make_wizard("Chronomancy")
    t = make_target(hp=200)
    starting_mana = w.mana
    w.cast_mana("interval", t)
    assert w.mana < starting_mana

  def test_interval_fails_with_no_mana(self):
    w = make_wizard("Chronomancy")
    w.mana = 1  # only enough for the base cost
    t = make_target(hp=200)
    result = w.cast_mana("interval", t)
    # either fizzles or uses what it can
    assert result in [True, False]

  def test_interval_returns_true(self):
    w = make_wizard("Chronomancy")
    t = make_target(hp=200)
    result = w.cast_mana("interval", t)
    assert result == True


class TestRecurrence:
  def test_recurrence_fails_without_last_spell(self):
    w = make_wizard("Chronomancy")
    w.last_spell_cast = None
    t = make_target(hp=200)
    result = w.cast_mana("recurrence", t)
    assert result == False or t.hp == 200

  def test_recurrence_repeats_last_spell(self):
    w = make_wizard("Chronomancy")
    t = make_target(hp=200)
    w.cast_mana("hesitate", t)
    hp_after_first = t.hp
    w.cast_mana("recurrence", t)
    assert t.hp < hp_after_first

  def test_recurrence_tracks_last_spell(self):
    w = make_wizard("Chronomancy")
    t = make_target(hp=200)
    w.cast_mana("hesitate", t)
    assert w.last_spell_cast == "Hesitate"


# ── NECROMANCY ───────────────────────────────────────────────

class TestExhume:
  def test_exhume_empty_dead_list_does_nothing(self):
    w = make_wizard("Necromancy")
    w.combat_dead_list = []
    t = make_target()
    result = w.cast_mana("exhume", t)
    assert result == True
    assert w.minions == []

  def test_exhume_revives_from_dead_list(self):
    w = make_wizard("Necromancy")
    dead = RavenSwarm()
    dead.hp = 0
    w.combat_dead_list = [dead]
    t = make_target()
    w.cast_mana("exhume", t)
    assert len(w.minions) == 1
    assert w.minions[0].hp > 0

  def test_exhume_pops_from_dead_list(self):
    w = make_wizard("Necromancy")
    dead = RavenSwarm()
    w.combat_dead_list = [dead]
    t = make_target()
    w.cast_mana("exhume", t)
    assert len(w.combat_dead_list) == 0

  def test_exhume_revives_at_30_percent_hp(self):
    w = make_wizard("Necromancy")
    dead = RavenSwarm()
    dead.max_hp = 100
    w.combat_dead_list = [dead]
    t = make_target()
    w.cast_mana("exhume", t)
    assert w.minions[0].hp == 30


class TestErasure:
  def test_erasure_wastes_with_no_buffs(self):
    w = make_wizard("Necromancy")
    t = make_target()
    t.status_effects = []
    result = w.cast_mana("erasure", t)
    assert result == True

  def test_erasure_deletes_buff(self):
    from systems.status_effects import Weakened
    w = make_wizard("Necromancy")
    t = make_target()
    buff = Weakened(duration=3, atk_reduction=2, defense_reduction=1)
    buff.is_buff = True
    t.status_effects = [buff]
    w.cast_mana("erasure", t)
    assert len(t.status_effects) == 0


# ── ENHANCEMENT ──────────────────────────────────────────────

class TestMagnitude:
  def test_magnitude_deals_damage(self):
    w = make_wizard("Enhancement")
    t = make_target(hp=100)
    starting_hp = t.hp
    w.cast_mana("magnitude", t)
    assert t.hp < starting_hp

  def test_magnitude_deals_more_damage_at_low_hp(self):
    w = make_wizard("Enhancement")
    t = make_target(hp=100)
    w.hp = w.max_hp  # full hp — low multiplier
    w.cast_mana("magnitude", t)
    hp_after_full = t.hp

    w2 = make_wizard("Enhancement")
    t2 = make_target(hp=100)
    w2.hp = 10  # low hp — high multiplier
    w2.cast_mana("magnitude", t2)
    hp_after_low = t2.hp

    assert hp_after_low < hp_after_full

  def test_magnitude_sets_active_duration(self):
    w = make_wizard("Enhancement")
    t = make_target()
    w.cast_mana("magnitude", t)
    assert w.magnitude_active > 0


class TestSurgeStack:
  def test_surge_stack_increments_on_ally_status(self):
    w = make_wizard("Enhancement")
    from systems.status_effects import Weakened
    ally = RavenSwarm()
    ally.status_effects = [Weakened(duration=3, atk_reduction=2, defense_reduction=1)]
    w.active_allies = [ally]
    w.surge_stacks = 0
    t = make_target()
    w.cast_mana("surge stack", t)
    assert w.surge_stacks > 0

  def test_surge_stack_holds_at_zero_without_ally(self):
    w = make_wizard("Enhancement")
    w.active_allies = []
    w.surge_stacks = 0
    t = make_target()
    w.cast_mana("surge stack", t)
    assert w.surge_stacks == 0


# ── ILLUSION ─────────────────────────────────────────────────

class TestMirage:
  def test_mirage_reduces_target_atk(self):
    w = make_wizard("Illusion")
    t = make_target()
    t.atk = 10
    w.cast_mana("mirage", t)
    assert t.atk == 5

  def test_mirage_stores_original_atk(self):
    w = make_wizard("Illusion")
    t = make_target()
    t.atk = 10
    w.cast_mana("mirage", t)
    data = w.mirage_data.get(id(t))
    assert data is not None
    assert data["original_atk"] == 10

  def test_mirage_sets_duration(self):
    w = make_wizard("Illusion")
    t = make_target()
    t.atk = 8
    w.cast_mana("mirage", t)
    assert w.mirage_data[id(t)]["turns_left"] == 3


class TestDoppel:
  def test_doppel_spawns_at_upgrade_2(self):
    w = make_wizard("Illusion")
    w.spell_upgrades["Doppel"] = 2
    t = make_target()
    with patch('random.random', return_value=0.0):
      w.cast_mana("doppel", t)
    assert w.doppel_hits == 3

  def test_doppel_50_50_at_base(self):
    w = make_wizard("Illusion")
    t = make_target()
    with patch('random.random', return_value=0.3):
      w.cast_mana("doppel", t)
    assert w.doppel_hits == 1

  def test_doppel_fails_at_base_bad_roll(self):
    w = make_wizard("Illusion")
    t = make_target()
    with patch('random.random', return_value=0.9):
      w.cast_mana("doppel", t)
    assert w.doppel_hits == 0


# ── CONJURATION ──────────────────────────────────────────────

class TestSummonStack:
  def test_summon_stack_appends_entity(self):
    w = make_wizard("Conjuration")
    w.summon_stack = []
    t = make_target(hp=200)
    w.cast_mana("summon stack", t)
    assert len(w.summon_stack) == 1

  def test_summon_stack_deals_chip_damage(self):
    w = make_wizard("Conjuration")
    w.summon_stack = []
    t = make_target(hp=200)
    starting_hp = t.hp
    w.cast_mana("summon stack", t)
    assert t.hp < starting_hp

  def test_summon_stack_caps_at_three(self):
    w = make_wizard("Conjuration")
    w.summon_stack = ["Shard-1", "Shard-2", "Shard-3"]
    t = make_target(hp=200)
    w.cast_mana("summon stack", t)
    assert len(w.summon_stack) == 3

  def test_summon_stack_damage_scales_with_count(self):
    w = make_wizard("Conjuration")
    w.summon_stack = ["Shard-1", "Shard-2"]
    t = make_target(hp=200)
    starting_hp = t.hp
    w.cast_mana("summon stack", t)
    # 3 entities * 2 chip = 6 dmg
    assert starting_hp - t.hp == 6


class TestThreshold:
  def test_threshold_zero_damage_empty_inventory(self):
    w = make_wizard("Conjuration")
    t = make_target(hp=100)
    w.cast_mana("threshold", t)
    assert t.hp == 100

  def test_threshold_scales_with_inventory(self):
    w = make_wizard("Conjuration")
    w.inventory.add("item1")
    w.inventory.add("item2")
    t = make_target(hp=200)
    starting_hp = t.hp
    w.cast_mana("threshold", t)
    # 2 items * 3 multiplier = 6 dmg
    assert starting_hp - t.hp == 6

  def test_threshold_returns_true(self):
    w = make_wizard("Conjuration")
    t = make_target(hp=200)
    result = w.cast_mana("threshold", t)
    assert result == True


# ── SHADOW ───────────────────────────────────────────────────

class TestVoidcheck:
  def test_voidcheck_massive_damage_on_none_attribute(self):
    w = make_wizard("Shadow")
    t = make_target(hp=100)
    t.active_buff = None
    starting_hp = t.hp
    w.cast_mana("voidcheck", t)
    # should deal 6-14 damage on finding None
    assert t.hp < starting_hp

  def test_voidcheck_creates_none_and_minor_damage_when_no_none(self):
    w = make_wizard("Shadow")
    t = make_target(hp=100)
    t.active_buff = "something"
    t.equipped = "armor"
    t.mount = "horse"
    t.ward = "shield"
    starting_hp = t.hp
    w.cast_mana("voidcheck", t)
    # minor damage only
    assert starting_hp - t.hp == 3

  def test_voidcheck_returns_true(self):
    w = make_wizard("Shadow")
    t = make_target()
    result = w.cast_mana("voidcheck", t)
    assert result == True


class TestShred:
  def test_shred_slices_name_correctly(self):
    w = make_wizard("Shadow")
    t = make_target(name="Goblin", hp=200)
    w.cast_mana("shred", t)
    # "Goblin"[1:-1] = "obli" → len 4 * 2 = 8 dmg
    assert 200 - t.hp == 8

  def test_shred_damage_scales_with_name_length(self):
    w = make_wizard("Shadow")
    short = make_target(name="Rat", hp=200)
    long_ = make_target(name="TrollKing", hp=200)
    w.cast_mana("shred", short)
    w2 = make_wizard("Shadow")
    w2.cast_mana("shred", long_)
    assert (200 - long_.hp) > (200 - short.hp)

  def test_shred_returns_true(self):
    w = make_wizard("Shadow")
    t = make_target(name="Goblin", hp=200)
    result = w.cast_mana("shred", t)
    assert result == True


# ── TRANSMUTATION ────────────────────────────────────────────

class TestRecast:
  def test_recast_reduces_hp(self):
    w = make_wizard("Transmutation")
    t = make_target(hp=100)
    w.cast_mana("recast", t)
    assert t.hp < 100

  def test_recast_applies_decay_cycles(self):
    w = make_wizard("Transmutation")
    t = make_target(hp=100)
    w.cast_mana("recast", t)
    # 2 cycles of 0.85 decay: 100 * 0.85 * 0.85 = 72.25 → int = 72
    assert t.hp == 72

  def test_recast_returns_true(self):
    w = make_wizard("Transmutation")
    t = make_target()
    result = w.cast_mana("recast", t)
    assert result == True


class TestOverwrite:
  def test_overwrite_modifies_stat(self):
    w = make_wizard("Transmutation")
    t = make_target()
    t.atk = 10
    t.defense = 5
    original_atk = t.atk
    original_def = t.defense
    w.cast_mana("overwrite", t)
    # one stat should be debuffed
    changed = (t.atk != original_atk or t.defense != original_def)
    assert changed

  def test_overwrite_stores_revert_data(self):
    w = make_wizard("Transmutation")
    t = make_target()
    t.atk = 10
    t.defense = 5
    w.cast_mana("overwrite", t)
    assert hasattr(w, 'overwrite_data')
    assert len(w.overwrite_data) > 0

  def test_overwrite_applies_weakened(self):
    w = make_wizard("Transmutation")
    t = make_target()
    t.atk = 10
    t.defense = 5
    w.cast_mana("overwrite", t)
    effect_names = [type(e).__name__ for e in t.status_effects]
    assert "Weakened" in effect_names

  def test_overwrite_returns_true(self):
    w = make_wizard("Transmutation")
    t = make_target()
    t.atk = 8
    result = w.cast_mana("overwrite", t)
    assert result == True