from entities.monster import Monster
import random


class Humanoid(Monster):
  def __init__(self, name="Villager", hp=20, desc="A person.", exp_value=10, atk=1, defense=0, level=1, gold_reward=0,
               loot_table=None, abilities=None, age=None, flame_resistance=None):
    super().__init__(name, hp, desc, exp_value, atk, defense, level, gold_reward, loot_table, abilities, age,
                     flame_resistance)
    self.mana = 10
    self.max_mana = 10
    self.manabda = 5
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
      desc="A wary man with blonde hair hiding his eyes.",
      exp_value=35,
      atk=4,
      defense=2,
      level=2,
      gold_reward=8,
      loot_table=["Sort Rune", "Tattered Cloak"],
      abilities=["Weak Push"]
    )
    self.true_name = "Caleb"
    self.mana = 15
    self.max_mana = 15
    self.manabda = 6
    self.faction = "Travelers"
    self.spells = ["Weak Push"]

  def attack(self, target):
    if self.mana >= 3 and random.randint(1, 100) > 40:
      self.mana -= 3
      dmg = random.randint(4, 8) + self.atk
      print(f"{self.name} casts Weak Push! {dmg} damage! Mana: {self.mana}/{self.max_mana}")
      return dmg
    else:
      dmg = random.randint(2, 5) + self.atk
      print(f"{self.name} slashes with a rusted dagger! {dmg} damage!")
      return dmg


class FrightenedWoman(Humanoid):
  def __init__(self):
    super().__init__(
      name="Frightened Woman",
      hp=20,
      desc="A homely woman, shaking with fear.",
      exp_value=0,
      atk=1,
      defense=0,
      level=1,
      gold_reward=2,
      loot_table=["Torn Shawl"],
      abilities=[]
    )
    self.true_name = "Mira"
    self.mana = 5
    self.max_mana = 5
    self.manabda = 2
    self.faction = "Travelers"
    self.can_fight = False
    self.spells = []

  def cower(self):
    print(f"{self.name} cowers behind cover, shaking.")

  def attack(self, target):
    if not self.can_fight:
      self.cower()
      return 0
    dmg = 1
    print(f"{self.name} throws a rock in desperation! {dmg} damage!")
    return dmg


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
    if self.mana >= 4 and random.randint(1, 100) > 50:
      self.mana -= 4
      dmg = random.randint(5, 9) + self.atk
      print(f"{self.name} casts Mana Drain! Baton crackles! {dmg} damage! Mana: {self.mana}/{self.max_mana}")
      return dmg
    else:
      dmg = random.randint(3, 7) + self.atk
      print(f"{self.name} swings a crackling baton! {dmg} damage!")
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

  def attack(self, target):
    if self.mana >= 8 and random.randint(1, 100) > 30:
      self.mana -= 8
      dmg = random.randint(10, 16) + self.atk
      print(f"{self.name} casts Soul Levy! Your mana feels weighed! {dmg} damage! Mana: {self.mana}/{self.max_mana}")
      return dmg
    elif self.mana >= 5:
      self.mana -= 5
      dmg = random.randint(7, 12) + self.atk
      print(f"{self.name} casts Audit! Numbers burn in the air! {dmg} damage! Mana: {self.mana}/{self.max_mana}")
      return dmg
    else:
      dmg = random.randint(6, 10) + self.atk
      print(f"{self.name} strikes with a ledger-bound staff! {dmg} damage!")
      return dmg