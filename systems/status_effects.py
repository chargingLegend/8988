import random


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
      if target.hp < 0:
        target.hp = 0
      message = f"{target.name} takes {self.damage_per_turn} {self.name} damage! [HP: {target.hp}]"

    self.duration -= 1
    return message

  def is_expired(self):
    return self.duration <= 0


# ── FIRE ─────────────────────────────────────────────────────

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


# ── COLD ─────────────────────────────────────────────────────

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


class Slowed(StatusEffect):
  """Target attacks every other turn. Skips odd ticks."""
  def __init__(self, duration=3):
    super().__init__("Slowed", duration, damage_per_turn=0)
    self.tick_count = 0

  def tick(self, target):
    self.tick_count += 1
    self.duration -= 1
    if self.duration <= 0:
      return f"{target.name} shakes off the rime. Speed returns."
    if self.tick_count % 2 == 0:
      target.skip_turn = True
      return f"{target.name} moves like cold honey. It cannot act this turn."
    return f"{target.name} is Slowed. It struggles."

  def is_expired(self):
    return self.duration <= 0


# ── SHADOW ────────────────────────────────────────────────────

class Disoriented(StatusEffect):
  """
  Interferes with spell casting. 40% chance next spell fizzles.
  Cooldown tracked on the entity that applied it — not here.
  Cannot stack: check before applying.
  """
  FIZZLE_CHANCE = 0.40

  def __init__(self, duration=2):
    super().__init__("Disoriented", duration, damage_per_turn=0)

  def tick(self, target):
    self.duration -= 1
    if self.duration <= 0:
      return f"Light finds {target.name} again. The fog clears."
    return f"{target.name} is Disoriented. Focus wavers."

  def is_expired(self):
    return self.duration <= 0

  @staticmethod
  def is_active(target):
    """Check if Disoriented is currently on target."""
    return any(type(e).__name__ == "Disoriented" for e in target.status_effects)

  @staticmethod
  def roll_fizzle():
    """Returns True if a spell fizzles due to Disorientation."""
    return random.random() < Disoriented.FIZZLE_CHANCE


# ── TIME ──────────────────────────────────────────────────────

class Stuttered(StatusEffect):
  """Target revealed — player gets first strike priority next turn."""
  def __init__(self, duration=1):
    super().__init__("Stuttered", duration, damage_per_turn=0)
    self.revealed = True

  def tick(self, target):
    self.duration -= 1
    if self.duration <= 0:
      self.revealed = False
      return f"{target.name} snaps back into real time. The window closes."
    return f"{target.name} stutters mid-existence. Its next move is readable."

  def is_expired(self):
    return self.duration <= 0


# ── PSYCHIC / ILLUSION ────────────────────────────────────────

class Shattered(StatusEffect):
  """Target loses turns and takes reduced action."""
  def __init__(self, duration=2, damage_per_turn=0):
    super().__init__("Shattered", duration, damage_per_turn)

  def tick(self, target):
    self.duration -= 1
    target.skip_turn = True
    if self.duration <= 0:
      return f"{target.name} pulls itself back together. Barely."
    return f"{target.name} evaluates as False. It cannot act."

  def is_expired(self):
    return self.duration <= 0


# ── PHYSICAL / FORCE ──────────────────────────────────────────

class Weakened(StatusEffect):
  """Reduces atk and defense temporarily."""
  def __init__(self, duration=3, atk_reduction=0, defense_reduction=0):
    super().__init__("Weakened", duration, damage_per_turn=0)
    self.atk_reduction = atk_reduction
    self.defense_reduction = defense_reduction
    self.applied = False

  def tick(self, target):
    if not self.applied:
      if self.atk_reduction and hasattr(target, 'atk'):
        target.atk = max(0, target.atk - self.atk_reduction)
      if self.defense_reduction and hasattr(target, 'defense'):
        target.defense = max(0, target.defense - self.defense_reduction)
      self.applied = True
    self.duration -= 1
    if self.duration <= 0:
      if self.atk_reduction and hasattr(target, 'atk'):
        target.atk += self.atk_reduction
      if self.defense_reduction and hasattr(target, 'defense'):
        target.defense += self.defense_reduction
      return f"{target.name} recovers from Weakened. Strength returns."
    return f"{target.name} is Weakened. (-{self.atk_reduction} atk / -{self.defense_reduction} def)"

  def is_expired(self):
    return self.duration <= 0


# ── SPECIAL MOVE CHARGE ───────────────────────────────────────

class Charging(StatusEffect):
  """
  Tracks a 3-turn special move charge.
  Interrupted by: taking damage >= 30% max HP in one hit,
  or receiving any status effect while charging.
  """
  def __init__(self, move_name="Special Move"):
    super().__init__("Charging", duration=3, damage_per_turn=0)
    self.move_name = move_name
    self.turns_charged = 0
    self.interrupted = False

  def tick(self, target):
    self.turns_charged += 1
    self.duration -= 1
    if self.duration <= 0:
      return f"{target.name} is ready. {self.move_name} fully charged."
    remaining = self.duration
    return f"{target.name} charges {self.move_name}. {remaining} turn(s) remaining."

  def is_ready(self):
    return self.turns_charged >= 3 and not self.interrupted

  def interrupt(self, target):
    self.interrupted = True
    self.duration = 0
    return f"{target.name}'s charge breaks. {self.move_name} lost."

  def is_expired(self):
    return self.duration <= 0 or self.interrupted