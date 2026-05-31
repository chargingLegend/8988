class Location:
  CAVE = "cave"
  MOUNTAIN = "mountain"
  FOREST = "forest"
  TOWN = "town"
  RUINS = "ruins"

  LOCATIONS = {
    CAVE: {
      "common": ["rock", "mushroom", "bat_wing", "dust"],
      "uncommon": ["crystal_shard", "glowing_moss"],
      "level_cap": 5,
      "boss": "Cave Troll",
      "enemy_table": [("Rat", 40), ("Bat", 35), ("Goblin", 25)]
    },
    MOUNTAIN: {
      "common": ["stone", "snow", "goat_hair"],
      "uncommon": ["frost_crystal", "eagle_feather"],
      "level_cap": 8,
      "boss": "Wraith",
      "enemy_table": [("Wolf", 60), ("Skeleton", 40)]
    },
    FOREST: {
      "common": ["stick", "leaf", "berry"],
      "uncommon": ["rare_herb", "spider_silk"],
      "level_cap": 10,
      "boss": "Troll King",
      "enemy_table": [("Giant Spider", 50), ("Wolf", 50)]
    }
  }