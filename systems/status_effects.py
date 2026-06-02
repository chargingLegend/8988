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

class Scorched(StatusEffect):
  def __init__(self, duration=2, damage_per_turn=3):
    super().__init__("Scorched", duration, damage_per_turn)

  def tick(self, target):
    result = super().tick(target)
    if not self.is_expired() and result:
      result += "\nThe heat is building. Something is about to give."
    return result

class Combusting(StatusEffect):
  def __init__(self, duration=4, damage_per_turn=10):
    super().__init__("Combusting", duration, damage_per_turn)

  def tick(self, target):
    result = super().tick(target)
    if not self.is_expired() and result:
      result += "\nFully ablaze. The screaming is secondary to the crackling."
    return result

class Frozen(StatusEffect):
  def __init__(self, duration=2):
    super().__init__("Frozen", duration, damage_per_turn=0)

  def tick(self, target):
    result = super().tick(target)
    if not self.is_expired() and not result:
      result = f"{target.name} is encased in ice. It cannot move."
    if not self.is_expired() and result:
      result += "\nThe ice holds. Not a twitch. Not a breath."
    return result


class Preserved(StatusEffect):
  def __init__(self, duration=2):
    super().__init__("Preserved", duration, damage_per_turn=0)

  def tick(self, target):
    result = super().tick(target)
    if not self.is_expired():
      result = f"{target.name} is locked in cryo-stasis. Its state cannot change."
      result += "\nThe ice remembers exactly what it caught."
    return result


class Frostbitten(StatusEffect):
  def __init__(self, duration=3, damage_per_turn=3):
    super().__init__("Frostbitten", duration, damage_per_turn)

  def tick(self, target):
    result = super().tick(target)
    if not self.is_expired() and result:
      result += "\nThe cold eats deeper. Flesh forgets warmth."
    return result