import random
from inventory import Inventory
from items import (Item, Consumable, Equipment, HPPotion, ManaPotion,
                   ManabdaPotion, PassRune, ExceptVial, FinallyFlask,
                   Cloak, Staff, Rod, Scepter)
from systems.status_effects import Burn, Scorched, Combusting


class Wizard:
  def __init__(self, name: str, level: int = 1, hp: int = 100, school: str = "Undecided",
               spells: list[str] | None = None, manabda: int = 8, max_mana: int = 20,
               mana: int = 20, inventory: Inventory | None = None) -> None:
    self.name = name
    self.level = level
    self.hp = hp
    self.max_hp = hp
    self.school = school
    self.manabda = manabda
    self.spells = spells if spells is not None else []
    self.spell_data = {}
    self.ability_data = {}
    self.inventory = inventory if inventory is not None else Inventory()
    self.status_effects = []
    self.exp = 0
    self.defense = 0
    self.gold = 0
    self.exp_to_next = self.calc_exp_to_next()
    self.max_mana = max_mana
    self.mana = mana
    self.spell_upgrades = {}
    self.ability_upgrades = {}
    self.abilities = []
    self.minions = []
    self.last_killed = None
    self.sort_acquired_by = None
    self.corruption = 0  # 0 = clean | 1-3 = shady | 4-7 = dark | 8+ = corrupted

  def __repr__(self) -> str:
    return (f"{self.name} the {self.school} Wizard | "
            f"LVL:{self.level} | "
            f"HP:{self.hp}/{self.max_hp} | "
            f"Mana: {self.mana}/{self.max_mana} | "
            f"Manabda: {self.manabda} | "
            f"Spells: {len(self.spells)}")

  def __str__(self) -> str:
    status = "alive" if self.is_alive() else "Fallen"
    return (f"{self.name} the {self.school} Wizard | "
            f"LVL:{self.level} | {status} | "
            f"HP: {self.hp}/{self.max_hp} | "
            f"Mana: {self.mana}/{self.max_mana} | "
            f"Manabda: {self.manabda} | "
            f"EXP: {self.exp}/{self.exp_to_next}")

  def is_alive(self) -> bool:
    return self.hp > 0

  def take_damage(self, dmg, dmg_type="physical") -> None:
    actual_dmg = max(1, dmg - self.defense)
    self.hp -= actual_dmg
    if self.hp < 0:
      self.hp = 0
    print(f"{self.name} takes {dmg} {dmg_type} damage! HP: {self.hp}")
    if not self.is_alive():
      print(f"{self.name} falls.")

  def add_status(self, status_effect) -> None:
    self.status_effects.append(status_effect)

  def tick_status_effects(self) -> str:
    messages = []
    for effect in self.status_effects[:]:
      result = effect.tick(self)
      if result:
        messages.append(result)
      if effect.is_expired():
        self.status_effects.remove(effect)
    return "\n".join(messages)

  def calc_exp_to_next(self) -> int:
    return int(33 * (1.3 ** (self.level - 1)))

  def gain_exp(self, amount: int) -> None:
    self.exp += amount
    print(f"{self.name} gains {amount} EXP! [{self.exp}/{self.exp_to_next}]")
    while self.exp >= self.exp_to_next:
      self.exp -= self.exp_to_next
      self.level_up()

  def level_up(self) -> None:
    self.level += 1
    self.exp_to_next = self.calc_exp_to_next()
    self.max_hp += 5
    self.hp = self.max_hp
    self.max_mana += 1
    self.mana = self.max_mana
    if self.level % 3 == 0:
      self.mana = min(8, self.mana + 1)
      print(f"The well deepens. mana: {self.mana}/8")
    print(f"\n*** {self.name} reached Level {self.level}! ***")
    print(f"Gained +5 Max HP and +1 Max Mana")
    print(f"Max HP: {self.max_hp} | Max Mana: {self.max_mana} | mana: {self.mana}")
    print(f"Next level at {self.exp_to_next} EXP\n")
    self.level_up_choice()

  def level_up_choice(self) -> None:
    print("You feel power settling into your bones. Choose your advancement:")
    print("1. Fortify Body: +10 Max HP")
    print("2. Expand Mind: +5 Max Mana")
    print("3. Empower Ability: strengthen a pythonic ability")
    print("4. Empower Spell: strengthen an existing spell")
    print("5. Learn Spell: learn a new spell for your school")
    choice = input("Choice 1-5: ")
    if choice == "1":
      self.add_hp_bonus()
    elif choice == "2":
      self.add_mana_bonus()
    elif choice == "3":
      self.empower_ability_choice()
    elif choice == "4":
      self.empower_spell_choice()
    elif choice == "5":
      try:
        self.learn_spell_choice()
      except ValueError as e:
        print(f"\n{e}")
        self.level_up_choice()
    else:
      print("No choice made. Power dissipates.")

  def add_hp_bonus(self, amount: int = 10) -> None:
    self.max_hp += amount
    self.hp += amount
    print(f"Vitality surges through you! +{amount} Max HP. Total: {self.max_hp}")

  def add_mana_bonus(self, amount: int = 5) -> None:
    self.max_mana += amount
    self.mana += amount
    print(f"Your mind expands! +{amount} Max Mana. Total: {self.max_mana}")

  def empower_ability_choice(self) -> None:
    if not self.abilities:
      print("You have no abilities to empower yet.")
      return
    print("Choose an ability to empower:")
    for i, ability in enumerate(self.abilities):
      current = self.ability_upgrades.get(ability, 0)
      print(f"{i+1}. {ability} (Lvl {current})")
    choice = input("Ability #: ")
    try:
      idx = int(choice) - 1
      ability = self.abilities[idx]
      self.ability_upgrades[ability] = self.ability_upgrades.get(ability, 0) + 1
      print(f"{ability} empowered! Now Level {self.ability_upgrades[ability]}")
    except:
      print("Invalid choice. Power dissipates.")

  def empower_spell_choice(self) -> None:
    if not self.spells:
      print("You have no spells to empower yet.")
      return
    print("Choose a spell to empower:")
    for i, spell in enumerate(self.spells):
      current = self.spell_upgrades.get(spell, 0)
      print(f"{i+1}. {spell} (Lvl {current})")
    choice = input("Spell #: ")
    try:
      idx = int(choice) - 1
      spell = self.spells[idx]
      self.spell_upgrades[spell] = self.spell_upgrades.get(spell, 0) + 1
      print(f"{spell} empowered! Now Level {self.spell_upgrades[spell]}")
    except:
      print("Invalid choice. Power dissipates.")

  def learn_spell_choice(self) -> None:
    if self.school == "Undecided":
      print("Choose a school first.")
      return
    available = [s for s in self.spell_data.keys() if s not in self.spells]
    if not available:
      raise ValueError("You have mastered all available spells. Choose something else.")
    print("Choose a spell to learn:")
    for i, spell in enumerate(available):
      print(f"{i+1}. {spell}")
    choice = input("Spell #: ")
    try:
      idx = int(choice) - 1
      if idx < 0 or idx >= len(available):
        raise IndexError
      spell = available[idx]
      self.spells.append(spell)
      print(f"Learned {spell}!")
    except (ValueError, IndexError):
      print("Invalid choice. Power dissipates.")

  def get_spell_power(self, spell_name: str) -> int:
    return self.spell_upgrades.get(spell_name, 0)

  def check_mana(self, cost: int) -> None:
    if self.mana < cost:
      raise ValueError(f"The well is dry. Have {self.mana}, need {cost}.")

  def check_manabda(self, cost: int) -> None:
    if self.manabda < cost:
      raise ValueError(f"The manabda is spent. Have {self.manabda}, need {cost}.")

  def cast_mana(self, spell_name, target=None):
    from systems.status_effects import (Disoriented, Burn, Frostbitten,
      Slowed, Stuttered, Shattered, Weakened)

    match = next((s for s in self.spells if s.lower() == spell_name.lower()), None)
    if not match:
      print("The spell fizzles. You don't know it.")
      return False
    spell_name = match

    if self.mana == 0:
      print("Nothing happens. The well, from which you draw your power is dry.")
      return False

    # ── disoriented fizzle check ──────────────────────────────
    if Disoriented.is_active(self):
      if Disoriented.roll_fizzle():
        self.mana -= 1
        print(f"*mana burns* mana left: {self.mana}")
        print(f"The disorientation takes hold. '{spell_name}' slips away before it forms.")
        print(f"The well gave something. The spell gave nothing.")
        return False

    self.mana -= 1
    print(f"*mana burns. One less in the well.* mana left: {self.mana}")

    spell_entry = self.spell_data.get(spell_name)
    if not spell_entry:
      print("The spell fizzles. Something is missing from the weave.")
      return False

    # ── route special python_concept spells ──────────────────
    if isinstance(spell_entry, dict) and spell_entry.get("python_concept"):
      return self._cast_special_spell(spell_name, spell_entry, target)

    # ── spell entry can be tuple (old) or dict (new with effects) ─
    if isinstance(spell_entry, dict):
      min_dmg = spell_entry.get("min_dmg", 0)
      max_dmg = spell_entry.get("max_dmg", 0)
      dmg_type = spell_entry.get("dmg_type", "arcane")
      desc = spell_entry.get("desc", "power lashes {target}.")
      effect = spell_entry.get("effect", None)
      effect_chance = spell_entry.get("effect_chance", 1.0)
      cooldown_key = spell_entry.get("cooldown_key", None)
      cooldown_turns = spell_entry.get("cooldown_turns", 0)
    else:
      min_dmg, max_dmg, dmg_type, desc = spell_entry
      effect = None
      effect_chance = 1.0
      cooldown_key = None
      cooldown_turns = 0

    # ── cooldown check ────────────────────────────────────────
    if cooldown_key:
      if not hasattr(self, 'spell_cooldowns'):
        self.spell_cooldowns = {}
      remaining = self.spell_cooldowns.get(cooldown_key, 0)
      if remaining > 0:
        print(f"'{spell_name}' is still recovering. {remaining} turn(s) remaining.")
        self.mana += 1  # refund
        return False

    power = self.get_spell_power(spell_name)

    # ── apply tier bonuses if tiers exist ────────────────────
    tiers = spell_entry.get("tiers", {})
    tier_data = tiers.get(str(power), {}) if power > 0 else {}
    if tier_data:
      min_dmg = tier_data.get("min_dmg", min_dmg)
      max_dmg = tier_data.get("max_dmg", max_dmg)
      effect = tier_data.get("effect", effect)
      effect_chance = tier_data.get("effect_chance", effect_chance)
    else:
      min_dmg += power
      max_dmg += power * 2

    # ── zero damage utility spells ────────────────────────────
    if min_dmg == 0 and max_dmg == 0:
      print(f"{self.name} weaves: '{spell_name}'.")
      if target:
        print(desc.format(target=target.name))
        if effect and random.random() < effect_chance:
          self._apply_spell_effect(effect, target, spell_name)
      else:
        print(desc.format(target="the empty air"))
      return True

    if not target:
      print(f"{self.name} weaves '{spell_name}' but there is no target. Power dissipates.")
      return True

    dmg = random.randint(min_dmg, max_dmg)
    print(f"{self.name} weaves: '{spell_name}' Lvl{power}!")
    print(desc.format(target=target.name))
    target.take_damage(dmg, dmg_type)

    # ── apply status effect ───────────────────────────────────
    if effect and random.random() < effect_chance:
      self._apply_spell_effect(effect, target, spell_name)

    # ── set cooldown ──────────────────────────────────────────
    if cooldown_key and cooldown_turns > 0:
      if not hasattr(self, 'spell_cooldowns'):
        self.spell_cooldowns = {}
      self.spell_cooldowns[cooldown_key] = cooldown_turns

    # ── legacy Ignite burn (backward compat) ─────────────────
    if spell_name == "Ignite" and not effect and random.random() < 0.5:
      burn = Burn(duration=3, damage_per_turn=5)
      target.add_status(burn)
      print(f"{target.name} catches fire!")

    self.last_spell_cast = spell_name
    return True

  def _cast_special_spell(self, spell_name, spell_entry, target):
    """Dispatch logic for all python_concept spells."""
    concept = spell_entry.get("python_concept", "")
    power = self.get_spell_power(spell_name)

    # ── resolve tier data if available ───────────────────────
    tiers = spell_entry.get("tiers", {})
    tier = tiers.get(str(power), {}) if power > 0 else {}

    def td(key, default):
      return tier.get(key, spell_entry.get(key, default))

    # ── SMELT — try/except ────────────────────────────────────
    if spell_name == "Smelt":
      resistance = getattr(target, 'fire_resistance', 0)
      threshold = td("resist_threshold", 10)
      print(f"{self.name} weaves: 'Smelt' Lvl{power}!")
      print(f"# try:")
      if resistance <= threshold:
        print(f"  heat pours into {target.name}. The weave holds.")
        dmg = random.randint(td("min_dmg", 5), td("max_dmg", 12))
        target.take_damage(dmg, "fire")
        if random.random() < td("effect_chance", 0.6):
          self._apply_spell_effect("Burn", target, spell_name)
      else:
        strip = td("strip_amount", 5)
        print(f"# except FireResistance:")
        print(f"  resistance too high — stripping {strip} fire resistance instead.")
        target.fire_resistance = max(0, resistance - strip)
        print(f"  {target.name} fire resistance: {target.fire_resistance}")
      return True

    # ── FLASHPOINT — bool ─────────────────────────────────────
    if spell_name == "Flashpoint":
      resistance = getattr(target, 'fire_resistance', 0)
      threshold = td("resist_threshold", 10)
      vulnerable = resistance < threshold
      print(f"{self.name} weaves: 'Flashpoint' Lvl{power}!")
      print(f"# vulnerable = {target.name}.fire_resistance < {threshold}")
      print(f"# vulnerable = {vulnerable}")
      if vulnerable:
        print(f"# if vulnerable: True — ignition condition met.")
        dmg = random.randint(td("min_dmg", 8), td("max_dmg", 18))
        print(spell_entry["desc"].format(target=target.name))
        target.take_damage(dmg, "fire")
        self._apply_spell_effect("Combusting", target, spell_name)
      else:
        print(f"# if vulnerable: False — condition not met. Flashpoint fizzles.")
        print(f"{target.name} has too much fire resistance. The spark finds no purchase.")
        self.mana += 1
      return True

    # ── GLACIAL GRIND — while/break ───────────────────────────
    if spell_name == "Glacial Grind":
      break_threshold = 0.25 if power >= 3 else 0.5
      print(f"{self.name} weaves: 'Glacial Grind' Lvl{power}!")
      print(f"# while {target.name}.hp > {target.name}.max_hp * {break_threshold}:")
      hits = 0
      base_dmg = random.randint(td("min_dmg", 3), td("max_dmg", 6))
      while target.hp > target.max_hp * break_threshold and target.is_alive():
        hits += 1
        print(f"  the cold grinds. Hit {hits}.")
        target.take_damage(base_dmg, "cold")
        if hits >= 4:
          break
      if target.hp <= target.max_hp * break_threshold:
        print(f"# break — {target.name} dropped below threshold. The loop ends.")
      if hits == 4:
        print(f"# break — max iterations reached.")
      if random.random() < td("effect_chance", 0.3):
        self._apply_spell_effect("Frostbitten", target, spell_name)
      return True

    # ── NULLFROST — None ──────────────────────────────────────
    if spell_name == "Nullfrost":
      nullify_count = 2 if power >= 2 else 1
      nullify_all = power >= 3
      print(f"{self.name} weaves: 'Nullfrost' Lvl{power}!")
      if target.status_effects:
        if nullify_all:
          count = len(target.status_effects)
          target.status_effects.clear()
          print(f"# all active effects set to None. {count} effect(s) dissolved.")
        else:
          for _ in range(min(nullify_count, len(target.status_effects))):
            effect_to_null = target.status_effects[0]
            print(f"# active_effect = {effect_to_null.name}")
            print(f"# active_effect = None")
            target.status_effects.remove(effect_to_null)
            print(f"  {effect_to_null.name} on {target.name} set to None. It dissolves.")
      else:
        print(f"# active_effect = None  ← already None")
        print(f"  nothing to nullify. The frost returns None.")
        print(f"  None.")
      return True

    # ── INTERVAL — range() ────────────────────────────────────
    if spell_name == "Interval":
      hit_range = td("hit_range", (1, 4))
      available_mana = self.mana
      max_hits = min(hit_range[1] - 1, available_mana)
      if max_hits < hit_range[0]:
        print(f"Not enough mana for even one Interval hit.")
        self.mana += 1
        return False
      print(f"{self.name} weaves: 'Interval' Lvl{power}!")
      print(f"# for beat in range({hit_range[0]}, {min(hit_range[1], max_hits + 1)}):")
      total_dmg = 0
      hit_count = random.randint(hit_range[0], min(hit_range[1] - 1, max_hits))
      for beat in range(hit_count):
        dmg = random.randint(td("min_dmg", 2), td("max_dmg", 5))
        print(f"  beat {beat + 1} — {dmg} time damage.")
        target.take_damage(dmg, "time")
        total_dmg += dmg
        self.mana -= spell_entry.get("mana_per_hit", 1)
        if not target.is_alive():
          break
      print(f"  Interval struck {hit_count} time(s). Total: {total_dmg} damage.")
      return True

    # ── RECURRENCE — for loop ─────────────────────────────────
    if spell_name == "Recurrence":
      last = getattr(self, 'last_spell_cast', None)
      if not last or last == "Recurrence":
        print(f"# Recurrence requires a previous spell to loop.")
        print(f"  No last spell found. Power dissipates.")
        self.mana += 1
        return False
      last_entry = self.spell_data.get(last)
      if not last_entry:
        print(f"  Last spell '{last}' has no data. Cannot recur.")
        self.mana += 1
        return False
      extra_cost = 1
      if self.mana < extra_cost:
        print(f"  Not enough mana to recur.")
        self.mana += 1
        return False
      self.mana -= extra_cost
      repeat_count = td("repeat_count", 3)
      print(f"{self.name} weaves: 'Recurrence' Lvl{power}!")
      print(f"# for iteration in range({repeat_count}):")
      for i in range(repeat_count):
        print(f"  iteration {i} — casting {last} again.")
        min_d = last_entry.get("min_dmg", 0)
        max_d = last_entry.get("max_dmg", 0)
        dtype = last_entry.get("dmg_type", "time")
        if max_d > 0:
          dmg = random.randint(min_d, max_d)
          target.take_damage(dmg, dtype)
        if not target.is_alive():
          break
      return True

    # ── EXHUME — list mutation ────────────────────────────────
    if spell_name == "Exhume":
      dead_list = getattr(self, 'combat_dead_list', [])
      print(f"{self.name} weaves: 'Exhume' Lvl{power}!")
      print(f"# dead_list = {[e.name for e in dead_list]}")
      if not dead_list:
        print(f"# dead_list is empty. Nothing to pull.")
        print(f"  The grave gives nothing back.")
        return True
      revived = dead_list.pop()
      revive_pct = td("revive_hp_percent", 0.3)
      revived_hp = int(revived.max_hp * revive_pct)
      revived.hp = revived_hp
      if td("revived_atk_bonus", 0):
        revived.atk += td("revived_atk_bonus", 0)
      if not hasattr(self, 'minions'):
        self.minions = []
      self.minions.append(revived)
      print(f"# dead_list.pop() → {revived.name}")
      print(f"  {revived.name} stirs at {revived_hp} HP. Added to field.")
      return True

    # ── ERASURE — del ─────────────────────────────────────────
    if spell_name == "Erasure":
      print(f"{self.name} weaves: 'Erasure' Lvl{power}!")
      buffs = [e for e in target.status_effects
               if hasattr(e, 'is_buff') and e.is_buff]
      delete_count = 2 if power >= 2 else 1
      delete_all = power >= 3
      if not buffs:
        print(f"# del target.active_buff — KeyError: no buff found.")
        print(f"  Nothing to delete. The spell wastes.")
        return True
      if delete_all:
        count = len(buffs)
        for b in buffs:
          target.status_effects.remove(b)
        print(f"  All {count} buff(s) on {target.name} — deleted. Gone.")
      else:
        for b in buffs[:delete_count]:
          print(f"# del {target.name}.{b.name}")
          target.status_effects.remove(b)
          print(f"  {b.name} on {target.name} — deleted. Not nulled. Gone.")
      return True

    # ── MAGNITUDE — integer operations ───────────────────────
    if spell_name == "Magnitude":
      if not hasattr(self, 'magnitude_active'):
        self.magnitude_active = 0
      duration = td("duration", 3)
      base_dmg = td("base_dmg", 6)
      ceiling = 4 if power >= 2 else 3
      hp_ratio = self.max_hp / max(self.hp, 1)
      multiplier = min(int(hp_ratio), ceiling)
      dmg = int(multiplier * base_dmg)
      print(f"{self.name} weaves: 'Magnitude' Lvl{power}!")
      print(f"# multiplier = int(max_hp / hp) = int({self.max_hp}/{self.hp}) = {int(hp_ratio)}")
      print(f"# dmg = {multiplier} * {base_dmg} = {dmg}")
      print(f"  the number finds {target.name}. {dmg} force damage.")
      target.take_damage(dmg, "force")
      self.magnitude_active = duration
      print(f"  Magnitude active for {duration} more turns.")
      return True

    # ── SURGE STACK — += ─────────────────────────────────────
    if spell_name == "Surge Stack":
      if not hasattr(self, 'surge_stacks'):
        self.surge_stacks = 0
      stack_bonus = td("stack_bonus", 2)
      max_stacks = td("max_stacks", 5)
      ally_has_status = any(
        hasattr(a, 'status_effects') and a.status_effects
        for a in getattr(self, 'active_allies', [])
      )
      if not ally_has_status and self.surge_stacks == 0:
        print(f"{self.name} weaves: 'Surge Stack' Lvl{power}!")
        print(f"# requires ally applying status damage — condition not met.")
        print(f"  The stack has no fuel. It holds at zero.")
        return True
      self.surge_stacks = min(
        self.surge_stacks + stack_bonus,
        max_stacks * stack_bonus
      )
      dmg = random.randint(td("min_dmg", 2), td("max_dmg", 4))
      total = dmg + self.surge_stacks
      print(f"{self.name} weaves: 'Surge Stack' Lvl{power}!")
      print(f"# surge_stacks += {stack_bonus}")
      print(f"# surge_stacks = {self.surge_stacks}")
      print(f"# dmg = base({dmg}) + stack({self.surge_stacks}) = {total}")
      print(f"  the value compounds. {total} force damage.")
      target.take_damage(total, "force")
      return True

    # ── MIRAGE — variable reassignment ───────────────────────
    if spell_name == "Mirage":
      original_atk = target.atk
      new_atk = int(target.atk * 0.5)
      duration = spell_entry["duration"] + power
      if not hasattr(self, 'mirage_data'):
        self.mirage_data = {}
      self.mirage_data[id(target)] = {
        "original_atk": original_atk,
        "turns_left": duration
      }
      target.atk = new_atk
      print(f"{self.name} weaves: 'Mirage' Lvl{power}!")
      print(f"# {target.name}.atk = {new_atk}  ← was {original_atk}")
      print(f"  {target.name} believes it is as strong as ever. It is not.")
      print(f"  Effect lasts {duration} turns.")
      return True

    # ── DOPPEL — is vs == ─────────────────────────────────────
    if spell_name == "Doppel":
      if power >= 2:
        chance = spell_entry["upgrade_2_chance"]
        hits = spell_entry["upgrade_2_hits"]
      elif power >= 1:
        chance = spell_entry["upgrade_1_chance"]
        hits = spell_entry["upgrade_1_hits"]
      else:
        chance = spell_entry["spawn_chance_base"]
        hits = spell_entry["hits_absorbed_base"]
      print(f"{self.name} weaves: 'Doppel' Lvl{power}!")
      print(f"# spawn_chance = {chance}")
      if random.random() < chance:
        self.doppel_hits = hits
        print(f"# doppel is self → False  (looks the same, is not the same)")
        print(f"# doppel == self → True   (structurally identical)")
        print(f"  something steps beside you. It will absorb {hits} hit(s).")
      else:
        self.doppel_hits = 0
        print(f"  the copy doesn't hold. It dissolves before it forms.")
      return True

    # ── SUMMON STACK — list.append() ─────────────────────────
    if spell_name == "Summon Stack":
      if not hasattr(self, 'summon_stack'):
        self.summon_stack = []
      max_stack = spell_entry["max_stack"]
      if len(self.summon_stack) >= max_stack:
        print(f"{self.name} weaves: 'Summon Stack' Lvl{power}!")
        print(f"# stack is full — len(stack) == {max_stack}")
        print(f"  the field won't hold another. Stack at maximum.")
      else:
        entity_name = f"Shard-{len(self.summon_stack) + 1}"
        self.summon_stack.append(entity_name)
        chip = spell_entry["chip_dmg_per_entity"] + power
        total_chip = len(self.summon_stack) * chip
        print(f"{self.name} weaves: 'Summon Stack' Lvl{power}!")
        print(f"# stack.append('{entity_name}')")
        print(f"# stack = {self.summon_stack}")
        print(f"  {entity_name} joins the field. Stack deals {total_chip} chip damage.")
        target.take_damage(total_chip, "force")
      return True

    # ── THRESHOLD — len() ─────────────────────────────────────
    if spell_name == "Threshold":
      inv_count = len(self.inventory.items)
      multiplier = spell_entry["multiplier"] + power
      dmg = inv_count * multiplier
      print(f"{self.name} weaves: 'Threshold' Lvl{power}!")
      print(f"# dmg = len(inventory) * {multiplier}")
      print(f"# dmg = {inv_count} * {multiplier} = {dmg}")
      if dmg == 0:
        print(f"  inventory is empty. len() returns 0. No damage.")
      else:
        print(f"  {target.name} feels the weight of every carried thing. {dmg} force damage.")
        target.take_damage(dmg, "force")
      return True

    # ── VOIDCHECK — None check ────────────────────────────────
    if spell_name == "Voidcheck":
      print(f"{self.name} weaves: 'Voidcheck' Lvl{power}!")
      none_attrs = [
        attr for attr in ['active_buff', 'equipped', 'mount', 'ward']
        if getattr(target, attr, None) is None
      ]
      if none_attrs:
        attr = none_attrs[0]
        dmg = random.randint(spell_entry["min_dmg"], spell_entry["max_dmg"]) + (power * 2)
        print(f"# if {target.name}.{attr} is None: True")
        print(f"  the void is found. Reaching in.")
        print(f"  {dmg} shadow damage.")
        target.take_damage(dmg, "shadow")
      else:
        minor = spell_entry["minor_dmg"] + power
        weakest = min(['atk', 'defense'], key=lambda a: getattr(target, a, 999))
        print(f"# if target has None attribute: False")
        print(f"# else: set {target.name}.{weakest} = None — creating the void")
        print(f"  no None found — creating one. {minor} shadow damage.")
        target.take_damage(minor, "shadow")
        setattr(target, weakest, None)
        print(f"  {target.name}.{weakest} = None")
      return True

    # ── SHRED — string slicing ────────────────────────────────
    if spell_name == "Shred":
      name = target.name
      sliced = name[1:-1]
      dmg = len(sliced) * 2 + power
      print(f"{self.name} weaves: 'Shred' Lvl{power}!")
      print(f"# '{name}'[1:-1] = '{sliced}'")
      print(f"# dmg = len('{sliced}') * 2 = {dmg}")
      print(f"  the middle is taken. What remains is a curse.")
      print(f"  '{sliced}' binds to {target.name}. {dmg} shadow damage.")
      target.take_damage(dmg, "shadow")
      if random.random() < spell_entry.get("effect_chance", 0.8):
        self._apply_spell_effect("Weakened", target, spell_name)
      return True

    # ── RECAST — type casting ─────────────────────────────────
    if spell_name == "Recast":
      cycles = spell_entry["cycles"] + power
      decay = spell_entry["decay_multiplier"]
      print(f"{self.name} weaves: 'Recast' Lvl{power}!")
      print(f"# hp = float({target.hp})")
      hp_float = float(target.hp)
      print(f"# for cycle in range({cycles}):")
      for cycle in range(cycles):
        hp_float *= decay
        print(f"  cycle {cycle}: float *= {decay} → {hp_float:.2f}")
      new_hp = int(hp_float)
      dmg = target.hp - new_hp
      print(f"# hp = int({hp_float:.2f}) = {new_hp}")
      print(f"  type cast complete. {target.name} loses {dmg} HP from the conversion.")
      target.hp = max(0, new_hp)
      if not target.is_alive():
        print(f"{target.name} falls.")
      return True

    # ── OVERWRITE — dict.update() ─────────────────────────────
    if spell_name == "Overwrite":
      stats = {k: getattr(target, k, None)
               for k in ['atk', 'defense'] if getattr(target, k, None) is not None}
      if not stats:
        print(f"  No stats to overwrite.")
        return True
      stat_key = random.choice(list(stats.keys()))
      original = stats[stat_key]
      new_val = int(original * spell_entry["debuff_multiplier"])
      duration = spell_entry["duration"] + power
      if not hasattr(self, 'overwrite_data'):
        self.overwrite_data = {}
      self.overwrite_data[f"{id(target)}_{stat_key}"] = {
        "original": original, "turns_left": duration,
        "target": target, "stat": stat_key
      }
      setattr(target, stat_key, new_val)
      print(f"{self.name} weaves: 'Overwrite' Lvl{power}!")
      print(f"# target_stats.update({{'{stat_key}': {new_val}}})")
      print(f"  {target.name}.{stat_key}: {original} → {new_val}")
      print(f"  The old value is gone. Lasts {duration} turns.")
      self._apply_spell_effect("Weakened", target, spell_name)
      return True

    # ── fallback for unmapped concepts ───────────────────────
    print(f"{self.name} weaves: '{spell_name}'.")
    if target and spell_entry.get("max_dmg", 0) > 0:
      dmg = random.randint(spell_entry["min_dmg"], spell_entry["max_dmg"]) + power
      target.take_damage(dmg, spell_entry.get("dmg_type", "arcane"))
    if spell_name != "Recurrence":
      self.last_spell_cast = spell_name
    return True

  def _apply_spell_effect(self, effect, target, spell_name):
    """Apply a named status effect to target with stacking and immunity guards."""
    from systems.status_effects import (Disoriented, Burn, Frostbitten,
      Slowed, Stuttered, Shattered, Weakened)

    # ── no stacking same effect ───────────────────────────────
    existing_names = [type(e).__name__ for e in target.status_effects]
    if effect in existing_names:
      print(f"{target.name} is already {effect}. The effect doesn't stack.")
      return

    # ── boss/miniboss immunity check ──────────────────────────
    immune = getattr(target, 'status_immunities', [])
    if effect in immune:
      print(f"{target.name} shrugs off {effect}. It's immune.")
      return

    effect_map = {
      "Burn": lambda: Burn(duration=3, damage_per_turn=5),
      "Frostbitten": lambda: Frostbitten(duration=3, damage_per_turn=3),
      "Slowed": lambda: Slowed(duration=3),
      "Disoriented": lambda: Disoriented(duration=2),
      "Stuttered": lambda: Stuttered(duration=1),
      "Shattered": lambda: Shattered(duration=2),
      "Weakened": lambda: Weakened(duration=3, atk_reduction=2, defense_reduction=1),
    }
    factory = effect_map.get(effect)
    if factory:
      status = factory()
      target.add_status(status)
      print(f"{target.name} is now {effect}!")
    else:
      print(f"Unknown effect: {effect}. Nothing happens.")

  def tick_spell_cooldowns(self):
    """Call once per combat turn to decrement cooldowns."""
    if not hasattr(self, 'spell_cooldowns'):
      return
    for key in list(self.spell_cooldowns):
      self.spell_cooldowns[key] -= 1
      if self.spell_cooldowns[key] <= 0:
        del self.spell_cooldowns[key]



  def cast_manabda(self, ability_name, target=None):
    if ability_name not in self.abilities:
      print("You reach for it. Nothing answers.")
      return False
    if self.manabda == 0:
      print("The manabda is spent. That well does not refill easily.")
      return False
    ability = self.ability_data.get(ability_name)
    if not ability:
      print(f"No data found for {ability_name}.")
      return False
    tiers = ability["tiers"]
    print(f"\n--- {ability_name} ---")
    for key, tier in tiers.items():
      if tier.get("requires_upgrade"):
        if self.ability_upgrades.get(ability_name, 0) >= 1:
          print(f"{key}. {tier['label']} - costs ALL manabda")
      else:
        print(f"{key}. {tier['label']} - costs {tier['cost']} manabda")
    choice = input("Choose: ").strip()
    selected = tiers.get(choice)
    if not selected:
      print("The moment passes. Manabda holds.")
      return False
    cost = self.manabda if selected["cost"] == "all" else selected["cost"]
    if self.manabda < cost:
      print(f"Not enough manabda. Need {cost}, have {self.manabda}.")
      return False
    self.manabda -= cost
    print(f"*manabda spent. {self.manabda}/8 remains.*")
    method = getattr(self, ability_name, None)
    if method is None:
      print(f"No effect logic found for {ability_name}.")
      return False
    result = method(target)
    if result:
      print(result)
    return True