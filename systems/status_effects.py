class StatusEffect:
  def __init__(self, name, duration, damage_per_turn=0):
    self.name = name
    self.duration = duration
    self.damage_per_turn = damage_per_turn

  def tick(self, target):
    if self.duration <= 0:
      return f"{target.name} recovers from {self.name}."

    message = ""
    if self.damage_per_turn > 0:
      target.hp -= self.damage_per_turn
      message = f"{target.name} takes {self.damage_per_turn} {self.name} damage! [HP: {target.hp}]"

    self.duration -= 1
    return message

  def is_expired(self):
    return self.duration <= 0


class Burn(StatusEffect):
  def __init__(self, duration=3, damage_per_turn=5):
    super().__init__("Burning", duration, damage_per_turn)

  def tick(self, target):
    result = super().tick(target)
    if not self.is_expired() and result:
      result += "\nThe flames crackle hungrily."
    return result