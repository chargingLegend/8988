import random
from systems.status_effects import Burn, Scorched, Combusting, Frozen, Preserved


# --- Elementals declared at top level so summon_elemental and wild_conjure can reference them ---

class FireElemental:
  def __init__(self, tier=1):
    tiers = {
      1: {"hp": 20, "atk": 8, "defense": 2, "name": "Ember Sprite"},
      2: {"hp": 40, "atk": 14, "defense": 4, "name": "Flame Stalker"},
      3: {"hp": 70, "atk": 22, "defense": 6, "name": "Inferno Ascendant"},
    }
    data = tiers.get(tier, tiers[1])
    self.name = data["name"]
    self.hp = data["hp"]
    self.atk = data["atk"]
    self.defense = data["defense"]
    self.is_servant = True
    self.tier = tier
    self.element = "fire"

  def attack(self, target):
    dmg = random.randint(self.atk - 2, self.atk + 2)
    print(f"{self.name} erupts in flame against {target.name} for {dmg}!")
    target.hp -= dmg
    return dmg


class StoneElemental:
  def __init__(self, tier=1):
    tiers = {
      1: {"hp": 35, "atk": 5, "defense": 8, "name": "Gravel Hulk"},
      2: {"hp": 60, "atk": 9, "defense": 14, "name": "Boulder Warden"},
      3: {"hp": 90, "atk": 14, "defense": 20, "name": "Mountain Ascendant"},
    }
    data = tiers.get(tier, tiers[1])
    self.name = data["name"]
    self.hp = data["hp"]
    self.atk = data["atk"]
    self.defense = data["defense"]
    self.is_servant = True
    self.tier = tier
    self.element = "stone"

  def attack(self, target):
    dmg = random.randint(self.atk - 1, self.atk + 3)
    print(f"{self.name} slams into {target.name} with crushing force for {dmg}!")
    target.hp -= dmg
    return dmg


class StormElemental:
  def __init__(self, tier=1):
    tiers = {
      1: {"hp": 18, "atk": 10, "defense": 1, "name": "Static Wisp"},
      2: {"hp": 35, "atk": 18, "defense": 3, "name": "Gale Striker"},
      3: {"hp": 55, "atk": 28, "defense": 5, "name": "Tempest Ascendant"},
    }
    data = tiers.get(tier, tiers[1])
    self.name = data["name"]
    self.hp = data["hp"]
    self.atk = data["atk"]
    self.defense = data["defense"]
    self.is_servant = True
    self.tier = tier
    self.element = "storm"

  def attack(self, target):
    dmg = random.randint(self.atk - 3, self.atk + 5)
    print(f"{self.name} crackles through {target.name} for {dmg}!")
    target.hp -= dmg
    return dmg


# --- Pyromancy ---

def map_fire(self, targets):
  cost = 3
  self.check_manabda(cost)
  self.manabda -= cost
  dmg = random.randint(3, 6) + self.ability_upgrades.get("map_fire", 0)
  for t in targets:
    t.take_damage(dmg, "fire")
    if random.random() < 0.4:
      t.add_status(Burn(duration=2, damage_per_turn=2))
  return f"Fire spreads across {len(targets)} foes for {dmg} each! mana: {self.manabda}"


def reduce_ash(self, target):
  cost = 5
  self.check_manabda(cost)
  self.manabda -= cost
  threshold = 8 + self.ability_upgrades.get("reduce_ash", 0) * 2
  if target.hp <= threshold:
    target.hp = 0
    return f"{target.name} turns to ash! mana: {self.manabda}"
  dmg = target.hp // 2
  target.take_damage(dmg, "fire")
  return f"{target.name} loses half its essence! {dmg} dmg! mana: {self.manabda}"


def pyromancy_burn(self, target):
  if self.school != "Pyromancy":
    print("Only a Pyromancer can wield this heat.")
    return False
  if getattr(target, 'flame_resistance', None) is None:
    print(f"{target.name} cannot be burned. The flame finds nothing to take.")
    return False
  print(f"\nFire answers your call.")
  print(f"Your manabda: {self.manabda}/8")
  print(f"\nHow much heat do you pour into {target.name}?")
  print(f"Their resistance: {target.flame_resistance}")
  print("1. Kindle     (heat 10)  - costs 2 manabda")
  print("2. Sear       (heat 20)  - costs 4 manabda")
  print("3. Incinerate (heat 35)  - costs 6 manabda")
  if self.ability_upgrades.get("pyromancy_burn", 0) >= 1:
    print("4. Inferno    (heat 60)  - costs ALL manabda")
  choice = input("Choose [1-4]: ").strip()
  options = {
    "1": (10, 2),
    "2": (20, 4),
    "3": (35, 6),
  }
  if self.ability_upgrades.get("pyromancy_burn", 0) >= 1:
    options["4"] = (60, self.manabda)
  if choice not in options:
    print("The flame sputters out.")
    return False
  heat, cost = options[choice]
  if self.manabda < cost:
    print(f"The well runs dry. Need {cost} manabda, have {self.manabda}.")
    return False
  self.manabda -= cost
  if heat >= target.flame_resistance * 2:
    target.add_status(Combusting(duration=4, damage_per_turn=10))
    dmg = random.randint(15, 25)
    target.take_damage(dmg, "fire")
    return (f"{target.name} ignites completely!\n"
            f"{dmg} fire damage and fully Combusting!\n"
            f"manabda: {self.manabda}")
  elif heat >= target.flame_resistance:
    target.add_status(Scorched(duration=2, damage_per_turn=3))
    dmg = random.randint(8, 15)
    target.take_damage(dmg, "fire")
    return (f"{target.name} is Scorched!\n"
            f"{dmg} fire damage. The heat is building.\n"
            f"manabda: {self.manabda}")
  else:
    target.add_status(Burn(duration=3, damage_per_turn=5))
    dmg = random.randint(3, 8)
    target.take_damage(dmg, "fire")
    return (f"Flames lick at {target.name}.\n"
            f"{dmg} fire damage. Burning but not breaking.\n"
            f"manabda: {self.manabda}")


# --- Chronomancy ---

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
    print(f"The well runs dry. Need {cost} mana, have {self.mana}.")
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


# --- Cryomancy ---

def freeze(self, target):
  if self.school != "Cryomancy":
    print("Only a Cryomancer can freeze time.")
    return False
  cost = 4
  self.check_manabda(cost)
  self.manabda -= cost
  duration = 2 + self.ability_upgrades.get("freeze", 0)
  target.add_status(Frozen(duration=duration))
  return (f"Ice closes around {target.name}. It stops mid-motion.\n"
          f"Frozen for {duration} turns. mana: {self.mana}")


def cryo_preserve(self, target):
  if self.school != "Cryomancy":
    print("Only a Cryomancer can cryo preserve.")
    return False
  cost = 6
  self.check_manabda(cost)
  self.manabda -= cost
  target.add_status(Preserved(duration=2))
  target.preserved = True
  return (f"{target.name} is sealed in cryo-stasis. Its state is locked.\n"
          f"Healing and buffs suspended for 2 turns. mana: {self.mana}")


# --- Necromancy ---

def raise_dead(self, target, allies):
  if self.school != "Necromancy":
    print("Only a Necromancer can command the dead.")
    return False
  print(f"\nYou reach into the space between heartbeats.")
  print(f"Your manabda: {self.manabda}/8")
  if not hasattr(target, 'is_dead') or not target.is_dead:
    print("They still breathe. Death hasn't finished with them.")
    return False
  cost = 3
  if self.manabda < cost:
    print(f"The well runs dry. Need {cost} manabda, have {self.manabda}.")
    return False
  self.manabda -= cost
  target.is_dead = False
  target.hp = max(1, target.hp // 2)
  allies.append(target)
  print(f"{target.name} lurches back. Half of what they were. Yours now.")
  print(f"manabda: {self.manabda}")
  print("\n[ledger] raise is a real Python keyword — it throws exceptions.")
  print("  jargon: 'raise ValueError()' interrupts execution with an error.")
  print("  plain:  like pulling a fire alarm. everything stops and looks at it.")
  print("  here we name it raise_dead so Python doesn't panic.")
  return True


def decay(self, target):
  if self.school != "Necromancy":
    print("Only a Necromancer commands entropy.")
    return False
  print(f"\nSomething vital begins to leave {target.name}.")
  print(f"Your manabda: {self.manabda}/8")
  print("What do you strip away?")
  print("1. Defense  (del target.defense)  - costs 2 manabda")
  print("2. Attack   (del target.atk)      - costs 3 manabda")
  choice = input("Choose [1-2]: ").strip()
  options = {
    "1": ("defense", 2),
    "2": ("atk", 3),
  }
  if choice not in options:
    print("The moment passes. Entropy recoils.")
    return False
  attr, cost = options[choice]
  if self.manabda < cost:
    print(f"The well runs dry. Need {cost} manabda, have {self.manabda}.")
    return False
  if not hasattr(target, attr):
    print(f"{target.name} has no {attr} left to rot.")
    return False
  self.manabda -= cost
  old_val = getattr(target, attr)
  delattr(target, attr)
  print(f"{target.name}'s {attr} crumbles. It had {old_val}. Now it has nothing.")
  print(f"manabda: {self.manabda}")
  print(f"\n[ledger] del removes an attribute from an object entirely.")
  print(f"  jargon: 'del object.attribute' unbinds the name from memory.")
  print(f"  plain:  like ripping a page out of a book. it's just gone.")
  return True


def animate(self, corpse_template, monster_class):
  if self.school != "Necromancy":
    print("Only a Necromancer breathes false life.")
    return False
  print(f"\nYou study what remains of {corpse_template['name']}.")
  print(f"Your manabda: {self.manabda}/8")
  level = corpse_template.get("level", 1)
  cost = level * 2
  print(f"Level {level} creature. Costs {cost} manabda to animate.")
  if self.manabda < cost:
    print(f"The well runs dry. Need {cost} manabda, have {self.manabda}.")
    return False
  self.manabda -= cost
  servant = monster_class()
  servant.hp = max(1, servant.hp // 2)
  servant.is_servant = True
  print(f"{servant.name} rises. Diminished. Obedient.")
  print(f"manabda: {self.manabda}")
  print(f"\n[ledger] __init__ is what Python calls when you instantiate a class.")
  print(f"  jargon: 'monster_class()' calls __init__ and returns a live object.")
  print(f"  plain:  like filling out a form to summon something into existence.")
  return servant


# --- Enhancement ---

def amplify(self, target):
  if self.school != "Enhancement":
    print("Only an Enhancer can push past the limit.")
    return False
  print(f"\nYou reach into your reserves. Focus narrows to a point.")
  print(f"Your manabda: {self.manabda}/8")
  print("How much do you pour in? Each manabda spent multiplies the next strike.")
  try:
    spent = int(input(f"Choose [1-{self.manabda}]: ").strip())
  except ValueError:
    print("The focus shatters. Nothing lands.")
    return False
  if spent < 1 or spent > self.manabda:
    print("That's not a number the universe respects.")
    return False
  peak_name = max(self.spell_data, key=lambda s: self.spell_data[s][1])
  peak_damage = self.spell_data[peak_name][1]
  self.manabda -= spent
  self.amplify_multiplier = spent
  print(f"\n{peak_name} locked at its ceiling. {peak_damage} base.")
  print(f"Next strike hits at x{spent}. The air around you tightens.")
  print(f"manabda: {self.manabda}")
  print(f"\n[ledger] max() finds the highest value in an iterable.")
  print(f"  jargon: 'max(dict, key=lambda x: dict[x][1])' scans by a specific field.")
  print(f"  plain:  like flipping through cards to find the one with the biggest number.")
  return True


def _apply_amplify(self, damage):
  if hasattr(self, 'amplify_multiplier'):
    damage *= self.amplify_multiplier
    del self.amplify_multiplier
  return damage


def temper(self, target):
  if self.school != "Enhancement":
    print("Only an Enhancer can smooth raw chaos.")
    return False
  print(f"\nYou study {target.name}. Something about it is uneven.")
  print(f"Your manabda: {self.manabda}/8")
  cost = 1
  if self.manabda < cost:
    print(f"The well runs dry. Need {cost} manabda, have {self.manabda}.")
    return False
  print("What do you temper?")
  options = {}
  index = 1
  for attr in ["hp", "atk", "defense", "durability"]:
    if hasattr(target, attr):
      val = getattr(target, attr)
      rounded = round(val, -1)
      print(f"{index}. {attr}: {val} → {rounded}  - costs {cost} manabda")
      options[str(index)] = (attr, val, rounded)
      index += 1
  if not options:
    print(f"{target.name} has nothing left worth smoothing.")
    return False
  choice = input(f"Choose [1-{index - 1}]: ").strip()
  if choice not in options:
    print("The moment passes.")
    return False
  attr, old_val, new_val = options[choice]
  self.manabda -= cost
  setattr(target, attr, new_val)
  print(f"\n{target.name}'s {attr} evens out. {old_val} becomes {new_val}.")
  print(f"manabda: {self.manabda}")
  print(f"\n[ledger] round() smooths a number to a given precision.")
  print(f"  jargon: 'round(val, -1)' rounds to the nearest 10.")
  print(f"  plain:  like sanding a rough edge until it sits flush.")
  return True


def surge(self, targets, buff_attr="atk", buff_amount=3):
  if self.school != "Enhancement":
    print("Only an Enhancer can push many at once.")
    return False
  print(f"\nYou extend your will outward. Everything in reach feels it.")
  print(f"Your manabda: {self.manabda}/8")
  cost = 2
  if self.manabda < cost:
    print(f"The well runs dry. Need {cost} manabda, have {self.manabda}.")
    return False
  if not targets:
    print("There is nothing here to surge.")
    return False
  self.manabda -= cost
  def apply_buff(t):
    if hasattr(t, buff_attr):
      setattr(t, buff_attr, getattr(t, buff_attr) + buff_amount)
    return t
  buffed = list(map(apply_buff, targets))
  names = [t.name for t in buffed if hasattr(t, "name")]
  print(f"\nThe surge moves through: {', '.join(names)}.")
  print(f"Each gains +{buff_amount} {buff_attr}.")
  print(f"manabda: {self.manabda}")
  print(f"\n[ledger] map() applies one function across every item in a list.")
  print(f"  jargon: 'map(func, iterable)' returns a map object — wrap in list() to see it.")
  print(f"  plain:  like stamping every envelope in a pile with the same stamp.")
  return buffed


# --- Illusion ---

def veil(self, target):
  if self.school != "Illusion":
    print("Only an Illusionist can unmake presence.")
    return False
  print(f"\nYou gather shadow around {target.name}.")
  print(f"Your manabda: {self.manabda}/8")
  print("How deep do you bury them?")
  print("1. A breath       (2 turns/choices)  - costs 2 manabda")
  print("2. A heartbeat    (4 turns/choices)  - costs 4 manabda")
  print("3. A long shadow  (6 turns/choices)  - costs 6 manabda")
  options = {
    "1": (2, 2),
    "2": (4, 4),
    "3": (6, 6),
  }
  choice = input("Choose [1-3]: ").strip()
  if choice not in options:
    print("The illusion collapses before it forms.")
    return False
  duration, cost = options[choice]
  if self.manabda < cost:
    print(f"The well runs dry. Need {cost} manabda, have {self.manabda}.")
    return False
  self.manabda -= cost
  target.veil_duration = duration
  target.is_veiled = True
  print(f"\n{target.name} slips from sight. {duration} turns or choices remain.")
  print(f"manabda: {self.manabda}")
  print(f"\n[ledger] filter() removes items from a list that don't pass a condition.")
  print(f"  jargon: 'list(filter(lambda x: x.is_veiled, targets))' hides veiled targets.")
  print(f"  plain:  like a bouncer with a list. if your name isn't on it, you don't exist.")
  return True


def _tick_veil(self, target):
  if hasattr(target, 'veil_duration') and target.is_veiled:
    target.veil_duration -= 1
    if target.veil_duration <= 0:
      target.is_veiled = False
      del target.veil_duration
      print(f"\n{target.name} surfaces back into sight. The illusion spent.")


def mimic(self, target):
  if self.school != "Illusion":
    print("Only an Illusionist can forge a reflection.")
    return False
  print(f"\nYou study {target.name}. Every flaw. Every edge.")
  print(f"Your manabda: {self.manabda}/8")
  print("How convincing do you make it?")
  print("1. Surface copy   (name only)            - costs 1 manabda")
  print("2. Shallow copy   (name, hp, atk)        - costs 3 manabda")
  print("3. Deep copy      (all attributes)       - costs 5 manabda")
  options = {
    "1": (["name"], 1),
    "2": (["name", "hp", "atk"], 3),
    "3": (["name", "hp", "atk", "defense", "level", "abilities"], 5),
  }
  choice = input("Choose [1-3]: ").strip()
  if choice not in options:
    print("The image wavers. Nothing holds.")
    return False
  attrs, cost = options[choice]
  if self.manabda < cost:
    print(f"The well runs dry. Need {cost} manabda, have {self.manabda}.")
    return False
  self.manabda -= cost
  decoy = {}
  for attr in attrs:
    if hasattr(target, attr):
      decoy[attr] = getattr(target, attr)
  decoy["is_decoy"] = True
  print(f"\nA copy of {target.name} steps forward. {len(attrs)} attributes mirrored.")
  print(f"Enemies won't know which is real.")
  print(f"manabda: {self.manabda}")
  print(f"\n[ledger] copy() duplicates an object without linking it to the original.")
  print(f"  jargon: 'dict.copy()' makes a shallow copy — nested objects still shared.")
  print(f"  plain:  like photocopying a page. looks the same. bleeds differently.")
  return decoy


def shatter(self, target):
  if self.school != "Illusion":
    print("Only an Illusionist can make something doubt its own existence.")
    return False
  print(f"\nYou turn {target.name}'s mind against itself.")
  print(f"Your manabda: {self.manabda}/8")
  print("How hard do you press the lie?")
  print("1. A whisper   (target skips next action)          - costs 2 manabda")
  print("2. A scream    (damage + skips next action)        - costs 4 manabda")
  print("3. Collapse    (heavy damage + 2 turn debuff)      - costs 6 manabda")
  options = {
    "1": (0, 1, 2),
    "2": (15, 1, 4),
    "3": (30, 2, 6),
  }
  choice = input("Choose [1-3]: ").strip()
  if choice not in options:
    print("The illusion finds no purchase. Their mind holds.")
    return False
  damage, skip_turns, cost = options[choice]
  if self.manabda < cost:
    print(f"The well runs dry. Need {cost} manabda, have {self.manabda}.")
    return False
  self.manabda -= cost
  if hasattr(target, 'hp') and damage > 0:
    target.hp -= damage
  target.skip_turns = skip_turns
  target.is_shattered = True
  print(f"\n{target.name} evaluates as False. It believes it has already lost.")
  if damage > 0:
    print(f"  {damage} psychic damage lands.")
  print(f"  {skip_turns} turn(s) lost to the collapse.")
  print(f"manabda: {self.manabda}")
  print(f"\n[ledger] bool() evaluates whether something is True or False in Python.")
  print(f"  jargon: 'bool(x)' returns False for 0, None, [], {{}}, empty strings.")
  print(f"  plain:  Python is always asking 'does this exist and does it matter.'")
  print(f"  QA note: truthiness bugs are some of the most common test failures.")
  return True


# --- Conjuration ---

def summon_elemental(self):
  if self.school != "Conjuration":
    print("Only a Conjurer can tear open the veil.")
    return False
  print(f"\nYou reach past the world's edge. Something stirs.")
  print(f"Your manabda: {self.manabda}/8")
  print("What do you call?")
  print("1. Fire Elemental  - volatile, high atk, low defense")
  print("2. Stone Elemental - slow, low atk, high defense")
  print("3. Storm Elemental - fragile, highest atk, almost no defense")
  element_choice = input("Choose [1-3]: ").strip()
  element_map = {
    "1": FireElemental,
    "2": StoneElemental,
    "3": StormElemental,
  }
  if element_choice not in element_map:
    print("The veil snaps shut. Nothing answers.")
    return False
  print("\nHow much do you pour into the call?")
  print("1. A whisper  (tier 1 elemental)  - costs 2 manabda")
  print("2. A shout    (tier 2 elemental)  - costs 4 manabda")
  print("3. A scream   (tier 3 elemental)  - costs 7 manabda")
  tier_map = {
    "1": (1, 2),
    "2": (2, 4),
    "3": (3, 7),
  }
  tier_choice = input("Choose [1-3]: ").strip()
  if tier_choice not in tier_map:
    print("The signal muddles. The veil closes.")
    return False
  tier, cost = tier_map[tier_choice]
  if self.manabda < cost:
    print(f"The well runs dry. Need {cost} manabda, have {self.manabda}.")
    return False
  self.manabda -= cost
  elemental_class = element_map[element_choice]
  servant = elemental_class(tier=tier)
  print(f"\n{servant.name} tears through. Yours. For now.")
  print(f"HP: {servant.hp} | ATK: {servant.atk} | DEF: {servant.defense}")
  print(f"manabda: {self.manabda}")
  print(f"\n[ledger] __init__ is called every time you instantiate a class.")
  print(f"  jargon: 'FireElemental(tier=2)' calls __init__ with tier=2 as an argument.")
  print(f"  plain:  like filling out a form with different answers each time.")
  return servant


def conjure_supply(self):
  if self.school != "Conjuration":
    print("Only a Conjurer can pull matter from nothing.")
    return False
  print(f"\nYou feel the weight of what you need. The void listens.")
  print(f"Your manabda: {self.manabda}/8")
  print("What do you conjure?")
  print("1. HP Potion")
  print("2. Manabda Potion")
  print("3. Mana Potion")
  supply_choice = input("Choose [1-3]: ").strip()
  supply_map = {
    "1": {
      "name": "HP Potion",
      "tiers": {
        "1": {"restore": 15, "label": "Vial", "cost": 1},
        "2": {"restore": 35, "label": "Flask", "cost": 3},
        "3": {"restore": 60, "label": "Draught", "cost": 5},
      },
      "attr": "hp",
    },
    "2": {
      "name": "Manabda Potion",
      "tiers": {
        "1": {"restore": 2, "label": "Vial", "cost": 2},
        "2": {"restore": 4, "label": "Flask", "cost": 4},
        "3": {"restore": 6, "label": "Draught", "cost": 6},
      },
      "attr": "manabda",
    },
    "3": {
      "name": "Mana Potion",
      "tiers": {
        "1": {"restore": 10, "label": "Vial", "cost": 1},
        "2": {"restore": 25, "label": "Flask", "cost": 3},
        "3": {"restore": 45, "label": "Draught", "cost": 5},
      },
      "attr": "mana",
    },
  }
  if supply_choice not in supply_map:
    print("The void finds no shape for that. Nothing forms.")
    return False
  supply = supply_map[supply_choice]
  print(f"\nHow much substance do you pull through?")
  for k, v in supply["tiers"].items():
    print(f"{k}. {supply['name']} {v['label']}  (+{v['restore']} {supply['attr']})  - costs {v['cost']} manabda")
  tier_choice = input("Choose [1-3]: ").strip()
  if tier_choice not in supply["tiers"]:
    print("The shape collapses. Nothing holds.")
    return False
  tier = supply["tiers"][tier_choice]
  if self.manabda < tier["cost"]:
    print(f"The well runs dry. Need {tier['cost']} manabda, have {self.manabda}.")
    return False
  self.manabda -= tier["cost"]
  attr = supply["attr"]
  if hasattr(self, attr):
    setattr(self, attr, getattr(self, attr) + tier["restore"])
  print(f"\nA {supply['name']} {tier['label']} solidifies in your hand.")
  print(f"+{tier['restore']} {attr} restored. {attr}: {getattr(self, attr)}")
  print(f"manabda: {self.manabda}")
  print(f"\n[ledger] dict key-value lookup retrieves exactly what you ask for.")
  print(f"  jargon: 'supply_map[choice][\"tiers\"][tier]' chains key access.")
  print(f"  plain:  like a vending machine. punch in the right code, get the right thing.")
  return {attr: tier["restore"]}


def wild_conjure(self, active_combat=False):
  if self.school != "Conjuration":
    print("Only a Conjurer gambles with the veil.")
    return False
  print(f"\nYou tear the veil without a map. Anything could answer.")
  print(f"Your manabda: {self.manabda}/8")
  print("How much do you risk?")
  print("1. A crack   (40% ally / 60% enemy)  - costs 1 manabda")
  print("2. A tear    (55% ally / 45% enemy)  - costs 2 manabda")
  print("3. A rip     (70% ally / 30% enemy)  - costs 3 manabda")
  odds_map = {
    "1": (0.40, 1),
    "2": (0.55, 2),
    "3": (0.70, 3),
  }
  choice = input("Choose [1-3]: ").strip()
  if choice not in odds_map:
    print("The veil ignores the hesitation. It closes.")
    return False
  ally_chance, cost = odds_map[choice]
  if self.manabda < cost:
    print(f"The well runs dry. Need {cost} manabda, have {self.manabda}.")
    return False
  self.manabda -= cost
  elementals = [FireElemental, StoneElemental, StormElemental]
  chosen_class = random.choice(elementals)
  summoned = chosen_class(tier=1)
  roll = random.random()
  if roll <= ally_chance:
    summoned.is_servant = True
    print(f"\n{summoned.name} tears through. It looks at you. Then at your enemies.")
    print(f"It has chosen. HP: {summoned.hp} | ATK: {summoned.atk}")
    print(f"manabda: {self.manabda}")
    print(f"\n[ledger] random.choice() picks one item from a list at random.")
    print(f"  jargon: 'random.choice([FireElemental, StoneElemental, StormElemental])'")
    print(f"  plain:  like reaching into a bag blindfolded. could be anything.")
    return {"servant": summoned}
  else:
    summoned.is_servant = False
    print(f"\n{summoned.name} tears through. It looks at you.")
    print(f"Then only at you.")
    print(f"The veil has a sense of humor.")
    print(f"manabda: {self.manabda}")
    if active_combat:
      print(f"\n{summoned.name} joins the fight — against you.")
    print(f"\n[ledger] random.choice() picks one item from a list at random.")
    print(f"  jargon: 'random.choice([FireElemental, StoneElemental, StormElemental])'")
    print(f"  plain:  like reaching into a bag blindfolded. could be anything.")
    return {"enemy": summoned}


# --- Shadow ---

def shroud(self, target):
  if self.school != "Shadow":
    print("Only a Shadow mage finds the crack in the light.")
    return False
  print(f"\nYou let the dark do the looking.")
  print(f"Your manabda: {self.manabda}/8")
  print("How deep do you probe?")
  print("1. Surface scan  (finds 1 vulnerability, light backstab)   - costs 2 manabda")
  print("2. Deep scan     (finds best vulnerability, hard backstab)  - costs 4 manabda")
  print("3. Total eclipse (all vulnerabilities exposed, full strike) - costs 6 manabda")
  options = {
    "1": (1, 10, 2),
    "2": (2, 22, 4),
    "3": (3, 38, 6),
  }
  choice = input("Choose [1-3]: ").strip()
  if choice not in options:
    print("The dark finds nothing. Light holds.")
    return False
  depth, backstab_dmg, cost = options[choice]
  if self.manabda < cost:
    print(f"The well runs dry. Need {cost} manabda, have {self.manabda}.")
    return False
  self.manabda -= cost
  vulnerabilities = []
  for attr in ["defense", "atk", "hp"]:
    if hasattr(target, attr):
      val = getattr(target, attr)
      if any([val < 5, val < 10 and attr == "defense", val < 20 and attr == "hp"]):
        vulnerabilities.append((attr, val))
  if not vulnerabilities:
    vulnerabilities.append(("resolve", 0))
  found = vulnerabilities[:depth]
  target.hp -= backstab_dmg
  print(f"\nThe dark returns with answers.")
  for attr, val in found:
    print(f"  {target.name}'s {attr} is exposed. ({val})")
  print(f"Shadow strikes the crack. {backstab_dmg} damage lands.")
  print(f"manabda: {self.manabda}")
  print(f"\n[ledger] any() returns True if at least one item in an iterable is True.")
  print(f"  jargon: 'any([val < 5, val < 10])' checks multiple conditions at once.")
  print(f"  plain:  like asking 'is anyone home' — one answer is enough.")
  return found


def _apply_siphon(self, damage):
  if hasattr(self, 'siphon_bonus'):
    damage += self.siphon_bonus
    del self.siphon_bonus
  return damage


def siphon(self, target):
  if self.school != "Shadow":
    print("Only a Shadow mage can drink another's strength.")
    return False
  print(f"\nYou reach into {target.name} and pull.")
  print(f"Your manabda: {self.manabda}/8")
  print("What do you drain?")
  print("1. Drain defense  (weaken armor, bonus to next hit)   - costs 2 manabda")
  print("2. Drain atk      (weaken strikes, bonus to next hit) - costs 3 manabda")
  print("3. Drain both     (status effect + heavy next hit)    - costs 5 manabda")
  options = {
    "1": (["defense"], 2),
    "2": (["atk"], 3),
    "3": (["defense", "atk"], 5),
  }
  choice = input("Choose [1-3]: ").strip()
  if choice not in options:
    print("The connection breaks. Nothing flows.")
    return False
  attrs, cost = options[choice]
  if self.manabda < cost:
    print(f"The well runs dry. Need {cost} manabda, have {self.manabda}.")
    return False
  self.manabda -= cost
  total_drained = 0
  for attr in attrs:
    if hasattr(target, attr):
      val = getattr(target, attr)
      drain = max(1, val // 3)
      setattr(target, attr, max(0, val - drain))
      total_drained += drain
      print(f"  {target.name}'s {attr} drops by {drain}. ({val} → {val - drain})")
  target.is_weakened = True
  target.weakened_turns = len(attrs) + 1
  self.siphon_bonus = total_drained
  print(f"\n{target.name} staggers. Diminished.")
  print(f"Status: weakened for {target.weakened_turns} turns.")
  print(f"Your next strike carries +{total_drained} stolen force.")
  print(f"manabda: {self.manabda}")
  print(f"\n[ledger] zip() pairs two iterables together element by element.")
  print(f"  jargon: 'zip(my_stats, target_stats)' links them into matched pairs.")
  print(f"  plain:  like matching socks. one from each pile, paired by position.")
  return total_drained


def eclipse(self, targets):
  if self.school != "Shadow":
    print("Only a Shadow mage calls down the dark on many.")
    return False
  print(f"\nYou let shadow choose the order of things.")
  print(f"Your manabda: {self.manabda}/8")
  print("How wide do you cast it?")
  print("1. Dim           (hit weakest target)         - costs 2 manabda")
  print("2. Darken        (hit 2 weakest targets)      - costs 4 manabda")
  print("3. Total Eclipse (hit all, weakest hit hard)  - costs 6 manabda")
  options = {
    "1": (1, 2),
    "2": (2, 4),
    "3": (len(targets), 6),
  }
  choice = input("Choose [1-3]: ").strip()
  if choice not in options:
    print("The shadow finds no shape. It retreats.")
    return False
  hits, cost = options[choice]
  if self.manabda < cost:
    print(f"The well runs dry. Need {cost} manabda, have {self.manabda}.")
    return False
  if not targets:
    print("There is nothing here for the dark to find.")
    return False
  self.manabda -= cost
  sorted_targets = sorted(targets, key=lambda t: t.hp)
  hit_targets = sorted_targets[:hits]
  print(f"\nShadow sorts the weak from the strong.")
  results = []
  for i, t in enumerate(hit_targets):
    dmg = max(8, 30 - (i * 6))
    t.hp -= dmg
    print(f"  {t.name} ({t.hp + dmg} hp) takes {dmg} shadow damage. ({t.hp} remaining)")
    results.append((t.name, dmg))
  print(f"manabda: {self.manabda}")
  print(f"\n[ledger] sorted() returns a new list ordered by a key you define.")
  print(f"  jargon: 'sorted(targets, key=lambda t: t.hp)' orders by hp low to high.")
  print(f"  plain:  like lining people up shortest to tallest. original list unchanged.")
  return results


# --- Transmutation ---

def transmute_vitae(self, target_item: str):
  if self.school != "Transmutation":
    print("Only a Transmutator can rewrite matter.")
    return False
  upgrade_map = {
    "hp_potion": ("hp_potion_ii", 15, 2),
    "hp_potion_ii": ("hp_potion_iii", 30, 4),
    "hp_potion_iii": ("hp_potion_iv", 50, 6),
  }
  if target_item not in upgrade_map:
    print(f"{target_item} resists the change. Matter holds its shape.")
    return False
  if target_item not in self.inventory.items:
    print(f"You reach for it. Your satchel is empty of {target_item}.")
    return False
  result, heal_value, cost = upgrade_map[target_item]
  if self.manabda < cost:
    print(f"The well runs dry. Need {cost} manabda, have {self.manabda}.")
    return False
  self.manabda -= cost
  self.inventory.remove(target_item)
  self.inventory.add(result)
  print(f"\nThe {target_item} shudders. Its shape rewrites itself.")
  print(f"It becomes something greater. +{heal_value} healing when used.")
  print(f"manabda: {self.manabda}")
  print(f"\n[ledger] dict lookup maps one value to another in constant time.")
  print(f"  jargon: 'upgrade_map[key]' retrieves the paired value directly.")
  print(f"  plain:  like a translation table. put the old word in, get the new one out.")
  return result


def transmute_arcana(self, target_item: str):
  if self.school != "Transmutation":
    print("Only a Transmutator can rewrite matter.")
    return False
  upgrade_map = {
    "mana_potion": ("mana_potion_ii", 10, 2),
    "mana_potion_ii": ("mana_potion_iii", 25, 4),
    "mana_potion_iii": ("mana_potion_iv", 45, 6),
  }
  if target_item not in upgrade_map:
    print(f"{target_item} resists the change. Its essence won't bend.")
    return False
  if target_item not in self.inventory.items:
    print(f"You reach for it. Your satchel is empty of {target_item}.")
    return False
  result, mana_value, cost = upgrade_map[target_item]
  if self.manabda < cost:
    print(f"The well runs dry. Need {cost} manabda, have {self.manabda}.")
    return False
  self.manabda -= cost
  self.inventory.remove(target_item)
  self.inventory.add(result)
  print(f"\nThe {target_item} hums. Something inside it expands.")
  print(f"It rewrites itself into something deeper. +{mana_value} mana when used.")
  print(f"manabda: {self.manabda}")
  print(f"\n[ledger] dict.get() retrieves a value safely without raising a KeyError.")
  print(f"  jargon: 'upgrade_map.get(key, default)' returns default if key is missing.")
  print(f"  plain:  like asking 'is this on the menu?' before ordering. no surprises.")
  return result
