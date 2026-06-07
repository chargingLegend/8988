from entities.monster import Monster
import random


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
    self.spell_data = {
      "Dim": (0, 0, "shadow", "light flees {target}. It blinks, confused."),
      "Mutter": (1, 5, "shadow", "dark words find the cracks in {target}'s resolve."),
      "Veil": (0, 0, "shadow", "he steps sideways out of your sight. For a moment.")
    }
    self.fled = False

  def attack(self, target):
    roll = random.randint(1, 100)
    target_low_hp = target.hp <= target.max_hp * 0.25

    # ── tactical escalation: target is near death ─────────────
    if target_low_hp and self.mana >= 4:
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

    # ── tactical escalation: target is near death ─────────────
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

  def attack(self, target):
    target_low_hp = target.hp <= target.max_hp * 0.25

    # ── tactical escalation: target is near death ─────────────
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