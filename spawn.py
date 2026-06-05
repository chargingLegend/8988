import random
from entities.monster import MONSTER_DB


class EnemySpawner:
  def __init__(self, location):
    self.location = location

  def spawn(self, player_level):
    if player_level >= self.location.level_cap:
      boss_name = self.location.boss
      if boss_name not in MONSTER_DB:
        raise ValueError(f"Boss {boss_name} not defined in MONSTER_DB")
      return MONSTER_DB[boss_name](), True

    enemy_table = self.location.enemy_table
    if not enemy_table:
      raise ValueError(f"No enemy_table defined for {self.location.__class__.__name__}")

    enemies, weights = zip(*enemy_table)
    enemy_name = random.choices(enemies, weights=weights, k=1)[0]

    if enemy_name not in MONSTER_DB:
      raise ValueError(f"Monster {enemy_name} not defined in MONSTER_DB")

    return MONSTER_DB[enemy_name](), False