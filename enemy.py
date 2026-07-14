import random

class Monster:
  def __init__(self, name="Unknown", hp=10, desc="A creature.", exp_value=0,
               atk=1, defense=0, level=1, gold_reward=0, loot_table=None,
               abilities=None, age=None, flame_resistance=None):
    self.name = name
    self.hp = hp
    self.max_hp = hp
    self.desc = desc
    self.status_effects = []
    self.exp_value = exp_value
    self.atk = atk
    self.defense = defense
    self.level = level
    self.gold_reward = gold_reward
    self.loot_table = loot_table or []
    self.abilities = abilities or []
    self.age = age
    self.flame_resistance = flame_resistance

  def __repr__(self):
    return f"{self.name}(HP:{self.hp}/{self.max_hp}, LVL:{self.level}, ATK:{self.atk})"

  def __str__(self):
    return f"{self.name} - {self.desc} [HP: {self.hp}/{self.max_hp}]"

  def is_alive(self):
    return self.hp > 0

  def take_damage(self, dmg, dmg_type="physical"):
    actual_dmg = max(1, dmg - self.defense)
    self.hp -= actual_dmg
    if self.hp < 0:
      self.hp = 0
    print(f"{self.name} takes {actual_dmg} {dmg_type} damage! HP: {self.hp}/{self.max_hp}")
    if not self.is_alive():
      print(f"{self.name} falls.")
    return actual_dmg

  def heal(self, amount):
    self.hp = min(self.max_hp, self.hp + amount)
    print(f"{self.name} heals for {amount}! HP: {self.hp}/{self.max_hp}")

  def attack(self, target):
    base_dmg = random.randint(max(1, self.atk - 1), self.atk + 1)
    print(f"{self.name} attacks {target.name} for {base_dmg}!")
    target.take_damage(base_dmg, "physical")
    return base_dmg

  def add_status(self, status_effect):
    self.status_effects.append(status_effect)
    print(f"{self.name} is afflicted with {status_effect.name}!")

  def remove_status(self, status_name):
    self.status_effects = [s for s in self.status_effects if s.name != status_name]

  def tick_status_effects(self):
    messages = []
    for effect in self.status_effects[:]:
      result = effect.tick(self)
      if result:
        messages.append(result)
      if effect.is_expired():
        messages.append(f"{self.name} recovers from {effect.name}.")
        self.status_effects.remove(effect)
    return "\n".join(messages)

  def drop_loot(self):
    drops = []
    for item, chance in self.loot_table:
      if random.randint(1, 100) <= chance:
        drops.append(item)
    return drops

  def on_spawn(self):
    return f"A wild {self.name} appears!"


class Rat(Monster):
  def __init__(self):
    super().__init__(name="Rat", hp=5, desc="A diseased sewer dweller.",
                     exp_value=3, level=1, atk=2, defense=0, gold_reward=1,
                     loot_table=[("Rat Tail", 70), ("Moldy Cheese", 10)],
                     abilities=["Disease"])

  def attack(self, target):
    dmg = random.randint(1, 3)
    print(f"{self.name} gnaws at {target.name}'s ankles for {dmg}!")
    target.take_damage(dmg, "physical")
    return dmg

class Bat(Monster):
  def __init__(self):
    super().__init__(name="Bat", hp=8, desc="A leathery creature with sharp shrieks.",
                     exp_value=5, level=1, atk=3, defense=0, gold_reward=2,
                     loot_table=[("Bat Wing", 40), ("Guano", 20)],
                     abilities=["Screech"])

  def attack(self, target):
    dmg = random.randint(2, 4)
    print(f"{self.name} dives and claws {target.name} for {dmg}!")
    target.take_damage(dmg, "physical")
    return dmg

class Goblin(Monster):
  def __init__(self):
    super().__init__(name="Goblin", hp=12, desc="A small, green-skinned scavenger.",
                     exp_value=8, level=2, atk=4, defense=1, gold_reward=3,
                     loot_table=[("Rusty Dagger", 30), ("Goblin Ear", 50)],
                     abilities=["Stab", "Loot Throw"],age = 20)
    self.stab_chance = 40
    self.stab_dmg = (2, 6)

  def attack(self, target):
    if random.randint(1, 100) <= self.stab_chance:
      dmg = random.randint(*self.stab_dmg)
      print(f"{self.name} uses STAB! Plunges dagger into {target.name} for {dmg}!")
      target.take_damage(dmg, "piercing")
      return dmg
    else:
      dmg = random.randint(3, 5)
      print(f"{self.name} stabs wildly at {target.name} for {dmg}!")
      target.take_damage(dmg, "piercing")
      return dmg

class RavenSwarm(Monster):
  def __init__(self):
    super().__init__(name="Raven Swarm", hp=15,
                     desc="Not birds. Too many eyes. Too much hunger.",
                     exp_value=50, level=2, atk=4, defense=0, gold_reward=25,
                     loot_table=[("Black Feather", 60), ("Crow's Eye", 10)],
                     abilities=["Swarm", "Peck Barrage"])
    self.attack_dmg = (3, 10)
    self.dmg_type = "piercing"
    self.hits = 3

  def attack(self, target):
    total_dmg = 0
    print(f"{self.name} descends on {target.name}!")
    for i in range(self.hits):
      dmg = random.randint(*self.attack_dmg)
      total_dmg += dmg
      print(f"  Beak {i+1} tears for {dmg}!")
      target.take_damage(dmg, self.dmg_type)
    return total_dmg

class Wolf(Monster):
  def __init__(self):
    super().__init__(name="Wolf", hp=18, desc="A pack hunter with gleaming fangs.",
                     exp_value=12, level=3, atk=6, defense=1, gold_reward=4,
                     loot_table=[("Wolf Pelt", 50), ("Fang", 30)],
                     abilities=["Howl"])

  def attack(self, target):
    dmg = random.randint(5, 7)
    print(f"{self.name} lunges and bites {target.name} for {dmg}!")
    target.take_damage(dmg, "piercing")
    return dmg

class Skeleton(Monster):
  def __init__(self):
    super().__init__(name="Skeleton", hp=15, desc="Animated bones that never rest.",
                     exp_value=15, level=4, atk=7, defense=2, gold_reward=6,
                     loot_table=[("Bone Shard", 60), ("Ancient Coin", 15)],
                     abilities=["Rattle"])

  def attack(self, target):
    dmg = random.randint(6, 8)
    print(f"{self.name} swings a rusted blade at {target.name} for {dmg}!")
    target.take_damage(dmg, "slashing")
    return dmg

class Spider(Monster):
  def __init__(self):
    super().__init__(name="Giant Spider", hp=22, desc="Venomous and patient.",
                     exp_value=18, level=5, atk=8, defense=1, gold_reward=7,
                     loot_table=[("Spider Silk", 45), ("Venom Gland", 20)],
                     abilities=["Web"])

  def attack(self, target):
    dmg = random.randint(7, 9)
    print(f"{self.name} sinks fangs into {target.name} for {dmg}!")
    target.take_damage(dmg, "poison")
    return dmg

class CaveTroll(Monster):
  def __init__(self):
    super().__init__(name="Cave Troll", hp=40,
                     desc="A massive brute with regenerative flesh.",
                     exp_value=35, level=8, atk=12, defense=3, gold_reward=15,
                     loot_table=[("Troll Hide", 40), ("Troll Blood", 15)],
                     abilities=["Regenerate"], age = 45)

  def attack(self, target):
    dmg = random.randint(10, 14)
    print(f"{self.name} smashes {target.name} with a club for {dmg}!")
    target.take_damage(dmg, "bludgeoning")
    return dmg

class Wraith(Monster):
  def __init__(self):
    super().__init__(name="Wraith", hp=35, desc="A cold specter that drains life.",
                     exp_value=40, level=10, atk=14, defense=4, gold_reward=20,
                     loot_table=[("Ectoplasm", 30), ("Grave Dust", 50)],
                     abilities=["Phase"])

  def attack(self, target):
    dmg = random.randint(12, 16)
    print(f"{self.name} reaches through {target.name}, chilling them for {dmg}!")
    target.take_damage(dmg, "necrotic")
    return dmg

class TrollKing(Monster):
  def __init__(self):
    super().__init__(name="Troll King", hp=100,
                     desc="The ruler of the deep caves. Ancient and furious.",
                     exp_value=150, level=15, atk=20, defense=6, gold_reward=75,
                     loot_table=[("King's Crown", 10), ("Troll Heart", 25), ("Ancient Bone", 40)],
                     abilities=["Roar", "Regenerate"], age = 55)

  def attack(self, target):
    dmg = random.randint(18, 22)
    print(f"{self.name} brings down a massive fist on {target.name} for {dmg}!")
    target.take_damage(dmg, "bludgeoning")
    return dmg


class Humanoid(Monster):
  def __init__(self, name="Villager", hp=20, desc="A person.", exp_value=10, atk=1, defense=0, level=1, gold_reward=0,
               loot_table=None, abilities=None, age=None, flame_resistance=None,
               mana=10, max_mana=10, manabda=5):
    super().__init__(name, hp, desc, exp_value, atk, defense, level, gold_reward, loot_table, abilities, age,
                     flame_resistance)
    self.mana = mana
    self.max_mana = max_mana
    self.manabda = manabda
    self.faction = "Unaffiliated"
    self.can_talk = True
    self.spells = []
    self.true_name = None

  def speak(self, dialogue: str):
    return f"{self.name}: '{dialogue}'"

  def reveal_name(self):
    if self.true_name and self.name != self.true_name:
      old_name = self.name
      self.name = self.true_name
      return f"{old_name} reveals his name: {self.true_name}."
    return None


class DesperateTraveler(Humanoid):
  def __init__(self):
    super().__init__(
      name="Desperate Traveler",
      hp=45,
      desc="A wary man with blonde hair hanging over his eyes. "
           "Something about him suggests he was more than this once. "
           "Or wanted to be.",
      exp_value=35,
      atk=4,
      defense=2,
      level=2,
      gold_reward=8,
      loot_table=[("Tattered Cloak", 60), ("Rusted Dagger", 40)],
      abilities=["Dim", "Mutter", "Veil"]
    )
    self.true_name = "Caleb"
    self.school = "Shadow"
    self.mana = 15
    self.max_mana = 15
    self.manabda = 6
    self.faction = "Travelers"
    self.spells = ["Dim", "Mutter", "Veil"]
    self.spell_cooldowns = {}
    self.spell_data = {
      "Dim": {
        "min_dmg": 1, "max_dmg": 3, "dmg_type": "shadow",
        "desc": "light flees {target}. It blinks, confused.",
        "effect": "Disoriented", "effect_chance": 0.75,
        "cooldown_key": "dim", "cooldown_turns": 3
      },
      "Mutter": {
        "min_dmg": 1, "max_dmg": 5, "dmg_type": "shadow",
        "desc": "dark words find the cracks in {target}'s resolve.",
        "effect": "Weakened", "effect_chance": 0.4
      },
      "Veil": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "shadow",
        "desc": "he steps sideways out of your sight. For a moment.",
        "effect": None
      }
    }
    self.fled = False

  def attack(self, target):
    from systems.status_effects import Disoriented
    roll = random.randint(1, 100)


    target_low_hp = target.hp <= target.max_hp * 0.25
    target_leveled = hasattr(target, 'level') and target.level >= 2
    if target_low_hp and target_leveled and self.mana >= 4:
      self.mana -= 4
      dmg = random.randint(6, 11) + self.atk
      print(f"\nHe sees it in your eyes.")
      print(f"The moment where something tips.")
      print(f"He doesn't hesitate.")
      print(f"Shadow folds around his blade. Both hands. Everything he has.")
      print(f"'Veil.' Whispered. Final.")
      print(f"The darkness hits like it has weight. {dmg} shadow damage.")
      print(f"Mana: {self.mana}/{self.max_mana}")
      target.take_damage(dmg, "shadow")
      return dmg


    dim_ready = self.spell_cooldowns.get("dim", 0) <= 0
    dim_not_active = not Disoriented.is_active(target)
    if self.mana >= 2 and roll > 70 and dim_ready and dim_not_active:
      self.mana -= 2
      dmg = random.randint(1, 3) + self.atk
      print(f"\nThe light around you bends wrong.")
      print(f"'Dim.' Barely a word. More like a decision.")
      print(f"Something hits you in the confusion. {dmg} shadow damage.")
      if random.random() < 0.75:
        target.add_status(Disoriented(duration=2))
        print(f"You feel the disorientation take hold. Spells may fail.")
      print(f"Mana: {self.mana}/{self.max_mana}")
      self.spell_cooldowns["dim"] = 3
      target.take_damage(dmg, "shadow")
      return dmg

    if self.mana >= 4 and roll > 60:
      self.mana -= 4
      dmg = random.randint(3, 7) + self.atk
      print(f"\nHe steps into shadow mid-stride.")
      print(f"You lose him for half a second.")
      print(f"Then he's behind you.")
      print(f"'Mutter.' He says it flat. Like a word he's said a thousand times.")
      print(f"Dark words find something soft. {dmg} shadow damage.")
      print(f"Mana: {self.mana}/{self.max_mana}")
      target.take_damage(dmg, "shadow")
      return dmg

    elif self.mana >= 2 and roll > 40:
      self.mana -= 2
      dmg = random.randint(2, 5) + self.atk
      print(f"\nHe flickers.")
      print(f"'Dim.' Quiet. Almost bored.")
      print(f"The light around him bends wrong for a moment.")
      print(f"Something hits you in the confusion. {dmg} shadow damage.")
      print(f"Mana: {self.mana}/{self.max_mana}")
      target.take_damage(dmg, "shadow")
      return dmg

    else:
      dmg = random.randint(2, 5) + self.atk
      print(f"\nThe spell won't come.")
      print(f"He draws a rusted dagger instead.")
      print(f"'Fine.' Like he's angry at himself.")
      print(f"The blade finds you anyway. {dmg} damage.")
      target.take_damage(dmg, "physical")
      return dmg

  def on_low_hp(self):
    if self.hp <= 0 and not self.fled:
      self.fled = True
      self.hp = 1
      return True
    return False


class Bloodweaver:
  """
  Mira's unique class. Cannot be chosen by the player.
  Heals by spending her own HP. Everything has a cost here.
  """
  SCHOOL = "Bloodweaver"

  SPELLS = {
    "Mend": {
      "flavor": "She presses her hand against your wound. Something moves from her into you.",
      "mechanic": "(Restores 15 player HP. Costs Mira 10 HP. Safe-ish.)",
      "player_restore": 15,
      "self_cost": 10,
    },
    "Staunch": {
      "flavor": "Her breath catches. She gives more than she should.",
      "mechanic": "(Restores 30 player HP. Costs Mira 20 HP. Use carefully.)",
      "player_restore": 30,
      "self_cost": 20,
    },
    "Lifegift": {
      "flavor": "She closes her eyes. When she opens them something is gone from her face.",
      "mechanic": "(Restores 60 player HP. Clears one status effect. Costs Mira 35 HP. Emergency only.)",
      "player_restore": 60,
      "self_cost": 35,
      "clears_status": True,
    },
  }

  PASSIVE_THRESHOLD = 0.20
  PASSIVE_HEAL = "Mend"


class FrightenedWoman(Humanoid):
  def __init__(self):
    super().__init__(
      name="Mira",
      hp=60,
      desc="A slight woman with careful eyes. "
           "She doesn't talk much. "
           "What she does, she means.",
      exp_value=0,
      atk=0,
      defense=0,
      level=1,
      gold_reward=0,
      loot_table=[],
      abilities=[]
    )
    self.true_name = "Mira"
    self.school = Bloodweaver.SCHOOL
    self.spells = list(Bloodweaver.SPELLS.keys())
    self.spell_data = Bloodweaver.SPELLS
    self.mana = 0
    self.max_mana = 0
    self.manabda = 0
    self.faction = "Travelers"
    self.can_fight = False
    self.passive_triggered = False
    self.passive_threshold = Bloodweaver.PASSIVE_THRESHOLD
    self.passive_heal = Bloodweaver.PASSIVE_HEAL

  def attack(self, target):
    print(f"\nMira doesn't move toward the fight.")
    print(f"She looks at you instead.")
    print(f"'Tell me where it hurts.'")
    return 0

  def mend(self, player):
    spell = Bloodweaver.SPELLS["Mend"]
    cost = spell["self_cost"]
    if self.hp <= cost:
      print(f"\nMira looks at her hands.")
      print(f"'I don't have enough left.'")
      print(f"She means it literally.")
      return False
    self.hp -= cost
    restore = spell["player_restore"]
    player.hp = min(player.max_hp, player.hp + restore)
    print(f"\n{spell['flavor']}")
    print(f"{spell['mechanic']}")
    print(f"+{restore} HP restored. [{player.hp}/{player.max_hp}]")
    print(f"Mira: {self.hp}/{self.max_hp} HP remaining.")
    return True

  def staunch(self, player):
    spell = Bloodweaver.SPELLS["Staunch"]
    cost = spell["self_cost"]
    if self.hp <= cost:
      print(f"\nMira shakes her head slowly.")
      print(f"'Not enough. I'm sorry.'")
      return False
    self.hp -= cost
    restore = spell["player_restore"]
    player.hp = min(player.max_hp, player.hp + restore)
    print(f"\n{spell['flavor']}")
    print(f"{spell['mechanic']}")
    print(f"+{restore} HP restored. [{player.hp}/{player.max_hp}]")
    print(f"Mira: {self.hp}/{self.max_hp} HP remaining.")
    return True

  def lifegift(self, player):
    spell = Bloodweaver.SPELLS["Lifegift"]
    cost = spell["self_cost"]
    if self.hp <= cost:
      print(f"\nMira looks at you for a long moment.")
      print(f"'If I had more to give, I would.'")
      print(f"'I don't.'")
      return False
    self.hp -= cost
    restore = spell["player_restore"]
    player.hp = min(player.max_hp, player.hp + restore)
    print(f"\n{spell['flavor']}")
    print(f"{spell['mechanic']}")
    print(f"+{restore} HP restored. [{player.hp}/{player.max_hp}]")
    if spell.get("clears_status") and player.status_effects:
      cleared = player.status_effects.pop(0)
      print(f"Status effect '{cleared.name}' cleared.")
      print(f"She absorbed it. You don't want to know what that costs.")
    print(f"Mira: {self.hp}/{self.max_hp} HP remaining.")
    if self.hp <= 10:
      print(f"\nShe sways slightly.")
      print(f"Catches herself on the wall.")
      print(f"'I'm alright.' She says it like she's reminding herself.")
    return True

  def passive_check(self, player):
    if self.passive_triggered:
      return False
    if not self.is_alive():
      return False
    threshold = int(player.max_hp * self.passive_threshold)
    if player.hp <= threshold:
      print(f"\nMira moves before you can ask.")
      print(f"She doesn't say anything.")
      print(f"She just acts.")
      result = self.mend(player)
      if result:
        self.passive_triggered = True
      return result
    return False

  def reset_passive(self):
    self.passive_triggered = False

  def heal_choice(self, player):
    if not self.is_alive():
      print(f"\nMira can't help. She's gone.")
      return False
    print(f"\n--- Mira [{self.hp}/{self.max_hp} HP] ---")
    print(f"'Tell me how bad it is.'")
    print(f"\n1. Mend")
    print(f"   {Bloodweaver.SPELLS['Mend']['flavor']}")
    print(f"   {Bloodweaver.SPELLS['Mend']['mechanic']}")
    print(f"\n2. Staunch")
    print(f"   {Bloodweaver.SPELLS['Staunch']['flavor']}")
    print(f"   {Bloodweaver.SPELLS['Staunch']['mechanic']}")
    print(f"\n3. Lifegift")
    print(f"   {Bloodweaver.SPELLS['Lifegift']['flavor']}")
    print(f"   {Bloodweaver.SPELLS['Lifegift']['mechanic']}")
    print(f"\n4. 'Save yourself. I'm fine.'")
    choice = input("Choose: ").strip()
    if choice == "1":
      return self.mend(player)
    elif choice == "2":
      return self.staunch(player)
    elif choice == "3":
      return self.lifegift(player)
    elif choice == "4":
      print(f"\nShe looks at you.")
      print(f"'Alright.' She doesn't argue.")
      print(f"'But I'm watching.'")
      return False
    else:
      print(f"\nShe waits.")
      print(f"'Whenever you're ready.'")
      return False


class Enforcer(Humanoid):
  def __init__(self, name: str = "Town Enforcer", level: int = 3):
    super().__init__(
      name=name,
      hp=60,
      desc="Armored thug with a crackling baton.",
      exp_value=40,
      atk=6,
      defense=4,
      level=level,
      gold_reward=15,
      loot_table=["Tithe Token", "Enforcer Baton"],
      abilities=["Mana Drain"]
    )
    self.true_name = None
    self.mana = 20
    self.max_mana = 20
    self.manabda = 10
    self.faction = "Enforcers"
    self.spells = ["Mana Drain"]

  def attack(self, target):
    target_low_hp = target.hp <= target.max_hp * 0.25


    if target_low_hp and self.mana >= 6:
      self.mana -= 6
      dmg = random.randint(10, 15) + self.atk
      print(f"{self.name} sees the opening.")
      print(f"The baton charges — both hands — full power.")
      print(f"'Finish it.' He says it to himself, not you.")
      print(f"The crack of it echoes off stone. {dmg} damage!")
      print(f"Mana: {self.mana}/{self.max_mana}")
      target.take_damage(dmg, "arcane")
      return dmg

    if self.mana >= 4 and random.randint(1, 100) > 50:
      self.mana -= 4
      dmg = random.randint(5, 9) + self.atk
      print(f"{self.name} casts Mana Drain! Baton crackles! {dmg} damage! Mana: {self.mana}/{self.max_mana}")
      target.take_damage(dmg, "arcane")
      return dmg
    else:
      dmg = random.randint(3, 7) + self.atk
      print(f"{self.name} swings a crackling baton! {dmg} damage!")
      target.take_damage(dmg, "physical")
      return dmg


class TitheCollector(Humanoid):
  def __init__(self):
    super().__init__(
      name="Tithe Collector",
      hp=120,
      desc="The underling. Draped in stolen manabda, eyes like ledger ink.",
      exp_value=100,
      atk=9,
      defense=6,
      level=5,
      gold_reward=50,
      loot_table=["Greater Sort Rune", "Tithe Ledger", "Collector's Ring"],
      abilities=["Soul Levy", "Audit"]
    )
    self.true_name = "Varric"
    self.mana = 40
    self.max_mana = 40
    self.manabda = 25
    self.faction = "Ruling Class"
    self.spells = ["Soul Levy", "Audit"]
    self.status_immunities = ["Disoriented"]

  def attack(self, target):
    target_low_hp = target.hp <= target.max_hp * 0.25


    if target_low_hp and self.mana >= 10:
      self.mana -= 10
      dmg = random.randint(18, 26) + self.atk
      print(f"{self.name} goes still.")
      print(f"Something behind his eyes does the math.")
      print(f"You can see the moment the number comes up.")
      print(f"'Final Collection.' Flat. Administrative.")
      print(f"He puts everything into it. Not rage. Efficiency. {dmg} arcane damage.")
      print(f"Mana: {self.mana}/{self.max_mana}")
      target.take_damage(dmg, "arcane")
      return dmg

    if self.mana >= 8 and random.randint(1, 100) > 30:
      self.mana -= 8
      dmg = random.randint(10, 16) + self.atk
      print(f"{self.name} casts Soul Levy! Your mana feels weighed! {dmg} damage! Mana: {self.mana}/{self.max_mana}")
      target.take_damage(dmg, "arcane")
      return dmg
    elif self.mana >= 5:
      self.mana -= 5
      dmg = random.randint(7, 12) + self.atk
      print(f"{self.name} casts Audit! Numbers burn in the air! {dmg} damage! Mana: {self.mana}/{self.max_mana}")
      target.take_damage(dmg, "arcane")
      return dmg
    else:
      dmg = random.randint(6, 10) + self.atk
      print(f"{self.name} strikes with a ledger-bound staff! {dmg} damage!")
      target.take_damage(dmg, "physical")
      return dmg

class Criminal(Humanoid):
  def __init__(self):
    super().__init__(
      name="Criminal",
      hp=30,
      desc="A hollow-eyed figure who couldn't pay the tithe. "
           "Now takes from those who can.",
      exp_value=20,
      atk=4,
      defense=1,
      level=2,
      gold_reward=6,
      loot_table=[("Stolen Coin", 60), ("Cracked Blade", 25)],
      abilities=["Desperation Strike"]
    )
    self.mana = 8
    self.max_mana = 8
    self.faction = "None"
    self.fled = False

  def attack(self, target):
    target_low_hp = target.hp <= target.max_hp * 0.25


    if target_low_hp and self.mana >= 4:
      self.mana -= 4
      dmg = random.randint(6, 10) + self.atk
      print(f"\n{self.name} sees the blood.")
      print(f"Something animal takes over.")
      print(f"The blade comes down with everything they have left. {dmg} damage!")
      target.take_damage(dmg, "physical")
      return dmg


    if random.randint(1, 100) <= 30:
      dmg1 = random.randint(2, 4) + self.atk
      dmg2 = random.randint(1, 3)
      print(f"{self.name} feints left — then right. {dmg1} damage!")
      target.take_damage(dmg1, "physical")
      print(f"A second slash from nowhere. {dmg2} damage!")
      target.take_damage(dmg2, "physical")
      return dmg1 + dmg2


    dmg = random.randint(3, 6) + self.atk
    print(f"{self.name} lunges with a cracked blade. {dmg} damage!")
    target.take_damage(dmg, "physical")
    return dmg



class Consequential(Monster):
  def __init__(self, weakened=False):
    if weakened:
      super().__init__(
        name="Half-Formed Consequential",
        hp=42,
        desc="A transformation that never finished. Still enough.",
        exp_value=60,
        atk=7,
        defense=2,
        level=4,
        gold_reward=0
      )
    else:
      super().__init__(
        name="The Consequential",
        hp=85,
        desc="Black fur through torn clothing. Three eyes on the edge of a face. A serrated mandible.",
        exp_value=90,
        atk=9,
        defense=3,
        level=5,
        gold_reward=0
      )
    self.weakened = weakened

  def attack(self, target):
    target_low_hp = target.hp <= target.max_hp * 0.25

    if target_low_hp:
      dmg = random.randint(10, 14) + self.atk
      print(f"The tongue shoots from the dark — tiny hands where barbs should be.")
      print(f"Each fingertip pulls in a direction that doesn't agree with the others. {dmg} damage!")
      target.take_damage(dmg, "physical")
      return dmg

    if random.randint(1, 100) > 60:
      dmg = random.randint(6, 10) + self.atk
      print(f"The serrated mandible strikes from the wrong side. {dmg} damage!")
      target.take_damage(dmg, "physical")
      return dmg

    dmg = random.randint(4, 8) + self.atk
    print(f"{self.name} lunges — appetite, not purpose. {dmg} damage!")
    target.take_damage(dmg, "physical")
    return dmg


class MotherRaven(Monster):
  def __init__(self):
    super().__init__(
      name="Mother Raven",
      hp=110,
      desc="Not what made the others. What the others are trying to become.",
      exp_value=100,
      atk=7,
      defense=2,
      level=5,
      gold_reward=0
    )
    self.turn_count = 0

  def attack(self, target):
    self.turn_count += 1

    if self.turn_count % 7 == 0:
      dmg = random.randint(8, 12) + self.atk
      print(f"She opens her beak. What comes out isn't a sound birds make.")
      print(f"The swarm answers — every surface empties at once. {dmg} damage!")
      target.take_damage(dmg, "physical")
      return dmg

    if random.randint(1, 100) > 55:
      dmg = random.randint(6, 9) + self.atk
      print(f"Her wingspan fills the space between walls. The gust alone staggers you. {dmg} damage!")
      target.take_damage(dmg, "physical")
      return dmg

    dmg = random.randint(3, 7) + self.atk
    print(f"Talons rake down from above. {dmg} damage!")
    target.take_damage(dmg, "physical")
    return dmg


class EnforcerCommander(Humanoid):
  def __init__(self, ravens_active=False):
    super().__init__(
      name="Enforcer Commander",
      hp=100,
      desc="Dark black and red regalia. A partially toothed grin in the shadow of a hood.",
      exp_value=120,
      atk=8,
      defense=5,
      level=6,
      gold_reward=0,
      loot_table=[],
      abilities=["Mana Drain"]
    )
    self.mana = 30
    self.max_mana = 30
    self.faction = "Enforcers"
    self.spells = ["Mana Drain"]
    self.ravens_active = ravens_active
    self.turn_count = 0

  def attack(self, target):
    self.turn_count += 1

    if self.ravens_active and self.turn_count % 7 == 0:
      dmg = random.randint(6, 10)
      print(f"Wings. The swarm pours into the square on a rhythm all its own. {dmg} damage!")
      target.take_damage(dmg, "physical")
      return dmg

    target_low_hp = target.hp <= target.max_hp * 0.25

    if target_low_hp and self.mana >= 8:
      self.mana -= 8
      dmg = random.randint(12, 16) + self.atk
      print(f"{self.name} sees the opening. He doesn't hurry toward it.")
      print(f"The strike lands like a verdict. {dmg} damage! Mana: {self.mana}/{self.max_mana}")
      target.take_damage(dmg, "arcane")
      return dmg

    if self.mana >= 5 and random.randint(1, 100) > 50:
      self.mana -= 5
      dmg = random.randint(7, 11) + self.atk
      print(f"{self.name} casts Mana Drain — practiced, economical. {dmg} damage! Mana: {self.mana}/{self.max_mana}")
      target.take_damage(dmg, "arcane")
      return dmg

    dmg = random.randint(4, 8) + self.atk
    print(f"{self.name} strikes without wasted motion. {dmg} damage!")
    target.take_damage(dmg, "physical")
    return dmg


class EnforcerGangSergeant(Humanoid):
  def __init__(self):
    super().__init__(
      name="Enforcer Gang Sergeant",
      hp=70,
      desc="The one who tells the batons where to swing.",
      exp_value=55,
      atk=7,
      defense=4,
      level=4,
      gold_reward=20,
      loot_table=["Enforcer Baton"],
      abilities=["Mana Drain"]
    )
    self.mana = 20
    self.max_mana = 20
    self.faction = "Enforcers"
    self.spells = ["Mana Drain"]

  def attack(self, target):
    target_low_hp = target.hp <= target.max_hp * 0.25

    if target_low_hp and self.mana >= 6:
      self.mana -= 6
      dmg = random.randint(9, 13) + self.atk
      print(f"{self.name} barks the order to himself and follows it. {dmg} damage! Mana: {self.mana}/{self.max_mana}")
      target.take_damage(dmg, "arcane")
      return dmg

    dmg = random.randint(4, 8) + self.atk
    print(f"{self.name} swings with a sergeant's efficiency. {dmg} damage!")
    target.take_damage(dmg, "physical")
    return dmg


class Dara(Humanoid):
  def __init__(self):
    super().__init__(
      name="Dara Rennick",
      hp=90,
      desc="Twilight Ledger operative. Warm right up until she isn't.",
      exp_value=85,
      atk=8,
      defense=3,
      level=5,
      gold_reward=0,
      loot_table=[],
      abilities=["Crimson Turn"]
    )
    self.mana = 25
    self.max_mana = 25
    self.faction = "Twilight Ledger"
    self.spells = ["Crimson Turn"]

  def attack(self, target):
    target_low_hp = target.hp <= target.max_hp * 0.25

    if target_low_hp and self.mana >= 10:
      self.mana -= 10
      dmg = random.randint(12, 16) + self.atk
      print(f"Her palm comes up, glowing in an outline of red.")
      print(f"A slow turning gesture. The air around you agrees with her. {dmg} damage! Mana: {self.mana}/{self.max_mana}")
      target.take_damage(dmg, "arcane")
      return dmg

    if self.mana >= 5 and random.randint(1, 100) > 50:
      self.mana -= 5
      dmg = random.randint(6, 10) + self.atk
      print(f"She moves the way she talks — no wasted syllables. {dmg} damage! Mana: {self.mana}/{self.max_mana}")
      target.take_damage(dmg, "arcane")
      return dmg

    dmg = random.randint(4, 8) + self.atk
    print(f"The knife was in her hand before you saw her draw it. {dmg} damage!")
    target.take_damage(dmg, "physical")
    return dmg


BESTIARY = {
  "Rat": Rat,
  "Bat": Bat,
  "Goblin": Goblin,
  "Raven Swarm": RavenSwarm,
  "Wolf": Wolf,
  "Skeleton": Skeleton,
  "Giant Spider": Spider,
  "Cave Troll": CaveTroll,
  "Wraith": Wraith,
  "Troll King": TrollKing,
  "Criminal": Criminal,
  "The Consequential": Consequential,
  "Mother Raven": MotherRaven,
  "Enforcer Commander": EnforcerCommander,
  "Enforcer Gang Sergeant": EnforcerGangSergeant,
  "Dara Rennick": Dara,
}