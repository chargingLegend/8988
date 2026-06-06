import random
from spawn import EnemySpawner


def grind(player, location):
  from combat import simple_combat  # ← moved here, breaks the circle

  if not location.grind_available:
    print("\nThere is nothing here worth fighting.")
    return

  grind_cap = location.level_cap + 2
  spawner = EnemySpawner(location)

  while True:
    if player.level >= grind_cap:
      print("\nYou have taken everything this place has to offer.")
      print("The enemies that remain don't even flinch when you pass.")
      break

    enemy, is_boss = spawner.spawn(player.level)
    print(f"\n{enemy.on_spawn()}")

    simple_combat(player, enemy)

    if not player.is_alive():
      print("\nThe ground claims you.")
      break

    if enemy.is_alive():
      print("\nIt still breathes. You pull back.")
      break

    player.gain_exp(enemy.exp_value)

    drops = enemy.drop_loot()
    if drops:
      print(f"\nAmong the remains — {', '.join(drops)}.")
      for drop in drops:
        player.inventory.add(drop)

    if enemy.gold_reward:
      player.gold = getattr(player, 'gold', 0) + enemy.gold_reward
      print(f"+{enemy.gold_reward} gold. Total: {player.gold}")

    again = input("\nPush further? [y/n]: ").strip().lower()
    if again != 'y':
      print("\nYou step back. The dark recedes.")
      break