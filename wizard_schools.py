import random
from systems.status_effects import (Burn, Scorched, Combusting,
  Frozen, Frostbitten, Slowed,
  Disoriented, Stuttered, Shattered, Weakened)


def choose_school(self, school):
  self.school = school
  print(f"A mark burns into your palm: {self.school}.")
  if school == "Pyromancy":
    print("Your skin ripples. Veins beneath glow ember-red.")
    print("A surge of warmth—bordering on hot—courses through your body.")
    print("The sensation is gratifying. Almost euphoric.")
    self.spells = ["Ignite", "Sear", "Cinder Ward"]
    self.spell_data = {
      "Ignite": {
        "min_dmg": 4, "max_dmg": 11, "dmg_type": "fire",
        "desc": "flame catches on {target}. It shrieks, blackened.",
        "effect": "Burn", "effect_chance": 0.5
      },
      "Sear": {
        "min_dmg": 3, "max_dmg": 7, "dmg_type": "fire",
        "desc": "a lance of heat lashes {target}. Flesh starts to bubble.",
        "effect": "Scorched", "effect_chance": 0.3
      },
      "Cinder Ward": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "ward",
        "desc": "embers orbit you. {target} feels the heat.",
        "effect": None
      },
    }
  elif school == "Cryomancy":
    print("Your breath fogs. Frost traces your fingertips.")
    print("A stillness settles in your chest, cold and absolute.")
    print("The world seems slower. Sharper. Distant.")
    self.spells = ["Frostbite", "Glaze", "Shard"]
    self.spell_data = {
      "Frostbite": {
        "min_dmg": 3, "max_dmg": 8, "dmg_type": "cold",
        "desc": "ice crusts over {target}. Wings crack.",
        "effect": "Frostbitten", "effect_chance": 0.4
      },
      "Glaze": {
        "min_dmg": 2, "max_dmg": 4, "dmg_type": "cold",
        "desc": "rime coats {target}. It moves like cold honey.",
        "effect": "Slowed", "effect_chance": 0.6
      },
      "Shard": {
        "min_dmg": 4, "max_dmg": 9, "dmg_type": "cold",
        "desc": "a spear of ice punches through {target}.",
        "effect": None
      },
    }
  elif school == "Chronomancy":
    print("The air ticks. Your shadow lags half a second behind you.")
    print("For a heartbeat, you see the echo of your next breath.")
    print("Time feels loose. Negotiable.")
    self.spells = ["Hesitate", "Foresight", "Stutter"]
    self.spell_data = {
      "Hesitate": {
        "min_dmg": 2, "max_dmg": 6, "dmg_type": "time",
        "desc": "{target} stutters mid-beat. Existence frays.",
        "effect": None
      },
      "Foresight": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "time",
        "desc": "you read {target}'s next beat before it arrives.",
        "effect": "Stuttered", "effect_chance": 1.0
      },
      "Stutter": {
        "min_dmg": 3, "max_dmg": 7, "dmg_type": "time",
        "desc": "{target} skips a moment. Parts of it arrive late.",
        "effect": "Slowed", "effect_chance": 0.35
      },
    }
  elif school == "Necromancy":
    print("The ground chills under your feet. Your shadow deepens.")
    print("A whisper you didn't think brushes the back of your skull.")
    print("Death recognizes you. And waits.")
    self.spells = ["Rattle", "Wither", "Gravechill"]
    self.spell_data = {
      "Rattle": {
        "min_dmg": 3, "max_dmg": 9, "dmg_type": "necrotic",
        "desc": "{target}'s bones remember the grave. They protest.",
        "effect": "Weakened", "effect_chance": 0.35
      },
      "Wither": {
        "min_dmg": 2, "max_dmg": 8, "dmg_type": "necrotic",
        "desc": "vitality flees {target} like startled crows.",
        "effect": None
      },
      "Gravechill": {
        "min_dmg": 4, "max_dmg": 8, "dmg_type": "necrotic",
        "desc": "the cold of tombs settles in {target}.",
        "effect": "Slowed", "effect_chance": 0.3
      },
    }
  elif school == "Enhancement":
    print("Muscle fibers sing. Bones feel dense as iron.")
    print("The mountain air tastes thin. You don't care.")
    print("Strength is a word. Now it is a state.")
    self.spells = ["Brace", "Surge", "Iron Skin"]
    self.spell_data = {
      "Brace": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "force",
        "desc": "you root yourself. {target} will find less purchase.",
        "effect": None
      },
      "Surge": {
        "min_dmg": 3, "max_dmg": 8, "dmg_type": "force",
        "desc": "kinetic wrath slams into {target}.",
        "effect": "Weakened", "effect_chance": 0.3
      },
      "Iron Skin": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "force",
        "desc": "your skin rings like struck steel. {target} notices.",
        "effect": None
      },
    }
  elif school == "Illusion":
    print("Colors lie. The corner of your eye breeds movement.")
    print("You doubt the weight of your own hands.")
    print("Truth becomes a choice, not a fact.")
    self.spells = ["Phantom", "Mutter", "False Step"]
    self.spell_data = {
      "Phantom": {
        "min_dmg": 2, "max_dmg": 6, "dmg_type": "psychic",
        "desc": "{target} strikes at horrors only it sees.",
        "effect": "Shattered", "effect_chance": 0.3
      },
      "Mutter": {
        "min_dmg": 2, "max_dmg": 5, "dmg_type": "psychic",
        "desc": "whispers convince {target} it is already wounded.",
        "effect": "Weakened", "effect_chance": 0.4
      },
      "False Step": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "psychic",
        "desc": "{target} misjudges distance. Its next move commits to nothing.",
        "effect": "Shattered", "effect_chance": 0.65
      },
    }
  elif school == "Conjuration":
    print("The space before you bends. Air thickens.")
    print("Something almost arrives, then decides not to.")
    print("The world feels less solid. More borrowed.")
    self.spells = ["Fetch", "Shardling", "Bind"]
    self.spell_data = {
      "Fetch": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "force",
        "desc": "you grasp at distance. Something shifts near {target}.",
        "effect": None
      },
      "Shardling": {
        "min_dmg": 3, "max_dmg": 9, "dmg_type": "force",
        "desc": "a conjured splinter hurls into {target}.",
        "effect": None
      },
      "Bind": {
        "min_dmg": 2, "max_dmg": 6, "dmg_type": "force",
        "desc": "invisible cords seize {target}'s limbs.",
        "effect": "Slowed", "effect_chance": 0.55
      },
    }
  elif school == "Shadow":
    print("Light bends away from you. Your edges blur.")
    print("Whispers you don't recognize brush your thoughts.")
    print("You feel unseen. And yet, watched.")
    self.spells = ["Dim", "Mutter", "Veil"]
    self.spell_data = {
      "Dim": {
        "min_dmg": 1, "max_dmg": 3, "dmg_type": "shadow",
        "desc": "light flees {target}. It blinks, confused.",
        "effect": "Disoriented", "effect_chance": 0.75,
        "cooldown_key": "dim", "cooldown_turns": 3
      },
      "Mutter": {
        "min_dmg": 2, "max_dmg": 7, "dmg_type": "shadow",
        "desc": "dark words eat at {target}'s resolve.",
        "effect": "Weakened", "effect_chance": 0.4
      },
      "Veil": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "shadow",
        "desc": "you cease to be a target. {target} loses you.",
        "effect": None
      },
    }
  elif school == "Transmutation":
    print("Your fingertips tingle. Stone would answer if you asked.")
    print("Lead and gold feel like the same word in different accents.")
    print("Matter is a suggestion.")
    self.spells = ["Shift", "Harden", "Gild"]
    self.spell_data = {
      "Shift": {
        "min_dmg": 2, "max_dmg": 7, "dmg_type": "arcane",
        "desc": "{target}'s mass forgets itself for a second.",
        "effect": "Weakened", "effect_chance": 0.35
      },
      "Harden": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "arcane",
        "desc": "air becomes stone around you. {target} feels the shift.",
        "effect": None
      },
      "Gild": {
        "min_dmg": 3, "max_dmg": 8, "dmg_type": "arcane",
        "desc": "{target}'s edges turn brittle-gold, then crack.",
        "effect": "Weakened", "effect_chance": 0.45
      },
    }


def learn_spell_sort(self, method="gift"):
  if "sort" not in self.spells:
    self.spells.append("sort")
    self.sort_acquired_by = method
    return "The runes on your palm shift. You understand how to use the rune to 'sort' now."
  return "You already understand the sort spell"


def sort(self, location):
  if "sort" not in self.spells:
    raise AttributeError("You trace the rune to be able to use the 'sort' ability, but it doesnt mean anything to you. not yet")
  common = getattr(location, 'common', None) or location.get('common', [])
  uncommon = getattr(location, 'uncommon', None) or location.get('uncommon', [])
  found = random.sample(common, k=min(2, len(common)))
  if random.random() < 0.10 and uncommon:
    found.append(random.choice(uncommon))
  for item in found:
    self.inventory.add(item)
  print(f"you focus on the Rune of sort")
  print(f"Found: {', '.join(str(i) for i in found)}")
  print(self.inventory)


def unlock_abilities(self):
  if self.school == "Pyromancy":
    self.ability_data.update({
      "pyromancy_burn": {
        "tiers": {
          "1": {"label": "Kindle (heat 10)", "cost": 2},
          "2": {"label": "Sear (heat 20)", "cost": 4},
          "3": {"label": "Incinerate (heat 35)", "cost": 6},
          "4": {"label": "Inferno (heat 60)", "cost": "all", "requires_upgrade": True}
        }
      },
      "map_fire": {
        "tiers": {
          "1": {"label": "Spread flame across targets", "cost": 3}
        }
      },
      "reduce_ash": {
        "tiers": {
          "1": {"label": "Collapse enemy to ash", "cost": 5}
        }
      }
    })
    self.abilities = ["pyromancy_burn", "map_fire", "reduce_ash"]
    self.learn_spell_sort()

  elif self.school == "Chronomancy":
    self.ability_data.update({
      "fast_forward_time": {
        "tiers": {
          "1": {"label": "A Score of Years (20)", "cost": 3, "years": 20},
          "2": {"label": "Two Generations (40)", "cost": 5, "years": 40},
          "3": {"label": "A Century (100)", "cost": 8, "years": 100},
          "4": {"label": "Molecular Dissolution", "cost": "all", "years": 999, "requires_upgrade": True}
        }
      },
      "rewind_time": {
        "tiers": {
          "1": {"label": "A Score of Years (20)", "cost": 3, "years": 20},
          "2": {"label": "Two Generations (40)", "cost": 5, "years": 40},
          "3": {"label": "A Century (100)", "cost": 8, "years": 100},
          "4": {"label": "Infant State", "cost": "all", "years": 999, "requires_upgrade": True}
        }
      }
    })
    self.abilities = ["fast_forward_time", "rewind_time"]
    self.learn_spell_sort()

  elif self.school == "Cryomancy":
    self.ability_data.update({
      "freeze": {
        "tiers": {
          "1": {"label": "Freeze target", "cost": 4}
        }
      },
      "cryo_preserve": {
        "tiers": {
          "1": {"label": "Seal in cryo-stasis", "cost": 6}
        }
      }
    })
    self.abilities = ["freeze", "cryo_preserve"]
    self.learn_spell_sort()

  elif self.school == "Necromancy":
    self.ability_data.update({
      "raise_dead": {
        "tiers": {
          "1": {"label": "Raise fallen enemy as ally", "cost": 3}
        }
      },
      "decay": {
        "tiers": {
          "1": {"label": "Strip defense (costs 2)", "cost": 2},
          "2": {"label": "Strip attack (costs 3)", "cost": 3}
        }
      },
      "animate": {
        "tiers": {
          "1": {"label": "Animate corpse (cost scales with level)", "cost": 2}
        }
      }
    })
    self.abilities = ["raise_dead", "decay", "animate"]
    self.learn_spell_sort()

  elif self.school == "Enhancement":
    self.ability_data.update({
      "amplify": {
        "tiers": {
          "1": {"label": "Pour manabda into next strike", "cost": 1}
        }
      },
      "temper": {
        "tiers": {
          "1": {"label": "Round a target attribute", "cost": 1}
        }
      },
      "surge": {
        "tiers": {
          "1": {"label": "Buff all allies", "cost": 2}
        }
      }
    })
    self.abilities = ["amplify", "temper", "surge"]
    self.learn_spell_sort()

  elif self.school == "Illusion":
    self.ability_data.update({
      "veil": {
        "tiers": {
          "1": {"label": "A breath (2 turns)", "cost": 2},
          "2": {"label": "A heartbeat (4 turns)", "cost": 4},
          "3": {"label": "A long shadow (6 turns)", "cost": 6}
        }
      },
      "mimic": {
        "tiers": {
          "1": {"label": "Surface copy (name only)", "cost": 1},
          "2": {"label": "Shallow copy (name, hp, atk)", "cost": 3},
          "3": {"label": "Deep copy (all attributes)", "cost": 5}
        }
      },
      "shatter": {
        "tiers": {
          "1": {"label": "A whisper (skip action)", "cost": 2},
          "2": {"label": "A scream (damage + skip)", "cost": 4},
          "3": {"label": "Collapse (heavy damage + debuff)", "cost": 6}
        }
      }
    })
    self.abilities = ["veil", "mimic", "shatter"]
    self.learn_spell_sort()

  elif self.school == "Conjuration":
    self.ability_data.update({
      "summon_elemental": {
        "tiers": {
          "1": {"label": "Tier 1 elemental", "cost": 2},
          "2": {"label": "Tier 2 elemental", "cost": 4},
          "3": {"label": "Tier 3 elemental", "cost": 7}
        }
      },
      "conjure_supply": {
        "tiers": {
          "1": {"label": "Vial", "cost": 1},
          "2": {"label": "Flask", "cost": 3},
          "3": {"label": "Draught", "cost": 5}
        }
      },
      "wild_conjure": {
        "tiers": {
          "1": {"label": "A crack (40% ally)", "cost": 1},
          "2": {"label": "A tear (55% ally)", "cost": 2},
          "3": {"label": "A rip (70% ally)", "cost": 3}
        }
      }
    })
    self.abilities = ["summon_elemental", "conjure_supply", "wild_conjure"]
    self.learn_spell_sort()

  elif self.school == "Shadow":
    self.ability_data.update({
      "shroud": {
        "tiers": {
          "1": {"label": "Surface scan", "cost": 2},
          "2": {"label": "Deep scan", "cost": 4},
          "3": {"label": "Total eclipse", "cost": 6}
        }
      },
      "siphon": {
        "tiers": {
          "1": {"label": "Drain defense", "cost": 2},
          "2": {"label": "Drain attack", "cost": 3},
          "3": {"label": "Drain both", "cost": 5}
        }
      },
      "eclipse": {
        "tiers": {
          "1": {"label": "Dim (hit weakest)", "cost": 2},
          "2": {"label": "Darken (hit 2 weakest)", "cost": 4},
          "3": {"label": "Total Eclipse (hit all)", "cost": 6}
        }
      }
    })
    self.abilities = ["shroud", "siphon", "eclipse"]
    self.learn_spell_sort()

  elif self.school == "Transmutation":
    self.ability_data.update({
      "transmute_vitae": {
        "tiers": {
          "1": {"label": "HP Potion → II", "cost": 2},
          "2": {"label": "HP Potion II → III", "cost": 4},
          "3": {"label": "HP Potion III → IV", "cost": 6}
        }
      },
      "transmute_arcana": {
        "tiers": {
          "1": {"label": "Mana Potion → II", "cost": 2},
          "2": {"label": "Mana Potion II → III", "cost": 4},
          "3": {"label": "Mana Potion III → IV", "cost": 6}
        }
      }
    })
    self.abilities = ["transmute_vitae", "transmute_arcana"]
    self.learn_spell_sort()


# ── SCHOOL_DATA for test imports ──────────────────────────────

SCHOOL_DATA = {
  "Pyromancy": {
    "spells": {
      "Ignite": {
        "min_dmg": 4, "max_dmg": 11, "dmg_type": "fire",
        "desc": "flame catches on {target}. It shrieks, blackened.",
        "effect": "Burn", "effect_chance": 0.5
      },
      "Sear": {
        "min_dmg": 3, "max_dmg": 7, "dmg_type": "fire",
        "desc": "a lance of heat lashes {target}. Flesh starts to bubble.",
        "effect": "Scorched", "effect_chance": 0.3
      },
      "Cinder Ward": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "ward",
        "desc": "embers orbit you. {target} feels the heat.",
        "effect": None
      },
    }
  },
}