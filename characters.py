import random
from Inventory import Inventory
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
    self.inventory = inventory if inventory is not None else Inventory()
    self.status_effects = []
    self.exp = 0
    self.exp_to_next = self.calc_exp_to_next()
    self.max_mana = max_mana
    self.mana = mana
    self.spell_upgrades = {}
    self.ability_upgrades = {}
    self.abilities = []
    self.minions = []
    self.last_killed = None
    self.sort_acquired_by = None

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
    print("5. Learn Spell: learn 1 of 2 non-starter spells for your school")
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
      self.learn_spell_choice()
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
      print("You've learned all spells for your school. Taking +5 HP instead.")
      self.add_hp_bonus(5)
      return
    print("Choose a spell to learn:")
    for i, spell in enumerate(available[:2]):
      print(f"{i+1}. {spell}")
    choice = input("Spell #: ")
    try:
      idx = int(choice) - 1
      spell = available[idx]
      self.spells.append(spell)
      print(f"Learned {spell}!")
    except:
      print("Invalid choice. Power dissipates.")

  def get_spell_power(self, spell_name: str) -> int:
    return self.spell_upgrades.get(spell_name, 0)

  def __repr__(self) -> str:
    return f"Wizard({self.name}) - LVL:{self.level} HP:{self.hp}/{self.max_hp} - School: {self.school} - Spells: {len(self.spells)} - mana: {self.mana} - Mana: {self.mana}/{self.max_mana}"

  def __str__(self) -> str:
    status = "alive" if self.is_alive() else "Fallen"
    return f"{self.name} the {self.school} Wizard | LVL:{self.level} | {status} | HP: {self.hp}/{self.max_hp} | Mana: {self.mana}/{self.max_mana} | mana: {self.mana}/8 | EXP: {self.exp}/{self.exp_to_next}"

  def is_alive(self) -> bool:
    return self.hp > 0

  def take_damage(self, dmg, dmg_type="physical")-> None:
    self.hp -= dmg
    if self.hp < 0:
      self.hp = 0
    print(f"{self.name} takes {dmg} {dmg_type} damage! HP: {self.hp}")
    if not self.is_alive():
      print(f"{self.name} falls.")

  def add_status(self, status_effect):
    self.status_effects.append(status_effect)

  def tick_status_effects(self):
    messages = []
    for effect in self.status_effects[:]:
      result = effect.tick(self)
      if result:
        messages.append(result)
      if effect.is_expired():
        self.status_effects.remove(effect)
    return "\n".join(messages)

  def choose_school(self, school):
    self.school = school
    print(f"A mark burns into your palm: {self.school}.")
    if school == "Pyromancy":
      print("Your skin ripples. Veins beneath glow ember-red.")
      print("A surge of warmth—bordering on hot—courses through your body.")
      print("The sensation is gratifying. Almost euphoric.")
      self.spells = ["Ignite", "Sear", "Cinder Ward"]
      self.spell_data = {
        "Ignite": (3, 8, "fire", "flame catches on {target}'s feathers. It shrieks, blackened."),
        "Sear": (2, 5, "fire", "a lance of heat lashes {target}. their Flesh starts to bubble from the intense heat."),
        "Cinder Ward": (0, 0, "ward", "embers orbit you. No damage, but the air warps.")
      }
    elif school == "Cryomancy":
      print("Your breath fogs. Frost traces your fingertips.")
      print("A stillness settles in your chest, cold and absolute.")
      print("The world seems slower. Sharper. Distant.")
      self.spells = ["Frostbite", "Glaze", "Shard"]
      self.spell_data = {
        "Frostbite": (2, 6, "cold", "ice crusts over {target}. Wings crack."),
        "Glaze": (1, 3, "cold", "rime coats {target}. It moves like cold honey."),
        "Shard": (3, 7, "cold", "a spear of ice punches through {target}.")
      }
    elif school == "Chronomancy":
      print("The air ticks. Your shadow lags half a second behind you.")
      print("For a heartbeat, you see the echo of your next breath.")
      print("Time feels loose. Negotiable.")
      self.spells = ["Hesitate", "Foresight", "Stutter"]
      self.spell_data = {
        "Hesitate": (1, 4, "time", "{target} stutters mid-beat. Existence frays."),
        "Foresight": (0, 0, "time", "you see {target}'s next beat. No damage, yet."),
        "Stutter": (2, 5, "time", "{target} skips a moment. Parts of it arrive late.")
      }
    elif school == "Necromancy":
      print("The ground chills under your feet. Your shadow deepens.")
      print("A whisper you didn’t think brushes the back of your skull.")
      print("Death recognizes you. And waits.")
      self.spells = ["Rattle", "Wither", "Gravechill"]
      self.spell_data = {
        "Rattle": (2, 7, "necrotic", "{target}'s bones remember the grave. They protest."),
        "Wither": (1, 6, "necrotic", "vitality flees {target} like startled crows."),
        "Gravechill": (3, 6, "necrotic", "the cold of tombs settles in {target}.")
      }
    elif school == "Enhancement":
      print("Muscle fibers sing. Bones feel dense as iron.")
      print("The mountain air tastes thin. You don’t care.")
      print("Strength is a word. Now it is a state.")
      self.spells = ["Brace", "Surge", "Iron Skin"]
      self.spell_data = {
        "Brace": (0, 0, "force", "you root yourself. No damage to {target}."),
        "Surge": (2, 6, "force", "kinetic wrath slams into {target}."),
        "Iron Skin": (0, 0, "force", "your skin rings like struck steel. No damage.")
      }
    elif school == "Illusion":
      print("Colors lie. The corner of your eye breeds movement.")
      print("You doubt the weight of your own hands.")
      print("Truth becomes a choice, not a fact.")
      self.spells = ["Phantom", "Mutter", "False Step"]
      self.spell_data = {
        "Phantom": (1, 4, "psychic", "{target} strikes at horrors only it sees."),
        "Mutter": (1, 3, "psychic", "whispers convince {target} it is already wounded."),
        "False Step": (0, 0, "psychic", "{target} misjudges distance. No damage.")
      }
    elif school == "Conjuration":
      print("The space before you bends. Air thickens.")
      print("Something almost arrives, then decides not to.")
      print("The world feels less solid. More borrowed.")
      self.spells = ["Fetch", "Shardling", "Bind"]
      self.spell_data = {
        "Fetch": (0, 0, "force", "you grasp at distance. {target} untouched."),
        "Shardling": (2, 7, "force", "a conjured splinter hurls into {target}."),
        "Bind": (1, 4, "force", "invisible cords seize {target}'s limbs.")
      }
    elif school == "Shadow":
      print("Light bends away from you. Your edges blur.")
      print("Whispers you don’t recognize brush your thoughts.")
      print("You feel unseen. And yet, watched.")
      self.spells = ["Dim", "Mutter", "Veil"]
      self.spell_data = {
        "Dim": (0, 0, "shadow", "light flees {target}. It blinks, confused."),
        "Mutter": (1, 5, "shadow", "dark words eat at {target}'s resolve."),
        "Veil": (0, 0, "shadow", "you cease to be a target. For a moment.")
      }
    elif school == "Transmutation":
      print("Your fingertips tingle. Stone would answer if you asked.")
      print("Lead and gold feel like the same word in different accents.")
      print("Matter is a suggestion.")
      self.spells = ["Shift", "Harden", "Gild"]
      self.spell_data = {
        "Shift": (1, 5, "arcane", "{target}'s mass forgets itself for a second."),
        "Harden": (0, 0, "arcane", "air becomes stone. Not at {target}."),
        "Gild": (2, 6, "arcane", "{target}'s edges turn brittle-gold, then crack.")
      }

  def learn_spell_sort(self, method="gift"):
    if "sort" not in self.spells:
      self.spells.append("sort")
      self.sort_acquired_by = method
      return "The runes on your palm shift. You understand how to use the rune to 'sort' now."
    return "You already understand the sort spell"

  def sort(self, location: dict):
    if "sort" not in self.spells:
      raise AttributeError("You trace the rune to be able to use the 'sort' ability, but it doesnt mean anything to you.not yet")
    found = random.sample(location["common"], k=2)
    if random.random() < 0.10:
      found.append(random.choice(location["uncommon"]))
    for item in found:
      self.inventory.add(item)
    print(f"you focus on the Rune of sort")
    print(f"Found: {', '.join(found)}")
    print(self.inventory)

  def check_mana(self, cost):
    if self.mana < cost:
      raise ValueError(f"The well is dry. Have {self.mana}, need {cost}.")

  def map_fire(self, targets):
    cost = 3
    self.check_mana(cost)
    self.mana -= cost
    dmg = random.randint(3, 6) + self.ability_upgrades.get("map_fire", 0)
    for t in targets:
      t.take_damage(dmg, "fire")
      if random.random() < 0.4:
        t.add_status(Burn(duration=2, damage_per_turn=2))
    return f"Fire spreads across {len(targets)} foes for {dmg} each! mana: {self.mana}"

  def reduce_ash(self, target):
    cost = 5
    self.check_mana(cost)
    self.mana -= cost
    threshold = 8 + self.ability_upgrades.get("reduce_ash", 0) * 2
    if target.hp <= threshold:
      target.hp = 0
      return f"{target.name} turns to ash! mana: {self.mana}"
    dmg = target.hp // 2
    target.take_damage(dmg, "fire")
    return f"{target.name} loses half its essence! {dmg} dmg! mana: {self.mana}"

  def pyromancy_burn(self, target):
    if self.school != "Pyromancy":
      print("Only a Pyromancer can wield this heat.")
      return False

    if getattr(target, 'flame_resistance', None) is None:
      print(f"{target.name} cannot be burned. The flame finds nothing to take.")
      return False

    print(f"\nFire answers your call.")
    print(f"Your mana: {self.mana}/8")
    print(f"\nHow much heat do you pour into {target.name}?")
    print(f"Their resistance: {target.flame_resistance}")
    print("1. Kindle     (heat 10)  - costs 2 mana")
    print("2. Sear       (heat 20)  - costs 4 mana")
    print("3. Incinerate (heat 35)  - costs 6 mana")

    if self.ability_upgrades.get("pyromancy_burn", 0) >= 1:
      print("4. Inferno    (heat 60)  - costs ALL mana")

    choice = input("Choose [1-4]: ").strip()

    options = {
      "1": (10, 2),
      "2": (20, 4),
      "3": (35, 6),
    }

    if self.ability_upgrades.get("pyromancy_burn", 0) >= 1:
      options["4"] = (60, self.mana)

    if choice not in options:
      print("The flame sputters out.")
      return False

    heat, cost = options[choice]

    if self.mana < cost:
      print(f"The well runs dry. Need {cost} mana, have {self.mana}.")
      return False

    self.mana -= cost

    if heat >= target.flame_resistance * 2:
      target.add_status(Combusting(duration=4, damage_per_turn=10))
      dmg = random.randint(15, 25)
      target.take_damage(dmg, "fire")
      return (f"{target.name} ignites completely!\n"
              f"{dmg} fire damage and fully Combusting!\n"
              f"mana: {self.mana}")

    elif heat >= target.flame_resistance:
      target.add_status(Scorched(duration=2, damage_per_turn=3))
      dmg = random.randint(8, 15)
      target.take_damage(dmg, "fire")
      return (f"{target.name} is Scorched!\n"
              f"{dmg} fire damage. The heat is building.\n"
              f"mana: {self.mana}")

    else:
      target.add_status(Burn(duration=3, damage_per_turn=5))
      dmg = random.randint(3, 8)
      target.take_damage(dmg, "fire")
      return (f"Flames lick at {target.name}.\n"
              f"{dmg} fire damage. Burning but not breaking.\n"
              f"mana: {self.mana}")

  def fast_forward_time(self, target, years=None):
    if self.school != "Chronomancy":
      print("Only a Chronomancer can bend time.")
      return False

    print(f"\nThe flow of time bends to your will.")
    print(f"Your mana: {self.mana}/8")
    print(f"\nHow far do you push {target.name} through time?")
    print("1. A Score of Years  (20 years)  - costs 3 mana")
    print("2. Two Generations   (40 years)  - costs 5 mana")
    print("3. A Century         (100 years) - costs 8 mana")

    if self.ability_upgrades.get("fast_forward_time", 0) >= 1:
      print("4. Molecular Dissolution       - costs ALL mana")

    choice = input("Choose [1-4]: ").strip()

    options = {
      "1": (20, 3),
      "2": (40, 5),
      "3": (100, 8),
    }

    if self.ability_upgrades.get("fast_forward_time", 0) >= 1:
      options["4"] = (999, self.mana)

    if choice not in options:
      print("The moment passes. Time snaps back.")
      return False

    years, cost = options[choice]

    if self.mana < cost:
      print(f"The well runs dry. Need {cost} mana, have {self.mana}.")
      return False

    self.mana -= cost

    if years == 999:
      target.hp = 0
      target.is_dust = True
      return (f"{target.name} comes apart at the molecular level.\n"
              f"They simply... cease. mana: {self.mana}")

    if hasattr(target, 'age') and target.age is not None:
      target.age += years

      if target.age >= 100:
        target.atk = max(1, target.atk - 10)
        target.hp = max(1, target.hp // 2)
        return (f"{target.name} withers {years} years!\n"
                f"Ancient now. Frail. Half the threat.\n"
                f"mana: {self.mana}")

      elif target.age >= 40:
        target.atk = max(1, target.atk - 5)
        return (f"{target.name} ages {years} years!\n"
                f"Slower. Weaker. Still dangerous.\n"
                f"mana: {self.mana}")

      else:
        return (f"Time moves over {target.name}.\n"
                f"They seem... unchanged. Was it enough?\n"
                f"mana: {self.mana}")

    elif hasattr(target, 'durability'):
      target.durability -= years * 5
      if target.durability <= 0:
        target.broken = True
        target.is_dust = True
        return f"The {target.name} crumbles to dust. mana: {self.mana}"
      return f"The {target.name} ages and weakens. mana: {self.mana}"

    return f"Time washes over {target.name}. Nothing changes. mana: {self.mana}"

  def rewind_time(self, target, years=None):
    if self.school != "Chronomancy":
      print("Only a Chronomancer can bend time.")
      return False

    if getattr(target, 'is_dust', False):
      print(f"{target.name} is dust. Even time cannot restore what is gone.")
      return False

    print(f"\nTime coils backward at your command.")
    print(f"Your manabda: {self.manabda}/8")
    print(f"\nHow far do you pull {target.name} back through time?")
    print("1. A Score of Years  (20 years)  - costs 3 mana")
    print("2. Two Generations   (40 years)  - costs 5 mana")
    print("3. A Century         (100 years) - costs 8 mana")

    if self.ability_upgrades.get("rewind_time", 0) >= 1:
      print("4. Infant State                - costs ALL mana")

    choice = input("Choose [1-4]: ").strip()

    options = {
      "1": (20, 3),
      "2": (40, 5),
      "3": (100, 8),
    }

    if self.ability_upgrades.get("rewind_time", 0) >= 1:
      options["4"] = (999, self.manabda)

    if choice not in options:
      print("The moment passes. Time snaps forward again.")
      return False

    years, cost = options[choice]

    if self.mana < cost:
      print(f"The well runs dry. Need {cost} mana, have {self.manabda}.")
      return False

    self.mana -= cost

    if years == 999:
      target.age = 0
      target.atk = max(1, target.atk // 4)
      target.hp = max(1, target.hp // 4)
      return (f"{target.name} shrinks. Regresses. Becomes something small and helpless.\n"
              f"Barely a threat. mana: {self.manabda}")

    if hasattr(target, 'age') and target.age is not None:
      target.age = max(0, target.age - years)

      if target.age <= 0:
        target.atk = max(1, target.atk // 4)
        target.hp = max(1, target.hp // 4)
        return (f"{target.name} regresses to infancy!\n"
                f"Pathetic now. Almost harmless.\n"
                f"mana: {self.mana}")

      elif target.age <= 10:
        target.atk = max(1, target.atk // 2)
        return (f"{target.name} becomes a youth!\n"
                f"Weaker. Confused. Still has teeth though.\n"
                f"mana: {self.mana}")

      else:
        target.atk += 2
        return (f"{target.name} grows younger by {years} years!\n"
                f"Faster. Angrier. More dangerous.\n"
                f"mana: {self.mana}")

    elif hasattr(target, 'broken') and target.broken:
      target.broken = False
      target.durability = getattr(target, 'max_durability', 100)
      return f"The {target.name} un-breaks. Restored. mana: {self.mana}"

    return f"Time reverses around {target.name}. Nothing meaningful changes. mana: {self.mana}"

  def freeze(self, target):
    if self.school != "Cryomancy":
      print("Only a Cryomancer can freeze time.")
      return False
    cost = 4
    self.check_manabda(cost)
    self.mana -= cost
    duration = 2 + self.ability_upgrades.get("freeze", 0)
    from systems.status_effects import Frozen
    target.add_status(Frozen(duration=duration))
    return (
      f"Ice closes around {target.name}. It stops mid-motion.\n"
      f"Frozen for {duration} turns. mana: {self.mana}"
    )

  def cryo_preserve(self, target):
    if self.school != "Cryomancy":
      print("Only a Cryomancer can cryo preserve.")
      return False
    cost = 6
    self.check_manabda(cost)
    self.mana -= cost
    from systems.status_effects import Preserved
    target.add_status(Preserved(duration=2))
    target.preserved = True
    return (
      f"{target.name} is sealed in cryo-stasis. Its state is locked.\n"
      f"Healing and buffs suspended for 2 turns. mana: {self.mana}"
    )

  def enumerate_fates(self, targets):
    cost = 3
    self.check_mana(cost)
    self.mana -= cost
    info = [f"{i}: {t.name} | HP:{t.hp} | ATK:{t.atk}" for i, t in enumerate(targets)]
    return "Fates revealed:\n" + "\n".join(info) + f"\nmana: {self.mana}"

  def transmute(self, target, new_material="gold"):
    cost = 5
    self.check_mana(cost)
    self.mana -= cost
    if getattr(target, 'is_animate', False):
      raise ValueError("Can't transmute living things! Use polymorph.")
    target.material = new_material
    return f"{target.name} becomes {new_material}! mana: {self.mana}"

  def polymorph(self, target):
    cost = 7
    self.check_mana(cost)
    self.mana -= cost
    forms = [("Rabbit", 70), ("Bear", 20), ("Statue", 10)]
    new_form = random.choices([f[0] for f in forms], weights=[f[1] for f in forms])[0]
    target.polymorphed_form = new_form
    return f"{target.name} becomes a {new_form}! mana: {self.mana}"

  def enhance_item(self, item_name):
    cost = 4
    self.check_mana(cost)
    self.mana -= cost
    result = self.inventory.upgrade(item_name)
    return f"{result} mana: {self.mana}"




  def cast_mana(self, spell_name, target=None):
    if spell_name not in self.spells:
      print("The spell fizzles. You don't know it.")
      return False
    if self.mana == 0:
      print("Nothing happens. The well, from which you draw your power is dry.")
      return False
    self.mana -= 1
    print(f"*mana burns. One less in the well.* mana left: {self.mana}")
    min_dmg, max_dmg, dmg_type, desc = self.spell_data.get(spell_name, (1, 3, "arcane", "power lashes {target}."))
    power = self.get_spell_power(spell_name)
    min_dmg += power
    max_dmg += power * 2
    if min_dmg == 0 and max_dmg == 0:
      print(f"{self.name} weaves: '{spell_name}'.")
      if target:
        print(desc.format(target=target.name))
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
    if spell_name == "Ignite" and random.random() < 0.5:
      burn = Burn(duration=3, damage_per_turn=5)
      target.add_status(burn)
      print(f"{target.name} catches fire!")
    return True

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
      print(f"{player.name} flees.The path teaches cowardice has a price: no exp gained!")
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
          enemy.attack(player)
    if not player.is_alive():
      break
  print("\n=== COMBAT ENDS ===")