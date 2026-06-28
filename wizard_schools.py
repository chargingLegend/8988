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
        "effect": "Burn", "effect_chance": 0.5,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 5, "max_dmg": 13, "effect_chance": 0.6},
          "2": {"min_dmg": 7, "max_dmg": 16, "effect_chance": 0.7},
          "3": {"min_dmg": 9, "max_dmg": 20, "effect_chance": 0.85}
        }
      },
      "Sear": {
        "min_dmg": 3, "max_dmg": 7, "dmg_type": "fire",
        "desc": "a lance of heat lashes {target}. Flesh starts to bubble.",
        "effect": "Scorched", "effect_chance": 0.3,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 4, "max_dmg": 9, "effect_chance": 0.45},
          "2": {"min_dmg": 6, "max_dmg": 12, "effect_chance": 0.6},
          "3": {"min_dmg": 8, "max_dmg": 15, "effect_chance": 0.75}
        }
      },
      "Cinder Ward": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "ward",
        "desc": "embers orbit you. {target} feels the heat.",
        "effect": None,
        "upgrade_level": 0,
        "tiers": {
          "1": {"defense_bonus": 3, "reflect_dmg": 1},
          "2": {"defense_bonus": 5, "reflect_dmg": 2},
          "3": {"defense_bonus": 8, "reflect_dmg": 4}
        }
      },
      "Smelt": {
        "min_dmg": 5, "max_dmg": 12, "dmg_type": "fire",
        "desc": "you try: heat pours into {target}.",
        "effect": "Burn", "effect_chance": 0.6,
        "python_concept": "try/except",
        "resist_threshold": 10,
        "on_resist": "strip",
        "strip_amount": 5,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 6, "max_dmg": 14, "strip_amount": 7},
          "2": {"min_dmg": 8, "max_dmg": 16, "strip_amount": 9},
          "3": {"min_dmg": 10, "max_dmg": 19, "strip_amount": 12}
        }
      },
      "Flashpoint": {
        "min_dmg": 8, "max_dmg": 18, "dmg_type": "fire",
        "desc": "the condition is met. {target} ignites completely.",
        "effect": "Combusting", "effect_chance": 1.0,
        "python_concept": "bool",
        "resist_threshold": 10,
        "on_above_threshold": "fizzle",
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 10, "max_dmg": 21, "resist_threshold": 12},
          "2": {"min_dmg": 12, "max_dmg": 24, "resist_threshold": 15},
          "3": {"min_dmg": 15, "max_dmg": 28, "resist_threshold": 20}
        }
      },
      "Hearthcall": {
        "min_dmg": 3, "max_dmg": 8, "dmg_type": "fire",
        "desc": "the flame remembers where it was sent from.\n"
                "{target} feels it twice — once going, once coming back.",
        "effect": "Burn", "effect_chance": 0.4,
        "python_concept": "return",
        "reflects_last_dmg": True,
        "reflect_percent": 0.5,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 4, "max_dmg": 10, "effect_chance": 0.5, "reflect_percent": 0.6},
          "2": {"min_dmg": 5, "max_dmg": 12, "effect_chance": 0.6, "reflect_percent": 0.75},
          "3": {"min_dmg": 7, "max_dmg": 15, "effect_chance": 0.7, "reflect_percent": 1.0}
        }
      },
      "Flashform": {
        "min_dmg": 6, "max_dmg": 10, "dmg_type": "fire",
        "desc": "a flame with one shape and one purpose.\n"
                "it exists for exactly one moment. then it doesn't.",
        "effect": "Scorched", "effect_chance": 0.75,
        "python_concept": "lambda",
        "single_use_per_combat": True,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 8, "max_dmg": 13, "effect_chance": 0.8},
          "2": {"min_dmg": 10, "max_dmg": 16, "effect_chance": 0.85, "uses_per_combat": 2},
          "3": {"min_dmg": 13, "max_dmg": 20, "effect_chance": 0.9, "uses_per_combat": 3}
        }
      },
      "Judgment Flame": {
        "min_dmg": 2, "max_dmg": 6, "dmg_type": "fire",
        "desc": "the fire reads {target} before it commits.\n"
                "what it finds decides what comes next.",
        "effect": "Burn", "effect_chance": 0.45,
        "python_concept": "if/else",
        "on_already_burning": {
          "min_dmg": 6, "max_dmg": 14, "effect": "Combusting",
          "desc": "it was already burning. the flame finds that acceptable."
        },
        "on_not_burning": {
          "min_dmg": 2, "max_dmg": 6, "effect": "Burn",
          "desc": "it wasn't burning. now it is."
        },
        "upgrade_level": 0,
        "tiers": {
          "1": {"effect_chance": 0.55,
                "on_already_burning": {"min_dmg": 8, "max_dmg": 16}},
          "2": {"effect_chance": 0.65,
                "on_already_burning": {"min_dmg": 10, "max_dmg": 18}},
          "3": {"effect_chance": 0.75,
                "on_already_burning": {"min_dmg": 12, "max_dmg": 20}}
        }
      },
      "Unlit": {
        "min_dmg": 4, "max_dmg": 9, "dmg_type": "fire",
        "desc": "not cold. not dark. just — the thing that kept the fire out\n"
                "is no longer the thing it was.\n"
                "{target} finds it has no answer for what comes next.",
        "effect": "Scorched", "effect_chance": 0.5,
        "python_concept": "not",
        "inverts_resistance": True,
        "resistance_duration": 2,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 5, "max_dmg": 11, "effect_chance": 0.6, "resistance_duration": 3},
          "2": {"min_dmg": 7, "max_dmg": 13, "effect_chance": 0.7, "resistance_duration": 4},
          "3": {"min_dmg": 9, "max_dmg": 16, "effect_chance": 0.8, "resistance_duration": 5,
                "also_inverts": "defense"}
        }
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
        "effect": "Frostbitten", "effect_chance": 0.4,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 4, "max_dmg": 10, "effect_chance": 0.5},
          "2": {"min_dmg": 6, "max_dmg": 13, "effect_chance": 0.65},
          "3": {"min_dmg": 8, "max_dmg": 16, "effect_chance": 0.8}
        }
      },
      "Glaze": {
        "min_dmg": 2, "max_dmg": 4, "dmg_type": "cold",
        "desc": "rime coats {target}. It moves like cold honey.",
        "effect": "Slowed", "effect_chance": 0.6,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 3, "max_dmg": 6, "effect_chance": 0.7},
          "2": {"min_dmg": 4, "max_dmg": 8, "effect_chance": 0.8},
          "3": {"min_dmg": 5, "max_dmg": 10, "effect_chance": 0.9}
        }
      },
      "Shard": {
        "min_dmg": 4, "max_dmg": 9, "dmg_type": "cold",
        "desc": "a spear of ice punches through {target}.",
        "effect": None,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 6, "max_dmg": 12},
          "2": {"min_dmg": 8, "max_dmg": 15, "effect": "Frostbitten", "effect_chance": 0.4},
          "3": {"min_dmg": 10, "max_dmg": 18, "effect": "Frozen", "effect_chance": 0.5}
        }
      },
      "Glacial Grind": {
        "min_dmg": 3, "max_dmg": 6, "dmg_type": "cold",
        "desc": "the cold grinds into {target}. It won't stop until they break.",
        "effect": "Frostbitten", "effect_chance": 0.3,
        "python_concept": "while/break",
        "loop_condition": "target_hp_above_half",
        "break_condition": "target_hp_below_half",
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 4, "max_dmg": 8, "effect_chance": 0.45},
          "2": {"min_dmg": 5, "max_dmg": 10, "effect_chance": 0.6},
          "3": {"min_dmg": 6, "max_dmg": 12, "effect_chance": 0.75,
                "break_condition": "target_hp_below_quarter"}
        }
      },
      "Nullfrost": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "cold",
        "desc": "the frost finds the active force in {target} and sets it to nothing.",
        "effect": None,
        "python_concept": "None",
        "nullifies": "active_status_effect",
        "on_nothing": "return_none",
        "upgrade_level": 0,
        "tiers": {
          "1": {"nullifies": "active_status_effect", "also_slows": True},
          "2": {"nullifies": "two_status_effects"},
          "3": {"nullifies": "all_status_effects", "min_dmg": 3, "max_dmg": 6}
        }
      },
      "The Still": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "cold",
        "desc": "nothing happens. the cold simply waits.\n"
                "{target} waits with it. that was the mistake.",
        "effect": "Slowed", "effect_chance": 0.9,
        "python_concept": "pass",
        "skips_turn": True,
        "next_spell_bonus": 1.5,
        "upgrade_level": 0,
        "tiers": {
          "1": {"next_spell_bonus": 1.75},
          "2": {"next_spell_bonus": 2.0, "effect": "Frozen", "effect_chance": 0.4},
          "3": {"next_spell_bonus": 2.5, "effect": "Frozen", "effect_chance": 0.65}
        }
      },
      "Cold Stride": {
        "min_dmg": 3, "max_dmg": 7, "dmg_type": "cold",
        "desc": "the frost moves through what it doesn't need.\n"
                "it finds {target} at the end of that decision.",
        "effect": "Frostbitten", "effect_chance": 0.45,
        "python_concept": "continue",
        "bypasses_defense": True,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 4, "max_dmg": 9, "effect_chance": 0.55},
          "2": {"min_dmg": 6, "max_dmg": 12, "effect_chance": 0.65},
          "3": {"min_dmg": 8, "max_dmg": 15, "effect_chance": 0.75,
                "also_bypasses": "status_resistance"}
        }
      },
      "Locked State": {
        "min_dmg": 2, "max_dmg": 5, "dmg_type": "cold",
        "desc": "whatever {target} is right now — that is what it stays.\n"
                "nothing changes it while the cold holds.",
        "effect": "Frozen", "effect_chance": 0.5,
        "python_concept": "immutable",
        "seals_current_state": True,
        "seal_duration": 2,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 3, "max_dmg": 7, "seal_duration": 3},
          "2": {"min_dmg": 4, "max_dmg": 9, "seal_duration": 4,
                "prevents_healing": True},
          "3": {"min_dmg": 5, "max_dmg": 11, "seal_duration": 5,
                "prevents_healing": True, "prevents_buff": True}
        }
      },
      "Tally Frost": {
        "min_dmg": 1, "max_dmg": 3, "dmg_type": "cold",
        "desc": "the cold counts. each hit numbered.\n"
                "each one more deliberate than the last.",
        "effect": "Slowed", "effect_chance": 0.3,
        "python_concept": "enumerate",
        "hit_count_bonus": True,
        "bonus_per_hit": 1,
        "max_hits": 4,
        "upgrade_level": 0,
        "tiers": {
          "1": {"max_hits": 5, "bonus_per_hit": 1.5},
          "2": {"max_hits": 6, "bonus_per_hit": 2},
          "3": {"max_hits": 7, "bonus_per_hit": 3,
                "effect_chance": 0.55}
        }
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
        "effect": None,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 3, "max_dmg": 8, "effect": "Stuttered", "effect_chance": 0.3},
          "2": {"min_dmg": 4, "max_dmg": 10, "effect": "Stuttered", "effect_chance": 0.5},
          "3": {"min_dmg": 6, "max_dmg": 12, "effect": "Slowed", "effect_chance": 0.65}
        }
      },
      "Foresight": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "time",
        "desc": "you read {target}'s next beat before it arrives.",
        "effect": "Stuttered", "effect_chance": 1.0,
        "upgrade_level": 0,
        "tiers": {
          "1": {"dodge_next_attack": True},
          "2": {"dodge_next_attack": True, "counter_dmg": 4},
          "3": {"dodge_next_two": True, "counter_dmg": 8}
        }
      },
      "Stutter": {
        "min_dmg": 3, "max_dmg": 7, "dmg_type": "time",
        "desc": "{target} skips a moment. Parts of it arrive late.",
        "effect": "Slowed", "effect_chance": 0.35,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 4, "max_dmg": 9, "effect_chance": 0.5},
          "2": {"min_dmg": 5, "max_dmg": 11, "effect_chance": 0.65},
          "3": {"min_dmg": 7, "max_dmg": 14, "effect_chance": 0.8}
        }
      },
      "Interval": {
        "min_dmg": 2, "max_dmg": 5, "dmg_type": "time",
        "desc": "time fractures into precise beats. Each one finds {target}.",
        "effect": None,
        "python_concept": "range()",
        "hit_range": (1, 4),
        "upgrade_1_range": (1, 6),
        "upgrade_2_range": (1, 8),
        "mana_per_hit": 1,
        "upgrade_level": 0,
        "tiers": {
          "1": {"hit_range": (1, 6), "min_dmg": 3, "max_dmg": 6},
          "2": {"hit_range": (1, 8), "min_dmg": 3, "max_dmg": 7},
          "3": {"hit_range": (2, 8), "min_dmg": 4, "max_dmg": 8}
        }
      },
      "Recurrence": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "time",
        "desc": "the last moment loops. It finds {target} again. And again. And again.",
        "effect": None,
        "python_concept": "for loop",
        "repeat_count": 3,
        "mana_cost_multiplier": 2,
        "requires_last_spell": True,
        "upgrade_level": 0,
        "tiers": {
          "1": {"repeat_count": 4},
          "2": {"repeat_count": 5, "mana_cost_multiplier": 1.5},
          "3": {"repeat_count": 6, "mana_cost_multiplier": 1.0}
        }
      },
      "Measured Breath": {
        "min_dmg": 1, "max_dmg": 4, "dmg_type": "time",
        "desc": "time given out in portions. no more than what is needed.\n"
                "{target} receives exactly what was decided.",
        "effect": "Slowed", "effect_chance": 0.5,
        "python_concept": "yield",
        "controlled_release": True,
        "mana_return_per_turn": 1,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 2, "max_dmg": 5, "mana_return_per_turn": 2},
          "2": {"min_dmg": 3, "max_dmg": 7, "mana_return_per_turn": 3},
          "3": {"min_dmg": 4, "max_dmg": 9, "mana_return_per_turn": 4,
                "effect_chance": 0.7}
        }
      },
      "The Moment That Was Everywhere": {
        "min_dmg": 4, "max_dmg": 8, "dmg_type": "time",
        "desc": "one instant. it touches all things at once.\n"
                "nothing in the field escapes it.",
        "effect": "Stuttered", "effect_chance": 0.6,
        "python_concept": "global",
        "hits_all_enemies": True,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 5, "max_dmg": 10, "effect_chance": 0.7},
          "2": {"min_dmg": 6, "max_dmg": 12, "effect_chance": 0.8},
          "3": {"min_dmg": 8, "max_dmg": 15, "effect_chance": 0.9,
                "effect": "Slowed"}
        }
      },
      "The Echo That Called Itself": {
        "min_dmg": 3, "max_dmg": 6, "dmg_type": "time",
        "desc": "a moment summons the moment before it.\n"
                "which summons the one before that.\n"
                "{target} cannot find where it ends.",
        "effect": "Disoriented", "effect_chance": 0.55,
        "python_concept": "recursion",
        "recursive_hits": 2,
        "dmg_reduction_per_call": 0.15,
        "upgrade_level": 0,
        "tiers": {
          "1": {"recursive_hits": 3, "dmg_reduction_per_call": 0.1},
          "2": {"recursive_hits": 4, "dmg_reduction_per_call": 0.08},
          "3": {"recursive_hits": 5, "dmg_reduction_per_call": 0.05}
        }
      },
      "Right Order": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "time",
        "desc": "events rearrange themselves into the sequence that serves you.\n"
                "{target} finds its advantages arriving in the wrong order.",
        "effect": "Weakened", "effect_chance": 0.7,
        "python_concept": "sorted",
        "reorders_enemy_buffs": True,
        "delays_strongest_buff": 2,
        "upgrade_level": 0,
        "tiers": {
          "1": {"delays_strongest_buff": 3, "min_dmg": 2, "max_dmg": 4},
          "2": {"delays_strongest_buff": 4, "min_dmg": 3, "max_dmg": 6,
                "also_reorders": "attack_pattern"},
          "3": {"delays_strongest_buff": 5, "min_dmg": 4, "max_dmg": 8,
                "reverses_turn_order": True}
        }
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
        "effect": "Weakened", "effect_chance": 0.35,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 4, "max_dmg": 11, "effect_chance": 0.5},
          "2": {"min_dmg": 6, "max_dmg": 13, "effect_chance": 0.65},
          "3": {"min_dmg": 8, "max_dmg": 16, "effect_chance": 0.8}
        }
      },
      "Wither": {
        "min_dmg": 2, "max_dmg": 8, "dmg_type": "necrotic",
        "desc": "vitality flees {target} like startled crows.",
        "effect": None,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 3, "max_dmg": 10, "effect": "Weakened", "effect_chance": 0.4},
          "2": {"min_dmg": 5, "max_dmg": 12, "effect": "Weakened", "effect_chance": 0.55},
          "3": {"min_dmg": 7, "max_dmg": 15, "effect": "Weakened", "effect_chance": 0.7}
        }
      },
      "Gravechill": {
        "min_dmg": 4, "max_dmg": 8, "dmg_type": "necrotic",
        "desc": "the cold of tombs settles in {target}.",
        "effect": "Slowed", "effect_chance": 0.3,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 5, "max_dmg": 10, "effect_chance": 0.45},
          "2": {"min_dmg": 6, "max_dmg": 12, "effect_chance": 0.6},
          "3": {"min_dmg": 8, "max_dmg": 14, "effect_chance": 0.75}
        }
      },
      "Exhume": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "necrotic",
        "desc": "you reach into the dead list. Something stirs.",
        "effect": None,
        "python_concept": "list mutation",
        "pulls_from": "combat_dead_list",
        "revive_hp_percent": 0.3,
        "upgrade_level": 0,
        "tiers": {
          "1": {"revive_hp_percent": 0.4},
          "2": {"revive_hp_percent": 0.5, "revived_atk_bonus": 2},
          "3": {"revive_hp_percent": 0.6, "revived_atk_bonus": 4, "can_revive_two": True}
        }
      },
      "Erasure": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "necrotic",
        "desc": "the key ceases to exist. Not emptied. Gone.",
        "effect": None,
        "python_concept": "del",
        "deletes": "active_buff",
        "on_nothing": "waste",
        "upgrade_level": 0,
        "tiers": {
          "1": {"deletes": "active_buff", "min_dmg": 2, "max_dmg": 4},
          "2": {"deletes": "two_buffs", "min_dmg": 3, "max_dmg": 6},
          "3": {"deletes": "all_buffs", "min_dmg": 4, "max_dmg": 8}
        }
      },
      "Last Pulled": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "necrotic",
        "desc": "whatever died most recently gets one more moment.\n"
                "it uses that moment on {target}.",
        "effect": None,
        "python_concept": "pop()",
        "pulls_last_dead": True,
        "single_strike": True,
        "strike_dmg_formula": "last_dead.atk * 0.75",
        "upgrade_level": 0,
        "tiers": {
          "1": {"strike_dmg_formula": "last_dead.atk * 1.0"},
          "2": {"strike_dmg_formula": "last_dead.atk * 1.25", "can_apply_effect": True},
          "3": {"strike_dmg_formula": "last_dead.atk * 1.5",
                "effect": "Weakened", "effect_chance": 0.6}
        }
      },
      "The Finding": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "necrotic",
        "desc": "you reach into the dead and pull out something specific.\n"
                "not what comes first. what you need.",
        "effect": "Weakened", "effect_chance": 0.5,
        "python_concept": "index()",
        "targets_specific_dead": True,
        "upgrade_level": 0,
        "tiers": {
          "1": {"effect_chance": 0.6, "min_dmg": 2, "max_dmg": 5},
          "2": {"effect_chance": 0.7, "min_dmg": 3, "max_dmg": 7},
          "3": {"effect_chance": 0.85, "min_dmg": 5, "max_dmg": 10,
                "also_copies_ability": True}
        }
      },
      "True Nature": {
        "min_dmg": 3, "max_dmg": 7, "dmg_type": "necrotic",
        "desc": "beneath what {target} appears to be — something older.\n"
                "you check what it actually is. the answer is useful.",
        "effect": "Weakened", "effect_chance": 0.45,
        "python_concept": "isinstance()",
        "reveals_type": True,
        "type_bonus_dmg": 4,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 4, "max_dmg": 9, "type_bonus_dmg": 6},
          "2": {"min_dmg": 6, "max_dmg": 11, "type_bonus_dmg": 8,
                "effect_chance": 0.6},
          "3": {"min_dmg": 8, "max_dmg": 14, "type_bonus_dmg": 12,
                "effect_chance": 0.75, "reveals_weakness": True}
        }
      },
      "Added To The Count": {
        "min_dmg": 2, "max_dmg": 5, "dmg_type": "necrotic",
        "desc": "one more name written into the list.\n"
                "{target} feels the weight of everything already on it.",
        "effect": "Weakened", "effect_chance": 0.4,
        "python_concept": "append",
        "adds_to_dead_list": True,
        "list_dmg_bonus": 1,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 3, "max_dmg": 7, "list_dmg_bonus": 2},
          "2": {"min_dmg": 4, "max_dmg": 9, "list_dmg_bonus": 3},
          "3": {"min_dmg": 5, "max_dmg": 11, "list_dmg_bonus": 4,
                "effect_chance": 0.6}
        }
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
        "effect": None,
        "upgrade_level": 0,
        "tiers": {
          "1": {"defense_bonus": 4, "duration": 2},
          "2": {"defense_bonus": 6, "duration": 3},
          "3": {"defense_bonus": 9, "duration": 3, "reflects_dmg": 2}
        }
      },
      "Surge": {
        "min_dmg": 3, "max_dmg": 8, "dmg_type": "force",
        "desc": "kinetic wrath slams into {target}.",
        "effect": "Weakened", "effect_chance": 0.3,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 4, "max_dmg": 10, "effect_chance": 0.45},
          "2": {"min_dmg": 6, "max_dmg": 13, "effect_chance": 0.6},
          "3": {"min_dmg": 8, "max_dmg": 16, "effect_chance": 0.75}
        }
      },
      "Iron Skin": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "force",
        "desc": "your skin rings like struck steel. {target} notices.",
        "effect": None,
        "upgrade_level": 0,
        "tiers": {
          "1": {"defense_bonus": 5, "duration": 3},
          "2": {"defense_bonus": 8, "duration": 4, "thorns_dmg": 2},
          "3": {"defense_bonus": 12, "duration": 5, "thorns_dmg": 4}
        }
      },
      "Magnitude": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "force",
        "desc": "the number calculates itself. {target} feels the result.",
        "effect": None,
        "python_concept": "integer operations",
        "damage_formula": "int((player.max_hp / player.hp) * base_dmg)",
        "base_dmg": 6,
        "duration": 3,
        "upgrade_level": 0,
        "tiers": {
          "1": {"base_dmg": 8, "duration": 4},
          "2": {"base_dmg": 10, "duration": 5},
          "3": {"base_dmg": 14, "duration": 5, "also_scales_with": "defense"}
        }
      },
      "Surge Stack": {
        "min_dmg": 2, "max_dmg": 4, "dmg_type": "force",
        "desc": "the value compounds. Each cast adds to what came before.",
        "effect": None,
        "python_concept": "+=",
        "stack_bonus": 2,
        "max_stacks": 5,
        "resets_on_damage": True,
        "resets_on_spell_switch": True,
        "upgrade_level": 0,
        "tiers": {
          "1": {"max_stacks": 6, "stack_bonus": 3},
          "2": {"max_stacks": 7, "stack_bonus": 4, "resets_on_damage": False},
          "3": {"max_stacks": 8, "stack_bonus": 5, "resets_on_damage": False,
                "resets_on_spell_switch": False}
        }
      },
      "All Of It": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "force",
        "desc": "nothing held back. {target} receives every calculation at once.",
        "effect": "Weakened", "effect_chance": 0.6,
        "python_concept": "*args",
        "damage_formula": "int((1 - (player.mana / player.max_mana)) * 10) + int(player.atk * 1.2)",
        "upgrade_level": 0,
        "tiers": {
          "1": {"damage_formula": "int((1 - (player.mana / player.max_mana)) * 14) + int(player.atk * 1.3)"},
          "2": {"damage_formula": "int((1 - (player.mana / player.max_mana)) * 18) + int(player.atk * 1.4)"},
          "3": {"damage_formula": "int((1 - (player.mana / player.max_mana)) * 22) + int(player.atk * 1.5)",
                "effect_chance": 0.8}
        }
      },
      "Whole Force": {
        "min_dmg": 5, "max_dmg": 10, "dmg_type": "force",
        "desc": "strength reduced to its purest form. No remainder.\n"
                "{target} receives exactly what the calculation allows.",
        "effect": None,
        "python_concept": "int()",
        "damage_formula": "int(player.atk * 1.5)",
        "upgrade_level": 0,
        "tiers": {
          "1": {"damage_formula": "int(player.atk * 1.75)"},
          "2": {"damage_formula": "int(player.atk * 2.0)",
                "effect": "Weakened", "effect_chance": 0.4},
          "3": {"damage_formula": "int(player.atk * 2.5)",
                "effect": "Weakened", "effect_chance": 0.6}
        }
      },
      "Ceiling": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "force",
        "desc": "whatever the highest value is — that becomes the only value.\n"
                "{target}'s floor rises to meet what it cannot exceed.",
        "effect": None,
        "python_concept": "max()",
        "sets_atk_to_max": True,
        "duration": 3,
        "upgrade_level": 0,
        "tiers": {
          "1": {"duration": 4, "also_sets_defense": True},
          "2": {"duration": 5, "also_sets_defense": True, "min_dmg": 3, "max_dmg": 6},
          "3": {"duration": 5, "also_sets_defense": True, "min_dmg": 5, "max_dmg": 10,
                "damage_formula": "int(max(player.atk, player.defense) * 1.5)"}
        }
      },
      "True Weight": {
        "min_dmg": 4, "max_dmg": 8, "dmg_type": "force",
        "desc": "the sign is removed. only the magnitude remains.\n"
                "{target}'s defense becomes its burden.",
        "effect": "Weakened", "effect_chance": 0.5,
        "python_concept": "abs()",
        "damage_formula": "int(enemy.defense * 0.5) + base_dmg",
        "base_dmg": 4,
        "upgrade_level": 0,
        "tiers": {
          "1": {"damage_formula": "int(enemy.defense * 0.65) + base_dmg", "effect_chance": 0.6},
          "2": {"damage_formula": "int(enemy.defense * 0.8) + base_dmg", "effect_chance": 0.7},
          "3": {"damage_formula": "int(enemy.defense * 1.0) + base_dmg", "effect_chance": 0.8}
        }
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
        "effect": "Shattered", "effect_chance": 0.3,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 3, "max_dmg": 8, "effect_chance": 0.45},
          "2": {"min_dmg": 4, "max_dmg": 10, "effect_chance": 0.6},
          "3": {"min_dmg": 6, "max_dmg": 13, "effect_chance": 0.75}
        }
      },
      "Mutter": {
        "min_dmg": 2, "max_dmg": 5, "dmg_type": "psychic",
        "desc": "whispers convince {target} it is already wounded.",
        "effect": "Weakened", "effect_chance": 0.4,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 3, "max_dmg": 7, "effect_chance": 0.55},
          "2": {"min_dmg": 4, "max_dmg": 9, "effect_chance": 0.7},
          "3": {"min_dmg": 5, "max_dmg": 11, "effect_chance": 0.8}
        }
      },
      "False Step": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "psychic",
        "desc": "{target} misjudges distance. Its next move commits to nothing.",
        "effect": "Shattered", "effect_chance": 0.65,
        "upgrade_level": 0,
        "tiers": {
          "1": {"effect_chance": 0.75, "min_dmg": 1, "max_dmg": 3},
          "2": {"effect_chance": 0.85, "min_dmg": 2, "max_dmg": 5},
          "3": {"effect_chance": 0.95, "min_dmg": 3, "max_dmg": 7,
                "next_attack_misses": True}
        }
      },
      "Mirage": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "psychic",
        "desc": "{target}'s strength is not what it believes it to be.",
        "effect": None,
        "python_concept": "variable reassignment",
        "reassigns": "atk",
        "new_value_formula": "int(target.atk * 0.5)",
        "duration": 3,
        "upgrade_level": 0,
        "tiers": {
          "1": {"new_value_formula": "int(target.atk * 0.4)", "duration": 4},
          "2": {"new_value_formula": "int(target.atk * 0.3)", "duration": 5},
          "3": {"new_value_formula": "int(target.atk * 0.2)", "duration": 5,
                "also_reassigns": "defense"}
        }
      },
      "Doppel": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "psychic",
        "desc": "something steps beside you. It looks exactly like you. It is not you.",
        "effect": None,
        "python_concept": "is vs ==",
        "spawn_chance_base": 0.5,
        "hits_absorbed_base": 1,
        "upgrade_level": 0,
        "tiers": {
          "1": {"spawn_chance_base": 0.75, "hits_absorbed_base": 2},
          "2": {"spawn_chance_base": 1.0, "hits_absorbed_base": 3},
          "3": {"spawn_chance_base": 1.0, "hits_absorbed_base": 4,
                "doppel_strikes_back": True}
        }
      },
      "The Convincing Absence": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "psychic",
        "desc": "{target} believes something stands between you.\n"
                "it isn't there. but the belief does what the object would have.",
        "effect": "Shattered", "effect_chance": 0.7,
        "python_concept": "None",
        "creates_false_obstacle": True,
        "obstacle_duration": 2,
        "upgrade_level": 0,
        "tiers": {
          "1": {"obstacle_duration": 3, "effect_chance": 0.8},
          "2": {"obstacle_duration": 4, "effect_chance": 0.85,
                "min_dmg": 2, "max_dmg": 5},
          "3": {"obstacle_duration": 5, "effect_chance": 0.9,
                "min_dmg": 3, "max_dmg": 7, "also_weakens": True}
        }
      },
      "Already There": {
        "min_dmg": 3, "max_dmg": 7, "dmg_type": "psychic",
        "desc": "the illusion was inside {target} before it looked.\n"
                "it has been there since before this fight began.",
        "effect": "Disoriented", "effect_chance": 0.6,
        "python_concept": "in",
        "bypasses_mental_resistance": True,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 4, "max_dmg": 9, "effect_chance": 0.7},
          "2": {"min_dmg": 5, "max_dmg": 11, "effect_chance": 0.8},
          "3": {"min_dmg": 7, "max_dmg": 14, "effect_chance": 0.9,
                "effect": "Shattered"}
        }
      },
      "The Other One": {
        "min_dmg": 2, "max_dmg": 6, "dmg_type": "psychic",
        "desc": "something that looks identical arrives.\n"
                "it is not the same thing. {target} cannot tell the difference.",
        "effect": "Disoriented", "effect_chance": 0.55,
        "python_concept": "copy",
        "spawns_copy": True,
        "copy_inherits_last_spell": True,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 3, "max_dmg": 8, "effect_chance": 0.65},
          "2": {"min_dmg": 4, "max_dmg": 10, "effect_chance": 0.75,
                "copy_acts_independently": True},
          "3": {"min_dmg": 5, "max_dmg": 12, "effect_chance": 0.85,
                "spawns_two_copies": True}
        }
      },
      "Certainty": {
        "min_dmg": 4, "max_dmg": 9, "dmg_type": "psychic",
        "desc": "the illusion becomes so complete {target} accepts it as fact.\n"
                "once accepted it cannot be questioned.",
        "effect": "Shattered", "effect_chance": 0.65,
        "python_concept": "assert",
        "locks_belief": True,
        "belief_duration": 3,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 5, "max_dmg": 11, "belief_duration": 4},
          "2": {"min_dmg": 6, "max_dmg": 13, "belief_duration": 5,
                "effect_chance": 0.75},
          "3": {"min_dmg": 8, "max_dmg": 16, "belief_duration": 5,
                "effect_chance": 0.85, "prevents_dispel": True}
        }
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
        "effect": None,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 2, "max_dmg": 5, "effect": "Weakened", "effect_chance": 0.3},
          "2": {"min_dmg": 3, "max_dmg": 7, "effect_chance": 0.45},
          "3": {"min_dmg": 4, "max_dmg": 9, "effect_chance": 0.6,
                "pulls_target_closer": True}
        }
      },
      "Shardling": {
        "min_dmg": 3, "max_dmg": 9, "dmg_type": "force",
        "desc": "a conjured splinter hurls into {target}.",
        "effect": None,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 4, "max_dmg": 11, "effect": "Weakened", "effect_chance": 0.3},
          "2": {"min_dmg": 6, "max_dmg": 14, "effect_chance": 0.45},
          "3": {"min_dmg": 8, "max_dmg": 17, "effect_chance": 0.6,
                "spawns_second_shardling": True}
        }
      },
      "Bind": {
        "min_dmg": 2, "max_dmg": 6, "dmg_type": "force",
        "desc": "invisible cords seize {target}'s limbs.",
        "effect": "Slowed", "effect_chance": 0.55,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 3, "max_dmg": 8, "effect_chance": 0.65},
          "2": {"min_dmg": 4, "max_dmg": 10, "effect_chance": 0.75,
                "also_weakens": True},
          "3": {"min_dmg": 5, "max_dmg": 12, "effect_chance": 0.85,
                "effect": "Shattered"}
        }
      },
      "Summon Stack": {
        "min_dmg": 1, "max_dmg": 2, "dmg_type": "force",
        "desc": "something is appended to the field. Then another. They chip away at {target}.",
        "effect": None,
        "python_concept": "list.append()",
        "stack_list": [],
        "max_stack": 3,
        "chip_dmg_per_entity": 2,
        "upgrade_level": 0,
        "tiers": {
          "1": {"max_stack": 4, "chip_dmg_per_entity": 3},
          "2": {"max_stack": 5, "chip_dmg_per_entity": 4},
          "3": {"max_stack": 6, "chip_dmg_per_entity": 5,
                "entities_act_independently": True}
        }
      },
      "Threshold": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "force",
        "desc": "the count is taken. {target} feels the weight of every carried thing.",
        "effect": None,
        "python_concept": "len()",
        "damage_formula": "len(player.inventory.items) * multiplier",
        "multiplier": 3,
        "upgrade_level": 0,
        "tiers": {
          "1": {"multiplier": 4},
          "2": {"multiplier": 5, "also_counts_spells": True},
          "3": {"multiplier": 6, "also_counts_spells": True,
                "also_counts_flags": True}
        }
      },
      "Paired Arrival": {
        "min_dmg": 2, "max_dmg": 5, "dmg_type": "force",
        "desc": "two things summoned together. bound to each other.\n"
                "what one does the other mirrors on {target}.",
        "effect": None,
        "python_concept": "zip",
        "paired_strike": True,
        "second_strike_percent": 0.6,
        "upgrade_level": 0,
        "tiers": {
          "1": {"second_strike_percent": 0.75, "min_dmg": 3, "max_dmg": 7},
          "2": {"second_strike_percent": 0.9, "min_dmg": 4, "max_dmg": 9},
          "3": {"second_strike_percent": 1.0, "min_dmg": 5, "max_dmg": 11,
                "third_strike_percent": 0.5}
        }
      },
      "The Catalogue": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "force",
        "desc": "every summoned thing stored, named, retrievable.\n"
                "{target} faces what was filed away for exactly this moment.",
        "effect": "Weakened", "effect_chance": 0.5,
        "python_concept": "dict",
        "accesses_stored_summons": True,
        "bonus_per_stored": 2,
        "upgrade_level": 0,
        "tiers": {
          "1": {"bonus_per_stored": 3, "effect_chance": 0.6},
          "2": {"bonus_per_stored": 4, "effect_chance": 0.7,
                "min_dmg": 2, "max_dmg": 5},
          "3": {"bonus_per_stored": 5, "effect_chance": 0.8,
                "min_dmg": 4, "max_dmg": 8, "releases_all_stored": True}
        }
      },
      "Called From Elsewhere": {
        "min_dmg": 4, "max_dmg": 10, "dmg_type": "force",
        "desc": "something brought in from outside the current space.\n"
                "it did not originate here. {target} has no defense against what it doesn't recognize.",
        "effect": "Disoriented", "effect_chance": 0.55,
        "python_concept": "import",
        "bypasses_known_resistances": True,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 5, "max_dmg": 12, "effect_chance": 0.65},
          "2": {"min_dmg": 7, "max_dmg": 15, "effect_chance": 0.75},
          "3": {"min_dmg": 9, "max_dmg": 18, "effect_chance": 0.85,
                "also_bypasses": "defense"}
        }
      },
      "Bound Pair": {
        "min_dmg": 3, "max_dmg": 7, "dmg_type": "force",
        "desc": "two conjured things locked together.\n"
                "neither changeable alone. {target} cannot address one without the other.",
        "effect": "Slowed", "effect_chance": 0.5,
        "python_concept": "tuple",
        "locks_two_debuffs": True,
        "debuff_duration": 3,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 4, "max_dmg": 9, "debuff_duration": 4},
          "2": {"min_dmg": 5, "max_dmg": 11, "debuff_duration": 5,
                "effect_chance": 0.65},
          "3": {"min_dmg": 7, "max_dmg": 14, "debuff_duration": 5,
                "effect_chance": 0.8, "prevents_dispel": True}
        }
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
        "cooldown_key": "dim", "cooldown_turns": 3,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 2, "max_dmg": 5, "cooldown_turns": 2},
          "2": {"min_dmg": 3, "max_dmg": 7, "cooldown_turns": 1},
          "3": {"min_dmg": 4, "max_dmg": 9, "cooldown_turns": 0,
                "effect_chance": 0.9}
        }
      },
      "Mutter": {
        "min_dmg": 2, "max_dmg": 7, "dmg_type": "shadow",
        "desc": "dark words eat at {target}'s resolve.",
        "effect": "Weakened", "effect_chance": 0.4,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 3, "max_dmg": 9, "effect_chance": 0.55},
          "2": {"min_dmg": 4, "max_dmg": 11, "effect_chance": 0.7},
          "3": {"min_dmg": 6, "max_dmg": 14, "effect_chance": 0.8}
        }
      },
      "Veil": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "shadow",
        "desc": "you cease to be a target. {target} loses you.",
        "effect": None,
        "upgrade_level": 0,
        "tiers": {
          "1": {"dodge_chance": 0.4, "duration": 2},
          "2": {"dodge_chance": 0.6, "duration": 3},
          "3": {"dodge_chance": 0.8, "duration": 3, "counter_on_dodge": True}
        }
      },
      "Voidcheck": {
        "min_dmg": 6, "max_dmg": 14, "dmg_type": "shadow",
        "desc": "you search {target} for the empty places. Then reach inside them.",
        "effect": None,
        "python_concept": "None check",
        "check_for": "None_attribute",
        "on_found": "massive_damage",
        "on_not_found": "set_weakest_to_none_then_minor_damage",
        "minor_dmg": 3,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 8, "max_dmg": 17, "minor_dmg": 4},
          "2": {"min_dmg": 10, "max_dmg": 20, "minor_dmg": 6},
          "3": {"min_dmg": 12, "max_dmg": 24, "minor_dmg": 8,
                "creates_none_attribute": True}
        }
      },
      "Shred": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "shadow",
        "desc": "you take the middle out of {target}'s name. What remains is a curse.",
        "effect": "Weakened", "effect_chance": 0.8,
        "python_concept": "string slicing [start:end]",
        "slice_start": 1,
        "slice_end": -1,
        "damage_formula": "len(target.name[1:-1]) * 2",
        "upgrade_level": 0,
        "tiers": {
          "1": {"damage_formula": "len(target.name[1:-1]) * 3"},
          "2": {"damage_formula": "len(target.name[1:-1]) * 4",
                "slice_start": 0, "slice_end": -2},
          "3": {"damage_formula": "len(target.name[1:-1]) * 5",
                "effect": "Disoriented", "effect_chance": 0.7}
        }
      },
      "The Nothing Done": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "shadow",
        "desc": "shadow moves through without acting.\n"
                "it leaves something behind anyway.\n"
                "{target} finds it later.",
        "effect": "Weakened", "effect_chance": 0.6,
        "python_concept": "pass",
        "delayed_dmg": 5,
        "delay_turns": 2,
        "upgrade_level": 0,
        "tiers": {
          "1": {"delayed_dmg": 7, "delay_turns": 2},
          "2": {"delayed_dmg": 10, "delay_turns": 2, "effect_chance": 0.7},
          "3": {"delayed_dmg": 14, "delay_turns": 1, "effect_chance": 0.8}
        }
      },
      "Everywhere Dark": {
        "min_dmg": 2, "max_dmg": 5, "dmg_type": "shadow",
        "desc": "shadow that doesn't stay in one place.\n"
                "every corner of the field carries a piece of it.",
        "effect": "Disoriented", "effect_chance": 0.5,
        "python_concept": "global",
        "applies_to_all_enemies": True,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 3, "max_dmg": 7, "effect_chance": 0.6},
          "2": {"min_dmg": 4, "max_dmg": 9, "effect_chance": 0.7},
          "3": {"min_dmg": 5, "max_dmg": 11, "effect_chance": 0.8,
                "persists_after_cast": True}
        }
      },
      "The Unseen": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "shadow",
        "desc": "you are confirmed absent from where they are looking.\n"
                "{target} strikes where you are not.",
        "effect": None,
        "python_concept": "not in",
        "removes_from_target_list": True,
        "duration": 2,
        "upgrade_level": 0,
        "tiers": {
          "1": {"duration": 3, "counter_dmg": 3},
          "2": {"duration": 4, "counter_dmg": 5},
          "3": {"duration": 4, "counter_dmg": 8,
                "removes_from_all_target_lists": True}
        }
      },
      "Cut": {
        "min_dmg": 5, "max_dmg": 11, "dmg_type": "shadow",
        "desc": "whatever was running — stops.\n"
                "clean. no wind down. no warning.\n"
                "{target}'s momentum ends here.",
        "effect": "Slowed", "effect_chance": 0.7,
        "python_concept": "break",
        "cancels_active_effect": True,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 7, "max_dmg": 14, "effect_chance": 0.8},
          "2": {"min_dmg": 9, "max_dmg": 17, "effect_chance": 0.85,
                "cancels_two_effects": True},
          "3": {"min_dmg": 11, "max_dmg": 20, "effect_chance": 0.9,
                "cancels_all_effects": True, "prevents_new_buffs": True}
        }
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
        "effect": "Weakened", "effect_chance": 0.35,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 3, "max_dmg": 9, "effect_chance": 0.5},
          "2": {"min_dmg": 5, "max_dmg": 11, "effect_chance": 0.65},
          "3": {"min_dmg": 7, "max_dmg": 14, "effect_chance": 0.8}
        }
      },
      "Harden": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "arcane",
        "desc": "air becomes stone around you. {target} feels the shift.",
        "effect": None,
        "upgrade_level": 0,
        "tiers": {
          "1": {"defense_bonus": 5, "duration": 3},
          "2": {"defense_bonus": 8, "duration": 4},
          "3": {"defense_bonus": 12, "duration": 4, "min_dmg": 3, "max_dmg": 6}
        }
      },
      "Gild": {
        "min_dmg": 3, "max_dmg": 8, "dmg_type": "arcane",
        "desc": "{target}'s edges turn brittle-gold, then crack.",
        "effect": "Weakened", "effect_chance": 0.45,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 4, "max_dmg": 10, "effect_chance": 0.55},
          "2": {"min_dmg": 6, "max_dmg": 13, "effect_chance": 0.65},
          "3": {"min_dmg": 8, "max_dmg": 16, "effect_chance": 0.75}
        }
      },
      "Recast": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "arcane",
        "desc": "the type of {target} changes. What was solid becomes something else entirely.",
        "effect": None,
        "python_concept": "type casting int()/float()/str()",
        "decay_multiplier": 0.85,
        "cycles": 2,
        "upgrade_level": 0,
        "tiers": {
          "1": {"cycles": 3, "decay_multiplier": 0.8},
          "2": {"cycles": 4, "decay_multiplier": 0.75},
          "3": {"cycles": 5, "decay_multiplier": 0.65,
                "also_changes_dmg_type": True}
        }
      },
      "Overwrite": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "arcane",
        "desc": "the old value is gone. A new one takes its place.\n"
                "{target} does not understand why.",
        "effect": "Weakened", "effect_chance": 1.0,
        "python_concept": "dict.update()",
        "overwrites": "random_combat_stat",
        "debuff_multiplier": 0.6,
        "duration": 3,
        "upgrade_level": 0,
        "tiers": {
          "1": {"debuff_multiplier": 0.5, "duration": 4},
          "2": {"debuff_multiplier": 0.4, "duration": 5,
                "overwrites": "two_combat_stats"},
          "3": {"debuff_multiplier": 0.3, "duration": 5,
                "overwrites": "all_combat_stats"}
        }
      },
      "Between States": {
        "min_dmg": 3, "max_dmg": 7, "dmg_type": "arcane",
        "desc": "matter that cannot decide what it is.\n"
                "{target} is held in decimal existence — not quite anything.",
        "effect": "Disoriented", "effect_chance": 0.6,
        "python_concept": "float()",
        "held_in_transition": True,
        "transition_duration": 2,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 4, "max_dmg": 9, "transition_duration": 3},
          "2": {"min_dmg": 5, "max_dmg": 11, "transition_duration": 4,
                "effect_chance": 0.7},
          "3": {"min_dmg": 7, "max_dmg": 14, "transition_duration": 4,
                "effect_chance": 0.8, "prevents_state_resolution": True}
        }
      },
      "Settled Form": {
        "min_dmg": 4, "max_dmg": 9, "dmg_type": "arcane",
        "desc": "matter forced to commit to the nearest whole state.\n"
                "{target}'s ambiguity ends here.",
        "effect": "Weakened", "effect_chance": 0.55,
        "python_concept": "round()",
        "forces_commitment": True,
        "locks_current_state": True,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 5, "max_dmg": 11, "effect_chance": 0.65},
          "2": {"min_dmg": 7, "max_dmg": 14, "effect_chance": 0.75,
                "also_rounds_down_defense": True},
          "3": {"min_dmg": 9, "max_dmg": 17, "effect_chance": 0.85,
                "rounds_down_all_stats": True}
        }
      },
      "Exchange": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "arcane",
        "desc": "two properties trade places.\n"
                "{target}'s greatest strength becomes its new weakness.",
        "effect": None,
        "python_concept": "swap",
        "swaps_atk_defense": True,
        "duration": 3,
        "upgrade_level": 0,
        "tiers": {
          "1": {"duration": 4, "min_dmg": 2, "max_dmg": 5},
          "2": {"duration": 5, "min_dmg": 3, "max_dmg": 7,
                "swap_is_permanent": False},
          "3": {"duration": 5, "min_dmg": 4, "max_dmg": 9,
                "also_swaps_hp_and_mana": True}
        }
      },
      "Divided": {
        "min_dmg": 3, "max_dmg": 8, "dmg_type": "arcane",
        "desc": "one thing becomes two lesser things.\n"
                "{target} finds itself facing the pieces of what it was.",
        "effect": "Weakened", "effect_chance": 0.5,
        "python_concept": "split()",
        "splits_enemy_atk": True,
        "split_percent": 0.5,
        "upgrade_level": 0,
        "tiers": {
          "1": {"min_dmg": 4, "max_dmg": 10, "split_percent": 0.4},
          "2": {"min_dmg": 5, "max_dmg": 12, "split_percent": 0.35,
                "effect_chance": 0.65},
          "3": {"min_dmg": 7, "max_dmg": 15, "split_percent": 0.25,
                "effect_chance": 0.8, "splits_defense_too": True}
        }
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
      "Smelt": {
        "min_dmg": 5, "max_dmg": 12, "dmg_type": "fire",
        "desc": "you try: heat pours into {target}.",
        "effect": "Burn", "effect_chance": 0.6,
        "python_concept": "try/except",
        "resist_threshold": 10, "on_resist": "strip",
        "strip_amount": 5, "upgrade_level": 0
      },
      "Flashpoint": {
        "min_dmg": 8, "max_dmg": 18, "dmg_type": "fire",
        "desc": "the condition is met. {target} ignites completely.",
        "effect": "Combusting", "effect_chance": 1.0,
        "python_concept": "bool",
        "resist_threshold": 10,
        "on_above_threshold": "fizzle", "upgrade_level": 0
      },
    }
  },
  "Cryomancy": {
    "spells": {
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
      "Glacial Grind": {
        "min_dmg": 3, "max_dmg": 6, "dmg_type": "cold",
        "desc": "the cold grinds into {target}. It won't stop until they break.",
        "effect": "Frostbitten", "effect_chance": 0.3,
        "python_concept": "while/break",
        "loop_condition": "target_hp_above_half",
        "break_condition": "target_hp_below_half", "upgrade_level": 0
      },
      "Nullfrost": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "cold",
        "desc": "the frost finds the active force in {target} and sets it to nothing.",
        "effect": None,
        "python_concept": "None",
        "nullifies": "active_status_effect",
        "on_nothing": "return_none", "upgrade_level": 0
      },
    }
  },
  "Chronomancy": {
    "spells": {
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
      "Interval": {
        "min_dmg": 2, "max_dmg": 5, "dmg_type": "time",
        "desc": "time fractures into precise beats. Each one finds {target}.",
        "effect": None,
        "python_concept": "range()",
        "hit_range": (1, 4), "upgrade_1_range": (1, 6),
        "upgrade_2_range": (1, 8), "mana_per_hit": 1, "upgrade_level": 0
      },
      "Recurrence": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "time",
        "desc": "the last moment loops. It finds {target} again. And again. And again.",
        "effect": None,
        "python_concept": "for loop",
        "repeat_count": 3, "mana_cost_multiplier": 2,
        "requires_last_spell": True, "upgrade_level": 0
      },
    }
  },
  "Necromancy": {
    "spells": {
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
      "Exhume": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "necrotic",
        "desc": "you reach into the dead list. Something stirs.",
        "effect": None,
        "python_concept": "list mutation",
        "pulls_from": "combat_dead_list",
        "revive_hp_percent": 0.3, "upgrade_level": 0
      },
      "Erasure": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "necrotic",
        "desc": "the key ceases to exist. Not emptied. Gone.",
        "effect": None,
        "python_concept": "del",
        "deletes": "active_buff",
        "on_nothing": "waste", "upgrade_level": 0
      },
    }
  },
  "Enhancement": {
    "spells": {
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
      "Magnitude": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "force",
        "desc": "the number calculates itself. {target} feels the result.",
        "effect": None,
        "python_concept": "integer operations",
        "damage_formula": "int((player.max_hp / player.hp) * base_dmg)",
        "base_dmg": 6, "duration": 3,
        "upgrade_1_duration": 4, "upgrade_2_duration": 5,
        "upgrade_2_multiplier_ceiling": 4, "upgrade_level": 0
      },
      "Surge Stack": {
        "min_dmg": 2, "max_dmg": 4, "dmg_type": "force",
        "desc": "the value compounds. Each cast adds to what came before.",
        "effect": None,
        "python_concept": "+=",
        "stack_bonus": 2, "max_stacks": 5,
        "resets_on_damage": True, "resets_on_spell_switch": True,
        "requires_ally_status_type": True, "upgrade_level": 0
      },
    }
  },
  "Illusion": {
    "spells": {
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
      "Mirage": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "psychic",
        "desc": "{target}'s strength is not what it believes it to be.",
        "effect": None,
        "python_concept": "variable reassignment",
        "reassigns": "atk",
        "new_value_formula": "int(target.atk * 0.5)",
        "duration": 3, "upgrade_level": 0
      },
      "Doppel": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "psychic",
        "desc": "something steps beside you. It looks exactly like you. It is not you.",
        "effect": None,
        "python_concept": "is vs ==",
        "spawn_chance_base": 0.5, "upgrade_1_chance": 0.75,
        "upgrade_2_chance": 1.0, "hits_absorbed_base": 1,
        "upgrade_1_hits": 2, "upgrade_2_hits": 3, "upgrade_level": 0
      },
    }
  },
  "Conjuration": {
    "spells": {
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
      "Summon Stack": {
        "min_dmg": 1, "max_dmg": 2, "dmg_type": "force",
        "desc": "something is appended to the field. Then another. They chip away at {target}.",
        "effect": None,
        "python_concept": "list.append()",
        "stack_list": [], "max_stack": 3,
        "chip_dmg_per_entity": 2, "upgrade_level": 0
      },
      "Threshold": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "force",
        "desc": "the count is taken. {target} feels the weight of every carried thing.",
        "effect": None,
        "python_concept": "len()",
        "damage_formula": "len(player.inventory.items) * multiplier",
        "multiplier": 3, "upgrade_level": 0
      },
    }
  },
  "Shadow": {
    "spells": {
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
      "Voidcheck": {
        "min_dmg": 6, "max_dmg": 14, "dmg_type": "shadow",
        "desc": "you search {target} for the empty places. Then reach inside them.",
        "effect": None,
        "python_concept": "None check",
        "check_for": "None_attribute",
        "on_found": "massive_damage",
        "on_not_found": "set_weakest_to_none_then_minor_damage",
        "minor_dmg": 3, "upgrade_level": 0
      },
      "Shred": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "shadow",
        "desc": "you take the middle out of {target}'s name. What remains is a curse.",
        "effect": "Weakened", "effect_chance": 0.8,
        "python_concept": "string slicing [start:end]",
        "slice_start": 1, "slice_end": -1,
        "damage_formula": "len(target.name[1:-1]) * 2", "upgrade_level": 0
      },
    }
  },
  "Transmutation": {
    "spells": {
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
      "Recast": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "arcane",
        "desc": "the type of {target} changes. What was solid becomes something else entirely.",
        "effect": None,
        "python_concept": "type casting int()/float()/str()",
        "decay_multiplier": 0.85, "cycles": 2, "upgrade_level": 0
      },
      "Overwrite": {
        "min_dmg": 0, "max_dmg": 0, "dmg_type": "arcane",
        "desc": "the old value is gone. A new one takes its place. {target} does not understand why.",
        "effect": "Weakened", "effect_chance": 1.0,
        "python_concept": "dict.update()",
        "overwrites": "random_combat_stat",
        "debuff_multiplier": 0.6, "duration": 3, "upgrade_level": 0
      },
    }
  },
}