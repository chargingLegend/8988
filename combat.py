from wizard import Wizard
from items import PassRune, ExceptVial, FinallyFlask, HPPotion, ManaPotion


def _dispatch_ability(player, enemy):
  """Route player ability choice to the correct method dynamically."""
  if not player.abilities:
    print("\nNo abilities have awakened in you yet.")
    return False

  print(f"\nAbilities: {player.abilities}")
  print(f"Manabda: {player.manabda}/8")
  chosen = input("Which ability?: ").strip().lower()

  # abilities that need a list of targets
  multi_target = ["map_fire", "surge", "eclipse", "wild_conjure"]
  # abilities that need no target (self or free-form)
  no_target = ["summon_elemental", "conjure_supply", "amplify",
               "transmute_vitae", "transmute_arcana"]

  if chosen not in player.abilities:
    print("That ability doesn't answer.")
    return False

  method = getattr(player, chosen, None)
  if not method:
    print("The ability exists but won't move. Something is missing.")
    return False

  if chosen in multi_target:
    result = method([enemy])
  elif chosen in no_target:
    result = method()
  else:
    result = method(enemy)

  if result:
    print(result)
  return True


def _check_charge_interrupt(entity, dmg_dealt):
  """Interrupt a special move charge if hit for >= 30% max HP."""
  from systems.status_effects import Charging
  for effect in entity.status_effects[:]:
    if isinstance(effect, Charging):
      threshold = getattr(entity, 'max_hp', 100) * 0.30
      if dmg_dealt >= threshold:
        msg = effect.interrupt(entity)
        entity.status_effects.remove(effect)
        print(f"\n{msg}")
        return True
  return False


def _tick_entity_cooldowns(entity):
  """Tick enemy spell cooldowns if present."""
  if hasattr(entity, 'spell_cooldowns'):
    for key in list(entity.spell_cooldowns):
      entity.spell_cooldowns[key] -= 1
      if entity.spell_cooldowns[key] <= 0:
        del entity.spell_cooldowns[key]


def simple_combat(player, enemy):
  print(f"\n=== COMBAT: {player.name} vs {enemy.name} ===")

  # ── companion init ────────────────────────────────────────
  mira = None
  if hasattr(player, 'flags') and player.flags.get('companion_mira'):
    from entities.humanoid import FrightenedWoman
    mira = FrightenedWoman()
    mira.reset_passive()
    print(f"\nMira stands back. Watching. Ready.")
    print(f"Mira: {mira.hp}/{mira.max_hp} HP")

  # ── additional companions initialize here ─────────────────


  while player.is_alive() and enemy.is_alive():

    # ── status ticks ─────────────────────────────────────────
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

    # ── spell cooldown ticks ──────────────────────────────────
    if hasattr(player, 'tick_spell_cooldowns'):
      player.tick_spell_cooldowns()
    _tick_entity_cooldowns(enemy)

    # ── skip turn check (Slowed, Shattered, etc) ──────────────
    if getattr(enemy, 'skip_turn', False):
      enemy.skip_turn = False
      print(f"\n{enemy.name} cannot act this turn.")
      continue

    # ── companion passives ────────────────────────────────────
    if mira and mira.is_alive():
      mira.passive_check(player)

    # ── status display ────────────────────────────────────────
    print(f"\n{player}")
    print(f"{enemy}")
    print(f"Spells: {player.spells} | Mana: {player.mana}/{player.max_mana}")
    if player.abilities:
      print(f"Abilities: {player.abilities} | Manabda: {player.manabda}/8")
    if mira and mira.is_alive():
      print(f"Mira: {mira.hp}/{mira.max_hp} HP | Type 'mira' to ask for healing.")

    # ── active status effects on player ──────────────────────
    if player.status_effects:
      active = [e.name for e in player.status_effects]
      print(f"Status: {', '.join(active)}")

    action = input("\nSpell name, 'ability', 'mira', or 'flee': ").strip().lower()

    # ── flee ──────────────────────────────────────────────────
    if action == 'flee':
      print(f"{player.name} flees.")
      print(f"The Path teaches cowardice has a price: no exp gained.")
      break

    # ── mira ──────────────────────────────────────────────────
    if action == 'mira':
      if mira and mira.is_alive():
        mira.heal_choice(player)
      else:
        print(f"\nShe isn't here.")
      continue

    # ── ability dispatcher ────────────────────────────────────
    if action == 'ability':
      ability_used = _dispatch_ability(player, enemy)
      if ability_used and enemy.is_alive():
        dmg = enemy.attack(player)
        if dmg:
          _check_charge_interrupt(player, dmg)
      continue

    # ── spell cast ────────────────────────────────────────────
    spell_hit = player.cast_mana(action, enemy)

    if not enemy.is_alive():
      break

    if spell_hit:
      print()
      is_frozen = any(type(e).__name__ == "Frozen" for e in enemy.status_effects)
      is_shattered = any(type(e).__name__ == "Shattered" for e in enemy.status_effects)
      if is_frozen:
        print(f"{enemy.name} is frozen solid. It cannot act.")
      elif is_shattered:
        print(f"{enemy.name} is shattered. It cannot act.")
      else:
        if player.inventory.has_item("Pass Rune"):
          print(f"\n{enemy.name} winds up to strike!")
          react = input("React with Pass Rune? [y/n]: ").strip().lower()
          if react == 'y':
            item = player.inventory.get_item("Pass Rune")
            item.use(player)
            player.inventory.remove("Pass Rune")
          else:
            dmg = enemy.attack(player)
            if dmg:
              _check_charge_interrupt(player, dmg)
        else:
          dmg = enemy.attack(player)
          if dmg:
            _check_charge_interrupt(player, dmg)

    reacted = False

    # ── reaction items ────────────────────────────────────────
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

    # ── death check with Finally Flask ───────────────────────
    if not player.is_alive():
      if player.inventory.has_item("Finally Flask"):
        flask = player.inventory.get_item("Finally Flask")
        flask.use(player)
        player.inventory.remove("Finally Flask")

  # ── post combat companion report ──────────────────────────
  if mira and mira.is_alive():
    print(f"\nMira: {mira.hp}/{mira.max_hp} HP after combat.")
    if mira.hp <= 20:
      print(f"She's pale. Unsteady.")
      print(f"'I'm alright.' She says it again.")
      print(f"You're not sure either of you believes it.")

  # ── post combat rewards ───────────────────────────────────
  if not enemy.is_alive():
    if enemy.gold_reward:
      player.gold = getattr(player, 'gold', 0) + enemy.gold_reward
      print(f"\n+{enemy.gold_reward} gold. Total: {player.gold}")
    drops = enemy.drop_loot()
    if drops:
      print(f"Among the remains — {', '.join(drops)}.")
      for drop in drops:
        player.inventory.add(drop)

  print("\n=== COMBAT ENDS ===")