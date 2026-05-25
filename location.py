class Location:
  CAVE = "cave"
  MOUNTAIN = "mountain"
  FOREST = "forest"
  TOWN = "town"
  RUINS = "ruins"

  LOCATIONS = {
    CAVE: {
      "common": ["rock", "mushroom", "bat_wing", "dust"],
      "uncommon": ["crystal_shard", "glowing_moss"]
    },
    MOUNTAIN: {
      "common": ["stone", "snow", "goat_hair"],
      "uncommon": ["frost_crystal", "eagle_feather"]
    },
    FOREST: {
      "common": ["stick", "leaf", "berry"],
      "uncommon": ["rare_herb", "spider_silk"]
    }
  }