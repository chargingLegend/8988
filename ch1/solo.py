from ui import print, input
from combat import simple_combat
from enemy import Enforcer, Consequential, MotherRaven


def paired_combat(player, enemy_a, enemy_b, sera_heals=0):
  """Two enemies at once. Player picks a target each turn.
  Both living enemies strike back each round.
  Returns remaining Sera heals."""
  print("\n=== PAIRED COMBAT BEGINS ===")
  enemies = [enemy_a, enemy_b]

  while player.is_alive() and any(e.is_alive() for e in enemies):
    living = [e for e in enemies if e.is_alive()]

    print(f"\n{player}")
    for i, e in enumerate(living, 1):
      print(f"[{i}] {e}")
    print(f"Spells: {player.spells} | Mana: {player.mana}/{player.max_mana}")

    prompt = "\nSpell name, 'ability', 'flee'"
    if sera_heals > 0:
      prompt += f", or 'sera' ({sera_heals} left)"
    action = input(prompt + ": ").strip().lower()

    if action == 'flee':
      print(f"{player.name} flees.")
      print("The Path teaches cowardice has a price: no exp gained.")
      break

    if action == 'sera' and sera_heals > 0:
      sera_heals -= 1
      heal = player.max_hp // 4
      player.hp = min(player.max_hp, player.hp + heal)
      print("\nSera's hands find the wound before you point to it.")
      print(f"+{heal} HP restored. [{player.hp}/{player.max_hp}]")
    elif action == 'sera':
      print("\nSera has nothing left to give. She keeps them off you.")
    else:
      target = living[0]
      if len(living) > 1:
        pick = input("Target [1/2]: ").strip()
        if pick == "2":
          target = living[1]
      player.cast_mana(action, target)

    for e in [e for e in enemies if e.is_alive()]:
      e.attack(player)

  return sera_heals


def _print_creature_solo(player):
  print("\nThe torchlight gives life to its features.")
  print("\nBlack fur bristling through shredded clothing.")
  print("Legs that belong to something arachnid —")
  print("except one, which is human,")
  print("and looks like it's trying to leave.")
  print("An arm that once was human,")
  print("and now appears to be a crab's pincer.")
  print("\nAnd a face —")
  print("what's left of one —")
  print("three eyes crowded together on its edge,")
  print("with a mouth full of sharp, glistening things")
  print("inside, stretched up toward its ears")
  print("on the left side.")


def _solo_promise_cell_onward(player, dropped_in=True):
  if dropped_in:
    print("\n\n'Ahh!' she cries, squinting her eyes shut")
    print("as if she's about to be hit.")
    print("\nYou console her, but quickly —")
    print("'No, no — I'm not here to hurt you. I'm here")
    print("to rescue you. Your sister sent me. Your")
    print("torturers are but a few seconds behind me.")
    print("We must make haste,' you say as you hurriedly")
    print("untie her.")
  else:
    print("\n\nThe corridor ends at a door.")
    print("Heavier than the others.")
    print("You put a spell through the mechanism.")
    print("\nInside — a woman flinches from the opening door.")
    print("'I'm here to rescue you,' you say quickly.")
    print("'Your sister sent me. We must make haste.'")
    print("You hurriedly untie her.")
  print("\nShe gushes out information as if she won't")
  print("make it — as if something at least needs")
  print("to outlast her.")
  print("\nThe artifacts. East. Near a colosseum.")
  player.flags['artifact_rumor_east'] = True

  if dropped_in:
    print("\nBut before you can get to the door —")
    print("\nThe monstrous thing drops down.")
    print("\nIt leaps forward.")

    print("\n[1] Jump out of the way.")
    print("[2] Stand your ground.")
    c5 = input("\n> ").strip()

    if c5 == "2":
      print("\nYou don't move.")
      print("\nIt lunges forward — and simultaneously")
      print("its tongue shoots out, wrapping itself")
      print("around your neck, lifting you up and off")
      print("your feet, pulling you toward it.")
      print("\nThe crab-like pincer on one of its arms")
      print("opens and closes.")
      print("\nOnce.")
      print("\nYou feel your innards spill forth")
      print("as your eyes close.")
      print("\n                    [ YOU DIED ]")
      player.hp = 0
      return

    print("\nIt takes the locked door out — breaking it off")
    print("its hinges, catapulting the door and creature")
    print("alike into the guards beyond.")
    print("\nBefore any of them can get their bearings,")
    print("you and Sera leap over the mess of swords")
    print("and limbs — both those that were human,")
    print("and those that were human once.")
    print("\nThe Enforcers, thinking it's the enemy,")
    print("lash their swords outward. A few strike")
    print("the monstrous thing. A few stab.")
    print("\nYou don't look back. You don't need to.")
    print("Screams — and the sound of what you picture")
    print("to be blood — jettison in all directions.")
    print("\nYou feel a spray of something hit your back.")
    print("\nBut you keep heading toward a door")
    print("with a ladder in the middle of it.")

  print("\nShe explains as you're making your way toward")
  print("the room — vaguely, because she's no expert —")
  print("that they're all tied to the Ledger.")
  print("\n'Ledger?' you query as you reach the door.")
  print("'What books? I thought I was supposed to find")
  print("an artifact. Why is any of it even important?'")
  print("\nShe stops you in your tracks, putting her hands")
  print("on your shoulders, and explains quickly,")
  print("her emerald eyes locking with yours:")
  print("\n'The Ledger is the voice that speaks to all")
  print("who enter this realm. Some more than others.")
  print("I don't know enough to make it make sense —")
  print("but the Enforcers wish to obtain all the")
  print("artifacts that are supposedly required")
  print("to summon it forth, in hopes of taking its")
  print("power, ruling this world, and turning it")
  print("more bleak than it already is.'")

  if dropped_in:
    print("\n'Quick! We must go!' she says, her head turning")
    print("toward the commotion behind you.")
    print("\nThe monstrous thing lies dead on the ground.")
    print("\n'The Consequential is dead — but they're getting")
    print("their heads on straight to take ours off,'")
    print("she says, as the Enforcers stand, pushing the")
    print("carcass and the door that held them down aside.")
    print("\nA few of them are already making their way")
    print("toward you.")

    print("\n[1] Stand and fight.")
    print("[2] Head into the room with the ladder —")
    print("    lock the door behind you.")
    c6 = input("\n> ").strip()

    if c6 == "1":
      print("\nThey come at you in pairs —")
      print("Sera pulling the attention of the ones")
      print("that don't.")
      heals = paired_combat(player, Enforcer(), Enforcer(), sera_heals=2)
      if player.is_alive():
        print("\nThe second pair steps over the first.")
        paired_combat(player, Enforcer(), Enforcer(), sera_heals=heals)
      if not player.is_alive():
        return
      print("\nYou both make for the ladder room.")
    else:
      print("\nYou pull Sera through, slam the door,")
      print("and drop the bar into its bracket.")
      print("The first fists land on the other side")
      print("a breath later.")

  print("\n\nThe ladder takes you both up.")
  print("\nThe aviary is vast.")
  print("More space than the dungeon below")
  print("should be able to contain.")
  print("\nRavens on every surface. Watching.")
  print("\nAnd from the center of it —")
  print("something much larger than a raven.")
  print("\nShe opens her beak.")
  print("What comes out isn't a sound birds make.")

  mother_raven = MotherRaven()
  simple_combat(player, mother_raven)
  if not player.is_alive():
    return
  player.gain_exp(mother_raven.exp_value)
  player.flags['mother_raven_defeated'] = True

  print("\n\nThe last spell leaves your hand with more force")
  print("than you thought yourself capable of.")
  print("\nIt catches the Mother Raven full center")
  print("in her chest.")
  print("\nThe walls couldn't stop the weight of her")
  print("crashing against them as they explode outwards,")
  print("splintering into thousands of tinier pieces")
  print("of wood and cascading downwards.")
  print("\nStones, beams, and Mother Raven fall downwards.")
  print("\nIn the square below, a waiting formation")
  print("of an Enforcer patrol shouts —")
  print("as Mother Raven and several tons of debris")
  print("silence them.")

  print("\nAmong the feathers on the floor —")
  print("one that's different from the others.")
  print("Longer. Darker.")
  print("It doesn't move when the others scatter.")
  print("\nYou take it.")
  print("Raven Talon acquired.")
  player.inventory.add("Raven Talon")

  print("\nSera steps to the broken edge beside you.")
  print("\n'Go — now, quickly, before they get their")
  print("wits back. I'll handle this. Tell my sister")
  print("I love her — and make sure you get those")
  print("artifacts before they can.'")
  player.flags['sera_freed'] = True
  player.flags['sera_stays_behind'] = True
  player.flags['sera_message_for_mira'] = True
  print("\nYou nod at each other.")
  print("\nYou look down. Piled against the facility wall,")
  print("right beneath the edge of it all — hay.")
  print("\nAs you're leaping over the side, you hear")
  print("that same commanding feminine voice yelling —")
  print("\n'STOP them!!'")
  print("\n            [ CHAPTER 1 ENDS — THE PROMISE PATH ]")


def solo_promise_dungeon(player):
  player.flags['ch1_branch_complete'] = True

  print("\nThen you hear it — if ever so faintly,")
  print("a gentle and meek-sounding crying")
  print("coming from the intersection.")
  print("\nIn a moment of heroism, you walk faster")
  print("toward it.")
  print("\nAs you near the intersection —")
  print("something lopes out of the darkness,")
  print("stopping in the middle of the merging paths.")
  print("\nYou stop cold in your tracks.")
  print("Beads of sweat form and rush down your face")
  print("almost instantly.")
  print("\nIt lifts its head up —")
  print("as if smelling... searching... hunting!")
  _print_creature_solo(player)
  print("\nYou notice a door slightly ajar,")
  print("right across from where you're standing.")
  print("\nYou're barely five feet away from the creature.")

  print("\n[1] Stay put — hope it turns around.")
  print("[2] Slip into the room.")
  c = input("\n> ").strip()

  if c == "1":
    print("\nIt doesn't turn around.")
    print("It leaps.")
    monster = Consequential()
    monster.name = "The Monstrous Thing"
    simple_combat(player, monster)
    if not player.is_alive():
      return
    player.gain_exp(monster.exp_value)
    print("\nIt dies the way it moved.")
    print("Wrong. In stages.")
    print("The human leg is the last part to stop.")
    print("\nThe crying is still there.")
    print("Down the right-hand corridor.")
    print("You follow it.")
    _solo_promise_cell_onward(player, dropped_in=False)
    return

  print("\nYou slip inside and go to close the door —")
  print("but it won't lock from the inside!")
  print("\nYou spot a chair.")
  print("\n[1] Brace the door with the chair.")
  print("[2] Brace it yourself.")
  c2 = input("\n> ").strip()

  if c2 == "2":
    print("\nYou set your weight against the door.")
    print("It hits like the whole dungeon swung it.")
    print("The door — and you — give way.")
    monster = Consequential()
    monster.name = "The Monstrous Thing"
    monster.atk = max(1, int(monster.atk * 0.75))
    simple_combat(player, monster)
    if not player.is_alive():
      return
    player.gain_exp(monster.exp_value)
    print("\nIt dies the way it moved.")
    print("Wrong. In stages.")
    print("The human leg is the last part to stop.")
    print("\nThe crying is still there.")
    print("You follow it.")
    _solo_promise_cell_onward(player, dropped_in=False)
    return

  print("\nYou jam the chair beneath the handle.")
  print("The first hit lands a heartbeat later.")
  print("The chair holds the creature back.")
  print("For how long — that isn't very certain.")
  print("\nThen you notice it: a set of fold-down stairs,")
  print("half-collapsed into the ceiling.")
  print("\nYou pull them down, climb, and close them")
  print("behind you — moving with haste.")

  print("\nYou move but a few inches forward after closing")
  print("the stairs upwards, in hopes that the creature")
  print("won't follow.")
  print("\nA noise makes you pause.")
  print("\nIt's coming from another hatch — a feminine voice")
  print("is yelling, one that sounds like it's used to")
  print("not being disobeyed.")
  print("\n'I want this intruder found! And now!")
  print("None have ever escaped this dungeon,")
  print("and I won't have this time become the first!'")
  print("\n'The Inquisitors will be swarming here if the")
  print("higher-ups become aware of this! The entire")
  print("program we have here will be in jeopardy!'")

  print("\nA hatch to your left. Her voice beneath it.")
  print("\n[1] Press your head down against it. Listen.")
  print("[2] Keep crawling. You've heard enough.")
  c3 = input("\n> ").strip()

  if c3 == "1":
    print("\n'The Ledger can't fall into their hands — we must")
    print("obtain it first. That woman we've been trying to")
    print("break holds the whereabouts of some of the")
    print("artifacts. Our sources have confirmed it! We need")
    print("to break her, to let this knowledge spill forth.")
    print("But if they show up, that'll all be in vain.'")
    print("\nThe attic spot you're leaning on creaks.")
    print("\n'Wait — quiet! What is that...")
    print("It's coming from directly above!'")

    print("\n[1] Sit still.")
    print("[2] Crawl away.")
    c4 = input("\n> ").strip()

    if c4 == "1":
      print("\nYou hear the sound of rocks being broken through")
      print("in a heartbeat — as not a half second later,")
      print("sharp, tiny, dagger-like fingers that feel wet")
      print("pierce through your skin, letting out gouts")
      print("of blood.")
      player.hp = max(1, player.hp - int(player.max_hp * 0.10))
      print(f"[-10% HP]  [{player.hp}/{player.max_hp}]")
      print("\nYou throw yourself back and start frantically")
      print("crawling away in the direction you originally")
      print("intended before you got in the crawl space —")
      print("toward the intersection.")
    else:
      print("\nThe tongue shoots through where you'd just been —")
      print("barely missing you.")
      print("\nAttached to the tongue are tiny, sharp, barbed")
      print("fingers that lash to and fro — each finger of the")
      print("hands stretching this way and that way,")
      print("trying to feel for you.")

    print("\n'Get up there and stop him!'")
  else:
    print("\nThe tongue shoots through where you'd just been —")
    print("barely missing you.")
    print("\nAttached to the tongue are tiny, sharp, barbed")
    print("fingers that lash to and fro — each finger of the")
    print("hands stretching this way and that way,")
    print("trying to feel for you.")
    print("\n'Get up there and stop him!'")

  print("\nYou crawl forward hurriedly.")
  print("\nSera's cries reach you as you turn in the")
  print("crawl-space intersection, toward her spot.")
  print("\nBehind you — the hatch bursts open.")
  print("\nAs you near her spot, you see a shower of rocks")
  print("cascade behind you, and a crab-like mandible")
  print("latching onto the platform.")
  print("\nWithout waiting to see what happens next,")
  print("you descend into Sera's cell.")
  print("\nBehind you, muffled through the boards:")
  print("\n'And you — devour them! Your meal's coming")
  print("early today!'")

  _solo_promise_cell_onward(player, dropped_in=True)