import random
from systems.status_effects import Burn, Scorched, Combusting


def choose_school(self, school):
  self.school = school
  print(f"A mark burns into your palm: {self.school}.")
  if school == "Pyromancy":
    print("Your skin ripples. Veins beneath glow ember-red.")
    print("A surge of warmth—bordering on hot—courses through your body.")
    print("The sensation is gratifying. Almost euphoric.")
    self.spells = ["Ignite", "Sear", "Cinder Ward"]
    self.spell_data = {
      "Ignite": (3, 8, "fire", "flame catches on {target}'s feathers. It shrieks, blackened."),
      "Sear": (2, 5, "fire", "a lance of heat lashes {target}. their Flesh starts to bubble from the intense heat."),
      "Cinder Ward": (0, 0, "ward", "embers orbit you. No damage, but the air warps.")
    }
  elif school == "Cryomancy":
    print("Your breath fogs. Frost traces your fingertips.")
    print("A stillness settles in your chest, cold and absolute.")
    print("The world seems slower. Sharper. Distant.")
    self.spells = ["Frostbite", "Glaze", "Shard"]
    self.spell_data = {
      "Frostbite": (2, 6, "cold", "ice crusts over {target}. Wings crack."),
      "Glaze": (1, 3, "cold", "rime coats {target}. It moves like cold honey."),
      "Shard": (3, 7, "cold", "a spear of ice punches through {target}.")
    }
  elif school == "Chronomancy":
    print("The air ticks. Your shadow lags half a second behind you.")
    print("For a heartbeat, you see the echo of your next breath.")
    print("Time feels loose. Negotiable.")
    self.spells = ["Hesitate", "Foresight", "Stutter"]
    self.spell_data = {
      "Hesitate": (1, 4, "time", "{target} stutters mid-beat. Existence frays."),
      "Foresight": (0, 0, "time", "you see {target}'s next beat. No damage, yet."),
      "Stutter": (2, 5, "time", "{target} skips a moment. Parts of it arrive late.")
    }
  elif school == "Necromancy":
    print("The ground chills under your feet. Your shadow deepens.")
    print("A whisper you didn't think brushes the back of your skull.")
    print("Death recognizes you. And waits.")
    self.spells = ["Rattle", "Wither", "Gravechill"]
    self.spell_data = {
      "Rattle": (2, 7, "necrotic", "{target}'s bones remember the grave. They protest."),
      "Wither": (1, 6, "necrotic", "vitality flees {target} like startled crows."),
      "Gravechill": (3, 6, "necrotic", "the cold of tombs settles in {target}.")
    }
  elif school == "Enhancement":
    print("Muscle fibers sing. Bones feel dense as iron.")
    print("The mountain air tastes thin. You don't care.")
    print("Strength is a word. Now it is a state.")
    self.spells = ["Brace", "Surge", "Iron Skin"]
    self.spell_data = {
      "Brace": (0, 0, "force", "you root yourself. No damage to {target}."),
      "Surge": (2, 6, "force", "kinetic wrath slams into {target}."),
      "Iron Skin": (0, 0, "force", "your skin rings like struck steel. No damage.")
    }
  elif school == "Illusion":
    print("Colors lie. The corner of your eye breeds movement.")
    print("You doubt the weight of your own hands.")
    print("Truth becomes a choice, not a fact.")
    self.spells = ["Phantom", "Mutter", "False Step"]
    self.spell_data = {
      "Phantom": (1, 4, "psychic", "{target} strikes at horrors only it sees."),
      "Mutter": (1, 3, "psychic", "whispers convince {target} it is already wounded."),
      "False Step": (0, 0, "psychic", "{target} misjudges distance. No damage.")
    }
  elif school == "Conjuration":
    print("The space before you bends. Air thickens.")
    print("Something almost arrives, then decides not to.")
    print("The world feels less solid. More borrowed.")
    self.spells = ["Fetch", "Shardling", "Bind"]
    self.spell_data = {
      "Fetch": (0, 0, "force", "you grasp at distance. {target} untouched."),
      "Shardling": (2, 7, "force", "a conjured splinter hurls into {target}."),
      "Bind": (1, 4, "force", "invisible cords seize {target}'s limbs.")
    }
  elif school == "Shadow":
    print("Light bends away from you. Your edges blur.")
    print("Whispers you don't recognize brush your thoughts.")
    print("You feel unseen. And yet, watched.")
    self.spells = ["Dim", "Mutter", "Veil"]
    self.spell_data = {
      "Dim": (0, 0, "shadow", "light flees {target}. It blinks, confused."),
      "Mutter": (1, 5, "shadow", "dark words eat at {target}'s resolve."),
      "Veil": (0, 0, "shadow", "you cease to be a target. For a moment.")
    }
  elif school == "Transmutation":
    print("Your fingertips tingle. Stone would answer if you asked.")
    print("Lead and gold feel like the same word in different accents.")
    print("Matter is a suggestion.")
    self.spells = ["Shift", "Harden", "Gild"]
    self.spell_data = {
      "Shift": (1, 5, "arcane", "{target}'s mass forgets itself for a second."),
      "Harden": (0, 0, "arcane", "air becomes stone. Not at {target}."),
      "Gild": (2, 6, "arcane", "{target}'s edges turn brittle-gold, then crack.")
    }


def learn_spell_sort(self, method="gift"):
  if "sort" not in self.spells:
    self.spells.append("sort")
    self.sort_acquired_by = method
    return "The runes on your palm shift. You understand how to use the rune to 'sort' now."
  return "You already understand the sort spell"


def sort(self, location: dict):
  if "sort" not in self.spells:
    raise AttributeError("You trace the rune to be able to use the 'sort' ability, but it doesnt mean anything to you. not yet")
  found = random.sample(location["common"], k=2)
  if random.random() < 0.10:
    found.append(random.choice(location["uncommon"]))
  for item in found:
    self.inventory.add(item)
  print(f"you focus on the Rune of sort")
  print(f"Found: {', '.join(found)}")
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


