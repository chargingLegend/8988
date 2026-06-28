import pytest
from unittest.mock import patch, MagicMock

from wizard import Wizard
from enemy import (RavenSwarm, Rat, Bat, Goblin, Wolf,
  Skeleton, Spider, CaveTroll, Wraith, TrollKing)
from inventory import Inventory
from location import (Vardeth, DrevsCave, SylasForest,
  FrostpeakMountain, OrathsRuins)
from items import (HPPotion, ManaPotion, ManabdaPotion,
  PassRune, ExceptVial, FinallyFlask, Cloak, Staff, Rod, Scepter)
from merchant import Maren
from enemy import DesperateTraveler, Enforcer, TitheCollector


def make_player(level=1, school="Pyromancy"):
  p = Wizard(name="Test", level=level, school=school)
  p.choose_school(school)
  p.gold = 0
  p.flags = {}
  p.corruption = 0
  return p


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


def test_raven_swarm_gold_reward_is_25():
  swarm = RavenSwarm()
  assert swarm.gold_reward == 25

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
  from enemy import FrightenedWoman
  with patch('builtins.input', return_value='flee') as mock_input:
    from combat import simple_combat
    simple_combat(p, enemy)
  prompt_calls = [str(c) for c in mock_input.call_args_list]
  assert any('mira' in c.lower() for c in prompt_calls)


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


  assert p.gold == 0

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


  assert kills[0] == 1


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
  assert p.hp == p.max_hp

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
  assert skeleton.hp == 14

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


import inspect
import enemy
from enemy import BESTIARY, Monster, Humanoid, FrightenedWoman, Criminal

import inspect
import enemy
from enemy import (BESTIARY, Monster, Humanoid, Rat, Bat, Goblin, RavenSwarm,
                   Wolf, Skeleton, Spider, CaveTroll, Wraith, TrollKing,
                   DesperateTraveler, FrightenedWoman, Enforcer,
                   TitheCollector, Criminal)


def test_bestiary_exists_and_replaces_monster_db():
  assert isinstance(BESTIARY, dict)
  assert not hasattr(enemy, 'MONSTER_DB')


def test_bestiary_has_all_expected_entries():
  expected = {"Rat", "Bat", "Goblin", "Raven Swarm", "Wolf", "Skeleton",
              "Giant Spider", "Cave Troll", "Wraith", "Troll King", "Criminal"}
  assert set(BESTIARY.keys()) == expected


def test_bestiary_values_are_classes_not_lazy_wrappers():
  for name, cls in BESTIARY.items():
    assert inspect.isclass(cls), f"{name} is not a class"


def test_every_bestiary_entry_instantiates():
  for name, cls in BESTIARY.items():
    creature = cls()
    assert creature.hp > 0, f"{name} spawned with no HP"
    assert creature.name, f"{name} spawned unnamed"


def test_raven_swarm_gold_reward_is_25():
  assert RavenSwarm().gold_reward == 25


def test_humanoid_inherits_monster():
  assert issubclass(Humanoid, Monster)


def test_all_humanoids_inherit_humanoid():
  for cls in (DesperateTraveler, FrightenedWoman, Enforcer,
              TitheCollector, Criminal):
    assert issubclass(cls, Humanoid), cls.__name__


def test_humanoid_speak_and_reveal():
  h = Humanoid()
  assert "test" in h.speak("test")
  caleb = DesperateTraveler()
  assert caleb.true_name == "Caleb"
  msg = caleb.reveal_name()
  assert caleb.name == "Caleb"
  assert "Caleb" in msg
  assert caleb.reveal_name() is None


def test_single_module_no_cross_imports():
  src = inspect.getsource(enemy)
  assert "entities.monster" not in src
  assert "entities.humanoid" not in src


def test_cipher_indices_spell_twilight_ledger():
  elements = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
  twilight = [19, 22, 8, 11, 8, 6, 7, 19]
  ledger = [11, 4, 3, 6, 4, 17]
  answer = "".join(elements[i] for i in twilight) + " " +\
           "".join(elements[i] for i in ledger)
  assert answer == "TWILIGHT LEDGER"


def test_drink_game_chance_table_is_monotonic():
  chances = {1: 25, 2: 50, 3: 75, 4: 95}
  vals = [chances[k] for k in sorted(chances)]
  assert vals == sorted(vals)
  assert all(0 < v < 100 for v in vals)


if __name__ == "__main__":
  import sys
  failed = 0
  for name, fn in sorted(globals().items()):
    if name.startswith("test_"):
      try:
        fn()
        print(f"  PASS  {name}")
      except AssertionError as e:
        failed += 1
        print(f"  FAIL  {name}: {e}")
  sys.exit(1 if failed else 0)

# ── SPELL TIER SYSTEM TESTS ───────────────────────────────

def test_pyromancy_ignite_has_tiers():
  p = make_player(school="Pyromancy")
  assert "tiers" in p.spell_data["Ignite"]

def test_pyromancy_ignite_tier_1_increases_damage():
  p = make_player(school="Pyromancy")
  base_max = p.spell_data["Ignite"]["max_dmg"]
  tier_1_max = p.spell_data["Ignite"]["tiers"]["1"]["max_dmg"]
  assert tier_1_max > base_max

def test_pyromancy_ignite_tier_3_is_strongest():
  p = make_player(school="Pyromancy")
  tier_2_max = p.spell_data["Ignite"]["tiers"]["2"]["max_dmg"]
  tier_3_max = p.spell_data["Ignite"]["tiers"]["3"]["max_dmg"]
  assert tier_3_max > tier_2_max

def test_pyromancy_ignite_tier_3_effect_chance_higher_than_base():
  p = make_player(school="Pyromancy")
  base_chance = p.spell_data["Ignite"]["effect_chance"]
  tier_3_chance = p.spell_data["Ignite"]["tiers"]["3"]["effect_chance"]
  assert tier_3_chance > base_chance

def test_all_pyromancy_base_spells_have_tiers():
  p = make_player(school="Pyromancy")
  for spell in ["Ignite", "Sear", "Cinder Ward"]:
    assert "tiers" in p.spell_data[spell], f"{spell} missing tiers"

def test_all_cryomancy_base_spells_have_tiers():
  p = make_player(school="Cryomancy")
  for spell in ["Frostbite", "Glaze", "Shard"]:
    assert "tiers" in p.spell_data[spell], f"{spell} missing tiers"

def test_all_chronomancy_base_spells_have_tiers():
  p = make_player(school="Chronomancy")
  for spell in ["Hesitate", "Foresight", "Stutter"]:
    assert "tiers" in p.spell_data[spell], f"{spell} missing tiers"

def test_upgrade_level_starts_at_zero_for_tiered_spells():
  p = make_player(school="Pyromancy")
  for spell, data in p.spell_data.items():
    if isinstance(data, dict) and "tiers" in data:
      assert data.get("upgrade_level", 0) == 0, f"{spell} upgrade_level not 0"


# ── NEW SPELL EXISTENCE TESTS ──────────────────────────────

def test_pyromancy_has_hearthcall():
  p = make_player(school="Pyromancy")
  assert "Hearthcall" in p.spell_data

def test_pyromancy_has_flashform():
  p = make_player(school="Pyromancy")
  assert "Flashform" in p.spell_data

def test_pyromancy_has_judgment_flame():
  p = make_player(school="Pyromancy")
  assert "Judgment Flame" in p.spell_data

def test_pyromancy_has_unlit():
  p = make_player(school="Pyromancy")
  assert "Unlit" in p.spell_data

def test_cryomancy_has_the_still():
  p = make_player(school="Cryomancy")
  assert "The Still" in p.spell_data

def test_cryomancy_has_cold_stride():
  p = make_player(school="Cryomancy")
  assert "Cold Stride" in p.spell_data

def test_necromancy_has_last_pulled():
  p = make_player(school="Necromancy")
  assert "Last Pulled" in p.spell_data

def test_necromancy_has_the_finding():
  p = make_player(school="Necromancy")
  assert "The Finding" in p.spell_data

def test_shadow_has_cut():
  p = make_player(school="Shadow")
  assert "Cut" in p.spell_data

def test_transmutation_has_exchange():
  p = make_player(school="Transmutation")
  assert "Exchange" in p.spell_data

def test_each_new_spell_has_python_concept():
  new_spells = {
    "Pyromancy": ["Hearthcall", "Flashform", "Judgment Flame", "Unlit"],
    "Cryomancy": ["The Still", "Cold Stride", "Locked State", "Tally Frost"],
    "Necromancy": ["Last Pulled", "The Finding", "True Nature", "Added To The Count"],
  }
  for school, spells in new_spells.items():
    p = make_player(school=school)
    for spell in spells:
      assert "python_concept" in p.spell_data[spell], f"{spell} missing python_concept"


# ── LEARN SPELL CHOICE TESTS ──────────────────────────────

def test_learn_spell_choice_raises_when_all_learned():
  p = make_player(school="Pyromancy")
  p.spells = list(p.spell_data.keys())
  with pytest.raises(ValueError, match="mastered all available spells"):
    p.learn_spell_choice()

def test_learn_spell_choice_adds_exactly_one_spell(monkeypatch):
  p = make_player(school="Pyromancy")
  before = len(p.spells)
  monkeypatch.setattr("builtins.input", lambda _: "1")
  p.learn_spell_choice()
  assert len(p.spells) == before + 1

def test_learn_spell_invalid_choice_does_not_add_spell(monkeypatch):
  p = make_player(school="Pyromancy")
  before = len(p.spells)
  monkeypatch.setattr("builtins.input", lambda _: "999")
  p.learn_spell_choice()
  assert len(p.spells) == before

def test_learned_spell_not_duplicate(monkeypatch):
  p = make_player(school="Pyromancy")
  monkeypatch.setattr("builtins.input", lambda _: "1")
  p.learn_spell_choice()
  assert len(p.spells) == len(set(p.spells))


# ── SPELL UPGRADE COUNTER TESTS ───────────────────────────

def test_spell_upgrades_starts_empty():
  p = make_player(school="Pyromancy")
  assert p.spell_upgrades == {}

def test_get_spell_power_returns_zero_by_default():
  p = make_player(school="Pyromancy")
  assert p.get_spell_power("Ignite") == 0

def test_get_spell_power_returns_upgrade_level():
  p = make_player(school="Pyromancy")
  p.spell_upgrades["Ignite"] = 2
  assert p.get_spell_power("Ignite") == 2

def test_empower_spell_increments_upgrade_counter(monkeypatch):
  p = make_player(school="Pyromancy")
  monkeypatch.setattr("builtins.input", lambda _: "1")
  p.empower_spell_choice()
  assert p.spell_upgrades.get("Ignite", 0) == 1

def test_empower_spell_twice_gives_level_two(monkeypatch):
  p = make_player(school="Pyromancy")
  monkeypatch.setattr("builtins.input", lambda _: "1")
  p.empower_spell_choice()
  p.empower_spell_choice()
  assert p.spell_upgrades.get("Ignite", 0) == 2


# ══════════════════════════════════════════════════════════════════════════════
# LEDGER TESTS
# ══════════════════════════════════════════════════════════════════════════════

from ledger import (
  _parse_input,
  _normalize,
  _find_concept,
  _is_twilight,
  _is_off_world,
  _is_gibberish,
  _display_response,
  LEDGER_RESPONSES,
  LEDGER_UNLOCKED_FLAG,
  LEDGER_INTRO_SEEN_FLAG,
  LEDGER_FIRST_CALL_FLAG,
)


class MockLedgerPlayer:
  def __init__(self, flags=None):
    self.name = "Aldric"
    self.school = "Pyromancy"
    self.flags = flags if flags is not None else {}


# ── _parse_input ───────────────────────────────────────────────────────────────

def test_parse_valid_input_returns_question_and_ok():
  question, status = _parse_input("ledger(what is a list)")
  assert question == "what is a list"
  assert status == "ok"

def test_parse_valid_input_uppercase_ledger():
  question, status = _parse_input("LEDGER(what is a list)")
  assert question == "what is a list"
  assert status == "ok"

def test_parse_valid_input_strips_whitespace():
  question, status = _parse_input("  ledger(what is a list)  ")
  assert question == "what is a list"
  assert status == "ok"

def test_parse_no_ledger_prefix_returns_no_ledger():
  question, status = _parse_input("what is a list")
  assert question is None
  assert status == "no_ledger"

def test_parse_ledger_alone_returns_no_parens():
  question, status = _parse_input("ledger")
  assert question is None
  assert status == "no_parens"

def test_parse_malformed_no_closing_paren():
  question, status = _parse_input("ledger(what is a list")
  assert question is None
  assert status == "malformed"

def test_parse_malformed_no_opening_paren():
  question, status = _parse_input("ledger what is a list)")
  assert question is None
  assert status == "malformed"

def test_parse_empty_parens_returns_empty():
  question, status = _parse_input("ledger()")
  assert question is None
  assert status == "empty"

def test_parse_whitespace_only_parens_returns_empty():
  question, status = _parse_input("ledger(   )")
  assert question is None
  assert status == "empty"

def test_parse_strips_single_quotes():
  question, status = _parse_input("ledger('what is a list')")
  assert question == "what is a list"
  assert status == "ok"

def test_parse_strips_double_quotes():
  question, status = _parse_input('ledger("what is a list")')
  assert question == "what is a list"
  assert status == "ok"

def test_parse_valid_input_with_punctuation():
  question, status = _parse_input("ledger(what is __init__?)")
  assert question == "what is __init__?"
  assert status == "ok"


# ── _normalize ─────────────────────────────────────────────────────────────────

def test_normalize_strips_what_is():
  assert _normalize("what is a list") == "a list"

def test_normalize_strips_what_are():
  assert _normalize("what are dictionaries") == "dictionaries"

def test_normalize_strips_explain():
  assert _normalize("explain inheritance") == "inheritance"

def test_normalize_strips_tell_me_about():
  assert _normalize("tell me about classes") == "classes"

def test_normalize_strips_how_does():
  assert _normalize("how does a for loop work") == "a for loop work"

def test_normalize_strips_how_do():
  assert _normalize("how do lists work") == "lists work"

def test_normalize_strips_question_mark():
  assert "?" not in _normalize("what is self?")

def test_normalize_strips_period():
  assert "." not in _normalize("explain functions.")

def test_normalize_lowercases():
  assert _normalize("What Is A List") == _normalize("what is a list")

def test_normalize_strips_whitespace():
  assert _normalize("  list  ") == "list"


# ── _find_concept ──────────────────────────────────────────────────────────────

def test_find_exact_match_list():
  assert _find_concept("list") == "list"

def test_find_via_normalize_what_is_list():
  assert _find_concept("what is a list") == "list"

def test_find_via_normalize_explain_inheritance():
  assert _find_concept("explain inheritance") == "inheritance"

def test_find_dunder_init():
  assert _find_concept("__init__") == "__init__"

def test_find_self():
  assert _find_concept("self") == "self"

def test_find_class():
  assert _find_concept("class") == "class"

def test_find_for_loop():
  assert _find_concept("for loop") == "for loop"

def test_find_while_loop():
  assert _find_concept("while loop") == "while loop"

def test_find_try_except():
  assert _find_concept("try/except") == "try/except"

def test_find_if_elif_else():
  assert _find_concept("if/elif/else") == "if/elif/else"

def test_find_not_in():
  assert _find_concept("not in") == "not in"

def test_find_f_string():
  assert _find_concept("f-string") == "f-string"

def test_find_dictionary():
  assert _find_concept("dictionary") == "dictionary"

def test_find_boolean():
  assert _find_concept("boolean") == "boolean"

def test_find_integer():
  assert _find_concept("integer") == "integer"

def test_find_float():
  assert _find_concept("float") == "float"

def test_find_string():
  assert _find_concept("string") == "string"

def test_find_variable():
  assert _find_concept("variable") == "variable"

def test_find_function():
  assert _find_concept("function") == "function"

def test_find_return():
  assert _find_concept("return") == "return"

def test_find_argument():
  assert _find_concept("argument") == "argument"

def test_find_parameter():
  assert _find_concept("parameter") == "parameter"

def test_find_break():
  assert _find_concept("break") == "break"

def test_find_continue():
  assert _find_concept("continue") == "continue"

def test_find_pass():
  assert _find_concept("pass") == "pass"

def test_find_import():
  assert _find_concept("import") == "import"

def test_find_module():
  assert _find_concept("module") == "module"

def test_find_scope():
  assert _find_concept("scope") == "scope"

def test_find_index():
  assert _find_concept("index") == "index"

def test_find_indexing():
  assert _find_concept("indexing") == "indexing"

def test_find_slice():
  assert _find_concept("slice") == "slice"

def test_find_slicing():
  assert _find_concept("slicing") == "slicing"

def test_find_concatenation():
  assert _find_concept("concatenation") == "concatenation"

def test_find_len():
  assert _find_concept("len") == "len"

def test_find_range():
  assert _find_concept("range") == "range"

def test_find_type():
  assert _find_concept("type") == "type"

def test_find_none():
  assert _find_concept("none") == "none"

def test_find_method():
  assert _find_concept("method") == "method"

def test_find_attribute():
  assert _find_concept("attribute") == "attribute"

def test_find_in():
  assert _find_concept("in") == "in"

def test_find_operators():
  assert _find_concept("operators") == "operators"

def test_find_iteration():
  assert _find_concept("iteration") == "iteration"

def test_find_returns_none_for_unknown():
  assert _find_concept("metaclass") is None

def test_find_returns_none_for_empty():
  assert _find_concept("") is None

def test_find_returns_none_for_niche_concept():
  assert _find_concept("generator") is None


# ── _is_twilight ───────────────────────────────────────────────────────────────

def test_twilight_ledger_exact():
  assert _is_twilight("twilight ledger") is True

def test_the_twilight_ledger():
  assert _is_twilight("the twilight ledger") is True

def test_twilight_alone():
  assert _is_twilight("twilight") is True

def test_drakkon():
  assert _is_twilight("drakkon") is True

def test_drakkon_tarkesh():
  assert _is_twilight("drakkon tarkesh") is True

def test_twilight_in_sentence():
  assert _is_twilight("tell me about the twilight ledger") is True

def test_non_twilight_returns_false():
  assert _is_twilight("what is a list") is False

def test_ledger_alone_not_twilight():
  assert _is_twilight("ledger") is False

def test_empty_string_not_twilight():
  assert _is_twilight("") is False


# ── _is_off_world ──────────────────────────────────────────────────────────────

def test_weather_is_off_world():
  assert _is_off_world("weather") is True

def test_sports_is_off_world():
  assert _is_off_world("sports") is True

def test_news_is_off_world():
  assert _is_off_world("news") is True

def test_politics_is_off_world():
  assert _is_off_world("politics") is True

def test_movie_is_off_world():
  assert _is_off_world("movie") is True

def test_music_is_off_world():
  assert _is_off_world("music") is True

def test_stock_is_off_world():
  assert _is_off_world("stock") is True

def test_crypto_is_off_world():
  assert _is_off_world("crypto") is True

def test_in_world_question_not_off_world():
  assert _is_off_world("what is a list") is False

def test_empty_string_not_off_world():
  assert _is_off_world("") is False


# ── _is_gibberish ──────────────────────────────────────────────────────────────

def test_numbers_only_is_gibberish():
  assert _is_gibberish("1234") is True

def test_single_char_is_gibberish():
  assert _is_gibberish("x") is True

def test_two_chars_is_gibberish():
  assert _is_gibberish("ab") is True

def test_empty_string_is_gibberish():
  assert _is_gibberish("") is True

def test_whitespace_only_is_gibberish():
  assert _is_gibberish("   ") is True

def test_valid_question_not_gibberish():
  assert _is_gibberish("what is a list") is False

def test_single_valid_word_not_gibberish():
  assert _is_gibberish("list") is False

def test_symbols_only_is_gibberish():
  assert _is_gibberish("!@#") is True


# ── LEDGER_RESPONSES structure ─────────────────────────────────────────────────

def test_all_concepts_are_tuples():
  for key, value in LEDGER_RESPONSES.items():
    assert isinstance(value, tuple), f"{key} is not a tuple"

def test_all_concepts_have_four_beats():
  for key, value in LEDGER_RESPONSES.items():
    assert len(value) == 4, f"{key} does not have 4 beats"

def test_all_beats_are_strings():
  for key, value in LEDGER_RESPONSES.items():
    for i, beat in enumerate(value):
      assert isinstance(beat, str), f"{key} beat {i} is not a string"

def test_all_lore_beats_non_empty():
  for key, value in LEDGER_RESPONSES.items():
    assert len(value[0]) > 0, f"{key} lore beat is empty"

def test_all_doc_beats_non_empty():
  for key, value in LEDGER_RESPONSES.items():
    assert len(value[1]) > 0, f"{key} documentation beat is empty"

def test_all_plain_beats_non_empty():
  for key, value in LEDGER_RESPONSES.items():
    assert len(value[2]) > 0, f"{key} plain terms beat is empty"

def test_all_example_beats_non_empty():
  for key, value in LEDGER_RESPONSES.items():
    assert len(value[3]) > 0, f"{key} example beat is empty"

def test_all_example_beats_contain_code():
  for key, value in LEDGER_RESPONSES.items():
    assert "=" in value[3] or "print" in value[3] or "#" in value[3], (
      f"{key} example beat does not appear to contain code"
    )

def test_expected_concepts_present():
  expected = [
    "__init__", "self", "class", "inheritance", "function", "return",
    "variable", "string", "integer", "float", "boolean", "list",
    "dictionary", "tuple", "set", "argument", "parameter", "for loop",
    "while loop", "if", "if/elif/else", "break", "continue", "pass",
    "try", "try/except", "except", "import", "module", "scope",
    "index", "indexing", "slice", "slicing", "concatenation", "f-string",
    "len", "range", "type", "none", "method", "attribute", "in",
    "not in", "operators", "iteration"
  ]
  for concept in expected:
    assert concept in LEDGER_RESPONSES, f"{concept} missing from LEDGER_RESPONSES"

def test_paired_concepts_share_same_response():
  assert LEDGER_RESPONSES["argument"] == LEDGER_RESPONSES["parameter"]
  assert LEDGER_RESPONSES["try"] == LEDGER_RESPONSES["try/except"]
  assert LEDGER_RESPONSES["try"] == LEDGER_RESPONSES["except"]
  assert LEDGER_RESPONSES["index"] == LEDGER_RESPONSES["indexing"]
  assert LEDGER_RESPONSES["slice"] == LEDGER_RESPONSES["slicing"]
  assert LEDGER_RESPONSES["if"] == LEDGER_RESPONSES["if/elif/else"]
  assert LEDGER_RESPONSES["import"] == LEDGER_RESPONSES["module"]
  assert LEDGER_RESPONSES["method"] == LEDGER_RESPONSES["attribute"]
  assert LEDGER_RESPONSES["in"] == LEDGER_RESPONSES["not in"]


# ── _display_response ──────────────────────────────────────────────────────────

def test_display_does_not_raise_for_any_concept(capsys):
  for concept in LEDGER_RESPONSES:
    _display_response(concept)
    captured = capsys.readouterr()
    assert len(captured.out) > 0, f"{concept} produced no output"

def test_display_contains_lore(capsys):
  _display_response("__init__")
  captured = capsys.readouterr()
  assert "spark of life" in captured.out

def test_display_contains_documentation(capsys):
  _display_response("list")
  captured = capsys.readouterr()
  assert "mutable" in captured.out

def test_display_contains_example_divider(capsys):
  _display_response("boolean")
  captured = capsys.readouterr()
  assert "---" in captured.out


# ── flag constants ─────────────────────────────────────────────────────────────

def test_unlocked_flag_is_string():
  assert isinstance(LEDGER_UNLOCKED_FLAG, str)

def test_intro_flag_is_string():
  assert isinstance(LEDGER_INTRO_SEEN_FLAG, str)

def test_first_call_flag_is_string():
  assert isinstance(LEDGER_FIRST_CALL_FLAG, str)

def test_flags_are_distinct():
  flags = {LEDGER_UNLOCKED_FLAG, LEDGER_INTRO_SEEN_FLAG, LEDGER_FIRST_CALL_FLAG}
  assert len(flags) == 3

def test_mock_ledger_player_unlocked():
  player = MockLedgerPlayer(flags={LEDGER_UNLOCKED_FLAG: True})
  assert player.flags.get(LEDGER_UNLOCKED_FLAG) is True

def test_mock_ledger_player_locked_by_default():
  player = MockLedgerPlayer()
  assert player.flags.get(LEDGER_UNLOCKED_FLAG) is None

def test_mock_ledger_player_intro_not_seen_by_default():
  player = MockLedgerPlayer()
  assert player.flags.get(LEDGER_INTRO_SEEN_FLAG) is None

def test_mock_ledger_player_first_call_not_set_by_default():
  player = MockLedgerPlayer()
  assert player.flags.get(LEDGER_FIRST_CALL_FLAG) is None