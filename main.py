from wizard import Wizard
from combat import simple_combat
from entities.monster import RavenSwarm
from items import (Item, Consumable, Equipment, HPPotion, ManaPotion,
                   ManabdaPotion, PassRune, ExceptVial, FinallyFlask,
                   Cloak, Staff, Rod, Scepter)
from entities.humanoid import DesperateTraveler, Enforcer, FrightenedWoman
from wizard_core import Wizard
import random

if __name__ == "__main__":
  print("A voice, not your own, scrapes the inside of your skull: 'The ledger awakens.'")
  print("The stone terminal in front you is cold. Dark. Silent.")
  print("it waits,just a few steps in front of you,the start of your career as a true wizard,aiming to rule the path")
  print("A prompt blinks across the top of it in red letters, It wants a name.")
  player_name = input("Enter True Name: ")
  player = Wizard(name=player_name)
  player.flags = {}

  print(f"\nSpellbook opens: {player.spells} | Mana: {player.mana}/{player.max_mana} | Manabda: {player.manabda}")
  print(f"\n{player}")
  print("\nYou are alone. The mountain air bites.")
  print(" more letters appear afterwards : Power has a price. The price has a name.")
  print("Choose it.")
  print("\nNine sigils are carved into stone before you:")
  print("Pyromancy - The School of Wrath. Burn, or be burned.")
  print("Cryomancy - The School of Stillness. Preserve, or entomb.")
  print("Chronomancy - The School of Time. Wait, or be forgotten.")
  print("Necromancy - The School of Ending. Keep, or be kept.")
  print("Enhancement - The School of Self. Break, or be broken.")
  print("Illusion - The School of Lies. See, or be deceived.")
  print("Conjuration - The School of Calling. Take, or be taken.")
  print("Shadow - The School of Secrets. Hide, or be hunted.")
  print("Transmutation - The School of Change. Bend, or be bent.")
  school = input("Choose thy School: ")
  player.choose_school(school.capitalize())

  print("\nThe silence breaks. Footsteps.")
  print(
    "a booming voice speaks in your head: he is here, you look up as the end of the words trail off into nothingness.")
  print("An older wizard stands where none stood before. He speaks no greeting.")
  print("He stares, casting a critical eye as if appraising your value... and barely nods.")
  print(
    "He pulls a ledger from his robe. Bound in obsidian.it flips open without him making it do so,then It vanishes again.")
  print("He turns to a great oaken door, black as obsidian, and shoves it open.")
  print("Fog billows from beyond. He steps through.")
  print("\nTwo paths present themselves:")
  print("1: Follow at a brisk pace to demand answers.")
  print("2: Hold. Get your bearings. Follow at a distance. He is not your master.")
  choice_1 = input("The choice is yours [1/2]: ")

  if choice_1 == "1":
    print(f"\n{player.name} follows at a brisk pace, catching the door before it shuts.")
  else:
    print(f"\n{player.name} waits. The door thuds shut. A moment passes.")
    print("You scoff. 'I care not what the old codger does or goes.'")
    print("'For my Path has just begun, and his part in it is done.'")
    print("You shove the door open yourself.")

  print("Beyond: a barren expanse of mountainous terrain under a starry, indifferent sky.")
  print("The Path begins where guidance ends.")
  print("\nThe wind carries a sound. A wail shrieks into the night sky.")
  print("To your right: two dark figures. Above them, a flock of ravens.")
  print("But these are not birds. Too many eyes. Too much hunger. They descend.")
  print("This world is an overlay. Bleak. Hungry.")
  print("Here, manabda is not given. It is spent.")
  print("\nThe mountain slope ahead descends toward a tiny town.")
  print("It bursts with activity. Tiny shadows move to and fro.")
  print("Commerce? Duels? Or just more hungry things? Unknown.")
  print("\nThree paths burn in your mind:")
  print("1: Help the figures. Manabda may be required. Death may follow.")
  print("2: Do not help. Skip the lesson. Skip the risk. Skip the reward.")
  print("3: Ignore both. Descend to the town. Chase answers, not people.")
  choice_2 = input("The Path demands choice. Not comfort. [1/2/3]: ")

  if choice_2 == "1":
    print("\nYou move toward the figures. The ravens shriek louder.")
    combat = RavenSwarm()
    simple_combat(player, combat)
    if player.is_alive():
      player.gain_exp(combat.exp_value)
      print("\nThe ravens scatter... for now.")
      print("The man stands. Medium build, average height. Mop of messy blonde hair hides his eyes.")
      print("The woman cowers behind him. Homely. Quiet. Hands over her head.")
      print("The man does not thank you. He glares. 'You. Pathwalker. Here to rob us?'")

      print("\n[1: 'I saved your lives. A thank you would suffice.']")
      print("[2: 'Rob you? I don't need your scraps. What is this place?']")
      print("[3: 'Easy. I'm not your enemy.']")
      print("[4: Say nothing. Conserve strength.]")
      choice_3 = input("Your response: ")

      if choice_3 == "1":
        print(f"\nThe man snorts. 'Gratitude is for the dead. The strong take.'")
        print(f"He eyes your spellbook. '{player.school}... so that's your gamble.'")
        print("'Either way. The town below doesn't care what School you chose. They'll bleed you too.'")
        player.flags['traveler_hostile'] = True
      elif choice_3 == "2":
        print("\n'Place?' He laughs, sharp and humorless. 'This is the Threshold.'")
        print("'Where fools come to walk the Path. Where true wizards are made.'")
        print("He spits. 'At least, that's the lie. None have ever returned. None.'")
        print("The woman whispers: 'They say the first voice was the last wizard who tried.'")
        player.flags['traveler_wary'] = True
      elif choice_3 == "3":
        print("\nYou raise empty hands. 'Easy. I just killed a swarm for you. I'm not your enemy.'")
        print("He studies you. The blonde hair doesn't move, but his shoulders drop a fraction.")
        print("'...No. No you're not. You could've let us die.' He exhales. 'My mistake.'")
        print("The woman peeks out from behind him. 'Thank you. Truly.'")
        print("\n[1: 'You mentioned a Tithe. What's going on?']")
        print("[2: 'We should move. That bell...' ]")
        print("[3: 'What's your name?' ]")
        choice_4 = input("Choose: ")

        if choice_4 == "1":
          print("\n'The town,' he says, voice low. 'It's not a town. It's a farm.'")
          print("'The Enforcers collect from Pathwalkers. Mana. Manabda. Whatever they can rip out.'")
          print("'For the underling. And above him...' He shakes his head. 'They don't walk the Path.'")
          print("'They rule this in-between. And they like it that way.'")
        elif choice_4 == "2":
          print("\nHe nods grimly. 'Right. The Tithe. We need to move.'")
          print("'But... thank you. For not being like the others.'")
        elif choice_4 == "3":
          print("\nHe tenses again. 'Names are currency here. You earn them, or you steal them.'")
          print("The woman touches his arm. 'She's right. Not yet.'")
          print("He sighs. 'Survive the town. Then we'll talk names.'")

        print("\nHe reaches into his coat. 'Look. We don't have much. But this...'")
        print("He drops a small stone rune into your hand. It hums. 'Sort.'")
        print("'Found it on a corpse last month. Couldn't make it work. Maybe you can.'")
        print("Item acquired: Sort Rune")
        print(player.inventory.add("Sort Rune"))
        player.flags['traveler_friend'] = True
      elif choice_3 == "4":
        print("\nSilence. The man shifts, uncomfortable with your stare.")
        print("The woman speaks first. 'Please... the town. They send the swarms.'")
        print("'For tribute. For the Enforcers. For the ones above them.'")
        if player.mana < player.max_mana:
          player.mana += 5
          if player.mana > player.max_mana: player.mana = player.max_mana
          print(f"You breathe. Mana recovers: {player.mana}/{player.max_mana}")

      print("\nA bell tolls from the town below. Once. Twice. Three times.")
      print("The man's face pales. 'The Tithe. The Enforcers are collecting.'")
      print("He grabs the woman's arm. 'We have to run. Or hide. Or pay.'")
      print("'If you're not marked by the ruling class, you're inventory to them.'")

      if player.flags.get('traveler_friend'):
        print("\n[1: 'Stay with me. We'll handle the Enforcers together.' ]")
        print("[2: 'Go. Hide. I'll draw them off.' ]")
        print("[3: 'Actually, I changed my mind. Give me that rune.' ]")
      else:
        print("\n[1: 'Tithe? Explain. Now.' ]")
        print("[2: 'I'll handle the Enforcers.' ]")
        print("[3: 'You tried to call me a thief. Draw.' ]")
        print("[4: 'Not my problem.' ]")

      choice_5 = input("The bell rings again. Choose: ")

      if player.flags.get('traveler_friend') and choice_5 == "1":
        print("\n'Together?' He looks at the woman, then you. 'Alright. But if we die...'")
        print("'We die trying to be more than inventory.' He draws a rusted dagger.")
        print("The woman doesn't fight, but she doesn't run either. She trusts you now.")
        player.flags['companion'] = "Traveler Duo"
      elif player.flags.get('traveler_friend') and choice_5 == "2":
        print("\n'That's... noble. Stupid, but noble.' He grips your shoulder briefly.")
        print("'Don't die for us, Pathwalker. The world needs fewer corpses.'")
        print("They flee into the fog. You turn toward the town alone.")
        player.flags['traveler_owes_life_debt'] = True
      elif player.flags.get('traveler_friend') and choice_5 == "3":
        print("\nThe woman flinches like you slapped her. The man's face shuts down.")
        print("'...Right. Should've known.' He pulls her away without another word.")
        print("No fight. Just disappointment. That hurts worse.")
        if "Sort Rune" in player.inventory.items:
          player.inventory.remove_item("Sort Rune")
          print("You feel the Sort Rune vanish from your pack. He took it back.")
      elif not player.flags.get('traveler_friend'):
        if choice_5 == "1":
          print("\n'The town's a factory,' he hisses. 'They extract... resources... from Pathwalkers.'")
          print("'The Enforcers work for an underling. Just a boot. But above him...'")
          print("He looks skyward. 'There are others. They don't walk the Path.'")
          print("'They rule this in-between. And they like it that way.'")
          print("The woman sobs. 'They took my sister. Said she had potential.'")
          print("\nThe man exhales. You didn't attack. He relaxes slightly.")
          print("He reaches into his coat. 'Here. You saved us. Even if you're a fool for it.'")
          print("He drops a small stone rune into your hand. It hums. 'Sort.'")
          print("Item acquired: Sort Rune")
          print(player.inventory.add("Sort Rune"))
        elif choice_5 == "2":
          print("\nYou descend toward the town. The bell grows louder.")
          print("The man calls after you: 'You'll die! They're not alone!'")
          print("If you don't stop the Enforcers now, the town stays under their heel.")
          print("The voice in your head is silent. Or is it a different one?")
        elif choice_5 == "3":
          traveler = DesperateTraveler()
          print("\nYou step toward him. 'You accused me of robbery after I saved you.'")
          print("His eyes narrow. 'And? Gratitude is weakness here. You want something?'")
          print("'Fine. Lesson one of the Path: take.' He draws his dagger. No words left.")
          print("\n[COMBAT INITIATED - NO DIPLOMACY]")
          simple_combat(player, traveler)
          if player.is_alive() and not traveler.is_alive():
            print("\nHe staggers, bleeding, then bolts into the fog. Gone.")
            print("The woman stares at you, terrified. 'He... he dropped this...'")
            print("At your feet: a small stone rune. It hums. 'Sort.'")
            print("Item acquired: Sort Rune")
            player.inventory.add_item("Sort Rune")
            print("\nThe woman won't leave your side now. 'I have nowhere else...'")
            player.flags['companion'] = "Frightened Woman"
          elif not player.is_alive():
            print("Darkness takes you. The Path ends here.")
            exit()
        elif choice_5 == "4":
          print("\nYou leave them. The bell tolls a fourth time.")
          print("Behind you, running footsteps. Then silence.")
          print("The Path doesn't reward mercy. Or does it? The voice doesn't say.")

  elif choice_2 == "2":
    print("\nYou do not help. The wail cuts short. Silence returns.")
    print("A lesson unlearned. Manabda unspent. Is that wise?")
    print("You turn away. The mountain air feels colder.")
    print("\nAhead, the town bell tolls. Four times. A warning?")
    print("Your path leads down, but the screams echo in your head.")
    print("Your School stirs within you. Your choices echo.")
    player.flags['ignored_travelers'] = True
    print(f"Current state: {player}")

  elif choice_2 == "3":
    print("\nYou ignore the screams. The town below calls louder.")
    print("Your goal is to rule all wizarding kind. Not save strays.")
    print("This is why none speak of it. It is not the same world.")
    player.flags['skipped_raven_fight'] = True

    print("\nAs you descend, the path splits. Left toward the bell tower. Right toward smoke.")
    print("The bell tolls once. The Ledger in your mind grows heavy.")
    print("[1: Toward the bell - confront the source]")
    print("[2: Toward the smoke - something's burning]")
    choice_6 = input("Choose: ")

    if choice_6 == "1":
      print("\nYou approach the bell tower. The sound rattles your teeth.")
      print("Two Enforcers stand guard. One turns. 'Pathwalker. Tithe or blood.'")
      print("\n[1: Fight the Enforcers]")
      print("[2: Pay Tithe - costs 5 mana + 3 manabda]")
      print("[3: Lie - attempt deception]")
      choice_7 = input("Choose: ")

      if choice_7 == "1":
        enforcer1 = Enforcer("Town Enforcer")
        enforcer2 = Enforcer("Town Enforcer")
        print("\n'Then bleed.' They draw batons crackling with stolen manabda.")
        simple_combat(player, enforcer1)
        if player.is_alive():
          simple_combat(player, enforcer2)
        if player.is_alive():
          print("\nThe Enforcers fall. Behind them, a chest. Inside: a Sort Rune.")
          print("'Belonged to the last Pathwalker who said no,' one gasps before dying.")
          print("Item acquired: Sort Rune")
          player.inventory.add_item("Sort Rune")
          player.flags['enforcers_defeated'] = True
      elif choice_7 == "2":
        if player.mana >= 5 and player.manabda >= 3:
          player.mana -= 5
          player.manabda -= 3
          print(f"\nYou pay. Mana: {player.mana}/{player.max_mana} | Manabda: {player.manabda}")
          print("'Smart. The Ruling Class appreciates compliance.'")
          print("They let you pass. No Sort rune. But you're alive.")
          player.flags['paid_tithe'] = True
        else:
          print("\n'You don't HAVE it.' They attack anyway.")
          enforcer1 = Enforcer("Town Enforcer")
          simple_combat(player, enforcer1)
      elif choice_7 == "3":
        print("\n'I serve the Ruling Class,' you lie.")
        if random.randint(1, 100) > 70:
          print("'Prove it. Show your mark.'")
          print("You have no mark. They attack.")
          enforcer1 = Enforcer("Town Enforcer")
          simple_combat(player, enforcer1)
        else:
          print("'Hmph. Move along, then. Don't let me catch you near the Tithe house.'")
          print("You bluffed past them. No combat. No Sort rune yet.")

    elif choice_6 == "2":
      print("\nYou approach the smoke. A building burns. Scorch marks on stone.")
      print("A corpse in traveler clothes lies nearby. Raven peck marks cover it.")
      print("In his hand: a cracked rune. It still hums faintly. 'Sort.'")
      print("\n[1: Take the Sort Rune]")
      print("[2: Leave it - seems cursed]")
      choice_8 = input("Choose: ")

      if choice_8 == "1":
        print("You pry it from his fingers. It burns, but you endure.")
        print("Item acquired: Damaged Sort Rune")
        player.inventory.add_item("Sort Rune")
        player.flags['found_dead_traveler'] = True
      else:
        print("You leave it. Some power isn't worth the price.")
        print("No Sort rune. The smoke stings your eyes.")

  if hasattr(player, 'inventory') and "Sort Rune" in player.inventory.items:
    print("\nThe Sort Rune in your pack begins to glow, hot against your ribs.")
    print("You pull it out. It floats from your palm, then seeps into your skin like water.")
    print("Your vision sharpens. The world... loads differently.")
    print("You can now SENSE objects. Sort the area.")
    print("\n[NEW ABILITY UNLOCKED: sort(location)]")
    print("Try: sort('mountain') or sort('town') to reveal items/enemies")
    if "sort" not in player.abilities:
      player.abilities.append("sort")
    player.inventory.remove("Sort Rune")

  print(f"\n=== CHAPTER 1 COMPLETE ===")
  print(f"{player}")
  print(f"Flags: {player.flags}")
  if "companion" in player.flags:
    print(f"Companion: {player.flags['companion']} follows you.")
  print("\nThe Path stretches onward...")