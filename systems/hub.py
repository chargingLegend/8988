def hub(player, location):
  from systems.grind import grind
  from combat import simple_combat
  from spawn import EnemySpawner

  location_key = location.__name__.lower()
  grind_cap = location.level_cap + 2

  print(f"\n\n=== {location.__name__.upper()} ===")
  print("The moment stretches. What will you do?\n")

  while True:
    options = {}
    option_num = 1

    if location.grind_available and player.level < grind_cap:
      options[str(option_num)] = 'grind'
      print(f"[{option_num}] Train     — push further into the dark")
      option_num += 1

    if 'sort' in player.spells:
      options[str(option_num)] = 'sort'
      print(f"[{option_num}] Sort      — read the composition of this place")
      option_num += 1

    if player.flags.get('maren_available'):
      options[str(option_num)] = 'trade'
      print(f"[{option_num}] Trade     — find Maren")
      option_num += 1

    if (player.flags.get(f'{location_key}_story_done')
        and player.level >= location.level_cap
        and not player.flags.get(f'{location_key}_boss_defeated')):
      options[str(option_num)] = 'challenge'
      print(f"[{option_num}] Challenge — something here is waiting for you")
      option_num += 1

    options[str(option_num)] = 'leave'
    print(f"[{option_num}] Move on")

    choice = input("\n> ").strip()

    if choice not in options:
      print("\nThe moment doesn't wait for indecision.")
      continue

    action = options[choice]

    if action == 'grind':
      grind(player, location)

    elif action == 'sort':
      player.sort(location)

    elif action == 'trade':
      from merchant import Merchant
      Merchant.visit(player)

    elif action == 'challenge':
      spawner = EnemySpawner(location)
      enemy, is_boss = spawner.spawn(location.level_cap)
      print(f"\nIt steps forward.")
      print(f"\n{enemy}")
      simple_combat(player, enemy)
      if not enemy.is_alive():
        player.flags[f'{location_key}_boss_defeated'] = True
        print(f"\nIt's done.")

    elif action == 'leave':
      print("\nYou turn away from it.")
      break