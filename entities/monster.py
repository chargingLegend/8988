import random

class Monster:
  def __init__(self, name="Unknown", hp=10, desc="A creature.", exp_value=0):
    self.name = name
    self.hp = hp
    self.desc = desc
    self.status = []
    self.exp_value = exp_value

  def __repr__(self):
    return f"{self.name} - HP: {self.hp} - {self.desc}"

  def is_alive(self):
    return self.hp > 0

  def take_damage(self, dmg, dmg_type="physical"):
    self.hp -= dmg
    if self.hp < 0:
      self.hp = 0
    print(f"{self.name} takes {dmg} {dmg_type} damage! HP: {self.hp}")
    if not self.is_alive():
      print(f"{self.name} falls.")

class RavenSwarm(Monster):
  def __init__(self, name="Raven Swarm", hp=15, desc="Not birds. Too many eyes. Too much hunger."):
    super().__init__(name, hp, desc, exp_value=50)
    self.attack_dmg = (1, 4)
    self.dmg_type = "piercing"

  def attack(self, target):
    dmg = random.randint(*self.attack_dmg)
    print(f"{self.name} swarms! Beaks and claws rake for {dmg}!")
    target.take_damage(dmg, self.dmg_type)
