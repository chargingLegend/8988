import random
from wizard import Wizard
from combat import simple_combat
from entities.monster import RavenSwarm
from entities.humanoid import DesperateTraveler, Enforcer, FrightenedWoman
from items import (HPPotion, ManaPotion, ManabdaPotion, PassRune,
                   ExceptVial, FinallyFlask, Cloak, Staff, Rod, Scepter)
from merchant import Maren


SPELL_DESCRIPTIONS = {
  "Pyromancy": {
    "Ignite": (
      "Fire finds purchase on anything that breathes.",
      "(Deals 3-8 fire damage. 50% chance to apply Burn — 5 damage per turn for 3 turns.)"
    ),
    "Sear": (
      "A lance of concentrated heat. Less elegant. More honest.",
      "(Deals 2-5 fire damage.)"
    ),
    "Cinder Ward": (
      "The air around you warps. Let them wonder what it costs.",
      "(No damage. Defensive ward. Embers orbit you.)"
    ),
  },
  "Cryomancy": {
    "Frostbite": (
      "Cold that remembers where it's been.",
      "(Deals 2-6 cold damage.)"
    ),
    "Glaze": (
      "Rime coats the target. Everything slows.",
      "(Deals 1-3 cold damage. Target movement impaired.)"
    ),
    "Shard": (
      "Ice doesn't ask permission.",
      "(Deals 3-7 cold damage.)"
    ),
  },
  "Chronomancy": {
    "Hesitate": (
      "A moment stolen. Never returned.",
      "(Deals 1-4 time damage. Target stutters.)"
    ),
    "Foresight": (
      "You see the next beat before it arrives.",
      "(No damage. Reveals target's next action.)"
    ),
    "Stutter": (
      "Parts of the target arrive late.",
      "(Deals 2-5 time damage.)"
    ),
  },
  "Necromancy": {
    "Rattle": (
      "Bones remember the grave. You remind them.",
      "(Deals 2-7 necrotic damage.)"
    ),
    "Wither": (
      "Vitality flees like it has somewhere better to be.",
      "(Deals 1-6 necrotic damage.)"
    ),
    "Gravechill": (
      "The cold of tombs is patient. You aren't.",
      "(Deals 3-6 necrotic damage.)"
    ),
  },
  "Enhancement": {
    "Brace": (
      "You root yourself. The mountain has nothing on you.",
      "(No damage. Defensive stance. Reduces incoming damage.)"
    ),
    "Surge": (
      "Kinetic wrath. Simple. Effective.",
      "(Deals 2-6 force damage.)"
    ),
    "Iron Skin": (
      "Your skin rings like struck steel.",
      "(No damage. Temporary armor buff.)"
    ),
  },
  "Illusion": {
    "Phantom": (
      "Give them something worse than you to fight.",
      "(Deals 1-4 psychic damage. Target strikes at phantoms.)"
    ),
    "Mutter": (
      "Whispers convince the target it is already losing.",
      "(Deals 1-3 psychic damage.)"
    ),
    "False Step": (
      "Distance becomes a lie. They believe it.",
      "(No damage. Target misjudges position.)"
    ),
  },
  "Conjuration": {
    "Fetch": (
      "You reach across space. Not there yet.",
      "(No damage. Retrieves distant objects.)"
    ),
    "Shardling": (
      "A conjured splinter. Small. Fast. Angry.",
      "(Deals 2-7 force damage.)"
    ),
    "Bind": (
      "Invisible cords. Very visible results.",
      "(Deals 1-4 force damage. Target movement restricted.)"
    ),
  },
  "Shadow": {
    "Dim": (
      "Light doesn't belong everywhere.",
      "(No damage. Removes target from combat visibility.)"
    ),
    "Mutter": (
      "Dark words find the cracks in resolve.",
      "(Deals 1-5 shadow damage.)"
    ),
    "Veil": (
      "You cease to be a target. For a moment.",
      "(No damage. You become untargetable for one turn.)"
    ),
  },
  "Transmutation": {
    "Shift": (
      "Mass forgets itself. Briefly.",
      "(Deals 1-5 arcane damage.)"
    ),
    "Harden": (
      "Air becomes stone. Not at them. At you.",
      "(No damage. Temporary defense buff.)"
    ),
    "Gild": (
      "Gold is brittle. They learn this firsthand.",
      "(Deals 2-6 arcane damage. Target becomes brittle.)"
    ),
  },
}

ABILITY_DESCRIPTIONS = {
  "Pyromancy": {
    "pyromancy_burn": (
      "Heat is a conversation. You decide how it ends.",
      "(Costs 2-all manabda. Applies Burn, Scorched, or Combusting based on heat poured vs target resistance.)"
    ),
    "map_fire": (
      "Fire doesn't pick favorites. Neither do you.",
      "(Costs 3 manabda. Deals fire damage to ALL enemies simultaneously. 40% chance to apply Burn per target.)"
    ),
    "reduce_ash": (
      "Some things don't need defeating. Just ending.",
      "(Costs 5 manabda. Instantly kills targets at 8 HP or below. Halves HP of stronger targets.)"
    ),
  },
  "Chronomancy": {
    "fast_forward_time": (
      "Age is a weapon. You just learned how to swing it.",
      "(Costs 3-all mana. Advances target's age. Weakens or destroys based on years pushed.)"
    ),
    "rewind_time": (
      "What was can be unmade. What is can be unwound.",
      "(Costs 3-all mana. Regresses target's age. Makes them younger — and more dangerous, or helpless.)"
    ),
  },
  "Cryomancy": {
    "freeze": (
      "Motion is a privilege. You revoke it.",
      "(Costs 4 manabda. Encases target in ice. Frozen targets cannot act.)"
    ),
    "cryo_preserve": (
      "Lock the moment. Nothing changes inside it.",
      "(Costs 6 manabda. Seals target in cryo-stasis. Suspends all status changes for 2 turns.)"
    ),
  },
  "Necromancy": {
    "raise_dead": (
      "Death is a door. You have a key.",
      "(Costs 3 manabda. Raises a fallen enemy as your ally at half HP.)"
    ),
    "decay": (
      "Strip what holds them together. Watch what's left.",
      "(Costs 2-3 manabda. Permanently removes defense or attack attribute from target.)"
    ),
    "animate": (
      "What fell can rise. Diminished. Obedient.",
      "(Costs level x2 manabda. Animates a corpse template as a servant at half HP.)"
    ),
  },
  "Enhancement": {
    "amplify": (
      "More. Always more. The well agrees.",
      "(Costs 1+ manabda. Multiplies next strike by manabda spent.)"
    ),
    "temper": (
      "Chaos has edges. You smooth them.",
      "(Costs 1 manabda. Rounds a target attribute to the nearest 10.)"
    ),
    "surge": (
      "One will. Every ally feels it.",
      "(Costs 2 manabda. Applies +3 attack buff to all allies simultaneously.)"
    ),
  },
  "Illusion": {
    "veil": (
      "Unseen is unkillable. For a while.",
      "(Costs 2-6 manabda. Makes target invisible for 2-6 turns.)"
    ),
    "mimic": (
      "A copy so good even you might forget which is real.",
      "(Costs 1-5 manabda. Creates a decoy with surface, shallow, or deep copied attributes.)"
    ),
    "shatter": (
      "Make them believe they've already lost.",
      "(Costs 2-6 manabda. Psychic damage plus skip turns. Heavier investment, heavier collapse.)"
    ),
  },
  "Conjuration": {
    "summon_elemental": (
      "Tear the veil. Something answers.",
      "(Costs 2-7 manabda. Summons Fire, Stone, or Storm Elemental at tier 1-3.)"
    ),
    "conjure_supply": (
      "The void provides. If you ask correctly.",
      "(Costs 1-6 manabda. Conjures HP, Mana, or Manabda potion directly.)"
    ),
    "wild_conjure": (
      "The veil has no obligation to be kind.",
      "(Costs 1-3 manabda. Random elemental summoned. 40-70% chance it's on your side.)"
    ),
  },
  "Shadow": {
    "shroud": (
      "The dark finds what light misses.",
      "(Costs 2-6 manabda. Scans for vulnerabilities and strikes the exposed crack.)"
    ),
    "siphon": (
      "Their strength. Your bonus. Simple math.",
      "(Costs 2-5 manabda. Drains defense and/or attack from target. Bonus added to your next strike.)"
    ),
    "eclipse": (
      "Shadow sorts the weak from the strong. You follow its judgment.",
      "(Costs 2-6 manabda. Hits 1 to all enemies sorted by HP. Weakest hit hardest.)"
    ),
  },
  "Transmutation": {
    "transmute_vitae": (
      "Lesser things become greater things. Matter agrees.",
      "(Costs 2-6 manabda. Upgrades HP Potion I → II → III → IV in inventory.)"
    ),
    "transmute_arcana": (
      "The essence rewrites itself. Something deeper emerges.",
      "(Costs 2-6 manabda. Upgrades Mana Potion I → II → III → IV in inventory.)"
    ),
  },
}


def display_spell_descriptions(school):
  spells = SPELL_DESCRIPTIONS.get(school, {})
  print(f"\nSpells awakened:")
  for spell, (flavor, mechanic) in spells.items():
    print(f"\n  {spell}")
    print(f"  {flavor}")
    print(f"  {mechanic}")


def display_ability_descriptions(school):
  abilities = ABILITY_DESCRIPTIONS.get(school, {})
  print(f"\nAbilities awakened:")
  for ability, (flavor, mechanic) in abilities.items():
    print(f"\n  {ability}")
    print(f"  {flavor}")
    print(f"  {mechanic}")


if __name__ == "__main__":

  print("Darkness.")
  print("Not the comfortable kind.")
  print("The kind that has weight. That presses.")
  print("\nThen — a sound.")
  print("Not heard. Felt.")
  print("Somewhere behind your sternum. A single word.")
  print("\n'The ledger awakens.'")
  print("\nLight bleeds in slowly. Stone walls. Cold air.")
  print("A terminal stands before you. Obsidian. Ancient.")
  print("It has been waiting. You get the sense it has been waiting")
  print("for a very long time.")
  print("\nA prompt blinks across its face in letters the color of embers.")
  print("It wants something simple.")
  print("It wants a name.")
  player_name = input("\nEnter True Name: ")
  player = Wizard(name=player_name)
  player.flags = {}
  player.gold = 0

  print(f"\nThe terminal pulses once. Accepts it.")
  print(f"Somewhere, something was written down.")

  print("\nThe stone before you shifts.")
  print("Nine sigils carve themselves into its face.")
  print("Slowly. Like they hurt to appear.")
  print("\nAbove them, words burn into existence:")
  print("'Power has a price. The price has a name.'")
  print("'Choose it.'")
  print("\n  Pyromancy     — The School of Wrath.      Burn, or be burned.")
  print("  Cryomancy     — The School of Stillness.  Preserve, or entomb.")
  print("  Chronomancy   — The School of Time.       Wait, or be forgotten.")
  print("  Necromancy    — The School of Ending.     Keep, or be kept.")
  print("  Enhancement   — The School of Self.       Break, or be broken.")
  print("  Illusion      — The School of Lies.       See, or be deceived.")
  print("  Conjuration   — The School of Calling.    Take, or be taken.")
  print("  Shadow        — The School of Secrets.    Hide, or be hunted.")
  print("  Transmutation — The School of Change.     Bend, or be bent.")
  school = input("\nChoose thy School: ")
  player.choose_school(school.capitalize())

  print(f"\nThe sigil for {player.school} burns brightest.")
  print("Then goes dark.")
  print("The mark is made.")
  display_spell_descriptions(player.school)
  print(f"\nMana: {player.mana}/{player.max_mana} | Manabda: {player.manabda}/8")

  print("\nThe silence after is absolute.")
  print("Then — footsteps.")
  print("From nowhere. From everywhere.")
  print("\nAn older wizard stands where none stood before.")
  print("He did not walk in. He simply is.")
  print("He looks at you the way a man looks at a tool he isn't sure will hold.")
  print("Then he nods. Once. Barely.")
  print("\nFrom his robe he draws a ledger.")
  print("Bound in obsidian. It opens without being opened.")
  print("Something is written. You don't see what.")
  print("It closes. Vanishes.")
  print("He turns to a door that was not there a moment ago.")
  print("Great oak. Black as the ledger. He shoves it open.")
  print("Fog pours through like it was waiting on the other side.")
  print("He steps through without looking back.")

  print("\nTwo paths present themselves:")
  print("1: Follow at a brisk pace. Demand answers.")
  print("2: Hold. Take your bearings. He is not your master.")
  choice_1 = input("\nThe choice is yours [1/2]: ")

  if choice_1 == "1":
    print(f"\nYou move. Catch the door before it shuts.")
    print("The fog is immediate. Cold. Thick.")
    print("You can see his silhouette ahead. Two steps. Three.")
    print("Then nothing.")
    print("The fog didn't take him. He simply stopped being there.")
    print("Like he was never coming with you.")
    print("Like this was always going to be yours alone.")
  else:
    print(f"\nYou stay. Let the door fall shut.")
    print("'I care not where the old man goes.'")
    print("'My Path has just begun. His part in it is done.'")
    print("\nA moment passes. Then another.")
    print("You shove the door open yourself.")
    print("You expect to find him waiting. Watching.")
    print("There is nothing.")
    print("Just the mountain. Just the dark.")
    print("The world didn't notice you took your time.")
    print("It just continued without you.")
    print("Somehow that is worse.")

  print("\n\nThe mountain opens up before you.")
  print("The air bites immediately. Thin and sharp.")
  print("Above — a sky that stops you mid-step.")
  print("\nStars. Vast and indifferent and countless.")
  print("The kind of sky that makes every question feel answerable")
  print("and every answer feel far away.")
  print("The darkness here is not cruel.")
  print("It is simply infinite.")
  print("Anything could be out there.")
  print("Everything could be out there.")
  print("\nThe Path begins where guidance ends.")

  print("\nThe mountain slope descends ahead of you.")
  print("Far below — impossibly far — a shape in the dark.")
  print("Too small to read. Too active to ignore.")
  print("Tiny shadows move against dim light.")
  print("A town. Or something that was one.")

  print("\nThe wind shifts.")
  print("It carries something with it.")
  print("A sound.")
  print("High. Desperate. Human.")
  print("\nTo your right — two dark figures on the slope.")
  print("Above them, a shape in the sky that is wrong.")
  print("Too many. Too quiet for birds.")
  print("Too hungry.")
  print("They descend.")

  print("\nThree paths burn in your mind:")
  print("1: Move toward the figures. Whatever comes, comes.")
  print("2: Watch. Do not help. The mountain doesn't ask you to.")
  print("3: Descend. The town calls louder than strangers do.")
  choice_2 = input("\nThe Path demands choice. Not comfort. [1/2/3]: ")

  if choice_2 == "1":
    print("\nYou move toward them.")
    print("The sound above sharpens into something that isn't quite a shriek.")
    print("More like a frequency. Something that wants to be inside your skull.")
    swarm = RavenSwarm()
    simple_combat(player, swarm)

    if player.is_alive():
      player.gain_exp(swarm.exp_value)
      print("\nThe swarm breaks.")
      print("Not defeated. Dispersed.")
      print("Like they decided you weren't worth the cost.")
      print("For now.")

      print("\nThe figures resolve in the dark.")
      print("A man. Medium build. A mop of blonde hair that hangs over his eyes")
      print("like he grew it that way on purpose.")
      print("Behind him — a woman. Slight. Quiet.")
      print("Her hands are still over her head.")
      print("She hasn't lowered them yet.")
      print("\nThe man looks at you.")
      print("Not with gratitude.")
      print("With suspicion sharp enough to cut.")
      print("'You.' His voice is controlled. Careful.")
      print("'Pathwalker.' Not a greeting. An identification.")
      print("'What do you want for it.'")

      print("\n[1: 'Nothing. I just killed a swarm for you.']")
      print("[2: 'What is this place? What are you running from?']")
      print("[3: 'Easy. I'm not your enemy.']")
      print("[4: Say nothing.]")
      choice_3 = input("\nYour response: ")

      if choice_3 == "1":
        print("\nHe studies you. Looking for the angle.")
        print("'Nobody does nothing for nothing out here.'")
        print(f"His eyes drop to your hands. To the mark.")
        print(f"'{player.school}.' He says it like he's filing it away.")
        print("'Either way. The town down there doesn't care what you chose.'")
        print("'They'll take from you same as anyone.'")
        player.flags['traveler_hostile'] = True

      elif choice_3 == "2":
        print("\nHe laughs. No humor in it.")
        print("'Place.' He says the word like it offends him.")
        print("'This is the Threshold. Where the Path begins.'")
        print("'Where people come with ideas about power and glory.'")
        print("He looks at the woman briefly. Something passes between them.")
        print("'Most of those ideas don't survive the first week.'")
        print("The woman speaks, barely above nothing:")
        print("'They say the voice at the start... was the last one who made it all the way.'")
        print("Silence.")
        player.flags['traveler_wary'] = True

      elif choice_3 == "3":
        print("\nYou raise empty hands.")
        print("'I just pulled a swarm off you. I'm not your enemy.'")
        print("\nHe watches you for a long moment.")
        print("The hair doesn't move. But his shoulders drop a fraction.")
        print("Something recalculates behind his eyes.")
        print("'...No.' Quiet. Like it costs him. 'No, you're not.'")
        print("'Could've walked past. Didn't.'")
        print("\nThe woman lowers her hands finally.")
        print("She looks at you with something that isn't quite relief")
        print("but is in the same neighborhood.")
        print("'Thank you.' Just that. But she means all of it.")

        print("\n[1: 'You mentioned Tithe. What's happening down there?']")
        print("[2: 'That bell. We should move.']")
        print("[3: 'What do I call you?']")
        choice_4 = input("\nChoose: ")

        if choice_4 == "1":
          print("\n'The town.' Voice dropped low now. 'It's not a town.'")
          print("'It's a collection point.'")
          print("'Enforcers run it. They work for someone called the Collector.'")
          print("'He works for people above him who don't have names.'")
          print("'They take mana. Manabda. Blood if they want it.'")
          print("'Call it Tithe. Dress it up however helps you sleep.'")
          print("The woman's voice, barely audible:")
          print("'They took my sister. Said she had... potential.'")
          print("She doesn't say what happened after that.")
          print("She doesn't have to.")

        elif choice_4 == "2":
          print("\nHe nods. Once. Sharp.")
          print("'Right. The Tithe bell. We're already late.'")
          print("'Move fast or don't move at all down there.'")
          print("He looks at you once more.")
          print("'Thanks. For what it's worth out here.'")
          print("He means it. It just costs him to say it.")

        elif choice_4 == "3":
          print("\nHe tenses immediately.")
          print("'Names are currency here.'")
          print("'You earn them. Or you take them. Nobody gives them.'")
          print("The woman touches his arm gently.")
          print("He exhales.")
          print("'Survive the town. Then we'll talk.'")
          print("It's the closest thing to trust he knows how to offer.")

        print("\nHe reaches into his coat.")
        print("Hesitates. Then pulls something out.")
        print("A small stone. Carved. It hums against his palm")
        print("like it's been waiting for the right hand.")
        print("'Found this on a corpse. Last month.'")
        print("'Couldn't make it work. Something about it knows what it wants.'")
        print("He holds it out.")
        print("'Maybe it wants you.'")
        print("\nItem acquired: Sort Rune")
        player.inventory.add("Sort Rune")
        player.flags['traveler_friend'] = True

      elif choice_3 == "4":
        print("\nYou say nothing.")
        print("The man shifts. Uncomfortable with the silence.")
        print("The woman speaks first. Soft. Like she's afraid of her own voice.")
        print("'The town... they send the swarms.'")
        print("'For people who don't come to the square.'")
        print("'For people who can't pay.'")
        print("She looks at her hands.")
        print("'For people like us.'")
        if player.mana < player.max_mana:
          player.mana = min(player.max_mana, player.mana + 5)
          print(f"\nThe stillness settles something in you.")
          print(f"Mana recovers quietly. [{player.mana}/{player.max_mana}]")

      print("\nFrom below — a bell.")
      print("Once.")
      print("Twice.")
      print("Three times.")
      print("\nThe man's face changes.")
      print("Whatever composure he had drains out of it.")
      print("'The Tithe bell.' Almost a whisper.")
      print("'They're collecting. We have to move.'")
      print("He looks at the woman. At you. At the slope below.")
      print("'Run. Hide. Pay. Those are the options.'")
      print("'If you're not marked by the Ruling Class...'")
      print("He doesn't finish. He doesn't need to.")

      if player.flags.get('traveler_friend'):
        print("\n[1: 'Stay with me. We handle this together.']")
        print("[2: 'Go. Hide. I'll draw them off.']")
        print("[3: 'Give me back that rune. I changed my mind.']")
      else:
        print("\n[1: 'Tell me more about this Tithe.']")
        print("[2: 'I'll handle the Enforcers.']")
        print("[3: 'You called me a thief. Prove you deserve defending.']")
        print("[4: 'Not my problem.' Turn away.]")

      choice_5 = input("\nThe bell rings again. Choose: ")

      if player.flags.get('traveler_friend'):
        if choice_5 == "1":
          print("\n'Together.' He says it like he's testing the word.")
          print("Looks at the woman.")
          print("She nods. Small but certain.")
          print("'Alright.' He draws a blade that's seen better decades.")
          print("'If this goes wrong...'")
          print("'It won't.' The woman says it quietly.")
          print("'It won't.' He repeats it. Like he needs to hear it twice.")
          player.flags['companion_duo'] = True
          player.flags['companion'] = "Caleb and Mira"

        elif choice_5 == "2":
          print("\n'That's...' He stops.")
          print("Looks at you properly for the first time.")
          print("'Don't die for us, Pathwalker.'")
          print("'The world needs fewer corpses and more people")
          print("who make choices like that.'")
          print("He pulls her into the dark. They're gone quickly.")
          print("You turn toward the slope alone.")
          player.flags['travelers_saved'] = True
          player.flags['traveler_owes_life_debt'] = True

        elif choice_5 == "3":
          print("\nThe woman flinches.")
          print("Like she expected it.")
          print("Like she's been expecting it her whole life.")
          print("The man's face closes like a door.")
          print("'Right.' Flat. Final. 'Should've known.'")
          print("He pulls her away. No anger. Just distance.")
          print("No fight. Just the sound of two people")
          print("who trusted wrong.")
          print("That's somehow the worst sound of all.")
          if player.inventory.has_item("Sort Rune"):
            player.inventory.remove("Sort Rune")
            print("\nThe rune goes cold in your pack. Then vanishes.")
            print("Like it agreed with him.")
          player.flags['traveler_betrayed'] = True

      else:
        if choice_5 == "1":
          print("\n'Factory.' He says it simply.")
          print("'That's what it is. Vardeth.'")
          print("'They extract from Pathwalkers. Everything they can reach.'")
          print("'Mana. Manabda. Sometimes more.'")
          print("The woman's voice breaks once. Just once.")
          print("'They took my sister. Said she had potential.'")
          print("Silence sits on all three of you.")
          print("\nHe exhales. Reaches into his coat.")
          print("'You didn't have to stop. You did anyway.'")
          print("He holds out the carved stone.")
          print("'Take it. It was never really mine.'")
          print("\nItem acquired: Sort Rune")
          player.inventory.add("Sort Rune")
          player.flags['traveler_friend'] = True

        elif choice_5 == "2":
          print("\nYou descend without another word.")
          print("Behind you, his voice carries on the wind:")
          print("'You'll die! They don't come alone!'")
          print("The bell swallows his words.")
          print("The slope takes you.")
          player.flags['travelers_ignored'] = True

        elif choice_5 == "3":
          print("\nYou step toward him.")
          print("'You called me a thief after I pulled that swarm off you.'")
          print("His eyes go flat. Something decides itself behind them.")
          print("'Fine.' He draws the blade.")
          print("'Everything out here gets taken.")
          print("Might as well be you doing the taking.'")
          traveler = DesperateTraveler()
          simple_combat(player, traveler)
          if player.is_alive():
            if traveler.hp <= 0:
              traveler.hp = 1
              print("\nHe goes down.")
              print("Stays down for a moment.")
              print("Then gets up.")
              print("Bleeding. Slower. But up.")
              print("He looks at you.")
              print("Something in it might be respect")
              print("if it wasn't so close to the other thing.")
              print("Then he runs.")
              print("Into the dark. Into the slope.")
              print("Gone.")
              print("\nThe woman hasn't moved.")
              print("She's looking at the space where he was.")
              print("'He said this was going to be something.'")
              print("'He said WE were going to be something.'")
              print("She looks at you.")
              print("Not asking. Just stating:")
              print("'I have nowhere to go.'")
              player.flags['companion_mira'] = True
              player.flags['caleb_enemy'] = True
              player.flags['companion'] = "Mira"
              print("\nAt her feet — the carved stone.")
              print("It fell when he ran.")
              print("Still humming.")
              print("Like it chose to stay.")
              print("\nItem acquired: Sort Rune")
              player.inventory.add("Sort Rune")
          elif not player.is_alive():
            print("\nDarkness.")
            print("The Path ends here.")
            print("Or perhaps it simply begins somewhere else.")
            exit()

        elif choice_5 == "4":
          print("\nYou turn away.")
          print("The bell tolls a fourth time.")
          print("Behind you — footsteps. Running.")
          print("Then nothing.")
          print("The mountain doesn't comment.")
          player.flags['travelers_ignored'] = True

  elif choice_2 == "2":
    print("\nYou stay where you are.")
    print("The sound cuts short.")
    print("Then silence.")
    print("The kind that comes after something has been decided.")
    print("\nYou don't look.")
    print("The mountain air feels different now. Colder.")
    print("Not because the temperature changed.")
    print("\nThe bell tolls from below. Four times.")
    print("You count them without meaning to.")
    player.flags['travelers_ignored'] = True

  elif choice_2 == "3":
    print("\nYou turn away from the sound.")
    print("The slope pulls you forward.")
    print("The town below pulls harder.")
    print("\nYou don't look back.")
    print("The Path doesn't require it.")
    player.flags['travelers_ignored'] = True
    player.flags['skipped_raven_fight'] = True

  if player.flags.get('travelers_ignored') and not player.flags.get('companion'):
    print("\nSomewhere behind you on the mountain —")
    print("something happens.")
    print("You don't know what.")
    print("You chose not to.")

  if player.inventory.has_item("Sort Rune"):
    print("\n\nThe Sort Rune in your pack grows warm.")
    print("Then hot.")
    print("You pull it out.")
    print("\nIt lifts from your palm without being thrown.")
    print("Hovers. Rotates once.")
    print("Then moves toward you — not fast, not slow —")
    print("and presses itself against the mark on your hand.")
    print("\nIt doesn't hurt.")
    print("It dissolves.")
    print("Through skin. Through bone.")
    print("Like it was always supposed to be inside you")
    print("and was simply waiting for permission.")
    print("\nYour vision doesn't change.")
    print("But something behind your vision does.")
    print("The world has... structure now.")
    print("You can feel the shape of things.")
    print("What they're made of. Where they're hiding.")
    print("\n[Sort Rune absorbed. Spell unlocked: sort]")
    print("(sort — Read the composition of any location.")
    print(" Reveals common items. 10% chance of uncovering something rarer.)")
    player.learn_spell_sort(method="absorbed")
    player.inventory.remove("Sort Rune")

  print("\n\nThe bell tolls again from somewhere below.")
  print("Lower. Longer. Different from the others.")
  print("Like a door closing far away.")
  print("Like something being decided without you.")
  print("\nAnd then —")
  print("\nIt starts beneath the skin.")
  print("Not pain.")
  print("Something adjacent to it.")
  print("A current. Moving through muscle and bone")
  print("like lightning that forgot to be dangerous.")
  print("\nYour hands are shaking.")
  print("Not from fear.")
  print("\nThe mark on your palm burns once.")
  print("Bright. Absolute.")
  print(f"\nSomething in you that was always there")
  print(f"but never awake")
  print(f"opens its eyes.")
  print(f"\nYour mind expands into shapes it didn't have before.")
  print(f"Power rushes through you like a river finding a new bed.")
  print(f"Like your body always knew this was coming")
  print(f"and was simply waiting for the world to catch up.")
  print(f"\nYou feel it settle. Deep. Permanent.")
  print(f"This is not a spell.")
  print(f"This is what you ARE now.")
  player.unlock_abilities()
  display_ability_descriptions(player.school)
  print(f"\nManabda: {player.manabda}/8")

  print("\n\nThe slope levels out.")
  print("The mountain releases you.")
  print("\nAnd you see it.")
  print("\nVardeth.")
  print("\nThe sky above it stops you cold.")
  print("Behind you — stars. Infinite. Indifferent. Full of possibility.")
  print("Ahead —")
  print("A twilight that has no business existing at this hour.")
  print("Deep purple. The color of something held too long.")
  print("And through it — red.")
  print("Not sunset red.")
  print("Not natural red.")
  print("Streaks of it.")
  print("Like something was dragged across the sky")
  print("and nobody cleaned it up.")
  print("Like nobody thought they should.")
  print("\nThe stars stop at the edge of Vardeth's sky.")
  print("Exactly at the edge.")
  print("Like they know better than to go further.")

  print("\n\nThe town breathes.")
  print("That's the only word for it.")
  print("Not with life. With effort.")
  print("\nThe streets are stone. Old stone. Tired stone.")
  print("People move through them the way water moves through cracks —")
  print("not going somewhere so much as")
  print("finding the path of least resistance.")
  print("\nMost wear the same expression.")
  print("Not sad. Past sad.")
  print("The kind of face that has made its peace with something")
  print("and is no longer fighting it.")
  print("\nTheir clothes are worn. Mended. Mended again.")
  print("Here and there — someone different.")
  print("Better fabric. Straighter back.")
  print("Eyes that move differently.")
  print("They don't linger.")
  print("They're always going somewhere.")
  print("Always busy with something that matters to someone above them.")

  print("\nMetal grates line the street at irregular intervals.")
  print("You almost don't notice the first one.")
  print("Then you hear it.")
  print("\nA sound from below.")
  print("Distant. Muffled.")
  print("Human.")
  print("\nYou keep walking.")
  print("Everyone keeps walking.")
  print("That might be the worst thing about it.")

  print("\nThe square opens up ahead.")
  print("Large. Too large for the town around it.")
  print("Like it was built for a different purpose")
  print("and this one grew up around it.")
  print("\nLines. Or what was left of lines.")
  print("The mass tithe ended roughly half an hour before you arrived.")
  print("You can tell by the way people are dispersing.")
  print("Slow. Careful.")
  print("Like moving too fast might draw attention.")
  print("\nAt the center — a device.")
  print("Larger than anything you'd expect.")
  print("A platform. Leather straps worn smooth from use.")
  print("Tubes that feed into containers")
  print("being carried away by people who don't make eye contact.")
  print("A dark bag hangs from the side of it.")
  print("It has seen too much use.")
  print("Everyone pretends not to see it.")
  print("\nAn Enforcer stands at each corner of the square.")
  print("Batons at their sides.")
  print("Not threatening right now.")
  print("Just present.")
  print("Just reminding.")

  if player.flags.get('companion_duo'):
    print("\nBeside you —")
    print("The man and the woman have kept pace.")
    print("He's been scanning the square since you entered it.")
    print("She's been watching the grates.")
    print("'Vardeth.' He says it quietly.")
    print("'First time seeing it up close.'")
    print("He doesn't say anything else.")
    print("He doesn't have to.")
  elif player.flags.get('companion_mira'):
    print("\nMira has stayed close since the mountain.")
    print("Not clinging. Just... near.")
    print("She looks at the square. At the device at its center.")
    print("At the dark bag.")
    print("Something in her face tightens.")
    print("Then deliberately relaxes.")
    print("'He brought me here because he said it would be worth it.'")
    print("She watches an Enforcer cross the square.")
    print("'I'm still deciding if he was right about anything.'")
    print("\nShe looks at the device.")
    print("Then at you.")
    print("Something passes between you that neither of you names.")
    print("Not yet.")
  elif player.flags.get('traveler_owes_life_debt'):
    print("\nThey're not here.")
    print("You sent them into the dark.")
    print("Whether that was mercy or abandonment")
    print("depends on what happens next.")
    print("You don't know yet.")

  print("\n\nYou need to move through Vardeth.")
  print("The square. The streets. The grates.")
  print("And somewhere in this town —")
  print("a door that doesn't look like much.")
  print("Behind it, an old woman who does.")

  print("\n[1: Approach an Enforcer. Pay Tithe openly.]")
  print("[2: Move through the square quietly. Find the side streets.]")
  print("[3: Approach the Enforcers. Tell them you want in.]")
  choice_9 = input("\nChoose: ")

  if choice_9 == "1":
    print("\nThe Enforcer clocks you before you reach him.")
    print("'Pathwalker.' Not surprised. They never look surprised.")
    print("'Mass tithe's done for today.'")
    print("He nods toward a side building.")
    print("'Private collection. Standard rate.'")
    print("'Or you can come back tomorrow for the square.'")
    print("He looks at you the way someone looks at a number.")
    print("\n[1: Submit to private collection — costs 3 Mana and 2 Manabda]")
    print("[2: 'I'll come back for the square.' Walk away.]")
    print("[3: Attack.]")
    choice_10 = input("Choose: ")

    if choice_10 == "1":
      if player.mana >= 3 and player.manabda >= 2:
        player.mana -= 3
        player.manabda -= 2
        print("\nThe building is small. Efficient.")
        print("A chair. A device identical to the one in the square.")
        print("Smaller. But identical.")
        print("A person whose job is to not have an expression.")
        print("\nYou strap in.")
        print("The leather is worn smooth.")
        print("Too many hands before yours.")
        print("The needle is cold.")
        print("A thin line of red moves down the tube.")
        print("Into the bag.")
        print("Nobody speaks.")
        print("When it's done they hand you a small stamped token")
        print("without looking at you.")
        print("'You're cleared.'")
        print(f"\nMana: {player.mana}/{player.max_mana} | Manabda: {player.manabda}/8")
        player.flags['paid_tithe'] = True
        player.flags['tithe_token'] = True
      else:
        print("\n'Not enough.' The Enforcer doesn't move.")
        print("'Come back when you have it.'")
        print("'Or don't come back.'")
        print("He turns away.")

    elif choice_10 == "2":
      print("\n'Your choice.' He doesn't care.")
      print("You move back into the street.")
      print("The square watches you go.")

    elif choice_10 == "3":
      print("\nThe Enforcer doesn't flinch.")
      print("'Finally.' Almost sounds like he was waiting for it.")
      enforcer1 = Enforcer("Town Enforcer")
      enforcer2 = Enforcer("Town Enforcer")
      simple_combat(player, enforcer1)
      if player.is_alive():
        simple_combat(player, enforcer2)
      if player.is_alive():
        print("\nThey're down.")
        print("The square has gone very quiet.")
        print("Everyone is looking at something else.")
        print("Nobody saw anything.")
        print("That's how it works here.")
        player.flags['enforcers_defeated'] = True

  elif choice_9 == "2":
    print("\nYou move with the crowd.")
    print("Head down. Pace steady.")
    print("The Enforcers track movement the way predators do —")
    print("looking for the thing that doesn't fit the pattern.")
    print("You fit the pattern.")
    print("For now.")
    print("\nThe side streets receive you.")
    print("Narrower. Darker.")
    print("The grates more frequent here.")
    print("You learn quickly not to look down.")
    print("You look down anyway.")
    print("Once.")
    print("You don't do it again.")

  elif choice_9 == "3":
    print("\nYou approach the nearest Enforcer.")
    print("'I want in.'")
    print("\nHe looks at you for a long moment.")
    print("'In.' He repeats it.")
    print("'You understand what that means.'")
    print("It isn't a question.")
    print("\n[1: 'I understand.']")
    print("[2: 'Tell me what it means first.']")
    choice_11 = input("Choose: ")

    if choice_11 == "1":
      print("\n'Smart.' He almost smiles.")
      print("'Report to the Collector's office. East end of the square.'")
      print("'Tell them Reth sent you.'")
      print("He looks you over once more.")
      print("'Don't make me regret it.'")
      player.flags['enforcer_aligned'] = True
      if player.flags.get('maren_spoke_freely'):
        print("\nSomething occurs to you.")
        print("Something an old woman said in hushed tones.")
        print("You file it away.")
        print("Information has value here.")
        print("You're beginning to understand that.")

    elif choice_11 == "2":
      print("\n'It means you collect.'")
      print("'It means people look at you")
      print("the way they look at bad weather.'")
      print("'Inevitable. Impersonal.'")
      print("He watches your face.")
      print("'Still want in?'")
      print("\n[1: 'Yes.']")
      print("[2: 'No.' Walk away.]")
      choice_12 = input("Choose: ")
      if choice_12 == "1":
        print("\n'East end. Collector's office. Tell them Reth.'")
        player.flags['enforcer_aligned'] = True
      else:
        print("\nHe nods.")
        print("'Smarter than you look.'")
        print("He turns away.")

  if player.flags.get('enforcer_aligned'):
    print("\n\nThe sky above Vardeth deepens.")
    print("The purple holds its ground.")
    print("The red streaks thicken.")
    print("Just slightly.")
    print("Undeniable if you're looking.")
    print("The sky noticed.")
    print("It's keeping track.")

  print("\n\nYou find her almost by accident.")
  print("A door that doesn't announce itself.")
  print("No sign. No window.")
  print("Just a door that's slightly warmer than the stone around it.")
  print("You push it open.")
  print("\nA counter. Old wood. Clean despite everything.")
  print("Shelves behind it. Sparse but considered.")
  print("And behind the counter —")
  print("an elderly woman who doesn't look up when you enter.")

  maren = Maren()
  maren.shop(player)

  print(f"\n\n=== CHAPTER 1 COMPLETE ===")
  print(f"\n{player}")
  print(f"\nGold: {player.gold}")
  print(f"Flags: {player.flags}")
  if player.flags.get('companion'):
    print(f"\n{player.flags['companion']} walks the Path with you.")
  print("\nVardeth sits behind you.")
  print("The purple sky sits above it.")
  print("The red hasn't faded.")
  print("\nThe Path stretches forward.")
  print("It doesn't say where.")
  print("It never does.")