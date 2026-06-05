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

  def check_mana(self, cost: int) -> None:
    if self.mana < cost:
      raise ValueError(f"The well is dry. Have {self.mana}, need {cost}.")

  def check_manabda(self, cost: int) -> None:
    if self.manabda < cost:
      raise ValueError(f"The manabda is spent. Have {self.manabda}, need {cost}.")

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