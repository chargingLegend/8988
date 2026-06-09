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
      "(Deals 4-11 fire damage. 50% chance to apply Burn — 5 damage per turn for 3 turns.)"
    ),
    "Sear": (
      "A lance of concentrated heat. Less elegant. More honest.",
      "(Deals 3-7 fire damage. 30% chance to apply Scorched — 3 damage per turn for 2 turns.)"
    ),
    "Cinder Ward": (
      "The air around you warps. Let them wonder what it costs.",
      "(No damage. Defensive ward. Embers orbit you.)"
    ),
  },
  "Cryomancy": {
    "Frostbite": (
      "Cold that remembers where it's been.",
      "(Deals 3-8 cold damage. 40% chance to apply Frostbitten — 3 damage per turn for 3 turns.)"
    ),
    "Glaze": (
      "Rime coats the target. Everything slows.",
      "(Deals 2-4 cold damage. 60% chance to apply Slowed — target skips every other turn.)"
    ),
    "Shard": (
      "Ice doesn't ask permission.",
      "(Deals 4-9 cold damage.)"
    ),
  },
  "Chronomancy": {
    "Hesitate": (
      "A moment stolen. Never returned.",
      "(Deals 2-6 time damage.)"
    ),
    "Foresight": (
      "You see the next beat before it arrives.",
      "(No damage. Applies Stuttered — reveals target's next move. Player gets first strike priority.)"
    ),
    "Stutter": (
      "Parts of the target arrive late.",
      "(Deals 3-7 time damage. 35% chance to apply Slowed.)"
    ),
  },
  "Necromancy": {
    "Rattle": (
      "Bones remember the grave. You remind them.",
      "(Deals 3-9 necrotic damage. 35% chance to apply Weakened — reduces target atk and defense.)"
    ),
    "Wither": (
      "Vitality flees like it has somewhere better to be.",
      "(Deals 2-8 necrotic damage.)"
    ),
    "Gravechill": (
      "The cold of tombs is patient. You aren't.",
      "(Deals 4-8 necrotic damage. 30% chance to apply Slowed.)"
    ),
  },
  "Enhancement": {
    "Brace": (
      "You root yourself. The mountain has nothing on you.",
      "(No damage. Defensive stance. Reduces incoming damage.)"
    ),
    "Surge": (
      "Kinetic wrath. Simple. Effective.",
      "(Deals 3-8 force damage. 30% chance to apply Weakened.)"
    ),
    "Iron Skin": (
      "Your skin rings like struck steel.",
      "(No damage. Temporary armor buff.)"
    ),
  },
  "Illusion": {
    "Phantom": (
      "Give them something worse than you to fight.",
      "(Deals 2-6 psychic damage. 30% chance to apply Shattered — target loses their next turn.)"
    ),
    "Mutter": (
      "Whispers convince the target it is already losing.",
      "(Deals 2-5 psychic damage. 40% chance to apply Weakened.)"
    ),
    "False Step": (
      "Distance becomes a lie. They believe it.",
      "(No damage. 65% chance to apply Shattered — target commits to nothing.)"
    ),
  },
  "Conjuration": {
    "Fetch": (
      "You reach across space. Not there yet.",
      "(No damage. Retrieves distant objects.)"
    ),
    "Shardling": (
      "A conjured splinter. Small. Fast. Angry.",
      "(Deals 3-9 force damage.)"
    ),
    "Bind": (
      "Invisible cords. Very visible results.",
      "(Deals 2-6 force damage. 55% chance to apply Slowed.)"
    ),
  },
  "Shadow": {
    "Dim": (
      "Light doesn't belong everywhere.",
      "(Deals 1-3 shadow damage. 75% chance to apply Disoriented — 40% spell fizzle for 2 turns. 3-turn cooldown. Cannot stack.)"
    ),
    "Mutter": (
      "Dark words find the cracks in resolve.",
      "(Deals 2-7 shadow damage. 40% chance to apply Weakened.)"
    ),
    "Veil": (
      "You cease to be a target. For a moment.",
      "(No damage. You become untargetable for one turn.)"
    ),
  },
  "Transmutation": {
    "Shift": (
      "Mass forgets itself. Briefly.",
      "(Deals 2-7 arcane damage. 35% chance to apply Weakened.)"
    ),
    "Harden": (
      "Air becomes stone. Not at them. At you.",
      "(No damage. Temporary defense buff.)"
    ),
    "Gild": (
      "Gold is brittle. They learn this firsthand.",
      "(Deals 3-8 arcane damage. 45% chance to apply Weakened.)"
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
  player.corruption = 0  # 0 = clean | 1-3 = shady | 4-7 = dark | 8+ = corrupted

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
  print("\nThen — that sensation again.")
  print("Not sound. Something behind sound.")
  print("The same place it came from before.")
  print("Behind your sternum. Low. Certain.")
  print("\n'He's here,' an assertive voice in your head declares, startling you.")
  print("\nThen — footsteps.")
  print("From nowhere. From everywhere.")
  print("\nAn older wizard stands where none stood before.")
  print("He did not walk in. He simply is.")
  print("\nHe looks at you.")
  print("Not the way someone looks at a person.")
  print("The way someone looks at a thing they've already assessed")
  print("and found to be less than they hoped for.")
  print("A long moment passes.")
  print("He says nothing.")
  print("Whatever question he asked himself, you weren't consulted.")
  print("Whatever answer he arrived at, it doesn't seem to impress him.")
  print("\nSomething about it sits wrong.")
  print("You don't know why. You file it away.")
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
    print(f"\nYou let the door fall shut.")
    print("You don't move after him.")
    print("He didn't ask you to. He didn't ask you anything.")
    print("That lands somewhere it shouldn't.")
    print("\nA moment passes. Then another.")
    print("You shove the door open yourself.")
    print("You expect to find him waiting. Watching.")
    print("There is nothing.")
    print("Just a jagged slope winding downwards into the unknown, strewn with sharp rocks jutting towards the sky.")
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
  print("\n'The Path begins where guidance ends,' adds the unfamiliar voice you heard before — the one that named your magic and defined you — giving you pause.")
  print("You look around, hoping to discern its source.")
  print("There are no clues.")

  print("\nThe mountain slope continues to descend downwards.")
  print("Far below — impossibly far — structures in the dark loom.")
  print("Too small to read. Too active to ignore.")
  print("Tiny shadows move against dim light.")
  print("A town. Or something that was one.")

  print("\nThe wind shifts.")
  print("It carries something with it.")
  print("A sound.")
  print("High. Desperate. Human.")
  print("\nA good couple hundred feet below you, on the right side of the slope, there are two figures obscured by the shadows of the night.")
  print("Above them, a shape in the sky that is wrong.")
  print("Too many. Too quiet for birds.")
  print("Too hungry.")
  print("They descend.")

  print("\nThree paths present themselves:")
  print("1: Move toward the figures. Whatever comes, comes.")
  print("2: You observe the ordeal for a moment or two. You aren't moved to help.")
  print("   This isn't what is required to conquer the Path.")
  print("3: Descend. The town calls louder than strangers do.")
  choice_2 = input("\nChoose [1/2/3]: ")

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
      print("He glances at the dispersing swarm. Back at you.")
      print("'What do you want for that heroic display of strength?' he scoffs.")
      print("Not a thank you. A negotiation opening.")

      print("\n[1: 'Are you serious? I just saved you from becoming dinner, maybe just some basic gratitude?']")
      print("[2: 'What is this place? What are you running from?']")
      print("[3: 'Easy. I'm not your enemy.']")
      print("[4: Say nothing.]")
      choice_3 = input("\nYour response: ")

      if choice_3 == "1":
        print("\nHe studies you. The suspicion doesn't leave his face.")
        print("If anything, it settles deeper.")
        print("A long pause before he speaks.")
        print("The words deliberately tumble out slowly, but flat and unimpressed — 'convenient timing.'")
        print("'People out here don't just happen to show up.'")
        print(f"His eyes drop to your hands. To the mark.")
        print(f"'{player.school}.' He says it like he's cataloguing evidence.")
        print("'Either way. The town down there doesn't care what you just did.'")
        print("'They'll take from you same as anyone.'")
        player.flags['traveler_wary'] = True

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
        print("'Easy. I'm not your enemy.'")
        print("\nHe watches you for a long moment.")
        print("The hair doesn't move. But his shoulders drop a fraction.")
        print("Something recalculates behind his eyes.")
        print("'...No.' Quiet. Like it costs him. 'No, you're not.'")
        print("'Could've walked past. Didn't.'")
        print("\nThe woman lowers her hands finally.")
        print("She looks at you with something that isn't quite relief")
        print("but is in the same neighborhood.")
        print("'Thank you.' Just that. But she means all of it.")

        print("\n[1: 'You said Tithe. What's happening down there?']")
        print("[2: 'That bell. We should move.']")
        print("[3: 'What do I call you?']")
        choice_4 = input("\nChoose: ")

        if choice_4 == "1":
          print("\n'The town.' Voice dropped low now. 'It's not a town.'")
          print("'It's a collection point.'")
          print("'Enforcers run it. They work for someone called the Collector.'")
          print("'He works for people above him who don't have names.'")
          print("'They take mana, and manabda alike without pause, and they'll take more in blood if their price isn't paid.'")
          print("'They call it Tithe. I call it unfair — tyranny. But most call it whatever excuse they have to, to be able to sleep.'")
          print("The woman's voice, barely audible:")
          print("'My sister came here not long ago.'")
          print("'She's... she was always like that. Certain of herself.'")
          print("'A prodigy, people said. She believed them.'")
          print("A pause.")
          print("The man with the mop of blonde hair remains glued to his past, as if the words cause reflection. He was very still.")
          print("'Caleb told me she was already here. Already making a name.'")
          print("'Said if she could do it, imagine what we could do together.'")
          print("She doesn't look at him.")
          print("'She was talking to the wrong people! About the wrong things!' he said in a voice that suggested she not push this into an argument.")
          print("'Enforcers were already watching her.'")
          print("'One morning we went to her room at the inn.'")
          print("'The door had been... it was off the hinges.'")
          print("A long silence.")
          print("'We don't know!.. we just don't.. know.' She started to sob.")
          player.flags['mira_sister_known'] = True

        elif choice_4 == "2":
          print("\nHe nods. Once. Sharp.")
          print("'We couldn't cover the Tithe. Simple as that.'")
          print("'Yesterday an Enforcer stopped us in the street.'")
          print("'Asked why we hadn't paid.'")
          print("'We had nothing to give him.'")
          print("He says it without shame. Just fact.")
          print("'So we ran. Back up the slope.'")
          print("'Back toward where all this started.'")
          print("'Figured if there was a way in, maybe there's a way out.'")
          print("He looks toward the fog where the threshold sits above them.")
          print("'There isn't.'")
          print("'It's a one way door.'")
          print("'Whatever brought you here doesn't bring you back.'")
          print("'We spent two days up here finding that out the hard way.'")
          print("\nAbove you, the remnants of the swarm pull away.")
          print("Back toward Vardeth. Back to whoever sent them.")
          print("Their work here either done or abandoned.")
          print("Either way — they're gone.")
          print("\nHe looks at you once more.")
          print("'Thanks. For what it's worth out here.'")
          print("He means it. It just costs him to say it.")

        elif choice_4 == "3":
          print("\nHe tenses immediately.")
          print("'Names are currency here.'")
          print("'You earn them. Or you take them. Nobody gives them.'")
          if player.flags.get('traveler_wary') and player.flags.get('mira_sister_known'):
            print("\nThe woman touches his arm gently.")
            print("He exhales.")
            print("Something passes across his face.")
            print("Not trust. Not yet.")
            print("But the door isn't all the way shut.")
            print("'...Mira.' He nods toward the woman.")
            print("'And I'm Caleb.'")
            print("He says it like it costs him.")
            print("He looks at you for a long moment.")
            print("'Her sister is somewhere in this town.'")
            print("'That's all you're getting.'")
          else:
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
      print("'Tithe mass.' Almost a whisper.")
      print("'They ring it when it's time to gather in the square and pay up.'")
      print("'Everyone in Vardeth stops what they're doing and goes.'")
      print("'Everyone.'")
      print("He looks at the woman. At you. At the slope below.")
      print("'For most people down there it's just another bad day.'")
      print("'For us...'")
      print("He glances up the slope where the swarm dissolved into nothing.")
      print("'When those things don't come back with what they were sent for...'")
      print("'...they'll know.'")
      print("'Nobody walks away from what they owe that town. Nobody.'")
      print("'Move. Or don't. But decide now.'")

      if player.flags.get('traveler_friend'):
        print("\n[1: 'Stay with me. We handle this together.']")
        print("[2: 'Go. Hide. I'll draw them off.']")
      else:
        print("\n[1: 'Tell me more about this Tithe.']")
        print("[2: 'I'll handle the Enforcers.']")
        print("[3: 'You don't know me. Don't assume what I'm after.']")
        print("[4: 'Not my problem.' Turn away.]")

      choice_5 = input("\nChoose: ")

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
          print("He pulls her toward the slope.")
          print("'Ravens only come for those who've been through that gate.'")
          print("'You never entered. They had no claim on you.'")
          print("'Up here we're just...'")
          print("He glances back toward Vardeth.")
          print("'...buying time.'")
          print("They move fast. The dark takes them.")
          print("You turn toward the town alone.")
          player.flags['travelers_saved'] = True
          player.flags['traveler_owes_life_debt'] = True

      else:
        if choice_5 == "1":
          print("\nHe stares at you.")
          print("The bell is ringing and you want answers.")
          print("'Not now.' Flat. Final.")
          print("He looks at Mira. She's already moving.")
          print("He follows without another word.")
          print("Whatever you were to each other in that moment —")
          print("the slope swallows it.")
          print("They're gone.")
          player.flags['travelers_ignored'] = True
          player.corruption += 1

        elif choice_5 == "2":
          print("\nHe looks at you for a long moment.")
          print("Then at Mira.")
          print("The bell tolls again.")
          print("'Right.' He says it quietly. Deciding something.")
          print("'Mira. We move. Now.'")
          print("She hesitates. Looks back toward Vardeth.")
          print("Toward wherever her sister is.")
          print("He doesn't look back.")
          print("'I know.' His voice drops. 'I know.'")
          print("'But we can't pay what we owe and we can't stay.'")
          print("They move up the slope. Away from the town.")
          print("Away from everything that brought them here.")
          print("You watch them go.")
          player.flags['travelers_ignored'] = True
          player.corruption += 1

        elif choice_5 == "3":
          print("\nYou step toward him.")
          print("'You don't know me.'")
          print("His eyes go flat. Something decides itself behind them.")
          print("'No.' He draws the blade.")
          print("'But I know what everything out here gets taken for.'")
          print("'Might as well be me doing the taking.'")
          traveler = DesperateTraveler()
          simple_combat(player, traveler)
          if player.is_alive():
            if traveler.hp <= 0 or traveler.fled:
              traveler.hp = 1
              print("\nHe staggers.")
              print("The dagger drops.")
              print("He looks at it on the ground.")
              print("Then at you.")
              print("Then at her.")
              print("\n'I don't need you!'")
              print("His voice cracks on the last word.")
              print("He looks at Mira.")
              print("Something in his face shifts.")
              print("His brow furrows.")
              print("Hard. Angry.")
              print("'NEITHER of you!'")
              print("It comes out like a bellow and a wound at the same time.")
              print("'My ambition will take me to the top!'")
              print("He takes a step back.")
              print("Then another.")
              print("'You just WATCH!'")
              print("\nThen he runs.")
              print("Into the dark. Into the slope.")
              print("The fog takes him faster than it should.")
              print("Gone.")
              print("\nSilence.")
              print("\nMira hasn't moved.")
              print("She's looking at the space where he was.")
              print("Not crying. Past crying.")
              print("'He said this was going to be something.'")
              print("'He said WE were going to be something.'")
              print("A long pause.")
              print("She looks at you.")
              print("Not asking. Just stating a fact about herself:")
              print("'I have nowhere to go.'")
              player.flags['companion_mira'] = True
              player.flags['caleb_enemy'] = True
              player.flags['companion'] = "Mira"
              print("\nShe looks down.")
              print("Something at her feet caught her eye.")
              print("She crouches slowly. Picks it up.")
              print("A small carved stone.")
              print("Markings that seem to shift when you're not looking directly.")
              print("It hums in her hand.")
              print("Then hums louder.")
              print("She looks at you with something like wonder.")
              print("\nHe notices. Looks at her. Then at you.")
              print("He nods toward her almost imperceptibly.")
              print("As if summoned by it, she speaks.")
              print("Her voice barely makes it out.")
              print("'I'm Mira.'")
              print("\nA pause.")
              print("'It never did that for him.'")
              print("She means the rune. She doesn't explain further.")
              print("\nShe holds it toward you.")
              print("The humming shifts the moment it gets close to your hand.")
              print("Like it's orienting.")
              print("Like it's finally arriving somewhere.")
              print("'We found it up here. Near the threshold.'")
              print("'He grabbed it the moment he saw it.'")
              print("'Said it was valuable. Carried it for weeks.'")
              print("'Nothing ever happened.'")
              print("She almost smiles.")
              print("'I think it was waiting for you.'")
              print("\n[Sort Rune acquired]")
              print("(A carved rune found at the very threshold of the Path.")
              print(" Carried for weeks by someone it didn't belong to.")
              print(" It hums differently for you.")
              print(" Something inside it has been patient. It's done waiting.)")
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
          print("Just the slope ahead of you.")
          print("Just the dark.")
          print("You keep moving.")
          player.flags['travelers_ignored'] = True
          player.corruption += 1

  elif choice_2 == "2":
    print("\nYou observe the ordeal for a moment.")
    print("Two figures. Something descending.")
    print("The sound — high, desperate — carries down the slope.")
    print("\nYou don't move.")
    print("\nThe sound cuts short.")
    print("Then silence.")
    print("The kind that comes after something has been decided.")
    print("\nYou don't look back.")
    print("The mountain air feels different now. Colder.")
    print("Not because the temperature changed.")
    print("\nThe bell tolls from below. Four times.")
    print("You count them without meaning to.")
    print("You don't know why that bothers you.")
    print("You keep moving.")
    player.flags['travelers_ignored'] = True
    player.corruption += 1

  elif choice_2 == "3":
    print("\nYou turn away from the sound.")
    print("It isn't your problem.")
    print("You didn't come here for strangers on a slope.")
    print("The Path doesn't ask you to.")
    print("\nThe town below pulls harder with every step.")
    print("Whatever is happening behind you —")
    print("it was already happening before you arrived.")
    print("It will keep happening after you're gone.")
    print("\nYou don't look back.")
    print("The slope takes you.")
    player.flags['travelers_ignored'] = True
    player.flags['skipped_raven_fight'] = True

  if player.flags.get('travelers_ignored') and not player.flags.get('skipped_raven_fight'):
    print("\nSomewhere behind you on the slope —")
    print("something concludes.")
    print("You heard enough to know what it was.")
    print("You keep moving.")

  if player.flags.get('skipped_raven_fight'):
    print("\nSomething happened on the slope behind you.")
    print("You're not sure what.")
    print("You didn't stop to find out.")

  if not player.inventory.has_item("Sort Rune") and "sort" not in player.spells:
    print("\n\nSomething catches your eye on the path ahead.")
    print("A small stone. Carved. Half-buried in the dirt.")
    print("Like it's been sitting there waiting for the right set of boots to walk past.")
    print("It hums faintly when you pick it up.")
    print("Louder when your hand closes around it.")
    print("You don't know what it is yet.")
    print("But it knows what you are.")
    player.inventory.add("Sort Rune")

  if player.inventory.has_item("Sort Rune"):
    print("\n\nThe Sort Rune in your pack grows warm.")
    print("Then hot.")
    print("You pull it out.")
    print("\nIt lifts from your palm without being thrown.")
    print("Hovers. Rotates once.")
    print("Then moves toward you — not fast, not slow —")
    print("and presses itself against the mark on your hand.")
    print("\nIt dissolves.")
    print("Through skin. Through bone.")
    print("\n[Sort Rune absorbed. Spell unlocked: sort]")
    print("(sort — Read the composition of any location.")
    print(" Reveals common items. 10% chance of uncovering something rarer.)")
    player.learn_spell_sort(method="absorbed")
    player.inventory.remove("Sort Rune")

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

  if player.flags.get('companion_duo') or player.flags.get('companion_mira'):
    print("\nCaleb slows before the square opens up.")
    print("He's already clocked the Enforcers at the corners.")
    print("You can tell by the way his eyes stopped moving.")
    print("\nHe doesn't say anything.")
    print("He reaches into his pack.")
    print("Pulls out a dark cloth — worn, shapeless, the kind of thing")
    print("that makes a person look like everyone else.")
    print("He pulls it over his shoulders without ceremony.")
    print("\nHe looks at Mira.")
    print("She's already adjusting — hood up, jacket reversed,")
    print("something about the way she carries herself deliberately flattened.")
    print("Less distinctive. More forgettable.")
    print("She's done this before.")
    print("\n'Once we're in there,' Caleb says quietly,")
    print("'we don't know each other.'")
    print("'Give it ten steps before you follow.'")
    print("He doesn't wait for a response.")

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

  print("\nBut the edges of the square are different.")
  print("Alive, even.")
  print("Stalls pressed up against the buildings that border it —")
  print("produce, cloth, dried things in bundles, a man with a cart of something")
  print("that smells like it was cooked this morning.")
  print("People moving between them.")
  print("Not the dispersing crowd. Different people.")
  print("The ones who have somewhere to be and something to trade.")
  print("Voices low. Business done quickly.")
  print("Eyes that flick to the center and flick away again.")
  print("\nThe buildings that ring the square are tall enough to lean.")
  print("Between them — gaps.")
  print("Narrow. Dark even now.")
  print("Alleyways that slot between the stone like afterthoughts,")
  print("running back into whatever Vardeth is behind its public face.")
  print("Mostly trash-filled corridors from the looks of it.")
  print("Others just as lonely and sad as the faces of most of the people in this square.")
  print("This is the whole town, more or less.")
  print("The square and the alleys feeding off it.")
  print("Everything else is just walls.")

  if player.flags.get('companion_duo'):
    print("\nBeside you —")
    print("The man and the woman have kept pace.")
    print("He's been scanning the square since you entered it.")
    print("She's been watching the grates.")
    print("'Vardeth.' He says it quietly.")
    print("'First time seeing it up close.'")
    print("He doesn't say anything else.")
    print("\nThe woman is looking at the crowd.")
    print("Not at the square. Not at the device.")
    print("At faces.")
    print("One by one.")
    print("Like she's looking for someone.")
    print("She doesn't say anything.")
    print("But her hands have gone very still.")
  elif player.flags.get('companion_mira'):
    print("\nMira has stayed close since the slope.")
    print("Not clinging. Just... near.")
    print("\nShe isn't looking at the device.")
    print("She isn't looking at the Enforcers.")
    print("She's looking at faces.")
    print("Moving through the crowd with her eyes the way someone does")
    print("when they're searching for one specific person")
    print("and terrified of what they might find.")
    print("Or not find.")
    print("\n'She has to be here somewhere...'")
    print("A pause.")
    print("'Did they take her?'")
    print("Her voice is tiny when she says it.")
    print("It doesn't feel like a question meant for answering.")
    print("She's already moved on to the next face.")
  elif player.flags.get('traveler_owes_life_debt'):
    print("\nThey're not here.")
    print("You sent them away from the slope.")
    print("What happens next isn't a weight you have to burden.")

  print("\n\nThe square settles around you.")
  print("The edges busy. The center — less so now.")

  print("\n[1: Approach an Enforcer. Pay Tithe openly.]")
  print("[2: Move through the square quietly. Find the alleyways.]")
  print("[3: Approach the Enforcers. Tell them you want in.]")
  if player.flags.get('companion_duo') or player.flags.get('companion_mira'):
    print("[4: Point them out. Tell the Enforcers what they're looking at.]")
  choice_9 = input("\nChoose: ")

  if choice_9 == "4" and (player.flags.get('companion_duo') or player.flags.get('companion_mira')):
    print("\nYou catch the nearest Enforcer's eye.")
    print("You nod — once — toward where they're standing.")
    print("\nThe Enforcer looks.")
    print("Then looks back at you.")
    print("Something passes between you that doesn't need words.")
    print("\nThree of them move at once.")
    print("Fast. Practiced.")
    print("The kind of coordinated that means they've done this many times.")

    if player.flags.get('companion_duo'):
      print("\nCaleb sees it half a second before it happens.")
      print("His hand goes to his weapon.")
      print("Gets halfway there.")
      print("His mouth opens —")
      print("\n'You absolute piece of —'")
      print("\nThe baton catches him across the side of the head.")
      print("He drops.")
      print("Mid-sentence.")
      print("That's all he gets.")

    if player.flags.get('companion_mira'):
      print("\nMira sees it happen to Caleb first.")
      print("Then she understands what you did.")
      print("Both at once.")
      print("\n'WHY —'")
      print("They grab her.")
      print("'WHY — JUST — WHY —'")
      print("Full sobs now. Uncontrolled.")
      print("'WHY WOULD YOU — WHY —'")
      print("They're dragging her and she's not even trying to stop them.")
      print("Just screaming at you.")
      print("'WHY —'")
      print("Over and over.")
      print("Until she's gone.")

    print("\nThe square absorbs it the way it absorbs everything.")
    print("Nobody saw anything.")
    print("Nobody ever does.")

    player.flags['companions_betrayed'] = True
    player.flags['caleb_in_dungeon'] = True
    player.flags['mira_in_dungeon'] = True
    player.flags.pop('companion_duo', None)
    player.flags.pop('companion_mira', None)
    player.flags.pop('companion', None)
    player.corruption += 5
    choice_9 = "3"
    player.flags['enforcer_aligned'] = True
    player.corruption = max(player.corruption, 3)

  if choice_9 == "1":
    print("\nThe Enforcer clocks you before you reach him.")
    print("'Pathwalker.'")
    print("He says it the way someone reads a number off a list.")
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
      print("You step back into the square.")
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
    print("\nThe alleyways receive you.")
    print("Narrower. Darker.")
    print("The grates more frequent here.")
    print("You learn quickly not to look down.")
    print("You look down anyway.")
    print("Once.")
    print("You don't do it again.")

  elif choice_9 == "3":
    print("\nYou approach the nearest Enforcer.")

    if player.flags.get('companion_duo') or player.flags.get('companion_mira'):
      print("\nYou don't look back.")
      print("You don't need to.")
      print("They'll read it from the direction you're walking.")
      print("\nWhen you glance back a moment later —")
      print("they're gone.")
      print("Not dramatically. Not with a scene.")
      print("Just — not there.")
      if player.flags.get('companion_mira'):
        print("Mira didn't look back either.")
        print("You notice that more than you expected to.")
      if player.flags.get('companion_duo'):
        print("Caleb did.")
        print("Once.")
        print("You caught it.")
        print("He didn't.")
      player.flags.pop('companion_duo', None)
      player.flags.pop('companion_mira', None)
      player.flags.pop('companion', None)
      player.flags['companions_left'] = True

    print("\n'I want in.'")
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
      player.corruption += 3  # moderate — chose the oppressor's side
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

  # ── corruption tag: enforcer alignment ───────────────────
  if player.flags.get('enforcer_aligned'):
    player.corruption = max(player.corruption, 3)

  # ── Collector's office — enforcer path ───────────────────
  if player.flags.get('enforcer_aligned') and not player.flags.get('dara_met'):
    print("\n\nEast end of the square.")
    print("The office isn't hard to find.")
    print("It's the only door with an Enforcer sigil above it")
    print("that nobody has bothered to clean.")
    print("\nYou push it open.")
    print("\nThe room is small. Practical.")
    print("A desk that has too many papers on it.")
    print("A second desk against the far wall — empty.")
    print("\n'Reth sent you.'")
    print("She doesn't look up when she says it.")
    print("Still writing something.")
    print("\n'He's not here.'")
    print("A pause.")
    print("'He's never here.'")
    print("\nShe sets her pen down.")
    print("\nShe looks up.")
    print("\n'But I'm here.'")
    print("She stands slowly.")
    print("'And you're here.'")
    print("\nShe walks toward you — unhurried, like she has all the time in the world —")
    print("one finger twisting idly at the end of her hair.")
    print("Smiling.")
    print("The kind of smile that knows exactly what it's doing.")
    print("\n'So.'")
    print("She stops just close enough.")
    print("'Name.'")

    print("\n[1: Give your name. Hold her gaze while you do it.]")
    print("[2: Give your name. Keep it professional.]")
    dara_enlist_choice = input("\nChoose: ").strip()

    if dara_enlist_choice == "1":
      print(f"\nYou give it.")
      print("\nShe repeats it back. Slowly.")
      print("Like she's deciding if she likes the sound of it.")
      print("\n'School?'")
      print("She already has her pen ready.")
      print("But she's not looking at the book.")
      print("\nYou tell her.")
      print("\nShe writes it down. Takes her time.")
      print("'Prior experience?'")
      print("\nYou answer.")
      print("\nShe closes the book.")
      print("Looks at you.")
      print("'You don't look like a collector.'")
      print("Not an insult. More like she's working something out.")
      print("'Most of them come in here already angry about something.'")
      print("'You're not.'")
      print("\nA beat.")
      print("\n'Interesting.'")
      print("\nShe goes back to her desk.")
      print("Sits down. Picks up her pen.")
      print("'East corridor. Tomorrow morning. Someone will brief you.'")
      print("She's back to her papers.")
      print("But she doesn't tell you to leave.")
      player.flags['dara_romance'] = True
    else:
      print(f"\nYou give it.")
      print("\nShe clocks the tone.")
      print("Goes back to her desk without a word.")
      print("\n'School. Prior experience.'")
      print("She writes it all down.")
      print("Closes the book.")
      print("'East corridor. Tomorrow morning.'")
      print("A pause.")
      print("'Don't be late.'")
      print("She goes back to her papers.")
      print("You're dismissed.")

    player.flags['dara_met'] = True
    player.flags['dara_path'] = 'enforcer'

  # ── approach to Maren's ───────────────────────────────────
  print("\n\nYou find it almost by accident.")
  print("A door that doesn't announce itself.")
  print("No sign. No window.")

  if player.corruption >= 8:
    print("Just a door that's slightly warmer than the stone around it.")
    print("You've stopped noticing things like that.")
    print("Or maybe you've just stopped caring what they mean.")
  elif player.corruption >= 4:
    print("Just a door that's slightly warmer than the stone around it.")
    print("You notice it the way you notice everything now.")
    print("Cataloguing. Assessing. Old habits are softer than new ones.")
  else:
    print("Just a door that's slightly warmer than the stone around it.")
    print("In Vardeth, warmth from anywhere feels like it means something.")

  print("\nThrough a smeared window, a woman moves behind the counter.")
  print("Small shop. Cramped shelves.")
  print("The glass has cracks that were never worth fixing —")
  print("or maybe there was never money to.")
  print("The place looks like it made peace with its own decline a long time ago.")
  print("But the shelves have stock.")
  print("In Vardeth, that alone means something.")

  if player.flags.get('companion_mira'):
    if player.corruption >= 4:
      print("\nMira stops one step behind you at the threshold.")
      print("You don't see her face.")
      print("You don't need to.")
      print("She follows. She always follows.")
      print("But something in the set of her shoulders is different now.")
      print("Like she's carrying something she didn't have before.")
    else:
      print("\nMira glances at the window. Then at you.")
      print("She glances at the shelves the way someone does")
      print("when they haven't seen proper goods in a while.")
      print("Just for a second.")
      print("Then her face goes careful again.")
      print("She doesn't say anything. She just follows.")

  if player.flags.get('enforcer_aligned'):
    print("\nThe woman inside clocks you before you reach the door.")
    print("The way she straightens isn't welcome.")
    print("It's bracing.")
  else:
    print("\nSomething about the door makes you slow down.")
    print("Not fear. Something else.")
    print("Like it's been waiting. Quietly. Without making a fuss about it.")

  print("\n[1: Go in.]")
  print("[2: Keep moving.]")
  approach_choice = input("\nChoose: ").strip()

  if approach_choice == "2":
    print("\nYou walk past it.")
    if player.flags.get('companion_mira'):
      print("Mira doesn't say anything.")
      print("But you hear her exhale.")
      print("Just once. Controlled.")
      print("'Okay.' That's all.")
    print("\nYou turn back into the square.")
    print("The grates in the floor catch your eye.")
    print("You keep walking.")
  else:
    maren = Maren()
    maren.shop(player, skip_greet=True)

  player.flags['vardeth_story_done'] = True
  player.flags['maren_available'] = True
  from systems.hub import hub
  from location import Vardeth
  hub(player, Vardeth)

  # ── Ledger moment — fires once if companions are with you ─────────────────
  if (player.flags.get('companion_mira') or player.flags.get('companion_duo')) \
      and not player.flags.get('mira_ledger_moment_done'):

    if player.flags.get('companion_duo'):
      print("\nYou're crossing the square when Caleb speaks.")
      print("Not to anyone in particular.")
      print("\n'That voice.'")
      print("He says it the way someone mentions a sound they keep hearing in a wall.")
      print("Flat. Slightly irritated.")
      print("'The one that comes from nowhere.'")
      print("'Talks like it already knows the answer to whatever it's about to say.'")
      print("'Sometimes it's useful. Sometimes it's just... there.'")
      print("He glances at you sideways.")
      print("'Tell me you've had that.'")
      print("\nYou look at him.")
      print("\n'Doesn't sit right,' he says before you can answer.")
      print("'Something that knows things it shouldn't.'")
      print("'I don't like not being able to account for it.'")
      print("He leaves it there.")
      print("Done with it. Or trying to be.")
      print("\nYou look at Mira.")
      print("\nShe has a faraway look.")
      print("Not troubled exactly. Somewhere between troubled and something else.")
      print("Like she's been thinking about the same thing for a long time")
      print("and hasn't decided what it means yet.")
      print("\nShe doesn't add anything.")
      print("She doesn't need to.")
      print("\nThe three of you keep walking.")
      print("Nobody says anything else about it.")

    else:
      print("\nYou're crossing the square when Mira stops.")
      print("Abruptly. Like she walked into something invisible.")
      print("\nShe doesn't move for a moment.")
      print("Then she turns to you.")
      print("\n'Have you heard it too?'")
      print("\nYou look at her.")
      print("'Heard what?'")
      print("\nShe hesitates.")
      print("Not because she doesn't know what she means.")
      print("Because she isn't sure how to say it without sounding like she's lost her mind.")
      print("\n'That voice.' She drops her own voice lower.")
      print("'The bold one. It doesn't speak often.'")
      print("'Sometimes it offers something — advice, almost. Like it's trying to help.'")
      print("'Other times it...' She stops.")
      print("'...probes. Like it's testing something in you.'")
      print("'Deciding if you're worth the trouble before it commits to anything.'")
      print("\nShe watches your face.")
      print("'You have. Haven't you.'")
      print("Not a question.")
      print("\nA beat of silence between you.")
      print("She nods once. Slowly.")
      print("Like something that was unresolved just settled.")
      print("She doesn't say anything else.")
      print("You keep walking.")
      print("Neither of you mention it again.")
      print("But something between you is different now.")
      print("Quieter. And somehow louder for it.")

    player.flags['mira_ledger_moment_done'] = True

  # ── Back in the square — tablet + prisoner transport ─────────────────────
  print("\n\nYou're back in the square.")
  print("You know it differently now.")
  print("The first time it stopped you.")
  print("The device. The straps. The people who walked past without looking.")
  print("Now you walk past without looking too.")
  print("You've learned the shape of it.")
  print("\nSomething near the center catches your eye.")
  print("Not the device — you know what that is.")
  print("Something beside it. Stone. Floor to waist height.")
  print("You almost walked past it the first time.")
  print("\nYou stop.")
  print("\nThe face is carved with twenty-six symbols.")
  print("Letters. All of them. A through Z.")
  print("Listed in order like a lesson someone cut into rock")
  print("and left for whoever was paying attention.")
  print("\nBeneath them, a question:")
  print("\n  'What is the order that starts between light and dark")
  print("   and holds all of the names meant to lift the world?'")
  print("\nA slot at the base. Wide enough for a hand.")
  print("A smaller line below:")
  print("  [ ATTEMPT COSTS: 2 Mana / 2 Manabda / 3 Gold ]")
  print("  [ REWARD: 50 Gold + Manabda Potion I ]")
  print("\nYou read it twice.")
  print("The answer isn't there yet.")
  print("You file it away.")
  print("Whatever this is — it's been here the whole time.")
  print("Waiting for someone to know enough to answer it.")

  print("\n[1: Reach toward the slot anyway.]")
  print("[2: Leave it. You don't have the answer yet.]")
  tablet_choice = input("\nChoose: ").strip()
  if tablet_choice == "1":
    print("\nYour hand slows on its own.")
    print("You don't have it.")
    print("Not yet.")
    print("You pull back.")

  # ── Prisoner transport — the thread that pulls everything ─────────────────
  print("\n\nYou're about to move on.")
  print("\nThen — movement on the far side of the square.")
  print("\nTwo Enforcers.")
  print("Between them, three people.")
  print("Hands bound. Heads down.")
  print("Moving fast. Not dragged. Walking.")
  print("Like they've decided compliance is the last thing they have left.")
  print("\nAcross the square. Past the tithe device.")
  print("To a door you hadn't noticed until now.")
  print("Set flush with the stonework on the far side.")
  print("Nearly invisible from this angle.")
  print("Steps descend behind it. Down.")
  print("\nThe Enforcer with the keys unlocks it.")
  print("They go in.")
  print("They come back out without the prisoners.")
  print("He locks it behind him.")
  print("Tries it once. Satisfied.")
  print("\nThen he does something unexpected.")
  print("He doesn't cross back through the square.")
  print("He turns. Moves along the wall.")
  print("Into a narrow gap between buildings — barely an alley.")
  print("A back way. Out of the square entirely.")

  if player.flags.get('companion_duo'):
    print("\nCaleb looks at you.")
    print("One word. Quiet.")
    print("'Follow.'")
  elif player.flags.get('companion_mira'):
    print("\nMira's hand brushes your arm. Once.")
    print("She tilts her head toward the alley.")
    print("That's all.")

  print("\n[1: Follow him into the alley.]")
  print("[2: Hold. Watch where he goes from here.]")
  follow_choice = input("\nChoose: ").strip()

  if follow_choice == "2":
    print("\nYou wait.")
    print("He doesn't reappear on any side of the square you can see.")
    print("Whatever that back way connects to — it's not visible from here.")
    print("\nYou wait long enough to be certain.")
    print("Then you go anyway.")

  # ── 4. The alley — criminal intercept, rookery spotted ───────────────────
  print("\n\nThe alley is narrow enough that the walls catch sound.")
  print("Smell of damp stone. Something old underneath it.")
  print("You move single file.")

  if player.flags.get('companion_duo'):
    print("\nCaleb goes first without being asked.")
    print("The kind of reflex that comes from experience, not bravery.")
  elif player.flags.get('companion_mira'):
    print("\nMira presses close to the wall. Practiced.")
    print("You match her without thinking about it.")

  print("\nHalfway down — a figure steps out of a recess in the stone.")
  print("Low hat. Shoulders that have been rained on many times.")
  print("He doesn't move toward you. Just blocks the path.")
  print("\n'Cost you to know what's down there.'")
  print("He nods toward the far end of the alley.")
  print("'Where they take 'em. Cost you one gold.'")

  print("\n[1: Pay him the gold upfront.]")
  print("[2: Refuse. Walk past him.]")
  alley_choice = input("\nChoose: ").strip()

  if alley_choice == "1":
    if player.gold >= 1:
      player.gold -= 1
      print("\nYou press the coin into his palm.")
      print("He looks at it.")
      print("Then looks at you.")
      print("'Appreciate it.'")
      print("He steps aside. Walks back into the recess.")
      print("You wait for the tip.")
      print("He doesn't give you one.")
      print("He just leans there, watching the far wall.")
      print("\nYou've been conned for a gold.")
      print("He was testing whether you were the kind who pays without knowing what they're buying.")
      print("Now he knows.")
    else:
      print("\nYou reach for gold you don't have.")
      print("He sees it before you do.")
      print("'Never mind.'")
      print("He steps aside anyway.")
      alley_choice = "2"

  if alley_choice == "2":
    print("\nYou move to walk past him.")
    print("He doesn't stop you.")
    print("\nBut as you pass he speaks.")
    print("'Sub-level. Below the dungeon floor.'")
    print("Quiet. Like he's talking to the wall.")
    print("'There's a lower tier they don't show on any map.'")
    print("'If you're going in — you want to know that.'")
    print("\nYou look at him.")
    print("He holds up one finger. One gold. After.")
    print("\nYou give it to him.")
    if player.gold >= 1:
      player.gold -= 1
    print("He takes it. Pockets it.")
    print("'Decent of you,' he says.")
    print("He doesn't say anything else.")
    player.flags['sub_level_known'] = True

  # Ravens spotted from the alley — source unknown yet
  print("\n\nYou're almost at the end of the alley when something moves above you.")
  print("Not wind.")
  print("\nYou look up.")
  print("\nRavens.")
  print("Sitting on a ledge near the roofline, set back from the square.")
  print("More than you'd expect.")
  print("You don't know what to make of it.")
  print("You keep moving.")


  # ── 5. Tavern — barkeep, drunk guard, keys ────────────────────────────────
  print("\n\nThe tavern sits at the end of the alley like it was waiting.")
  print("Low ceiling. Smell of old smoke and something being reheated.")
  print("\nBefore you reach the door —")
  print("a guard pushes out of it.")
  print("Lists sideways. Catches himself on the frame.")
  print("Doesn't notice he did it.")
  print("Keys on his belt. Heavy ones. Iron.")
  print("They catch what little light there is as he disappears back inside.")

  if player.flags.get('companion_mira') or player.flags.get('companion_duo'):
    print("\nMira watches him for a moment.")
    print("\n'He seems like the type to overindulge,' she says quietly.")
    print("'He can barely make it inside without stumbling.'")
    print("She glances at you.")
    print("'We could help him along. Get the keys when he's completely off his rocker.'")
    print("A pause.")
    print("'Or we could just take the direct approach and lift them now.'")
    print("'That might raise a few eyebrows don't you think.'")
    if player.flags.get('companion_duo'):
      print("\nCaleb glances at you sideways.")
      print("'But hey — I'm not the raven conqueror like you, so what do I know.'")
      print("Every word dripping with sarcastic intent.")
  else:
    print("\nYou watch him catch himself on the door frame.")
    print("He doesn't notice he did it.")
    print("\nThe keys are right there on his belt.")
    print("You could wait. Buy him a drink or two.")
    print("Wait until he's completely off his rocker and lift them clean.")
    print("Or you could just take the direct approach.")
    print("Might raise a few eyebrows.")
    print("You almost smile at that.")

  print("\n[1: Help him along. Buy the drinks. Wait him out.]")
  print("[2: Take the direct approach. Lift them now.]")
  tavern_choice = input("\nChoose: ").strip()

  print("\n\nThe tavern receives you.")
  print("Low ceiling. A few people. None of them interested in you.")
  print("\nThe barkeep is behind the counter.")
  print("The kind of face that has dried out every variety of trouble")
  print("and stopped reacting to any of them.")
  print("She doesn't look up when you come in.")
  print("\nIn the far corner — the guard.")
  print("Jacket half-undone. Cup in front of him.")
  print("Head drooping.")

  if tavern_choice == "2":
    print("\nYou move toward him. Careful. Slow.")
    print("You get close.")
    print("You reach.")
    print("\nOne eye opens.")
    print("He doesn't move otherwise. Just looks at you.")
    print("\n'Buy me a drink first.'")
    print("He closes the eye again.")
    print("\nYou take a step back.")
    print("Even drunk ones have instinct.")
    tavern_choice = "1"

  if tavern_choice == "1":
    print("\nYou go to the bar.")
    print("The barkeep still hasn't looked up.")
    print("You put four gold on the counter.")
    if player.gold >= 4:
      player.gold -= 4
      print("\nShe looks at it.")
      print("Then she looks at you.")
      print("'His tab.' You nod toward the corner.")
      print("\nShe picks up the four gold.")
      print("Doesn't say anything.")
      print("Just pours.")
      print("\nYou wait.")
      print("\nHalf an hour. Maybe a little more.")
      print("You nurse something cheap.")
      print("Watch the room without watching it.")

      if player.flags.get('companion_mira') and player.flags.get('companion_duo'):
        print("\nMira finds a seat near the wall. Facing the door.")
        print("Caleb leans against the wall near the rear.")
        print("He looks bored. He isn't.")
      elif player.flags.get('companion_mira'):
        print("\nMira finds a seat near the wall. Facing the door.")
        print("Her hands are folded on the table.")
        print("She could wait longer than this. You can tell.")
      elif player.flags.get('companion_duo'):
        print("\nCaleb leans against the wall near the rear.")
        print("He looks bored. He isn't.")

      print("\nThe guard's head drops fully.")
      print("The kind of sleep that catches you mid-thought.")
      print("His breathing changes.")
      print("His hand goes slack.")
      print("\nYou move.")
      print("The keys come free without a sound.")
      print("You pocket them.")
      print("You walk out.")
      player.flags['dungeon_keys'] = True
      print("\nYou have the keys.")
    else:
      print("\nYou don't have four gold.")
      print("The barkeep still hasn't looked at you.")
      print("You step back.")
      print("You'll need another way in.")
      player.flags['tavern_gold_failed'] = True


  # ── 6. Planning conversation — what we don't know, points to Enforcer office
  print("\n\nOutside. The alley mouth. Evening light going grey.")
  print("You stop.")

  if player.flags.get('companion_duo') and player.flags.get('companion_mira'):
    print("\nCaleb folds his arms.")
    print("'We know where they go in. We know the door.'")
    print("'We don't know the layout. We don't know the rotation.'")
    print("'And we don't know what we're walking into once we're past the first level.'")
    print("\nMira is quiet for a moment.")
    print("'The sub-level,' she says.")
    print("'Whatever's down there — they're not advertising it.'")
    print("'Which means it matters.'")
    print("\nCaleb nods once. Reluctant. Like agreeing costs him something.")
    print("'We need the transport record. The intake list.'")
    print("'Wherever they log who goes in — that's where the names are.'")
    print("\nA beat.")
    print("'Enforcer office,' Mira says.")
    print("'Has to be. They don't run something like this without documentation.'")
  elif player.flags.get('companion_mira'):
    print("\nMira leans against the wall.")
    print("'We know the door. We know it goes down.'")
    print("'We don't know who's in there. We don't know the rotation.'")
    print("She pauses.")
    print("'We need the intake record. Names. Dates. Where they put people.'")
    print("'The Enforcers document everything — they have to, at their scale.'")
    print("'There's an office somewhere in this district.'")
    print("'If there's a list, it's there.'")
  elif player.flags.get('companion_duo'):
    print("\nCaleb looks at the door from a distance.")
    print("'We're missing the intake record,' he says.")
    print("'Go in blind and we're guessing the whole way.'")
    print("'Enforcer office. There's always an office.'")
    print("'They run on paper. That's how you hold people accountable.'")
    print("'Or how you pretend to.'")
  else:
    print("\nYou think it through.")
    print("You know the door. You know it goes down.")
    print("You don't know the rotation. You don't know who's in there.")
    print("You don't know what they did with the three people you watched walk in.")
    print("\nA record exists somewhere. It has to.")
    print("Something that logs intake. Names. Assignments.")
    print("The Enforcers are an organization. Organizations document.")
    print("\nThere's an office in this district.")
    print("You're certain of it now.")

  player.flags['enforcer_office_known'] = True


  # ── 7. Enforcer office + Dara ─────────────────────────────────────────────
  print("\n\nThe Enforcer office sits at the east end of the square.")
  print("Not hidden. Just unremarkable.")
  print("A building that doesn't want to be noticed and mostly succeeds.")
  print("\nYou approach.")

  moral_path = player.corruption < 4

  if moral_path:
    # Moral path — overhear Dara, she doesn't know you're there
    print("\nYou stop outside the window.")
    print("It's open. Not wide. Wide enough.")
    print("\nA voice inside. A woman's voice.")
    print("Dry delivery. Like she finds most things slightly obvious.")
    print("\nShe's talking to someone who isn't responding much.")
    print("Working through something. An intake record, by the sound of it.")
    print("\n'...Twilight gets the cipher, Ledger sets the key.'")
    print("She says it the way you'd say something you've been told to remember")
    print("and have remembered so many times it's lost all texture.")
    print("Flat. Functional.")
    print("'Two words. That's the whole thing. You'd think they'd make it harder.'")
    print("She flips a page.")
    print("'Twilight. Ledger. In that order. That's the door.'")
    print("\nA pause.")
    print("Then she laughs, very briefly, at something on the page.")
    print("'Honestly, it's embarrassing.'")
    print("\nSomething shifts in the room. A stool. She's standing.")
    print("You step back from the window.")
    player.flags['cipher_answer_known'] = True
    player.flags['cipher_answer_source'] = 'overheard'
    player.flags['dara_met'] = True
    player.flags['dara_path'] = 'moral'

    print("\n[You now know the cipher answer: Twilight, Ledger.]")
    print("[She doesn't know you were there.]")

    if player.flags.get('companion_mira'):
      print("\nMira is looking at you.")
      print("Eyes sharp. Quiet question in them.")
      print("You nod once.")
      print("She nods back.")
      print("Enough said.")
    elif player.flags.get('companion_duo'):
      print("\nCaleb exhales.")
      print("Very quiet.")
      print("'There it is,' he says.")
      print("That's all.")

  else:
    # Immoral path — go in, she spots you, romance seed
    print("\nYou go in.")
    print("\nShe's behind a desk.")
    print("Late twenties, maybe early thirties — it's hard to tell in this light.")
    print("Dark hair. The kind of stillness that isn't calm so much as controlled.")
    print("She looks up when you enter.")
    print("She was expecting someone else.")
    print("She doesn't show it.")
    print("\n'This isn't a public office.'")
    print("Not aggressive. Just true.")
    print("\nShe studies you for a moment.")
    print("The way someone does when they're deciding which version of a situation this is.")
    print("Deciding whether you're a problem or something more interesting.")

    print("\n[1: Hold her gaze. Let the interest show.]")
    print("[2: Keep it even. Just the information.]")
    dara_gaze = input("\nChoose: ").strip()

    if dara_gaze == "1":
      print("\nYou hold it.")
      print("You don't hide that you're holding it.")
      print("\nShe notices.")
      print("Something in her expression shifts — not much.")
      print("Enough.")
      print("\nShe reaches for the paper in front of her.")
      print("Doesn't look at it.")
      print("'The intake cipher,' she says.")
      print("'Twilight and Ledger. In that order.'")
      print("'If you already knew that, you didn't need to come here.'")
      print("'Which means you did.'")
      print("\nShe tilts her head.")
      print("Very slightly.")
      print("'Interesting.'")
      player.flags['dara_romance'] = True
    else:
      print("\nYou keep your face even.")
      print("This is a transaction. You want it to stay that way.")
      print("\nShe reads that too.")
      print("Different read. Not disappointed.")
      print("Just — filed.")
      print("\n'The cipher is two words,' she says.")
      print("'Twilight. Ledger.'")
      print("'You can find the door yourself.'")
      print("She goes back to the page in front of her.")
      print("You're dismissed. Cleanly.")

    player.flags['cipher_answer_known'] = True
    player.flags['cipher_answer_source'] = 'dara_direct'
    player.flags['dara_met'] = True
    player.flags['dara_path'] = 'immoral'
    player.flags['enforcer_aligned'] = True

    if player.flags.get('companion_mira'):
      print("\nMira is outside when you come back through the door.")
      print("She reads your face.")
      print("She doesn't say anything about what she reads there.")
      print("Just starts walking.")
      print("You fall in beside her.")
      print("The silence has a shape to it.")


  # ── 8. Cipher puzzle solve — concatenation mechanic, Ledger footnote ──────
  print("\n\nYou're back in the square.")
  print("The stone tablet sits where it always has.")
  print("Twenty-six letters carved in order.")
  print("The question below them.")

  if not player.flags.get('cipher_answer_known'):
    print("\nYou stand in front of it.")
    print("The answer isn't there yet.")
    print("You can feel the gap where it should be.")
    print("You keep walking.")
  else:
    print("\nThis time you stop differently.")
    print("You know what it's asking now.")
    print("\nThe answer is two words.")
    print("Not the words themselves — the way they fit together.")
    print("The slot at the base is waiting.")

    print("\n[1: Attempt the cipher. (Costs: 2 Mana, 2 Manabda, 3 Gold)]")
    print("[2: Leave it for now.]")
    cipher_choice = input("\nChoose: ").strip()

    if cipher_choice == "1":
      can_attempt = (
        player.mana >= 2 and
        player.manabda >= 2 and
        player.gold >= 3
      )
      if can_attempt:
        player.mana -= 2
        player.manabda -= 2
        player.gold -= 3

        print("\nYou reach toward the slot.")
        print("Your hand goes in.")
        print("\nFor a moment — nothing.")

        print("\nThen the Ledger speaks.")
        print("Not loud. Never loud.")
        print("The way it always speaks — like it was already there, waiting for you to be ready.")

        print("\n  ┌──────────────────────────────────────────────────────────┐")
        print("  │  LEDGER FOOTNOTE — Indexing and Concatenation            │")
        print("  └──────────────────────────────────────────────────────────┘")
        print("\n  'The alphabet is a list.'")
        print("  'Twenty-six elements. Each one has a position.'")
        print("  'The first element sits at index zero. Not one. Zero.'")
        print("  'This is not a convention. It is the nature of the structure.'")
        print()
        print("  'A cipher built on the alphabet is built on those positions.'")
        print("  'You take the letters you need. You join them.'")
        print("  'That joining — one sequence appended to another — is concatenation.'")
        print()
        print("  'In the language of the world beneath this one:'")
        print()
        print("  '    elements = [\'A\',\'B\',\'C\',\'D\',\'E\',\'F\',\'G\',\'H\',\'I\',")
        print("  '                \'J\',\'K\',\'L\',\'M\',\'N\',\'O\',\'P\',\'Q\',\'R\',")
        print("  '                \'S\',\'T\',\'U\',\'V\',\'W\',\'X\',\'Y\',\'Z\']")
        print()
        print("  '    answer = (elements[19] + elements[22] + elements[8]")
        print("  '             + elements[11] + elements[8] + elements[6]")
        print("  '             + elements[7] + elements[19] + \' \'")
        print("  '             + elements[11] + elements[4] + elements[3]")
        print("  '             + elements[6] + elements[4] + elements[17])")
        print()
        print("  '    # = \'TWILIGHT LEDGER\''")
        print()
        print("  'The tablet does not ask for the letters.'")
        print("  'It asks for the order.'")
        print("  'Everything that follows flows from that sequence.'")
        print("  '                                         — The Ledger'")
        print("  └──────────────────────────────────────────────────────────┘")

        print("\nThe slot accepts your hand fully.")
        print("Something clicks. Deep in the stone.")
        print("The tablet face shifts — just slightly.")
        print("A compartment. Thin. Barely visible.")
        print("Inside: a small pouch. Fifty gold.")
        print("And a potion you recognize on sight.")

        player.gold += 50
        potion = ManabdaPotion()
        player.inventory.add_item(potion)
        player.flags['cipher_solved'] = True

        print(f"\n  + 50 Gold")
        print(f"  + {potion.name} added to inventory")

        if player.flags.get('companion_mira'):
          print("\nMira watches the compartment close itself back into the stone.")
          print("'The letters,' she says quietly.")
          print("'They were always the answer. The order is what makes them mean something.'")
          print("She looks at you.")
          print("Something in her face you don't quite have a name for.")
        elif player.flags.get('companion_duo'):
          print("\nCaleb looks at the closed tablet.")
          print("'Hm.' That's all.")
          print("High praise from him.")

      else:
        print("\nYou don't have the resources.")
        print("You pull back.")
        print("The slot doesn't fight you.")
        print("It just waits.")
    else:
      print("\nNot yet.")
      print("You know the answer now.")
      print("But you leave it.")
      print("It'll still be here.")


  # ── 9. Dungeon door — go in or decline ────────────────────────────────────
  print("\n\nBack across the square.")
  print("To the far wall.")
  print("To the door set flush with the stone.")
  print("\nYou stand in front of it.")

  if player.flags.get('companion_duo') and player.flags.get('companion_mira'):
    print("\nCaleb is two steps back. Arms loose. Ready.")
    print("Mira is directly beside you.")
    print("Neither of them speaks.")
    print("They've already decided.")
    print("They're waiting on you.")
  elif player.flags.get('companion_mira'):
    print("\nMira stands beside you.")
    print("Her breathing is controlled.")
    print("'She's down there,' she says.")
    print("Not asking. Not hoping.")
    print("Just saying it out loud so it's real.")
    print("'I can feel it.'")
    print("\nShe looks at you.")
    print("'I'm going in regardless. You don't have to.'")
    print("A beat.")
    print("'But I'd rather you did.'")
  elif player.flags.get('companion_duo'):
    print("\nCaleb stands at your shoulder.")
    print("'You sure about this?' he says.")
    print("Not doubt. Just the question you ask before something that can't be undone.")

  print("\nThe door sits in the stone.")
  print("No sound from below.")
  print("Either it's empty down there, or whatever's down there")
  print("has learned that sound travels upward.")
  print("\nYou have the keys." if player.flags.get('dungeon_keys') else
    "\nYou don't have the keys. You'll need another way.")

  print("\n[1: Go in.]")
  print("[2: Not yet. There's more to know first.]")
  dungeon_choice = input("\nChoose: ").strip()

  if dungeon_choice == "2":
    print("\nYou step back.")

    if player.flags.get('companion_mira'):
      print("\nMira closes her eyes. Just for a moment.")
      print("Then opens them.")
      print("'Okay,' she says.")
      print("'We come back.'")
      print("The way she says it isn't agreement.")
      print("It's a promise she's making to herself.")
    elif player.flags.get('companion_duo'):
      print("\nCaleb nods.")
      print("'Good call,' he says. 'Probably.'")

    print("\nYou move back into the square.")
    print("The door stays where it is.")
    print("It'll be there when you're ready.")
    player.flags['dungeon_declined'] = True

  else:
    # Enter dungeon
    if player.flags.get('dungeon_keys'):
      print("\nYou put the key in the lock.")
      print("It turns clean.")
      print("Well-maintained. Someone oils these locks.")
      print("That tells you something.")
      player.flags['dungeon_opened'] = True

    elif player.school == "Pyromancy":
      print("\nNo keys. You look at the hinges instead.")
      print("Iron. Old. Three of them.")
      print("Above in the square — a cart scrapes stone. Voices.")
      print("Cover noise. You don't wait for better.")

      class DungeonHinge:
        def __init__(self):
          self.name = "iron hinge"
          self.flame_resistance = 15
          self.hp = 30
          self.is_object = True
          def add_status(self, s): pass
          def take_damage(self, dmg, dtype):
            self.hp -= dmg
        add_status = add_status
        take_damage = take_damage

      hinge = DungeonHinge()
      result = player.pyromancy_burn(hinge)
      if result:
        print(f"\n{result}")
      if hinge.hp <= 0 or getattr(hinge, 'flame_resistance', 15) <= 0:
        print("\nThe hinge pins soften and give.")
        print("The door lifts free on its own weight.")
        player.flags['dungeon_opened'] = True
      else:
        print("\nNot enough heat.")
        print("The hinges are scorched but holding.")
        print("You step back.")
        player.flags['dungeon_no_entry'] = True

    elif player.school == "Chronomancy":
      print("\nNo keys. You press your hand flat against the lock face.")
      print("Iron. Solid. Made to last.")
      print("You ask it how long it's been here.")
      print("You ask it to keep going.")

      class DungeonLock:
        def __init__(self):
          self.name = "dungeon lock"
          self.durability = 40
          self.age = 30
          self.broken = False
          self.is_dust = False
          self.is_object = True

      lock = DungeonLock()
      result = player.fast_forward_time(lock)
      if result:
        print(f"\n{result}")
      if lock.broken or lock.is_dust:
        print("\nThe lock crumbles from the inside out.")
        print("Rust where iron was. Dust where rust was.")
        print("The door swings free.")
        player.flags['dungeon_opened'] = True
      else:
        print("\nThe lock is weakened but not gone.")
        print("It holds.")
        player.flags['dungeon_no_entry'] = True

    else:
      print("\nNo keys. No way through.")
      print("The door doesn't move for wanting.")
      print("\nYou step back.")
      player.flags['dungeon_no_entry'] = True

    if player.flags.get('dungeon_opened'):
      print("\nThe door opens.")
      print("Steps descend into dark.")
      print("The dark isn't empty.")
      print("You can feel that much from here.")
      print("\nYou go in.")

      if player.flags.get('companion_mira'):
        print("\nMira goes first.")
        print("No hesitation.")
        print("Her feet find the steps without sound.")
        print("You follow.")
        if player.flags.get('companion_duo'):
          print("Caleb comes last.")
          print("He pulls the door closed behind him.")
          print("Gently.")
          print("The dark receives you.")
      elif player.flags.get('companion_duo'):
        print("\nCaleb signals once — two fingers, down — then goes.")
        print("You follow.")
        print("The dark receives you.")
      else:
        print("The dark receives you.")

      player.flags['dungeon_entered'] = True
      print("\n\n  [The dungeon begins.]")
      print("  [Story continues below.]")
      print("\n  — inside dungeon continues in this file —")