import random
from ui import print, input
from combat import simple_combat
from enemy import Enforcer, Consequential, MotherRaven, EnforcerCommander, Dara
from systems.checkpoint import save_checkpoint
from ch1.solo import solo_promise_dungeon
from ch1.duo import duo_dungeon_route


def the_dungeon(player):
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
    print("Not doubt. Just the question you ask before something\n"
          "that can't be undone.")

  print("\nThe door sits in the stone.")
  print("No sound from below.")
  print("Either it's empty down there, or whoever — or whatever\n"
        "— is down there has learned that screams from below\n"
        "matter little to those above.")
  print("\nYou have the keys." if player.flags.get('dungeon_keys') else
    "\nYou don't have the keys. You'll need another way.")

  if player.flags.get('enforcer_aligned'):
    print("\nA shape separates from the shadow near the far wall.")
    print("You knew before you saw her.")
    print("Something in the way the air changes.")
    print("\nDara.")
    print("Two Enforcer escorts materialize at her flanks.")
    print("They were always there. You just didn't see them.")
    print("\nShe looks at the door. Then at you.")
    print("Then — unhurried, like she's deciding something she\n"
          "already decided — she turns to the escorts.")
    print("\n'That won't be necessary.' Her voice is full of\n"
          "control.")
    print("'Leave us.'")
    print("\nThey go. No hesitation. No question.")
    print("Their boots find the steps back up into the square")
    print("and for a moment — just a moment —")
    print("their silhouettes fill the stairway and cut off every\n"
          "thread of light")
    print("filtering down from above.")
    print("Total dark.")
    print("You. Her. The door.")
    print("Then they're gone and the dark becomes just dim again.")
    print("\nShe produces a key from inside her coat.")
    print("Doesn't hand it to you yet.")
    print("Just holds it.")
    print("\n'You want to know how this place works,' she says.")
    print("Not a question.")
    print("'Not the town. The organization.'")
    print("She turns the key slowly in her fingers.")
    print("'Most people in the Twilight think they're part of\n"
          "something ancient.'")
    print("'Something inevitable. Like they found the winning side\n"
          "early and had enough sense to change sides.'")
    print("\nA pause. She looks at the door.")
    print("'They're not wrong about the power. They're wrong about\n"
          "who holds it.'")
    print("'The ones at the top don't know what they're sitting on\n"
          "top of.'")
    print("'They named themselves after something they've never\n"
          "seen.'")
    print("'Something that doesn't belong to them.'")
    print("'Something that doesn't belong to anyone — yet.'")
    print("\nShe finally looks at you.")
    print("Something in it that isn't quite readable.")
    print("Assessment. Curiosity. Something else underneath both\n"
          "of those.")
    print("\n'I have a hunch about you,' she says.")
    print("'I'm usually right about hunches.'")
    print("'Usually.'")
    print("\nShe steps to the door. Slides the key in.")
    print("It turns without sound.")
    print("Well-oiled. Of course it is.")
    print("\n'Stay close,' she says. 'And try not to enjoy this too\n"
          "much.'")
    print("A beat.")
    print("'Or do. I won't tell anyone.'")
    player.flags['dungeon_opened'] = True
    player.flags['dara_dungeon'] = True

  can_enter = (
    player.flags.get('dungeon_opened') or
    player.flags.get('dungeon_keys') or
    player.school in ("Pyromancy", "Chronomancy")
  )

  if can_enter:
    print("\n[1: Go in.]")
    print("[2: Not yet. There's more to know first.]")
    dungeon_choice = input("\nChoose: ").strip()
  else:
    print("\n[1: Not yet — find another way in.]")
    dungeon_choice = "2"

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

        def add_status(self, s):
          pass

        def take_damage(self, dmg, dtype):
          self.hp -= dmg

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
      print("\nNo keys. You press your hand flat against the lock\n"
            "face.")
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
      if not player.flags.get('tavern_marked'):
        print("\nExcept the door is locked — try finding a key?")
        print("\nSomewhere in the square behind you,")
        print("a tavern sits with its light on.")
        print("Vardeth sleeps badly. But something in there doesn't\n"
              "sleep at all.")
        if player.flags.get('companion_mira'):
          print("\nMira doesn't say anything.")
          print("She just looks at the door.")
          print("Then back at the square.")
          print("The direction she looks is not accidental.")
        elif player.flags.get('companion_duo'):
          print("\nCaleb tilts his head toward the square.")
          print("'There's usually a key,' he says.")
          print("'And usually someone who has it.'")
          print("'And usually somewhere that someone goes after a long\n"
                "shift.'")
          print("He leaves it there.")
        else:
          print("\nYou stand with it a moment.")
          print("The door isn't going anywhere.")
          print("Neither is whoever's holding the key to it.")
        player.flags['dungeon_no_entry'] = True

      else:
        print("\nExcept the door is locked — and you already know where\n"
              "the key is. Try going back for it?")
        if player.flags.get('companion_mira'):
          print("\nMira's jaw tightens.")
          print("'We were right there,' she says.")
          print("'He was right there.'")
          print("She doesn't add anything else.")
          print("She doesn't need to.")
        elif player.flags.get('companion_duo'):
          print("\nCaleb exhales.")
          print("'The guard. The tavern. The keys on his belt.'")
          print("'We walked past all three.'")
          print("He says it without heat. Just inventory.")
        else:
          print("\nYou know exactly where the key is.")
          print("You know exactly who has it.")
          print("You just have to go back.")
        player.flags['dungeon_no_entry'] = True

    if player.flags.get('dungeon_opened'):
      save_checkpoint(player)
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
          print("He pulls the door closed behind him. Gently.")
          print("The lock turns once — a sound like a conclusion.\n"
                "Whatever light was left above narrows to nothing.")
          print("The dark receives you.")
        else:
          print("The door draws shut behind you.")
          print("The lock turns once — a sound like a conclusion.\n"
                "Whatever light was left above narrows to nothing.")
          print("The dark receives you.")
      elif player.flags.get('companion_duo'):
        print("\nCaleb signals once — two fingers, down — then goes.")
        print("You follow.")
        print("The door draws shut behind you.")
        print("The lock turns once — a sound like a conclusion.\n"
              "Whatever light was left above narrows to nothing.")
        print("The dark receives you.")
      else:
        print("The door draws shut behind you.")
        print("The lock turns once — a sound like a conclusion.\n"
              "Whatever light was left above narrows to nothing.")
        print("The dark receives you.")

      player.flags['dungeon_entered'] = True
      print("\n\n  [The dungeon begins.]")
      print("  [Story continues below.]")
      print("\n  — inside dungeon continues in this file —")

      print("\nThe stairs go down further than they should.")
      print("The stone here is older than anything built above it.")
      print("\nThe smell hits first. Rust — old and deep, like bones\n"
            "that had been still too long and were only now\n"
            "remembering how to move.")
      print("\nThe entrance isn't a room.")
      print("It's a space that was never meant to be one.")
      _solo_entrance = not (player.flags.get('companion_mira')
                            or player.flags.get('companion_duo')
                            or player.flags.get('dara_dungeon'))
      if not _solo_entrance:
        print("Iron maidens line the near wall — three of them,\n"
              "mouths shut.")
        print("A barrel sits beside them, filled with spiked things\n"
              "that would throw horror into the spirit of\n"
              "even the most brave.")
        print("Not stored here. Kept here.")
        print("There's a difference.")
      print("\nThe path ahead stretches forward into dark.")
      print("Every few feet a torch burns in its bracket.")
      print("The light doesn't comfort.")
      print("It just means someone wanted to see\n"
            "what was happening down here.")

      if player.flags.get('dara_dungeon'):
        print("\nDara doesn't slow down.")
        print("Her eyes move across the iron maidens the way\n"
              "yours might move across furniture.")
        print("Taking inventory. Nothing more.")
        print("\nShe doesn't look at the barrel.")
        print("She already knows what's in it.")

      print("\nYou take a step forward.")
      print("\nThen —")
      print("\nA scream.")
      print("Human. Distant.")
      print("The kind that comes from somewhere past endurance.")
      print("\nThen silence.")
      if _solo_entrance:
        print("\nhhhrrrRRRNNN—")
        print("\nA growl rises from somewhere down within")
        print("the deep darkness of the stretching corridor")
        print("that lies in front of you.")
        print("\nThen cuts off clean.")
        print("Like whatever made it decided it was done.")
        print("\nThe silence after it is almost worst...")
        print("\nYou look left to right in paranoia —")
        print("though the noise came from the shadows ahead,")
        print("all that stares back at you is a line of iron maidens")
        print("along the walls.")
        print("Random barrels fill the space between you and them,")
        print("some of them closed and some of them opened,")
        print("filled to the brim with metal spiked things.")
        print("\nThe torchlight flickers, barely illuminating the hallway.")
        print("You move forward, a few steps at a time, slow and careful.")
      else:
        print("\nThen something else.")
        print("A sound that starts low and builds —\n"
              "running almost parallel in rhythm to the scream,\n"
              "like it's answering it.")
        print("It rises.")
        print("Then cuts off clean.")
        print("Like whatever made it decided it was done.")
        print("\nThe silence after it is worse than the sound.")

      if player.flags.get('dara_dungeon'):
        print("\nDara doesn't stop walking.")

      if player.flags.get('companion_mira') and player.flags.get('companion_duo'):
        print("\nCaleb doesn't move.")
        print("His hand finds your arm — not grabbing, just there.")
        print("A warning.")
        print("\nMira moves.")
        print("One step. Two.")
        print("Then she says the name.")
        print("\n'Sera.'")
        print("Not loud. Barely above breath.")
        print("But certain.")
        print("\nAnd then she runs.")

      elif player.flags.get('companion_mira'):
        print("\nMira stops.")
        print("Everything in her goes still.")
        print("\nThen she says the name.")
        print("\n'Sera.'")
        print("The word barely makes it out.")
        print("\nAnd then she runs.")

      elif player.flags.get('companion_duo'):
        print("\nCaleb doesn't move.")
        print("He listens to the silence after.")
        print("'That second sound,' he says.")
        print("'That's not a prisoner.'")
        print("He looks at you.")
        print("'Whatever they're doing down here —\n"
              "it's not just about the tithe.'")

      elif not player.flags.get('dara_dungeon'):
        if player.flags.get('promised_sister_search') or \
           player.flags.get('promised_source'):
          print("\nYou know the answers to helping Caleb and Mira")
          print("are somewhere in this dungeon.")
          print("\nBut now you're here alone — lost, without any")
          print("sort of guide forward.")
          print("\nYou stop — hesitating, rethinking your progression onwards.")
          print("Is this really worth it?")
          print("But you remember your promise,")
          print("and hope that the ends will justify the bravery needed.")
          if player.flags.get('promised_source'):
            print("\nAnd stopping the ravens from helping the Enforcers")
            print("is a win everyone in this town needs too.")
          print("\nSomewhere above all the cells you hear")
          print("what sounds almost like the great rustling")
          print("of wings moving.")
          print("\nThe dark dank dread of places like this")
          print("plays tricks on the mind.")
          print("Maybe it's just your imagination though?")
          print("\nThe darkness ahead is willing to test that resolve.")
        else:
          print("\nNo promise brought you here.")
          print("No one is waiting on you.")
          print("\nYou came because dungeons like this")
          print("have things worth taking,")
          print("and because the town talks about this one")
          print("the way people talk about a debt")
          print("they're hoping gets forgotten.")
          print("\nSomewhere above all the cells you hear")
          print("what sounds almost like the great rustling")
          print("of wings moving.")
          print("\nThe dark dank dread of places like this")
          print("plays tricks on the mind.")
          print("Maybe it's just your imagination though?")

      if player.flags.get('companion_mira'):
        print("\nShe's already at the first corridor branch.")
        print("Moving fast. Not looking back.")
        print("\nYou can follow. You can try to stop her.")
        print("Or you can let her go.")
        print("\n[1] Run after her")
        print("[2] Let her go")

        mira_choice = input("\n> ").strip()

        if mira_choice == "1":
          roll = random.randint(1, 100)

          if roll <= 60:
            print("\nYou catch her arm.")
            print("She pulls against it — hard.")
            print("'Let go of me.'")
            print("Not angry. Desperate.")
            print("'That could be her.'")
            print("\nYou hold.")
            print("She stops pulling.")
            print("Breathes.")
            print("\n'We go together,' you say.")
            print("Or you don't say anything.")
            print("The grip says it.")
            print("\nShe nods. Once.")
            print("Doesn't look at you.")
            print("'Together then.'")
            player.flags['mira_held'] = True

          else:
            roll2 = random.randint(1, 100)
            if roll2 <= 80:
              print("\nYou're faster.")
              print("She knows it the moment you pull alongside her.")
              print("\nYou step in front.")
              print("She almost runs into you.")
              print("'Move.' Her voice is raw.")
              print("\n'Not alone,' you say.")
              print("\nShe stares at you.")
              print("Then past you.")
              print("Then back.")
              print("\n'Fine.' Barely a word.")
              print("'But we move now.'")
              player.flags['mira_held'] = True

            else:
              roll3 = random.randint(1, 100)
              if roll3 <= 50:
                print("\nYou catch her.")
                print("Barely.")
                print("One hand on her shoulder, pulling her back\n"
                      "into the wall.")
                print("She doesn't fight it this time.")
                print("She's listening.")
                print("\nSomewhere deeper in the dark —")
                print("a sound.")
                print("Not the scream. Something quieter.")
                print("Something that might be a voice.")
                print("\nMira goes absolutely still.")
                print("'Did you hear that.'")
                print("Not a question.")
                player.flags['mira_held'] = True

              else:
                print("\nShe's gone.")
                print("Around the corner before you clear the entrance.")
                print("The torchlight swallows her.")
                print("\nYou're alone in the entrance.")
                print("The iron maidens watch.")
                print("The barrel sits.")
                print("The dark ahead has two problems in it now.")
                player.flags['companion_mira'] = False
                player.flags['mira_split'] = True

        else:
          print("\nYou don't move.")
          print("The torchlight swallows her.")
          if player.flags.get('companion_duo'):
            print("\nCaleb says nothing.")
            print("There's nothing worth saying to it.")
            print("\nJust the two of you, the entrance,\n"
                  "and the dark she ran into.")
          else:
            print("\nJust you and the entrance and the dark she ran into.")
          player.flags['companion_mira'] = False
          player.flags['mira_split'] = True

      if player.flags.get('dara_dungeon'):
        print("\nDara leads you forward.")
        print("Past the entrance. Down the corridor.")
        print("\nThe first cell is empty.")
        print("The second has someone in it.")
        print("You don't look too long.")
        print("\nThe third —")
        print("\nCaleb.")
        print("\nHe's in the chair. Wrists bound behind him.")
        print("He sees you before he sees her.")
        print("Something crosses his face — recognition, calculation,\n"
              "then nothing.")
        print("He locks it down fast.")
        print("Not fast enough.")
        print("\n'Pathwalker,' he says.")
        print("Flat. Like he's reading it off a wall.")
        print("'Didn't take you for an Enforcer's errand.'")
        print("\nDara steps past you into the cell.")
        print("She doesn't hurry.")
        print("She takes his hand — almost gently —")
        print("and bends two fingers back.")
        print("\nCaleb makes a sound he clearly didn't intend to make.")
        print("\nShe tilts her head.")
        print("Watches his face with the focused attention of someone\n"
              "who finds the information there genuinely interesting.")
        print("Her tongue moves slowly across her lower lip.")
        print("\n'Mm,' she says.")
        print("Quiet. Almost private.")
        print("'I like it when they hurt.'")
        print("\nShe glances back at you over her shoulder.")
        print("The same look she gave you in the office.")
        print("Except now there's something openly hungry in it.")
        print("You're not entirely sure what she's hungry for.")
        print("Pain isn't the whole of it. Maybe not even the main\n"
              "course.")
        print("\nShe releases his hand.")
        print("Caleb breathes. Doesn't give her the satisfaction of\n"
              "holding it.")
        print("\n'They didn't pay their tithe,' she says to you, not\n"
              "looking away from him.")
        print("'Whether they had the means to is a separate question.\n"
              "One nobody asked.'")
        print("She steps back. Makes room. Like she's offering you\n"
              "something.")
        print("'I'll let you two get reacquainted.'")
        print("\nShe leans in the doorframe.")
        print("Watching. Waiting.")
        print("Like this is exactly how she planned to spend her\n"
              "evening.")
        print("\nThe wall beside you catches your eye.")
        print("Steel pegs. Evenly spaced.")
        print("Each one holding something.")
        print("\nA hammer.")
        print("Garden shears.")
        print("A saw.")
        print("\nThey're clean.")
        print("That's somehow worse than if they weren't.")

        print("\n[1] The hammer.")
        print("[2] The shears.")
        print("[3] The saw.")
        print("[4] Your fist.")
        print("[5] Step back. You're done here.")

        torture_choice = input("\n> ").strip()

        if torture_choice == "1":
          print("\nYou take the hammer off the peg.")
          print("It's heavier than it looks.")
          print("\nCaleb watches you cross the room.")
          print("He doesn't close his eyes.")
          print("\nYou bring it down on the table beside his hand.")
          print("Not his hand. Beside it.")
          print("The sound fills the cell completely.")
          print("\nCaleb exhales.")
          print("Slowly.")
          print("Like he's measuring what he has left.")
          print("\n'She mentioned the desert,' he says.")
          print("Flat. Like it costs him nothing.")
          print("'That's all I have.'")
          print("\nDara nods from the doorframe.")
          print("'See,' she says.")
          print("'Efficient.'")
          player.corruption += 1

        elif torture_choice == "2":
          print("\nYou take the shears off the peg.")
          print("They open and close with a sound like\n"
                "a question being asked.")
          print("\nCaleb looks at them.")
          print("Then at you.")
          print("Something behind his eyes does a calculation\n"
                "he doesn't like the answer to.")
          print("\nYou don't say anything.")
          print("You don't have to.")
          print("\nThe shears find what they're looking for.")
          print("Blood follows immediately.")
          print("More than you expected.")
          print("\nCaleb makes a sound that doesn't have a name.")
          print("\nFrom the doorframe —")
          print("'There it is,' Dara says.")
          print("Quiet. Almost warm.")
          print("'Sometimes you just have to know what to pop\n"
                "off the list to get to what matters.'")
          print("\nCaleb is breathing hard.")
          print("'Ruins,' he gets out.")
          print("'She said something about ruins.\n"
                "Leading into a desert.'")
          print("'That's everything. That's all of it.'")
          print("\nDara smiles.")
          print("First real one you've seen from her.")
          player.corruption += 2
          player.flags['dara_smile'] = True

        elif torture_choice == "3":
          print("\nYou take the saw off the peg.")
          print("You don't move toward him.")
          print("You just hold it.")
          print("Let him look at it.")
          print("\nCaleb looks.")
          print("\nThe silence that follows is a different kind\n"
                "of silence than what came before.")
          print("\nHe talks before you take a single step.")
          print("\n'Ruins,' he says.")
          print("'East of here. She said the ruins lead somewhere.\n"
                "Into a desert. Said there was something there\n"
                "worth finding.'")
          print("'That's it. That's everything.'")
          print("\nYou put the saw back on the peg.")
          print("\nDara raises an eyebrow from the doorframe.")
          print("'Sometimes,' she says,")
          print("'the idea is enough.'")
          player.corruption += 1

        elif torture_choice == "4":
          print("\nYou put nothing in your hand.")
          print("You cross the room.")
          print("\nCaleb sees it coming.")
          print("Doesn't move.")
          print("\nThe impact is immediate and personal in a way\n"
                "the tools aren't.")
          print("\nHe spits.")
          print("Takes a breath.")
          print("Looks at you with something that isn't quite\n"
                "respect but is adjacent to it.")
          print("\n'East,' he says.")
          print("'Ruins. Then desert.'")
          print("'She didn't say more than that.'")
          print("\nDara watches from the doorframe.")
          print("Says nothing.")
          print("Which from her feels like approval.")
          player.corruption += 1

        elif torture_choice == "5":
          print("\nYou step back.")
          print("Put distance between yourself and the chair.")
          print("\nDara goes very still in the doorframe.")
          print("\n'Interesting choice,' she says.")
          print("The warmth is gone from her voice.")
          print("Not anger. Something colder than anger.")
          print("\nShe looks past you.")
          print("Down the corridor.")
          print("A look that means something you don't understand yet.")
          print("\nThen a sound.")
          print("From the dark at the end of the hall.")
          print("Low. Building.")
          print("Something between a breath and a warning.")
          print("\nThe shape that fills the doorframe is enormous.")
          print("Black fur through shredded clothes.")
          print("Three spider legs. One human.")
          print("A crab arm on the wrong side.")
          print("A mouth that starts at the cheekbone and\n"
                "twists all the way to the ear.")
          print("Three arachnid eyes where one used to be.")
          print("All of them open.")
          print("All of them on you.")
          print("\nSaliva hits the floor in thick ropes.")
          print("Blood-tinged. Spreading.")
          print("\nDara doesn't move.")
          print("Doesn't offer you anything.")
          print("Doesn't say a word.")
          print("\nYou have no reason it would stop.")
          print("You gave it none.")
          player.flags['dara_disappointed'] = True
          player.flags['consequential_combat'] = True

          consequential = Consequential()
          simple_combat(player, consequential)
          if player.is_alive():
            player.gain_exp(consequential.exp_value)
            print("\nThe thing that shouldn't exist stops existing.")
            print("It takes a long time to fall.")
            print("\nDara pushes off the doorframe.")
            print("Looks at what's left of it.")
            print("Then at you.")
            print("\n'Waste,' she says.")
            print("You're not sure which of you she means.")



        if not torture_choice == "5":
          print("\nDara's hand moves to her coat pocket.")
          print("She produces something small.")
          print("Barely visible in the torchlight.")
          print("\nA book the size of a keychain.")
          print("A tiny sword thrust up from its spine.")
          print("\nShe holds it out to you.")
          print("\n'You'll need this.'")
          print("\nSomething moves in the shadow at the end\n"
                "of the corridor.")
          print("Large. Wrong.")
          print("The sound of it breathing reaches you\n"
                "before anything else does.")
          print("\n'Quickly,' she says.")
          print("Same tone she'd use to tell you the time.")
          print("\nYou take it.")
          print("The sword pricks your finger before you've\n"
                "fully decided to let it.")
          print("The book pulls warm.")
          print("Tunes itself to something in you that didn't\n"
                "know it was there.")
          print("\nThe Consequential fills the doorframe.")
          print("\nIt's enormous up close.")
          print("The saliva that drops from the twisted mouth\n"
                "hits the floor in thick ropes.")
          print("Blood-tinged. Spreading dark.")
          print("It doesn't move with purpose.")
          print("It moves with appetite.")
          print("\nThen it stops.")
          print("\nReads you.")
          print("\nSteps back one pace. Just one.")
          print("Enough.")
          print("\nDara doesn't look at it.")
          print("She looks at Caleb.")
          print("\n'Now,' she says.")
          print("'Time for you to get reacquainted as well.'")
          print("\nShe gestures toward the Consequential.")
          print("Toward Caleb.")
          print("The same casual movement she might use to\n"
                "introduce two people at a gathering.")
          print("\nCaleb sees it.")
          print("Sees the half of the face that's still a face.")
          print("\nSomething in him understands before his\n"
                "mind catches up.")
          print("\n'No.'")
          print("\nQuiet first.")
          print("Then —")
          print("\n'Nooo — no — no —'")
          print("\nDara pulls the cell door closed.")
          print("\nThe sound of it latching is very small against\n"
                "what's coming from inside.")
          print("\nShe's already walking.")
          print("Back toward the corridor.")
          print("Back toward deeper dark.")
          print("\n'We're done here,' she says.")
          print("\nShe doesn't look back.")
          print("\n'And so is he.'")
          player.flags['binding_tome'] = True
          player.flags['mira_consequential_revealed'] = True

        if not torture_choice == "5":
          print("\n\nDara moves away from the doorframe.")
          print("Into the corridor.")
          print("Not an invitation. Just movement.")
          print("You follow because the alternative is\n"
                "staying in the cell with Caleb.")
          print("\n'This place has a name,' she says.")
          print("Not looking at you.")
          print("'Most don't know it.\n"
                "The organization does.\n"
                "Some of the older prisoners figure it out\n"
                "eventually.'")
          print("\nShe stops.")
          print("Looks at a wall that has nothing on it.")
          print("\n'The Never Was.'")
          print("Flat. Like she's reading it off a document.")
          print("'That's what they call it.\n"
                "What we call it.'")
          print("\nA pause.")
          print("'The Twilight Ledger has been here longer\n"
                "than Vardeth has.'")
          print("'Longer than most things.'")
          print("'They didn't build this place.\n"
                "But they learned to use it.'")
          print("\nShe starts walking again.")
          print("'There's a prisoner further in,' she says.")
          print("'She had information we needed.\n"
                "She chose not to give it.'")
          print("'Repeatedly.'")
          print("\nThe way she says repeatedly.")
          print("Like it's an administrative note.")
          print("Like it explains everything that followed.")
          print("\n'She's at the end of the corridor.'")
          print("'Whatever's left of her.'")

        print("\n\nThe door at the end of the corridor is different\n"
              "from the others.")
        print("Heavier.")
        print("The lock on it newer than everything else down here.")
        print("Someone wanted to ensure that whoever was inside\n"
              "stayed inside.")
        print("No chances would be taken with this prisoner.")
        print("\nDara stops beside it.")
        print("Doesn't knock.")
        print("Just looks at you.")
        print("Then she opens it.")

        print("\n\nThe smell hits before the light adjusts.")
        print("\nSera is in the chair.")
        print("She's been there long enough that whatever bracing\n"
              "she started with has simply become the shape of her now.")
        print("\nBlood long since dried trails down from her lips\n"
              "in dark lines.")
        print("Bruised eyelids hover above emerald green eyes\n"
              "that still have a faint glimmer of life to them.")
        print("Her tattered clothing is coated in a colorful\n"
              "mismatch that can only be described as vomit.")
        print("\nShe doesn't look up when the door opens.")
        print("\nShe looks up when she hears your footsteps.")
        print("Not Dara's. Yours.")
        print("\nHer eyes find you before they find Dara.")
        print("Just for a second.")
        print("Something moves in them —")
        print("not hope exactly.")
        print("The memory of what hope felt like.")
        print("\nThen she sees Dara and it goes out.")
        print("\n'Again,' she says.")
        print("Barely voice. More air than sound.")
        print("\nDara says nothing.")
        print("Steps to the side.")
        print("Makes room.")
        print("For you.")

        print("\n[1] 'We have your sister. Tell us what we want\n"
              "    or she suffers.'")
        print("[2] 'You're already on your last leg. Why not make\n"
              "    it easy — have a peaceful one instead of full\n"
              "    of agony until the last bittersweet moment.'")

        sera_choice = input("\n> ").strip()

        if sera_choice == "1":
          print("\nSomething happens to Sera's face.")
          print("Not breaking.")
          print("Something quieter than breaking.")
          print("Something that was already broken\n"
                "finding a new way to fracture.")
          print("\n'You're lying,' she says.")
          print("But her voice has an uncertainty that betrays\n"
                "the accuracy of her prior words.")
          print("\n'Maybe,' you say.")
          print("'Answer — and you'll find out.'")
          print("'That shows dedication. Shows promise.'")
          print("\nThe silence that follows is its own kind of answer.")
          print("\nShe closes her eyes.")
          print("\n'There are rumors,' she starts.")
          print("Each word costs something.")
          print("'Eastern reaches. Past the ruins.\n"
                "Into the desert.'")
          print("A breath.")
          print("'Something old. Something that doesn't\n"
                "belong there.'")
          print("Another breath. Longer.")
          print("'The artifacts. All five.'")
          print("'That's how you find it.\n"
                "That's how you stop them.'")
          print("Her eyes open. Find yours.")
          print("'The Ledger. The real one.\n"
                "Not their imitation.'")
          print("The faintest thing — almost a laugh.")
          print("'It's the only way to become what you're\n"
                "supposed to be.'")
          print("'A wizard. In absolute certainty.'")
          print("\nShe stops.")
          print("The effort of that many words has cost her\n"
                "the last of something she can't get back.")
          print("\n'East,' she says again.")
          print("Quieter.")
          print("'Start east.'")

          print("\nDara lifts her hand.")
          print("A slow turning gesture.")
          print("Her palm glows in an outline of red.")
          print("\nSera's head snaps left.")
          print("Then right.")
          print("A loud crack issues from somewhere it shouldn't.")
          print("\nHer body sags forward.")
          print("Blood drips from her lips onto the floor.")

          print("\n\nDara doesn't look at what's in the chair.")
          print("She looks at you.")
          print("\nSomething in her face you haven't seen before.")
          print("Not warmth exactly.")
          print("Closer to recognition.")
          print("Like she's seeing something she wasn't sure\n"
                "was there.")
          print("\n'We could take over,' she says.")
          print("As she locks eyes with you.")
          print("She slowly closes the distance between you\n"
                "in a few steps.")
          print("'Together,' she adds.")
          print("As she trails a finger down the side of\n"
                "your cheek.")
          print("\nThe kiss isn't long and it doesn't need to be.")
          print("But it has intent that isn't lost on you.")
          print("\nShe steps back.")
          print("\n'That's the first of many rewards,' she says.")
          print("'If you play your cards right.'")
          print("\nShe turns.")
          print("Walks toward the door.")
          print("Doesn't look back.")
          player.flags['dara_kiss'] = True

        elif sera_choice == "2":
          print("\nSera looks at you for a long moment.")
          print("She's doing a calculation with less than\n"
                "she had an hour ago.")
          print("\n'Peaceful,' she repeats.")
          print("Testing the word for structural integrity.")
          print("\n'You know what you have,' you say.")
          print("You don't move toward her.")
          print("You don't need to.")
          print("'You know what happens if you don't give it.'")
          print("'It doesn't have to go that way.'")
          print("\nShe looks at what's left of her hands.")
          print("Then back at you.")
          print("\n'East,' she says.")
          print("Measured. Like she's conserving what she has\n"
                "left and spending it carefully.")
          print("'Past the ruins. Into the desert.'")
          print("A breath.")
          print("'Something old out there.\n"
                "Something that doesn't belong.'")
          print("Another breath.")
          print("'Five artifacts. All five together.'")
          print("'That's how you find the Ledger.\n"
                "The real one.'")
          print("Her eyes find yours and hold them.")
          print("'Stop the Twilight Ledger.'")
          print("'Become what you were always supposed to be.'")
          print("'A wizard. In absolute certainty.'")
          print("\nAlmost nothing left now.")
          print("\n'East,' she says one more time.")

          print("\nDara lifts her hand.")
          print("A slow turning gesture.")
          print("Her palm glows in an outline of red.")
          print("\nSera's head snaps left.")
          print("Then right.")
          print("The crack is loud and final.")
          print("\nHer body sags forward.")
          print("Blood drips from her lips onto the floor.")

          print("\n\nDara doesn't look at what's in the chair.")
          print("She looks at you.")
          print("A slow nod.")
          print("The kind that means something coming from her.")
          print("\n'We could take over,' she says.")
          print("As she locks eyes with you.")
          print("She slowly closes the distance in a few steps.")
          print("'Together,' she adds.")
          print("As she trails a finger down the side of\n"
                "your cheek.")
          print("\nThe kiss is measured. Deliberate.")
          print("The way everything she does is deliberate.")
          print("It doesn't need to be long to be what it is.")
          print("\nShe steps back.")
          print("Studies you for a moment like she's filing\n"
                "something away.")
          print("\n'First of many rewards,' she says.")
          print("'If you play your cards right.'")
          print("\nShe walks toward the door.")
          print("Doesn't look at what's in the chair.")
          print("Doesn't look back.")
          player.flags['dara_kiss'] = True

        player.flags['sera_dead'] = True
        player.flags['artifact_rumor_east'] = True

      else:
        if player.flags.get('mira_held'):
          print("\nMira stops.")
          print("All that forward momentum — gone.")
          print("She just stands there.")
          print("Looking at you.")
          print("Not with anything specific.")
          print("Just — looking.")
          print("Like you're the first thing that's made sense")
          print("since she heard that scream.")

          print("\n[1] Let her stay in it.")
          print("[2] Step aside gently.")

          mira_comfort_choice = input("\n> ").strip()

          if mira_comfort_choice == "1":
            print("\nYour arm finds her shoulders.")
            print("She exhales.")
            print("Long. Slow.")
            print("Like she's been holding it since the scream.")
            print("\nThere's nothing to say that the moment")
            print("isn't already saying.")
            player.flags['mira_romance_comfort'] = True

          else:
            print("\nYou move.")
            print("Gently. Barely. Just enough.")
            print("\nShe straightens.")
            print("Doesn't look at you.")
            print("'Right,' she says.")
            print("Voice completely flat.")
            print("'We should go.'")
            player.flags['mira_romance_rejected'] = True

        print("\n'Keep your wits about you,' you say.")
        print("'We don't know what's lurking down here.'")
        if player.flags.get('companion_mira') and player.flags.get('companion_duo'):
          print("\nMira nods. Once.")
          print("Whatever was driving her forward pulls back")
          print("just enough to be careful.")
          print("\nCaleb draws level with you.")
          print("'Wits,' he says. 'Right.'")
          print("'I'd settle for a way out that isn't behind us.'")
        elif player.flags.get('companion_mira'):
          print("\nMira nods. Once.")
          print("Whatever was driving her forward pulls back")
          print("just enough to be careful.")
        elif player.flags.get('companion_duo'):
          print("\nCaleb checks the corner ahead before you reach it.")
          print("Old habit. Good one.")
        else:
          print("\nYou say it to the dark.")
          print("The dark doesn't argue.")
        print("\nYou move.")
        print("\nThe corridor stretches.")
        print("Every few feet a torch.")
        print("Every few feet a door.")
        print("Most of them shut.")
        print("Some with sounds behind them you don't")
        print("stop to identify.")

        if player.flags.get('companion_mira') and not player.flags.get('companion_duo'):
          print("\nThen — on the right.")
          print("A door with a face behind the bars.")
          print("\nCaleb.")
          print("\nYou see him before he sees you.")
          print("Wrists bound. On the floor.")
          print("Something happened in here since whoever")
          print("put him here left.")
          print("You don't know what.")
          print("His face tells you it wasn't nothing.")
          print("\nHe looks up.")
          print("Sees you.")
          print("Then sees Mira.")
          print("\nWhat crosses his face isn't relief.")
          print("It's something that has no clean name.")
          print("Recognition and grief arriving at the same time.")
          print("\nHe doesn't say anything.")
          print("What comes out isn't words.")
          print("It's a roar.")
          print("Low. Ragged.")
          print("The sound of someone who has been holding")
          print("something back for too long.")
          print("The kind of sound that travels.")
          print("\nMira goes still beside you.")
          print("She doesn't speak.")
          print("But her eyes —")
          print("her eyes say everything her mouth won't.")
          print("Remorse.")
          print("Deep and settled.")
          print("Like she's been carrying it since before")
          print("she knew she was carrying it.")

          print("\n[1] Open the door.")
          print("[2] Keep moving.")

          caleb_mira_choice = input("\n> ").strip()

          if caleb_mira_choice == "1":
            print("\nYou reach for the lock.")
            print("It gives.")
            print("\nCaleb doesn't move toward you.")
            print("He moves toward Mira.")
            print("Reaching.")
            print("Saying her name now — actually saying it —")
            print("the way you say something you weren't sure")
            print("you'd get to say again.")
            print("\nThen the sound comes.")
            print("From the corridor behind you.")
            print("Low. Rhythmic. Wrong.")
            print("\nThe Consequential fills the doorframe.")
            print("\nBlack fur through shredded clothes.")
            print("Three spider legs. One human.")
            print("The crab arm on the wrong side.")
            print("The mouth twisting upward to the ear.")
            print("Three arachnid eyes.")
            print("All open.")
            print("All finding the easiest thing in the room first.")
            print("\nCaleb.")
            print("Still reaching for Mira.")
            print("Not looking at what came through the door.")
            print("\nIt moves.")

            print("\n[1] Fight it.")
            print("[2] Flee.")

            fight_choice = input("\n> ").strip()

            if fight_choice == "1":
              print("\nYou move between it and Caleb.")
              print("It doesn't care.")
              print("You are an obstacle. Not a threat.")
              print("Not yet.")
              print("\nCaleb's screams follow you.")
              print("Getting louder.")
              print("Then fading to gurgling.")
              print("Then nothing.")
              print("The nothing is worse.")
              print("\nMira makes a sound beside you.")
              print("You've never heard that sound from a person before.")
              print("\nThe Consequential turns its attention to you.")
              player.flags['caleb_dead'] = True
              player.flags['consequential_combat'] = True

              consequential = Consequential()
              simple_combat(player, consequential)
              if player.is_alive():
                player.gain_exp(consequential.exp_value)
                print("\nIt falls the way buildings fall.")
                print("Slow. Then all at once.")
                print("\nThe cell is quiet.")
                print("What's left in it doesn't need looking at.")
                print("Mira looks anyway.")
                print("Then stops looking.")

            else:
              print("\nYou grab Mira.")
              print("She doesn't resist.")
              print("Something in her has gone somewhere else.")
              print("\nYou move.")
              print("Back into the corridor.")
              print("Fast.")
              print("\nCaleb's screams follow you.")
              print("Getting louder.")
              print("Then fading to gurgling.")
              print("Then nothing.")
              print("The nothing is worse.")
              print("\nThe sound of it behind you.")
              print("Then — nothing.")
              print("It doesn't follow past the doorframe.")
              print("\nYou don't stop to wonder why.")
              player.flags['caleb_dead'] = True
              player.flags['mira_witnessed'] = True

          else:
            print("\nYou don't stop.")
            print("\nMira follows.")
            print("She doesn't look back.")
            print("That costs her something.")
            print("You can see it in the set of her shoulders.")

            import random
            roll = random.randint(1, 100)

            if roll <= 50:
              print("\nCaleb's screams follow you down the corridor.")
              print("Getting louder before they fade.")
              print("Then to gurgling.")
              print("Then nothing.")
              print("The nothing is the worst part.")
              print("\nThen — a different sound answers from ahead.")
              print("Low. Building.")
              print("\nThe Consequential rounds the corner.")
              print("\nBlack fur through shredded clothes.")
              print("Three spider legs. One human.")
              print("The crab arm. The twisted mouth.")
              print("Three arachnid eyes finding you immediately.")

              print("\n[1] Fight it.")
              print("[2] Flee.")

              drawn_choice = input("\n> ").strip()

              if drawn_choice == "1":
                print("\nYou stand your ground.")
                player.flags['consequential_combat'] = True

                consequential = Consequential()
                simple_combat(player, consequential)
                if player.is_alive():
                  player.gain_exp(consequential.exp_value)
                  print("\nIt dies without a sound.")
                  print("That's the strangest part.")
              else:
                print("\nYou run.")
                print("Mira runs.")
                print("It follows for three corridors.")
                print("Then it doesn't.")
                print("\nYou don't know why.")
                print("You don't stop to find out.")
                player.flags['consequential_fled'] = True

            else:
              print("\nHis voice fades behind you.")
              print("The corridor ahead stays quiet.")
              print("\nFor now.")

        if (not player.flags.get('companion_mira')
            and not player.flags.get('companion_duo')
            and (player.flags.get('travelers_ignored')
                 or player.flags.get('skipped_raven_fight')
                 or player.flags.get('travelers_abandoned'))):
          player.flags['consequential_identity'] = 'mira'

          print("\n\nThird cell on the right — fingers around the bars.")
          print("\n'Hey. HEY.'")
          print("\nA man as disheveled in his temperament")
          print("as he is in his looks.")
          print("Blood is streaked through his hair,")
          print("matted to both sides of his face,")
          print("adding a dark hue to his dirty blonde curls.")
          print("\n'It doesn't look like either of us are looking our best")
          print("with how you're dressed — but it could do wonders")
          print("if you could change how my outlook looks.'")
          print("\n'They've already turned my beloved into one of...")
          print("those... things.'")
          print("\nThe last bit of information leaves his mouth")
          print("almost unwillingly.")
          print("As if he can't believe what he's saying.")
          print("Or what he saw.")
          print("\n'Why are you even in here?'")
          print("\nIt's the first thing you've said to him.")
          print("He laughs. There's no humor anywhere near it.")
          print("\n'Ask them. They never read us a charge.")
          print("The ravens dropped us on the slope")
          print("and the Enforcers scooped us up like a catch.'")
          print("\n'But they didn't ask me about ME.")
          print("Not once. Three days of questions")
          print("and every one was about her.'")
          print("\n'Sera. My beloved's sister.'")
          print("\n'We shared tables with her.")
          print("Taverns. Inns. Half a winter of nights")
          print("where the four walls were the only safe thing")
          print("in Vardeth.'")
          print("\n'Someone was counting those nights.")
          print("The ravens didn't catch us by luck —")
          print("the Enforcers were fishing")
          print("for everyone who sat at that table.'")
          print("\n'Where she'd been. Who she wrote to.")
          print("What she knows about things going east.'")
          print("\nHis knuckles go white on the bars.")
          print("\n'I gave them nothing.")
          print("Which is the only reason")
          print("I'm still something they keep.'")
          print("\n'These Enforcers are much craftier than their")
          print("fashion would make one guess.")
          print("It could be a great boon to someone who's lost")
          print("in the dark about their organization.'")
          print("\nHe pauses. And slowly adds:")
          print("\n'And this place.'")

          print("\n[1] Open the cell.")
          print("[2] Information first. Then the door.")
          print("[3] Keep walking.")

          cell_choice = input("\n> ").strip()

          if cell_choice == "3":
            print("\nYou keep walking.")
            print("\nHe doesn't beg. Not at first.")
            print("\nThen, slowly:")
            print("\n'Don't leave me... you can't leave me.")
            print("You mustn't!'")
            print("\nThen his voice rises.")
            print("\n'You CAN'T... don't GO!'")
            print("\nIt rises with every call")
            print("as your footsteps take you away.")
            player.flags['caleb_left_in_cell'] = True

          else:
            if cell_choice == "2":
              print("\nYou don't reach for the lock.")
              print("\n'Information first. Then the door.'")
              print("\nSomething like respect crosses his face.")
              print("It doesn't stay long.")
              print("\n'Fine. Smart. Awful, but smart.'")
              print("\n'The Enforcers aren't the power here.")
              print("They're the muscle. Everything they take,")
              print("every body they drag in — it's tallied,")
              print("reported. Sent up.'")
              print("\n'I've heard the guards say a name")
              print("when they think the cells are asleep.")
              print("The Twilight Ledger.'")
              print("\n'They don't say it like a name.")
              print("They say it like a landlord.'")
              print("\n'And below — past the new lock —")
              print("that's where their real business is.")
              print("Whatever they turned my beloved into,")
              print("it happened down there.'")
              print("\nHe steps back from the bars.")
              print("\n'That's everything I have.'")
              print("\n'Your turn.'")
              player.flags['enforcer_structure_known'] = True

            print("\nThe lock gives.")
            print("\nCaleb shoves the door from the inside —")
            print("hard, eager, nearly putting it through you.")
            print("You step aside as it swings.")
            print("\n'Knew it. Knew today would shape up to be som—'")
            print("\nHis words will never be finished.")
            print("Right at that moment an orange serrated mandible")
            print("strikes forward, pinching off the lower part")
            print("of his jaw in one stroke.")
            print("\nYou trace the strike back with your eyes")
            print("to a thing that makes the rest of the dungeon")
            print("look cozy in comparison.")
            print("\nBlack fur bristles through the open pockets")
            print("of torn clothing.")
            print("It has three eyes grouped together on the edge")
            print("of what used to be a human face.")
            print("Stretching down from them to its chin")
            print("is a mouth full of sharpened glistening points,")
            print("so sharp they seem almost like miniature swords.")
            print("Its lower body consists of three arachnid-like legs,")
            print("with a human fourth jutting out —")
            print("as if trying to escape from the reality")
            print("of what it is.")
            print("\nThe door is still swinging.")
            print("That's how fast.")
            print("\nIt stands over what it did,")
            print("still in a way nothing hungry is still.")
            print("\nThen — a long hungry tongue with barbed fingers")
            print("protruding from it trails out from behind")
            print("the mouth. Toward you.")
            print("Closer and closer.")
            print("\nIt moves like it's carrying an injury")
            print("nobody gave it.")
            player.flags['caleb_dead'] = True
            player.flags['consequential_combat'] = True

            consequential = Consequential(weakened=True)
            simple_combat(player, consequential)
            if player.is_alive():
              player.gain_exp(consequential.exp_value)
              print("\nIt dies slowly.")
              print("The human leg is the last part to stop.")
              print("\nThe corridor is quiet.")
              print("Two strangers who won't leave this place,")
              print("and you never learned either of their names")
              print("past the one he gave you.")

        print("\n\nFurther down —")
        print("A cell door hanging open.")
        print("Not unlocked. Broken.")
        print("From the inside.")
        print("\nWhatever was in there isn't anymore.")
        print("\nThe guard on the floor beside it didn't")
        print("make it far after.")
        print("\nSomething small catches the torchlight")
        print("near his hand.")
        print("\nA book.")
        print("Keychain-sized.")
        print("A tiny sword thrust up from its spine.")
        print("\nYou take it.")
        print("It feels like it should mean something.")
        print("You're not wrong about that.")
        print("You're just wrong about what.")
        player.flags['tome_acquired'] = True
        player.flags['tome_understood'] = False

        print("\n\nVoices.")
        print("Around the next bend.")
        print("Two of them. Low.")
        if player.flags.get('companion_mira') and player.flags.get('companion_duo'):
          print("\nThe three of you press flat against the wall.")
        elif player.flags.get('companion_mira'):
          print("\nYou and Mira press against the wall.")
        elif player.flags.get('companion_duo'):
          print("\nCaleb flattens against the wall beside you.")
        else:
          print("\nYou press against the wall.")
        print("\n'...third one this week that's gotten loose...'")
        print("\n'...tomes are the only thing that keeps")
        print("them back...'")
        print("\n'...Commander's going to have our heads")
        print("if another one reaches the upper levels...'")
        print("\n'...not our call anyway.")
        print("The Twilight Ledger wants the prisoner")
        print("kept breathing till she talks...'")
        print("\n'...you don't ask the Twilight questions.")
        print("You lock the doors an' you collect your pay...'")
        print("\nTheir voices start to dwindle away.")
        print("Till they're nothing anymore.")
        print("But memories.")
        if player.flags.get('companion_mira'):
          print("\nMira looks at you.")
          print("Then at the small book in your hand.")
          print("Neither of you says anything.")
        elif player.flags.get('companion_duo'):
          print("\nCaleb eyes the small book in your hand.")
          print("'Whatever that is,' he says.")
          print("'Don't lose it.'")
        else:
          print("\nYou look at the small book in your hand.")
        print("\nYou already know what you're thinking.")
        print("That this little thing could keep those")
        print("creatures back.")
        print("That you're holding safety in your palm.")
        print("\nYou're half right.")
        print("You just don't know which half yet.")

        _solo_promise_route = (
          player.flags.get('promised_sister_search')
          and not player.flags.get('companion_mira')
          and not player.flags.get('companion_duo')
          and not player.flags.get('dara_dungeon'))
        _duo_route = (player.flags.get('companion_mira')
                      and player.flags.get('companion_duo'))
        if _solo_promise_route:
          solo_promise_dungeon(player)
        elif _duo_route:
          duo_dungeon_route(player)
        else:
          print("\n\nThe corridor splits.")
          print("\nLeft — a ladder bolted to the wall.")
          print("Above it, the sound of wings.")
          print("Dozens of them.")
          print("Maybe more.")
          print("\nRight — the corridor continues.")
          print("Longer. Darker.")
          print("Something at the end of it that isn't")
          print("moving but feels like it should be.")
          print("\nAlong the walls between here and there —")
          print("doors.")
          print("Most of them quiet in the way that means")
          print("there's nothing left to make noise.")
          print("One of them isn't quiet.")
          print("A sound from behind it.")
          print("Soft. Rhythmic.")
          print("Someone sobbing.")
          print("Long past the point where sobbing helps.")

          print("\n[1] Go left — toward the ladder.")
          print("[2] Go right — toward whatever's at the end.")

          split_choice = input("\n> ").strip()

          if split_choice == "1":
            print("\nYou start up the ladder.")
            print("Three rungs. Four.")
            print("\nThen a sound from the corridor below.")
            print("Faint. Human.")
            print("A voice past the point where voices carry hope.")
            print("But a voice.")
            if player.flags.get('companion_mira'):
              print("\nMira's hand locks around the rung beside yours.")
              print("'Someone's alive down there.'")
              print("She's already climbing back down.")
            elif player.flags.get('companion_duo'):
              print("\nCaleb stops below you.")
              print("'Wings keep,' he says.")
              print("'That doesn't.'")
            else:
              print("\nThe wings above will keep.")
              print("Whatever is below won't.")
            print("\nYou climb back down.")
            print("\nThe corridor takes you past the sobbing door.")
            print("You don't stop.")
            print("You can't help whoever that is right now.")
            print("\nThe corridor ends at a door.")
            print("Heavier than the others.")
            print("The lock on it newer than everything else down here.")
            print("Someone wanted to ensure that whoever")
            print("was inside stayed inside.")
            player.flags['rookery_first'] = True
            player.flags['sera_path'] = True

          else:
            print("\nYou go right.")
            print("Mira beside you.")
            print("The sobbing door passes on your left.")
            print("Neither of you stops.")
            print("Whatever is behind it —")
            print("you can't help it right now.")
            print("\nThe corridor ends at a door.")
            print("Heavier than the others.")
            print("The lock on it newer than everything")
            print("else down here.")
            print("Someone wanted to ensure that whoever")
            print("was inside stayed inside.")
            print("No chances would be taken with this prisoner.")
            player.flags['sera_path'] = True

          if player.flags.get('companion_mira'):
            if player.flags.get('sera_path'):
              print("\n\nThe smell hits before the light adjusts.")
              print("\nSera is in the chair.")
              print("She's been there long enough that whatever")
              print("bracing she started with has simply become")
              print("the shape of her now.")
              print("\nBlood long since dried trails down from her lips")
              print("in dark lines.")
              print("Bruised eyelids hover above emerald green eyes")
              print("that still have a faint glimmer of life to them.")
              print("Her tattered clothing is coated in a colorful")
              print("mismatch that can only be described as vomit.")
              print("\nShe doesn't look up when the door opens.")
              print("\nShe looks up when she hears Mira's footsteps.")
              print("\nHer eyes find her sister before anything else.")
              print("\nMira doesn't slow down when she sees her.")
              print("She crosses the room in three steps.")
              print("Drops to her knees.")
              print("Pulls Sera into her arms.")
              print("\nSera makes a sound.")
              print("\nMira pulls back immediately.")
              print("Like she's been burned.")
              print("\n'I didn't mean to hurt you.'")
              print("'I'm sorry.'")
              print("'I'm sorry for everything.'")
              print("Tears are coming faster than the words.")
              print("'That I ever left your side.'")
              print("'None of this would've happened if me")
              print("and Caleb hadn't strayed too far.'")
              print("\nSera lets a gasp of pain escape.")
              print("\nMira's hand moves to her face.")
              print("Carefully.")
              print("Brushing stray blonde hairs that aren't")
              print("matted to her face out of Sera's vision.")
              print("\nSera looks at her.")
              print("Really looks.")
              print("Like she's memorizing something.")
              print("\n'There's nothing you could've done,'")
              print("she says.")
              print("'To stop it.'")
              print("\nA breath. Harder than the last one.")
              print("\n'But please listen.'")
              print("'I don't have much time left in this world.'")
              print("'Or much before someone comes.'")
              print("\nShe finds your eyes too.")
              print("Both of you now.")
              print("\n'Listen closely.'")
              print("'For this time I've got left —'")
              print("A pause that costs her.")
              print("'— can do you some good.'")
              print("'Both of you.'")
              print("'And maybe even help this bleak world'")
              print("'have even but a strand of hope.'")

              print("\n[1] Help unbind her — work at the knots.")
              print("[2] Stay back — keep watch.")

              bind_choice = input("\n> ").strip()

              if bind_choice == "1":
                print("\nYou move to her wrists.")
                print("The knots are tight. Deliberate.")
                print("Someone knew what they were doing")
                print("when they tied them.")
                print("\n'East of here,' Sera says.")
                print("'Past the ruins. Into the desert.'")
                print("'There's something there. Something old.'")
                print("'Something that doesn't belong in a place")
                print("like that.'")
                print("\nA sound from the corridor.")
                print("Distant. Getting less distant.")
                print("\n'An artifact,' she continues.")
                print("Like she doesn't hear it.")
                print("'One of five.'")
                print("'Five together — that's how you find it.'")
                print("'The Ledger. The real one.'")
                print("\nThe knot gives slightly. Not enough.")
                print("\n'They named themselves after it,'")
                print("she says.")
                print("'The Twilight Ledger.'")
                print("'Imitators.'")
                print("'The real thing makes them look like")
                print("children playing at power.'")
                print("\nThe footsteps are closer now.")
                print("\n'Gather the five,' she says.")
                print("'Stop them.'")
                print("'Become what you were always supposed to be.'")
                print("'A wizard. In absolute certainty.'")
                print("\nShe looks at Mira one more time.")
                print("\n'There's something in the aviary above,'")
                print("she says.")
                print("'Mother Raven.'")
                print("'Deal with her before you leave.'")
                print("'Or she'll hound you to no end.'")
                print("\nA breath.")
                print("\n'Go.'")

              else:
                print("\nYou stay at the door.")
                print("Eyes on the corridor.")
                print("\n'East,' Sera says behind you.")
                print("'Past the ruins. Into the desert.'")
                print("'Something old. Something that doesn't belong.'")
                print("'An artifact. One of five.'")
                print("\nSilence from the corridor. For now.")
                print("\n'Five together — that's how you find")
                print("the Ledger.'")
                print("'The real one. Not their imitation.'")
                print("'Gather them. Stop the Twilight Ledger.'")
                print("'Become what you were always supposed to be.'")
                print("'A wizard. In absolute certainty.'")
                print("\nSomething moves at the far end of the corridor.")
                print("You can't see it yet.")
                print("You can hear it.")
                print("\n'The aviary above,' she says.")
                print("'Mother Raven.'")
                print("'Deal with her or she'll follow you out.'")
                print("\n'Go,' she says.")
                print("'Both of you.'")

              print("\n\nIt fills the doorframe the way wrong things")
              print("fill spaces.")
              print("\nBlack fur through shredded clothes.")
              print("Three spider legs. One human.")
              print("The crab arm on the wrong side.")
              print("The mouth twisting up to the ear.")
              print("Three arachnid eyes finding the easiest")
              print("target in the room.")
              print("\nSera.")
              print("\nMira moves. You move.")
              print("Neither of you is fast enough.")
              print("\nIt's not violent exactly.")
              print("It's efficient.")
              print("Like it's done this before.")
              print("Like this is simply what it does.")
              print("\nSera makes a sound that has no name.")
              print("\nThen she doesn't make any sound.")
              print("\nMira is shaking.")
              print("Not crying.")
              print("Something past crying.")
              player.flags['sera_dead'] = True
              player.flags['artifact_rumor_east'] = True

              print("\n\nYou turn toward the entrance.")
              print("Mira beside you.")
              print("\nThree steps from the door —")
              print("\nSomething shoots from the dark.")
              print("Long. Wrong.")
              print("Moving faster than something that size")
              print("should move.")
              print("\nIt finds Sera around the waist.")
              print("\nThe sound it makes when it tightens —")
              print("\nMira grabs Sera's shoulder.")
              print("Then her arm.")
              print("Holding. Pulling.")
              print("\nSera looks at her.")
              print("\n'Go,' she says.")
              print("'I'm done for anyway.'")
              print("'Please.'")
              print("'Just go.'")

              print("\n[1] Listen to her. Let go.")
              print("[2] Fight for her.")

              exit_choice = input("\n> ").strip()

              if exit_choice == "1":
                print("\nMira's hands release.")
                print("Slowly.")
                print("Like each finger has to be convinced separately.")
                print("\nThe tongue pulls back.")
                print("\nSera's eyes find Mira's one last time.")
                print("\nThe body splits.")
                print("The sound it makes travels further")
                print("than it should.")
                print("\nA long shriek issues from her lips.")
                print("\nThe dusty stone floor receives her.")
                print("Almost immediately after — silence.")
                print("\nMira doesn't look away.")
                print("That's the bravest thing you've seen")
                print("anyone do.")
                print("\n'We go,' she says.")
                print("Voice completely flat.")
                print("'Now.'")

              else:
                print("\nYou move between it and Sera.")
                print("\nThe Consequential turns its attention to you.")
                print("Something in it recalibrates.")
                print("Slows. Not afraid.")
                print("Just — accounting for the obstacle.")
                print("\nIt's weaker than the ones in the corridor.")
                print("Whatever transformation made it is incomplete.")
                print("Half of what it should be.")
                print("Still enough.")
                player.flags['consequential_combat'] = True
                player.flags['consequential_weakened'] = True

                consequential = Consequential(weakened=True)
                simple_combat(player, consequential)
                if player.is_alive():
                  player.gain_exp(consequential.exp_value)

                print("\nWhen it's over —")
                print("\nSera is already gone.")
                print("The fight bought her nothing except")
                print("the knowledge that someone tried.")
                print("\nThe body on the floor is very still.")
                print("\nMira looks at it for a long moment.")
                print("\n'She told us to go,' she says quietly.")
                print("'We should've listened.'")
                print("\nShe turns toward the corridor.")
                print("'Come on.'")


          elif not player.flags.get('companion_duo'):
            print("\nThe lock is newer than everything else down here.")
            if player.school == "Pyromancy":
              print("It isn't newer than fire.")
              print("\nYour hands glow a molten red,")
              print("then seem to zap forward.")
              print("You hold your palm against the mechanism")
              print("until the metal remembers it was liquid once.")
              print("\nIt runs. The door forgets its argument.")
            elif player.school == "Chronomancy":
              print("You press your hand flat against it")
              print("and ask it to stop being new.")
              print("\nDecades happen to it.")
              print("Rust blooms like something growing in fast-forward.")
              print("The shackle crumbles off its own pin.")
            else:
              print("A keyring hangs from a nail beside the frame.")
              print("Arrogance. Or shift-change laziness.")
              print("\nEither way — the third key turns.")

            if (player.flags.get('travelers_ignored')
                or player.flags.get('skipped_raven_fight')
                or player.flags.get('travelers_abandoned')):
              print("\nThe room behind it isn't a cell.")
              print("It's an office that lost an argument with a prison.")
              print("\nA desk. Papers. A cot bolted to the wall.")
              print("\nA woman looks at the opening door")
              print("with a downcast composure —")
              print("braced the way people brace")
              print("when every visit has cost them something.")
              print("\nThen:")
              print("\n'Oh — you're not one of them.'")
              print("\nA pause.")
              print("\n'Or are you? The outfit is the same.")
              print("But not the entrance.'")
              print("\nShe is weakened. Withered.")
              print("But not hollowed out —")
              print("not the way this place finishes people.")
              print("The dungeon is full,")
              print("and full dungeons have short attention spans.")
              print("\n'A man... named...'")
              print("\nYou hesitate for a split second,")
              print("recalling the doomed man's name.")
              print("\n'Caleb!'")
              print("\n'He said they must've been keeping tabs.")
              print("That they had a feeling they could get")
              print("out of him what they couldn't out of you.'")
              print("\nShe goes still.")
              print("She doesn't ask the question she wants to ask.")
              print("You watch her decide not to.")
              print("\n'Where is he now?'")
              print("\nIt isn't the question.")
              print("It's the closest safe one.")

              print("\n[1] 'Something got to him. Something wearing torn clothes.'")
              print("[2] 'He didn't make it. That's all I know.'")

              sera_told = input("\n> ").strip()

              if sera_told == "1":
                print("\nShe looks at the wall for a while.")
                print("\nWhen she looks back, something in her")
                print("has been put away where you can't see it.")
                print("\n'The Enforcers keep worse than guards")
                print("down here,' she says.")
                print("\nFlat. Final.")
                player.flags['sera_heard_description'] = True
              else:
                print("\nA quiet nod.")
                print("\n'This place is good at that.'")

              print("\n'Why do they keep you like this?'")
              print("\n'Because I counted what they couldn't.'")
              print("\n'Everything they take goes east.")
              print("Past the ruins. Into the desert.'")
              print("\n'There's something out there. Something old.")
              print("Something that doesn't belong in a place")
              print("like that.'")
              print("\n'An artifact. One of five.")
              print("Five together — that's how you find it.'")
              print("\n'The Ledger. The real one.'")
              print("\n'They named themselves after it.")
              print("The Twilight Ledger. Imitators.")
              print("The real thing makes them look like")
              print("children playing at power.'")
              print("\n'Gather the five. Stop them.")
              print("Become what you were always supposed to be.")
              print("A wizard. In absolute certainty.'")
              player.flags['artifact_rumor_east'] = True
              player.flags['sera_freed'] = True
              player.flags['sera_with_you'] = True

              print("\n'One more thing. The aviary above.")
              print("Mother Raven.")
              print("Deal with her before you leave —")
              print("or she'll hound you to no end.'")

              print("\nShe stands. It costs her something.")
              print("She pays it without comment.")
              print("\n'When I walk out of here, I'm not running.")
              print("They built this place out of people.")
              print("Emptied families into cells.")
              print("I'm going to find what's left of those families.'")
              print("\n'People can be a weapon too.'")

            else:
              print("\nThe room behind it isn't a cell.")
              print("It's an office that lost an argument with a prison.")
              print("\nA desk. Papers. A cot bolted to the wall.")
              print("\nA woman looks at the opening door")
              print("with a downcast composure —")
              print("braced the way people brace")
              print("when every visit has cost them something.")
              print("\nThen:")
              print("\n'Oh — you're not one of them.'")
              print("\nA pause.")
              print("\n'Or are you? The outfit is the same.")
              print("But not the entrance.'")
              print("\nShe is weakened. Withered.")
              print("But not hollowed out —")
              print("not the way this place finishes people.")
              print("\n'Your sister is looking for you.'")
              print("\nStillness.")
              print("\n'Mira.'")
              print("\nShe says the name like a word")
              print("from a language she stopped")
              print("letting herself speak.")
              print("\n'Alive? Is she— '")
              print("She catches it. Rebuilds her voice.")
              print("'Is she alive?'")
              print("\n'Alive. Outside the town.")
              print("Waiting at dusk for word of you.'")
              print("\nShe sits back down.")
              print("It isn't weakness.")
              print("It's the opposite —")
              print("she lets herself have exactly")
              print("three seconds of it.")
              print("\nThen she stands.")
              print("\n'Then listen. What I know is why")
              print("they keep me.")
              print("You're going to carry it out of here")
              print("even if I don't make it past the door.'")
              print("\n'Everything they take goes east.")
              print("Past the ruins. Into the desert.'")
              print("\n'There's something out there. Something old.")
              print("Something that doesn't belong in a place")
              print("like that.'")
              print("\n'An artifact. One of five.")
              print("Five together — that's how you find it.'")
              print("\n'The Ledger. The real one.'")
              print("\n'They named themselves after it.")
              print("The Twilight Ledger. Imitators.")
              print("The real thing makes them look like")
              print("children playing at power.'")
              print("\n'Gather the five. Stop them.")
              print("Become what you were always supposed to be.")
              print("A wizard. In absolute certainty.'")
              print("\n'One more thing. The aviary above.")
              print("Mother Raven.")
              print("Deal with her before you leave —")
              print("or she'll hound you to no end.'")
              player.flags['artifact_rumor_east'] = True
              player.flags['sera_freed'] = True
              player.flags['sera_with_you'] = True
              player.flags['sera_knows_mira_waiting'] = True

          else:
            print("\nThe lock is newer than everything else down here.")
            print("You put a spell through the mechanism.")
            print("The door gives.")
            print("\nInside — a woman rises from a bolted cot.")
            print("Weakened. Withered. Watching you.")
            print("\nShe tells you what she counted for them:")
            print("everything they take goes east,")
            print("and what they hunt out there numbers five.")
            print("Old things. Artifact-old.")
            player.flags['artifact_rumor_east'] = True
            player.flags['sera_freed'] = True
            player.flags['sera_with_you'] = True

          print("\n\nThe corridor offers two endings.")
          print("\nUp — the ladder, and the wings,")
          print("and whatever keeps making more of them.")
          print("\nOr back the way you came.")
          print("Past the cells. Past the iron maidens.")
          print("Past whoever is still posted at the door.")

          print("\n[1] Climb. Deal with the source.")
          print("[2] You've done what you came for. Slip out.")

          aviary_choice = input("\n> ").strip()

          if aviary_choice == "1":
            if player.flags.get('rookery_first'):
              print("\n\nThe ladder waits where you left it.")
            else:
              print("\n\nBack down the corridor — the ladder.")
              print("Bolted to the wall.")
            print("Above — the sound of wings.")
            print("Dozens. Maybe more.")

            if player.flags.get('companion_mira'):
              print("\nMira goes first.")
              print("You follow.")
              print("\nHalfway up —")

              ladder_roll = random.randint(1, 100)

              if ladder_roll <= 50:
                print("\nSomething shoots from below.")
                print("Impossibly long.")
                print("Moving faster than anything that size")
                print("should move.")
                print("\nIt finds Mira's ankle.")
                print("\nShe makes a sound — surprise first,")
                print("then pain —")
                print("as it pulls.")
                print("\nHer hands lose the rung.")
                print("\nWhat's wrapped around her ankle isn't smooth.")
                print("Tiny hands where the barbs should be.")
                print("Each fingertip its own barb.")
                print("Pulling in directions that don't agree")
                print("with each other.")
                print("\n'Go,' she says.")
                print("\nYou reach for her.")
                print("Your fingers find her wrist.")
                print("\nThe tongue pulls harder.")
                print("\n'Go,' she says again.")
                print("Louder. Not a request.")
                print("\nHer wrist slips through your fingers.")
                print("\nThe dark below receives her.")
                print("\nYou keep climbing.")
                print("There's nothing else to do.")
                player.flags['mira_lost'] = True

              else:
                print("\nYou both reach the top.")
                print("Mira pulls herself up beside you.")
                print("\n'What is that,' she says.")
                print("Not a question.")
                player.flags['mira_rookery'] = True

            elif player.flags.get('companion_duo'):
              print("\nCaleb goes last.")
              print("'If something grabs me,' he says.")
              print("'Keep climbing.'")
              print("He isn't joking.")
              print("\nNothing grabs anyone.")
              print("Somehow that's worse.")
            else:
              print("\nYou climb alone.")
              print("The dark below watches you do it.")

            print("\n\nThe aviary is vast.")
            print("More space than the dungeon below")
            print("should be able to contain.")
            print("\nRavens everywhere.")
            print("On every surface.")
            print("Watching.")
            print("\nThey don't move when you enter.")
            print("\nThen — from the center of it.")
            print("\nSomething larger than a raven.")
            print("Much larger.")
            print("\nMother Raven doesn't look like what made")
            print("the others.")
            print("She looks like what the others are trying")
            print("to become.")
            print("Black. Enormous.")
            print("Her wingspan fills the space between walls")
            print("when she opens it.")
            print("Her eyes are wrong —")
            print("too many of them, too aware.")
            print("\nShe opens her beak.")
            print("What comes out isn't a sound birds make.")

            mother_raven = MotherRaven()
            simple_combat(player, mother_raven)

            if player.is_alive():
              player.gain_exp(mother_raven.exp_value)
              print("\n\nThe last spell leaves your hand before")
              print("you've fully decided to throw it.")
              print("\nIt finds her.")
              print("\nThe force of it —")
              print("\nThe wall couldn't contain what happened next.")
              print("She goes through it.")
              print("Stone. Dark. Gone.")
              print("\nThe ravens on every surface go still.")
              print("Then scatter.")
              print("Through gaps you didn't see before.")
              print("Gone.")
              print("\nThe aviary is quiet.")
              print("For the first time since you entered it.")
              print("\nSomething shifts in you.")
              print("Not power exactly.")
              print("Understanding.")
              print("Like something that was almost clear")
              print("has finally resolved.")
              player.flags['mother_raven_defeated'] = True

              print("\nAmong the feathers on the floor —")
              print("one that's different from the others.")
              print("Longer. Darker.")
              print("It doesn't move when the others scatter.")
              print("\nYou take it.")
              print("Raven Talon acquired.")
              player.inventory.add("Raven Talon")

          else:
            print("\nYou move back through the dungeon")
            print("the way water moves through a crack.")
            print("Quiet. Committed.")
            print("\nThe cells watch you pass.")
            print("Whoever is still in them")
            print("has learned not to call out.")
            print("\nThen — a lantern swings around the corner.")
            print("\nOne Enforcer. Alone.")
            print("Doing the rounds nobody thought mattered.")
            print("\nHis eyes go wide.")
            print("His hand goes to his belt.")
            print("Only one of those was the right decision.")

            patrol_one = Enforcer()
            simple_combat(player, patrol_one)
            if player.is_alive():
              player.gain_exp(patrol_one.exp_value)

              print("\nYou drag the body into an open cell.")
              print("The irony isn't lost on you.")
              print("You don't have time to enjoy it.")
              print("\nThe entrance hall is close now.")
              print("Torchlight. Night air pushing in")
              print("through the seams of the door.")
              print("Almost.")
              print("\nA voice from the other side. Muffled.")
              print("\n'Kell? That you?'")
              print("\nIt isn't.")
              print("\nYou answer with the door.")
              print("\nThen the door, then the night stares down")
              print("from above as the chill of the cold evening")
              print("hits your skin.")
              print("You're free of that loathsome place!")
              print("\nNow you're face to face with an Enforcer")
              print("who was smacked by you flinging open the door.")

              patrol_two = Enforcer()
              simple_combat(player, patrol_two)
              if player.is_alive():
                player.gain_exp(patrol_two.exp_value)

                print("\nBehind you lie things unresolved.")
                print("But you neither have the time nor patience")
                print("to confront it.")


      if not player.flags.get('ch1_branch_complete'):
        if player.flags.get('sera_with_you'):
          print("\nShe takes in a big breath of the cold air")
          print("as a giant moon looks downward, casting light —")
          print("illuminating a figure draped in dark black")
          print("and red regalia.")
          print("A partially toothed mouth grins from the shadows")
          print("of the hood it rests under.")
          print("\n'I knew it couldn't be this easy,' Sera murmurs —")
          print("her body sways backwards for a second,")
          print("a side effect from the horrors of however long")
          print("she's been locked up.")
          print("\n'Of course he knows my face.")
          print("He was the one who stuck me in that hellhole.'")

        print("\n\nThe square receives you when you emerge.")
        print("\nHe's already there.")
        print("Older than you expected.")
        print("Built like someone who used to be larger.")
        print("Two Enforcers flank him.")
        print("More in the shadows.")
        print("\nHis eyes find you immediately.")
        print("\n'The dungeon had visitors,' he says.")
        print("Not a question.")
        print("\n'You'll need to come with us.'")

        if not player.flags.get('dara_dungeon'):
          print("\nFrom the alleyway to the left —")
          print("movement.")
          print("\nDara.")
          print("She takes in the Commander.")
          print("Takes in you.")
          print("Does a calculation.")
          print("Fast.")
          print("\nThe Commander sees her.")
          print("Something in his face shifts.")
          print("This wasn't just about you.")
          print("\n'Rennick,' he says.")
          print("Her last name like a door closing.")
          print("'The financial records.'")
          print("'We need to talk about the financial records.'")
          print("\nDara doesn't look at him.")
          print("She looks at you.")
          print("One second.")
          print("That's all.")
          print("\nThen the square isn't quiet anymore.")

          print("\n[1] Fight the Commander.")
          print("[2] Help Dara.")
          print("[3] Slip away while they're occupied.")

          boss_choice = input("\n> ").strip()

          if boss_choice == "1":
            print("\nYou move toward the Commander.")
            print("He turns his full attention to you.")
            print("Dara handles what's left.")
            print("\nWhat follows is attrition.")
            print("He's capable. His flanking Enforcers less so.")
            if not player.flags.get('mother_raven_defeated'):
              print("\nThe ravens arrive before the fight")
              print("is three turns old.")
              print("Every seven turns after that.")
              print("More of them.")
              player.flags['enforcer_combat'] = True
            else:
              print("\nWithout the swarm it's a matter of")
              print("what you came out of that dungeon with.")
              print("It's enough.")
              player.flags['enforcer_combat'] = True

            commander = EnforcerCommander(
              ravens_active=not player.flags.get('mother_raven_defeated')
            )
            simple_combat(player, commander)
            if player.is_alive():
              player.gain_exp(commander.exp_value)

          elif boss_choice == "2":
            print("\nYou move to Dara's side.")
            print("She doesn't acknowledge it.")
            print("But she adjusts.")
            print("Makes room for what you're about to do.")
            print("\nThe Commander divides his attention.")
            print("That's his mistake.")
            player.flags['enforcer_combat'] = True
            player.flags['helped_dara'] = True

            commander = EnforcerCommander(
              ravens_active=not player.flags.get('mother_raven_defeated')
            )
            simple_combat(player, commander)
            if player.is_alive():
              player.gain_exp(commander.exp_value)
              print("\nDara finishes the last flanker")
              print("without looking at it.")

          else:
            print("\nYou don't move toward either of them.")
            print("\nWhile the Commander's attention is on Dara —")
            print("and Dara's attention is on the Commander —")
            print("\nYou move.")
            print("Into the alleyway.")
            print("Away from the square.")
            print("Away from all of it.")
            print("\nThe sounds of the fight follow you")
            print("for half a block.")
            print("Then they don't.")
            player.flags['enforcer_avoided'] = True

        else:
          print("\nDara doesn't break stride.")
          print("'Commander.'")
          print("\n'We've been going through the ledgers,'")
          print("he says.")
          print("'The financial ones.'")
          print("\nSomething happens in Dara's posture.")
          print("So small you'd miss it if you weren't")
          print("standing right beside her.")
          print("A recalculation. Fast.")
          print("\n'Discrepancies,' he says.")
          print("'Consistent ones.'")
          print("'Over a considerable period.'")
          print("\nHe looks at you.")
          print("Takes you in. Files you somewhere.")
          print("\n'Who's this?'")
          print("\n'A valuable asset,' Dara says.")
          print("'Recruited tonight.'")
          print("\n'Convenient,' he says.")
          print("\nThe flanking Enforcers shift their weight.")
          print("The ones in the shadows move closer to the light.")
          print("\n'You'll need to come with us,'")
          print("he says to Dara.")
          print("'Both of you.'")

          print("\n[1] Don't wait. Move first.")
          print("[2] Let Dara make the call.")

          dara_boss_choice = input("\n> ").strip()

          if dara_boss_choice == "1":
            print("\nYou move before he finishes the sentence.")
            print("\nDara notes it.")
            print("Files it.")
            print("Moves to flank.")
            player.flags['enforcer_combat'] = True

          else:
            print("\nDara moves first.")
            print("You follow her lead.")
            player.flags['enforcer_combat'] = True

          commander = EnforcerCommander(ravens_active=True)
          simple_combat(player, commander)
          if player.is_alive():
            player.gain_exp(commander.exp_value)

        if (player.flags.get('sera_with_you')
            and player.flags.get('enforcer_combat')
            and player.is_alive()):
          if player.hp > player.max_hp * 0.25:
            print("\n\nSera steps past you to look at what's left")
            print("of the man who kept her.")
            print("\nShe pulls out his keys.")
            print("\n'I'm going to free everyone from the likes")
            print("of them, and take back this city.'")
            print("\n'Now go — do what I was stopped from doing.")
            print("Free this world from the likes of them")
            print("and anyone else that would wish to chain us all.'")
            player.flags['sera_resistance_lives'] = True
          else:
            print("\n\nYou're standing. It costs you everything")
            print("you had left — and something that wasn't yours.")
            print("\nSera is not standing.")
            player.flags['sera_sacrificed'] = True

        if player.flags.get('enforcer_combat') and player.is_alive():
          print("\n\nThe square is quiet in the way squares get quiet")
          print("after something loud has happened in them.")
          print("\nThe Commander is down.")
          print("His flanking Enforcers scattered into the dark.")

          print("\nSomething catches the torchlight near")
          print("the Commander's coat.")
          print("A seal. Heavy. Enforcer insignia.")
          print("The kind that opens doors.")
          print("Or closes them.")
          print("\nCommander's Seal acquired.")
          player.inventory.add("Commander's Seal")

        if (player.flags.get('enforcer_combat') and player.is_alive()
            and not player.flags.get('dara_dungeon')
            and not (not player.flags.get('companion_mira')
                     and not player.flags.get('companion_duo')
                     and (player.flags.get('travelers_ignored')
                          or player.flags.get('skipped_raven_fight')
                          or player.flags.get('travelers_abandoned')))):
          print("\n\nAcross the square — Dara straightens.")
          print("The last Enforcer near her isn't getting up.")
          print("\nShe looks at you.")
          print("Takes stock of what you did to the Commander.")
          print("Files it somewhere.")
          print("\n'Well,' she says.")
          print("'This complicates my evening.'")

          print("\n[1] Let her walk.")
          print("[2] She's Twilight Ledger. Finish it.")

          dara_confront = input("\n> ").strip()

          if dara_confront == "2":
            print("\nShe reads it in you before you move.")
            print("Something in her face almost approves.")
            print("\n'There it is,' she says.")
            dara = Dara()
            simple_combat(player, dara)
            if player.is_alive():
              player.gain_exp(dara.exp_value)
              player.flags['dara_killed'] = True
              if player.flags.get('helped_dara'):
                player.corruption += 3
          else:
            print("\nYou don't move.")
            print("She holds your eyes a moment longer.")
            print("\n'Smart,' she says.")
            print("Or maybe 'Soft.'")
            print("The distance eats the word.")
            print("\nThen the alley takes her.")
            player.flags['dara_spared'] = True

        if player.flags.get('dara_dungeon'):
          print("\n\nDara is already moving.")
          print("Back toward the alleyway.")
          print("Away from the light.")
          print("\n'The ones who ran will be back,'")
          print("she says.")
          print("Not looking at you.")
          print("'With more.'")
          print("\nShe stops.")
          print("Looks back at you once.")
          print("\n'We shouldn't be here when they return.'")
          print("A grin crosses her face.")
          print("The first one that isn't calculated.")
          print("'Besides.'")
          print("'We have matters to attend to.'")
          player.flags['dara_permanent_companion'] = True

        if player.flags.get('dara_killed'):
          print("\nDara goes down the way capable people go down.")
          print("Surprised.")
          print("Like she was certain this wasn't how")
          print("it would end.")
          print("\nSomething small falls from her coat.")
          print("Lands near her hand.")
          print("\n15 gold.")
          print("That's all she was carrying that was hers.")
          print("\nYou take it.")
          print("She would've.")
          player.gold += 15