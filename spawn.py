import random
from entities import monster

class EnemySpawner:
    def __init__(self, location, locations_dict):
        self.location = location
        self.LOCATIONS = locations_dict

    def spawn(self, player_level):
        if self.location not in self.LOCATIONS:
            raise ValueError(f"Location {self.location} not found in LOCATIONS")

        loc_data = self.LOCATIONS[self.location]
        level_cap = loc_data["level_cap"]

        if player_level >= level_cap:
            boss_name = loc_data["boss"]
            if boss_name not in monster:
                raise ValueError(f"Boss {boss_name} not defined in MONSTER_DB")
            return monster[boss_name], True

        enemy_table = loc_data["enemy_table"]
        if not enemy_table:
            raise ValueError(f"No enemy_table defined for {self.location}")

        enemies, weights = zip(*enemy_table)
        enemy_name = random.choices(enemies, weights=weights, k=1)[0]

        if enemy_name not in monster:
            raise ValueError(f"Monster {enemy_name} not defined in MONSTER_DB")

        return monster[enemy_name], False