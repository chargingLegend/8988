from wizard import Wizard
from items import PassRune, ExceptVial, FinallyFlask, HPPotion, ManaPotion


def simple_combat(player, enemy):
  print(f"\n=== COMBAT: {player.name} vs {enemy.name} ===")
  while player.is_alive() and enemy.is_alive():
    player_msgs = player.tick_status_effects()
    if player_msgs:
      print(player_msgs)
    if not player.is_alive():
      break
    enemy_msgs = enemy.tick_status_effects()
    if enemy_msgs:
      print(enemy_msgs)
    if not enemy.is_alive():
      break

    print(f"\n{player}")
    print(f"{enemy}")
    print(f"Your spells: {player.spells} | mana: {player.mana}")
    action = input("Cast a spell by name, or type 'flee': ").strip()

    if action.lower() == 'flee':
      print(f"{player.name} flees. The path teaches cowardice has a price: no exp gained!")
      break

    spell_hit = player.cast_mana(action, enemy)

    if not enemy.is_alive():
      break

    if spell_hit:
      print()
      is_frozen = any(type(e).__name__ == "Frozen" for e in enemy.status_effects)
      if is_frozen:
        print(f"{enemy.name} is frozen solid. It cannot act.")
      else:
        if player.inventory.has_item("Pass Rune"):
          print(f"\n{enemy.name} winds up to strike!")
          react = input("React with Pass Rune? [y/n]: ").strip().lower()
          if react == 'y':
            item = player.inventory.get_item("Pass Rune")
            item.use(player)
            player.inventory.remove("Pass Rune")
          else:
            enemy.attack(player)
        else:
          enemy.attack(player)

    reacted = False

    if player.is_alive() and player.hp <= player.max_hp // 4 and not reacted:
      if player.inventory.has_item("Except Vial"):
        print(f"\n{player.name} is critically wounded!")
        react = input("Use Except Vial? [y/n]: ").strip().lower()
        if react == 'y':
          item = player.inventory.get_item("Except Vial")
          item.use(player)
          player.inventory.remove("Except Vial")
          reacted = True

    if player.is_alive() and player.hp <= player.max_hp // 2 and not reacted:
      for tier in ["I", "II", "III", "IV"]:
        potion_name = f"HP Potion {tier}"
        if player.inventory.has_item(potion_name):
          print(f"\n{player.name} is wounded!")
          heal = input(f"Use {potion_name}? [y/n]: ").strip().lower()
          if heal == 'y':
            item = player.inventory.get_item(potion_name)
            item.use(player)
            player.inventory.remove(potion_name)
            reacted = True
          break

    if player.is_alive() and player.mana <= player.max_mana // 2 and not reacted:
      for tier in ["I", "II", "III", "IV"]:
        potion_name = f"Mana Potion {tier}"
        if player.inventory.has_item(potion_name):
          print(f"\n{player.name} is running low on mana!")
          use = input(f"Use {potion_name}? [y/n]: ").strip().lower()
          if use == 'y':
            item = player.inventory.get_item(potion_name)
            item.use(player)
            player.inventory.remove(potion_name)
            reacted = True
          break

    if not player.is_alive():
      if player.inventory.has_item("Finally Flask"):
        flask = player.inventory.get_item("Finally Flask")
        flask.use(player)
        player.inventory.remove("Finally Flask")

  print("\n=== COMBAT ENDS ===")