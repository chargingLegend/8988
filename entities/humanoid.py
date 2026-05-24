from entities.monster import Monster

class Humanoid(Monster):
  def __init__(self, name="Villager", hp=20, desc="A person.", exp_value=10):
    super().__init__(name, hp, desc, exp_value)