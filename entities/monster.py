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
                     exp_value=50, level=2, atk=4, defense=0, gold_reward=5,
                     loot_table=[("Black Feather", 60), ("Crow's Eye", 10)],
                     abilities=["Swarm", "Peck Barrage"])
    self.attack_dmg = (1, 4)
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

MONSTER_DB = {
    "Rat": Rat,
    "Bat": Bat,
    "Goblin": Goblin,
    "Raven Swarm": RavenSwarm,
    "Wolf": Wolf,
    "Skeleton": Skeleton,
    "Giant Spider": Spider,
    "Cave Troll": CaveTroll,
    "Wraith": Wraith,
    "Troll King": TrollKing
  }