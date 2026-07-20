from ui import print, input
from wizard import Wizard
from descriptions import display_spell_descriptions


def prologue():
  print("Darkness.")
  print("Not the comfortable kind.")
  print("The kind that has weight. That presses.")
  print("\nThen — a sound.")
  print("Not heard. Felt.")
  print("Somewhere behind your sternum. A single word.")
  print("\n'The ledger awakens.'")
  print("\nLight bleeds in slowly. Stone walls. Cold air.")
  print("A terminal stands before you. Obsidian. Ancient.")
  print("It has been waiting. You get the sense it has been\n"
        "waiting")
  print("for a very long time.")
  print("\nA prompt blinks across its face in letters the color of\n"
        "embers.")
  print("It wants something simple.")
  print("It wants a name.")
  player_name = input("\nEnter True Name: ")
  player = Wizard(name=player_name)
  player.flags = {}
  player.gold = 0
  player.corruption = 0

  print(f"\nThe terminal pulses once. Accepts it.")
  print(f"Somewhere, something was written down.")

  print("\nThe stone before you shifts.")
  print("Nine sigils carve themselves into its face.")
  print("Slowly. Like they hurt to appear.")
  print("\nAbove them, words burn into existence:")
  print("'Power has a price. The price has a name.'")
  print("'Choose it.'")
  print("\n  Pyromancy     — The School of Wrath.      Burn, or be burned.")
  print("Cryomancy — The School of Stillness. Preserve, or\n"
        "entomb.")
  print("Chronomancy — The School of Time. Wait, or be\n"
        "forgotten.")
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
  print("\n'He's here,' an assertive voice in your head declares,\n"
        "startling you.")
  print("\nThen — footsteps.")
  print("From nowhere. From everywhere.")
  print("\nAn older wizard stands where none stood before.")
  print("He did not walk in. He simply is.")
  print("\nHe looks at you.")
  print("Not the way someone looks at a person.")
  print("The way someone looks at a thing they've already\n"
        "assessed")
  print("and found to be less than they hoped for.")
  print("A long moment passes.")
  print("He says nothing.")
  print("Whatever question he asked himself, you weren't\n"
        "consulted.")
  print("Whatever answer he arrived at, it doesn't seem to\n"
        "impress him.")
  print("\nSomething about it sits wrong.")
  print("You don't know why. You file it away.")
  print("\nFrom his robe he draws a ledger.")
  print("Bound in obsidian. It opens without being opened.")
  print("Something is written. You don't see what.")
  print("It closes. Vanishes.")
  print("He turns to a door that was not there a moment ago.")
  print("Great oak. Black as the ledger. He shoves it open.")
  print("Fog pours through like it was waiting on the other\n"
        "side.")
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
    print("Just a jagged slope winding downwards into the unknown,\n"
          "strewn with sharp rocks jutting towards the sky.")
    print("The world didn't notice you took your time.")
    print("It just continued without you.")
    print("Somehow that is worse.")

  return player