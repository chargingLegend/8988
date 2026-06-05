class Location:
  level_cap = 0
  boss = None
  enemy_table = []
  common = []
  uncommon = []
  rare = []


class Town(Location):
  vendors = []
  requires_tithe = False
  grind_available = False


class Vardeth(Town):
  level_cap = 4
  boss = "Enforcer_Gang_Sergeant"
  enemy_table = [("Enforcer", 70), ("Criminal", 30)]
  common = ["broken_pavement", "paper_scrap", "empty_bottle"]
  uncommon = ["silver_pendant", "half_filled_ink_bottle"]
  rare = ["enforcer_badge", "collectors_ledger"]
  vendors = ["Maren"]
  requires_tithe = True
  grind_available = True


class FreeHollow(Town):
  level_cap = 3
  boss = "Bandit_Lord"
  enemy_table = [("Criminal", 60), ("Enforcer", 40)]
  common = ["clay_shard", "worn_rope", "bread_crumb"]
  uncommon = ["traders_coin", "freedom_pamphlet"]
  rare = ["rebels_sigil", "hollow_charter"]
  vendors = ["Traveling Merchant"]
  requires_tithe = False
  grind_available = True


class Cave(Location):
  grind_available = True
  boss = None
  enemy_table = []
  level_cap = 0


class DrevsCave(Cave):
  level_cap = 6
  boss = "Cave Troll"
  enemy_table = [("Rat", 40), ("Bat", 35), ("Goblin", 25)]
  common = ["rock", "mushroom", "bat_wing", "dust"]
  uncommon = ["crystal_shard", "glowing_moss"]
  rare = ["troll_blood_vial", "cave_pearl"]
  vendors = ["Drev"]


class CrystalGrotta(Cave):
  level_cap = 9
  boss = "Crystal Basilisk"
  enemy_table = [("Bat", 50), ("Goblin", 30), ("Rat", 20)]
  common = ["quartz_dust", "damp_moss", "cave_mushroom"]
  uncommon = ["crystal_shard", "basilisk_scale"]
  rare = ["heart_crystal", "petrified_eye"]


class Shadowhollow(Cave):
  level_cap = 11
  boss = "Shadow Wraith"
  enemy_table = [("Bat", 60), ("Skeleton", 40)]
  common = ["shadow_dust", "black_moss", "hollow_bone"]
  uncommon = ["void_shard", "wraith_cloth"]
  rare = ["shadow_core", "hollow_crown"]


class Forest(Location):
  grind_available = True
  boss = None
  enemy_table = []
  level_cap = 0


class SylasForest(Forest):
  level_cap = 10
  boss = "Troll King"
  enemy_table = [("Giant Spider", 50), ("Wolf", 50)]
  common = ["stick", "leaf", "berry"]
  uncommon = ["rare_herb", "spider_silk"]
  rare = ["ancient_root", "glowspore"]
  vendors = ["Syla"]


class MireWood(Forest):
  level_cap = 12
  boss = "Bog Witch"
  enemy_table = [("Giant Spider", 45), ("Wolf", 35), ("Rat", 20)]
  common = ["bog_reed", "mud_clump", "swamp_berry"]
  uncommon = ["witchwood", "mire_moss"]
  rare = ["bog_witch_staff", "cursed_root"]


class WhisperGrove(Forest):
  level_cap = 8
  boss = "Ancient Treant"
  enemy_table = [("Wolf", 55), ("Giant Spider", 45)]
  common = ["whisper_leaf", "pale_bark", "moonberry"]
  uncommon = ["treant_bark", "grove_crystal"]
  rare = ["heartwood", "ancient_seed"]


class Mountain(Location):
  grind_available = True
  boss = None
  enemy_table = []
  level_cap = 0


class FrostpeakMountain(Mountain):
  level_cap = 8
  boss = "Wraith"
  enemy_table = [("Wolf", 60), ("Skeleton", 40)]
  common = ["stone", "snow", "goat_hair"]
  uncommon = ["frost_crystal", "eagle_feather"]
  rare = ["wraith_essence", "ancient_ore"]


class StormridgeMountain(Mountain):
  level_cap = 10
  boss = "Stone Golem"
  enemy_table = [("Wolf", 40), ("Skeleton", 35), ("Goblin", 25)]
  common = ["granite_chunk", "frozen_moss", "wind_crystal"]
  uncommon = ["stormstone", "golem_fragment"]
  rare = ["heart_of_the_mountain", "tempest_shard"]


class AshenPeak(Mountain):
  level_cap = 14
  boss = "Volcanic Drake"
  enemy_table = [("Skeleton", 45), ("Wolf", 35), ("Goblin", 20)]
  common = ["ash", "scorched_bone", "obsidian_chip"]
  uncommon = ["magma_crystal", "drake_scale"]
  rare = ["volcanic_core", "ashen_crown"]


class Ruins(Location):
  grind_available = True
  boss = None
  enemy_table = []
  level_cap = 0


class OrathsRuins(Ruins):
  level_cap = 12
  boss = "Lich"
  enemy_table = [("Skeleton", 50), ("Wraith", 50)]
  common = ["crumbled_stone", "bone_dust", "torn_cloth"]
  uncommon = ["grave_dust", "ancient_coin"]
  rare = ["lich_fragment", "forgotten_spellscroll"]
  vendors = ["Orath"]


class ForgottenTemple(Ruins):
  level_cap = 15
  boss = "Undead High Priest"
  enemy_table = [("Skeleton", 40), ("Wraith", 40), ("Goblin", 20)]
  common = ["temple_stone", "offering_dust", "faded_cloth"]
  uncommon = ["blessed_fragment", "priest_relic"]
  rare = ["high_priests_staff", "divine_shard"]


class CollapsingCitadel(Ruins):
  level_cap = 13
  boss = "Fallen Knight"
  enemy_table = [("Skeleton", 60), ("Wraith", 40)]
  common = ["rusted_metal", "broken_shield", "stone_dust"]
  uncommon = ["knights_crest", "citadel_stone"]
  rare = ["fallen_blade", "knights_oath_fragment"]