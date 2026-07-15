import random
import builtins
from wizard import Wizard
from combat import simple_combat
from enemy import (RavenSwarm, DesperateTraveler, Enforcer, FrightenedWoman,
                   Consequential, MotherRaven, EnforcerCommander, Dara)
from items import (HPPotion, ManaPotion, ManabdaPotion, PassRune,
                   ExceptVial, FinallyFlask, Cloak, Staff, Rod, Scepter)
from merchant import Maren
from systems.checkpoint import save_checkpoint

_lines_since_pause = 0
PAGE_HEIGHT = 18

def print(*args, **kwargs):
  global _lines_since_pause
  builtins.print(*args, **kwargs)
  text = " ".join(str(a) for a in args)
  _lines_since_pause += text.count("\n") + 1
  if _lines_since_pause >= PAGE_HEIGHT:
    builtins.input("\n  [ press Enter ▼ ]")
    _lines_since_pause = 0

def input(prompt=""):
  global _lines_since_pause
  _lines_since_pause = 0
  return builtins.input(prompt)


def resolve_ch1_route(flags):
  if (flags.get('promised_sister_search')
      and not flags.get('companion_mira')
      and not flags.get('companion_duo')
      and not flags.get('dara_dungeon')):
    return 'solo_promise'
  if (flags.get('companion_mira')
      and flags.get('companion_duo')):
    return 'duo'
  return 'default'


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


def _print_creature_duo(player):
  print("\nThe torchlight gives life to its features.")
  print("\nBlack fur bristling through shredded clothing.")
  print("Legs that belong to something arachnid —")
  print("except one, which is human, joined up")
  print("at the hip — kicking out at what isn't")
  print("attacking it.")
  print("Or maybe fighting the fact")
  print("that this is its existence.")
  print("\nAn arm that once was human,")
  print("and now appears to be a crab's pincer.")
  print("\nAnd a face —")
  print("what's left of one —")
  print("three eyes crowded together on its edge,")
  print("with a mouth full of sharp, glistening things")
  print("inside, stretched up toward its ears")
  print("on the left side.")


def duo_dungeon_route(player):
  player.flags['ch1_branch_complete'] = True

  print("\n\nThe corridor splits.")
  print("\nLeft — a ladder bolted to the wall.")
  print("Above it, the sound of wings.")
  print("\nRight — the corridor continues.")
  print("Longer. Darker.")
  print("\nMira doesn't ask. She's already moving right.")

  print("\nYou start walking forward.")
  print("Caleb ahead, half-turned — watching the way")
  print("you came the whole time.")
  print("Mira behind you.")
  print("\nThen — a door on the left.")
  print("A sound from behind it.")
  print("Soft. Rhythmic.")
  print("Someone sobbing.")
  print("Long past the point where sobbing helps.")
  print("\nMira stops.")
  print("\n'We can't just leave them.'")
  print("\nCaleb doesn't stop.")
  print("'We can. We have to.")
  print("Every door we open is time Sera")
  print("doesn't have.'")
  print("\n'You sounded just like them right now.")
  print("Do you hear yourself?'")
  print("\n'I sounded like someone who's trying")
  print("to not waste time on a goal")
  print("that's not our goal!'")
  print("His voice raises slightly in anger.")
  print("'I sound like someone who's trying")
  print("to keep us on tra—'")
  print("\nHis words cut off midway as his mouth")
  print("drops open, staring past Mira,")
  print("from the way you all came.")
  print("\nAlmost as if on cue, you and Mira turn")
  print("your heads in the direction —")
  print("as a sound accompanies the movement.")
  print("\n'hrrrnnHahH'")
  _print_creature_duo(player)
  print("\n'RUN!' Caleb shouts — before anyone")
  print("has the chance to investigate.")
  print("\nThey run. He turns in the direction")
  print("of Sera's cell, Mira behind him.")

  print("\n[1] Run with them.")
  print("[2] Stand your ground. Alone.")
  c = input("\n> ").strip()

  if c == "2":
    monster = Consequential()
    simple_combat(player, monster)
    if not player.is_alive():
      return
    player.gain_exp(monster.exp_value)
    print("\nIt dies the way it moved.")
    print("Wrong. In stages.")
    print("The human leg is the last part to stop.")
    print("\nThe corridor is quiet again.")
    print("The sobbing behind the door isn't.")
    print("\nYou follow the way they ran.")
    print("\nYou find the cell by the sound of voices.")
    print("\nInside — Sera, unbound, on her feet.")
    print("Mira's arm still around her like")
    print("it forgot how to be anywhere else.")
    print("Caleb at the desk, going through papers.")
    print("\nWhatever the reunion was,")
    print("you weren't in it.")
    print("\nSera looks up.")
    print("'Your friend,' she says to Mira.")
    print("Then to you: 'They told me")
    print("what you stopped back there.'")
    player.flags['duo_stood_alone'] = True
  else:
    print("\nIt follows.")
    print("You hear it behind you the whole way —")
    print("wrong feet on old stone.")
    print("\nThe cell door is open ahead. You all pour in —")
    print("and it fills the doorframe behind you.")
    monster = Consequential()
    monster.atk = max(1, monster.atk - 2)
    simple_combat(player, monster)
    if not player.is_alive():
      return
    player.gain_exp(monster.exp_value)
    print("\nIt dies the way it moved.")
    print("Wrong. In stages.")
    print("The human leg is the last part to stop.")
    print("\nMira pulls her sister into an embrace —")
    print("long, and lovingly held,")
    print("like she's making up for every day")
    print("of it at once.")

  print("\n'How touching.'")
  print("\nFrom the doorframe.")
  print("\n'Too bad this is where it all ends for you.'")
  print("\nDara — in full regalia, and with a sadistic")
  print("grin on her face as she casually walks")
  print("a few steps into the room.")
  print("\nShe isn't hurrying. Doesn't need to.")
  print("People who hold the only exit don't have to.")
  print("\nShe takes the room in.")
  print("Mira. Caleb. Sera, unbound. And you.")
  print("A calculation happens behind her eyes.")
  print("She starts speaking while looking you")
  print("straight in the eyes.")
  print("\n'Do you know what she's worth?'")
  print("She nods at Sera.")
  print("'They think she's a map to the artifacts.")
  print("Which she is.")
  print("But maps can't always be trusted —")
  print("especially if one doesn't have a legend")
  print("to decipher them.' She sighs.")
  print("'I'd hoped to use torture as a way")
  print("of acting as that legend.'")
  print("\nShe continues on as she shares glances")
  print("with the entire party — her perfectly")
  print("brown hair framing her face, as if even it")
  print("was too scared to move.")
  print("\n'The Twilight believes it's ancient.")
  print("Inevitable. The leadership believes it")
  print("hardest — sitting on something")
  print("they've never seen and don't understand.'")
  print("\n'I understand it. I ALONE can harness it!'")
  print("\n'There's a voice under this world.")
  print("It has more names than the world")
  print("has languages.")
  print("The Twilight Ledger named themselves")
  print("after one of them —")
  print("children naming themselves after a king.'")
  print("\n'I intend to meet the king.'")
  print("\nCaleb, flat:")
  print("'She's confessing.")
  print("People confess when they've decided")
  print("the audience won't repeat it.'")
  print("And slowly adds:")
  print("'Because they won't be able to.'")
  print("\n'He's quick,' Dara says.")
  print("'I can see why they kept you breathing.'")
  print("\nThe knife is in her hand")
  print("before you see her draw it.")

  boss = Dara()
  boss.atk = max(1, boss.atk - 2)
  simple_combat(player, boss)
  if not player.is_alive():
    return
  player.gain_exp(boss.exp_value)
  player.flags['dara_dead'] = True

  print("\nShe goes down the way she did everything.")
  print("Efficiently. No wasted syllables.")
  print("\nAt the end she looks at you.")
  print("Only you.")
  print("\n'Looks like you'll be that legend,' she says.")
  print("\nThen nothing more, as she closes her eyes.")
  print("\nSera breaks the silence that follows.")
  print("\n'More will be coming.")
  print("She didn't walk this deep alone —")
  print("and dead operatives get noticed")
  print("faster than live prisoners.'")
  print("\nNobody argues.")
  print("\nYou all move — back down the corridor,")
  print("toward the way out.")
  print("\nYou almost leave.")
  print("\nThen Caleb stops.")
  print("\n'This is only part of the problem solved.'")
  print("He turns back to face the three of you.")
  print("'The ravens. Something down here")
  print("is sending them. We walk out now,")
  print("and every road we take after this,")
  print("we take being assaulted by their pursuit.'")
  print("\nSera goes still — remembering.")
  print("\n'I saw them. Through the door slot,")
  print("when they moved me. Guards hauling meat —")
  print("raw, buckets of it. Like something")
  print("was being fed.")
  print("Or someone.'")
  print("\nShe points down to the opposite end")
  print("of the corridor.")
  print("\n'A door. With a lone ladder in it.")
  print("That direction.'")
  print("\nThe party moves — checking doors")
  print("quickly along the route to it.")
  print("But each one is either a victim")
  print("long forgotten, or a lone room")
  print("waiting to ensnare its next capture.")

  print("\n\nThe ladder ends at a latch.")
  print("\nYou go first — ease it open")
  print("a finger's width. Peek.")
  print("\nPeeking through the gap —")
  print("\nThe aviary is vast.")
  print("More space than the dungeon below")
  print("should be able to contain.")
  print("\nRavens on every surface. Still.")
  print("\nAnd at the center —")
  print("\nLarger than the rustling of wings")
  print("you thought was just a figment")
  print("of your imagination when you entered")
  print("the dungeon.")
  print("She stands at least ten feet tall.")
  print("Blacker than the nighttime sky")
  print("could ever hope to be.")
  print("\nA smell of dirt, rot, and droppings")
  print("assaults your senses all at the same time.")
  print("\nHer wings are pinned elegantly to her")
  print("as she sits atop a branch extending")
  print("from a manmade post in the middle")
  print("of her roost.")
  print("\nShe doesn't look like what made the others —")
  print("but for sure what they one day")
  print("might become, if lucky.")
  print("\nShe noticed you as soon as you peeked")
  print("into her lair.")
  print("But she took no interest.")
  print("For what threat lay in you?")
  print("\nThe others climb through behind you.")
  print("Still, she doesn't move.")
  print("\nThen Sera pulls herself into the room.")
  print("\nThe one thing she hadn't counted on.")
  print("\nThe head turns.")
  print("Every eye finds the hatch.")
  print("\nShe pauses.")
  print("\nThe entrance of Sera made her give pause —")
  print("maybe doubt crossed her mind,")
  print("maybe recognition from senses.")
  print("The whys will never be known.")
  print("\nBut it gave the party enough time")
  print("to go on the offense.")
  print("\nThen she erupts off the branch.")
  print("\nCaleb takes a talon across the shoulder.")
  print("A wing-buffet slams Mira into the frame.")
  print("The beak finds you before you find")
  print("your footing.")
  player.hp = max(1, player.hp - 8)
  print(f"[-8 HP]  [{player.hp}/{player.max_hp}]")

  mother_raven = MotherRaven()
  mother_raven.atk = max(1, mother_raven.atk - 2)
  simple_combat(player, mother_raven)
  if not player.is_alive():
    return
  player.gain_exp(mother_raven.exp_value)
  player.flags['mother_raven_defeated'] = True

  print("\nThe last spell finds her mid-flight.")
  print("\nShe doesn't go through a wall.")
  print("She doesn't take the room with her.")
  print("\nShe just stops —")
  print("like something enormous being unplugged —")
  print("and slumps.")
  print("\nThe floor takes her weight")
  print("and the whole aviary shudders once.")
  print("\nThen stillness.")
  print("\nThe ravens on every surface go still.")
  print("Then scatter — through gaps you didn't")
  print("see before. Gone.")

  print("\nAmong the feathers on the floor —")
  print("one that's different from the others.")
  print("Longer. Darker.")
  print("It doesn't move when the others scatter.")
  print("\nYou take it.")
  print("Raven Talon acquired.")
  player.inventory.add("Raven Talon")

  print("\nSera steps around the body.")
  print("\n'Now you know what I know.")
  print("East. Past the ruins. Into the desert.")
  print("Five artifacts. Together they find it —")
  print("the Ledger. The real one.")
  print("The thing these imitators named")
  print("themselves after.")
  print("\nGet to them first.")
  print("Because you've seen tonight what")
  print("the people who want them are willing")
  print("to do to a stranger.")
  print("Imagine what they'd do with a god.'")
  player.flags['artifact_rumor_east'] = True
  player.flags['sera_freed'] = True

  print("\nCaleb points — up, across the aviary.")
  print("\nAn opening. Top of the far wall,")
  print("where the roof stopped agreeing")
  print("with the architecture.")
  print("Night air moving through it.")
  print("\nYou climb to it. Look down.")
  print("\nBelow, piled against the facility wall —")
  print("hay.")

  print("\n[1] Take the fall.")
  print("[2] Look for another way down.")
  cf = input("\n> ").strip()

  if cf == "1":
    print("\nYou jump.")
    print("The hay does most of the catching.")
    print("The ground does the rest.")
    player.hp = max(1, player.hp - int(player.max_hp * 0.25))
    print(f"[-25% HP]  [{player.hp}/{player.max_hp}]")
  else:
    print("\nYou work your way down — ledge, seam,")
    print("drainpipe, prayer.")
    print("It mostly works.")
    player.hp = max(1, player.hp - int(player.max_hp * 0.10))
    print(f"[-10% HP]  [{player.hp}/{player.max_hp}]")

  print("\nThe night receives you at the bottom.")
  print("The other three come down after —")
  print("slower, smarter, together.")
  print("\nSera looks back at the facility once.")
  print("\n'We're staying. All three of us.")
  print("There's a resistance in this town —")
  print("it just doesn't know it yet.")
  print("We're going to introduce it to itself,")
  print("and take this town back.'")
  print("\nMira takes your hand. Just for a moment.")
  print("Caleb nods once — the whole speech")
  print("he's capable of.")
  print("\nIt isn't your goal to stay")
  print("and play freedom fighter.")
  print("\nEast is.")
  print("\nSo off you go.")
  print("\n              [ CHAPTER 1 ENDS — DUO PATH ]")


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

  print("\n\nThe mountain opens up before you.")
  print("The air bites immediately. Thin and sharp.")
  print("Above — a sky that stops you mid-step.")
  print("\nStars. Vast and indifferent and countless.")
  print("The kind of sky that makes every question feel\n"
        "answerable")
  print("and every answer feel far away.")
  print("The darkness here is not cruel.")
  print("It is simply infinite.")
  print("Anything could be out there.")
  print("Everything could be out there.")
  print("\n'The Path begins where guidance ends,' adds the\n"
        "unfamiliar voice you heard before — the one that named\n"
        "your magic and defined you — giving you pause.")
  print("You look around, hoping to discern its source.")
  print("There are no clues.")

  print("\nThe mountain slope continues to descend downwards.")
  print("Far below — impossibly far — structures in the dark\n"
        "loom.")
  print("Too small to read. Too active to ignore.")
  print("Tiny shadows move against dim light.")
  print("A town. Or something that was one.")

  print("\nThe wind shifts.")
  print("It carries something with it.")
  print("A sound.")
  print("High. Desperate. Human.")
  print("\nA good couple hundred feet below you, on the right side\n"
        "of the slope, there are two figures obscured by the\n"
        "shadows of the night.")
  print("Above them, a shape in the sky that is wrong.")
  print("Too many. Too quiet for birds.")
  print("Too hungry.")
  print("They descend.")

  print("\nThree paths present themselves:")
  print("1: Move toward the figures. Whatever comes, comes.")
  print("2: You observe the ordeal for a moment or two. You\n"
        "aren't moved to help.")
  print("   This isn't what is required to conquer the Path.")
  print("3: Descend. The town calls louder than strangers do.")
  choice_2 = input("\nChoose [1/2/3]: ")

  if choice_2 == "1":
    print("\nYou move toward them.")
    print("The sound above sharpens into something that isn't\n"
          "quite a shriek.")
    print("More like a frequency. Something that wants to be\n"
          "inside your skull.")
    swarm = RavenSwarm()
    simple_combat(player, swarm)

    if player.is_alive():
      player.gain_exp(swarm.exp_value)
      print("\nThe swarm breaks.")
      print("Not defeated. Dispersed.")
      print("Like they decided you weren't worth the cost.")
      print("For now.")

      print("\nThe figures resolve in the dark.")
      print("A man. Medium build. A mop of blonde hair that hangs\n"
            "over his eyes")
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
      print("'What do you want for that heroic display of strength?'\n"
            "he scoffs.")
      print("Not a thank you. A negotiation opening.")

      print("\n[1: 'Are you serious? I just saved you from becoming\n"
            "dinner, maybe just some basic gratitude?']")
      print("[2: 'What is this place? What are you running from?']")
      print("[3: 'Easy. I'm not your enemy.']")
      print("[4: Say nothing.]")
      choice_3 = input("\nYour response: ")

      if choice_3 == "1":
        print("\nHe studies you. The suspicion doesn't leave his face.")
        print("If anything, it settles deeper.")
        print("A long pause before he speaks.")
        print("The words deliberately tumble out slowly, but flat and\n"
              "unimpressed — 'convenient timing.'")
        print("'People out here don't just happen to show up.'")
        print(f"His eyes drop to your hands. To the mark.")
        print(f"'{player.school}.' He says it like he's cataloguing evidence.")
        print("'Either way. The town down there doesn't care what you\n"
              "just did.'")
        print("'They'll take from you same as anyone.'")
        player.flags['traveler_wary'] = True

      elif choice_3 == "2":
        print("\nHe laughs. No humor in it.")
        print("'Place.' He says the word like it offends him.")
        print("'This is the Threshold. Where the Path begins.'")
        print("'Where people come with ideas about power and glory.'")
        print("He looks at the woman briefly. Something passes between\n"
              "them.")
        print("'Most of those ideas don't survive the first week.'")
        print("The woman speaks, barely above nothing:")
        print("'They say the voice at the start... was the last one\n"
              "who made it all the way.'")
        print("Silence.")
        player.flags['traveler_wary'] = True

      elif choice_3 == "3":
        print("\nYou raise empty hands.")
        print("'Easy. I'm not your enemy.'")
        print("\nHe watches you for a long moment.")
        print("The hair doesn't move. But his shoulders drop a\n"
              "fraction.")
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
          print("'Enforcers run it. They work for someone called the\n"
                "Collector.'")
          print("'He works for people above him who don't have names.'")
          print("'They take mana, and manabda alike without pause, and\n"
                "they'll take more in blood if their price isn't paid.'")
          print("'They call it Tithe. I call it unfair — tyranny. But\n"
                "most call it whatever excuse they have to, to be able\n"
                "to sleep.'")
          print("The woman's voice, barely audible:")
          print("'My sister came here not long ago.'")
          print("'She's... she was always like that. Certain of\n"
                "herself.'")
          print("'A prodigy, people said. She believed them.'")
          print("A pause.")
          print("The man with the mop of blonde hair remains glued to\n"
                "his past, as if the words cause reflection. He was very\n"
                "still.")
          print("'Caleb told me she was already here. Already making a\n"
                "name.'")
          print("'Said if she could do it, imagine what we could do\n"
                "together.'")
          print("She doesn't look at him.")
          print("'She was talking to the wrong people! About the wrong\n"
                "things!' he said in a voice that suggested she not push\n"
                "this into an argument.")
          print("'Enforcers were already watching her.'")
          print("'One morning we went to her room at the inn.'")
          print("'The door had been... it was off the hinges.'")
          print("A long silence.")
          print("'We don't know!.. we just don't.. know.' She started to\n"
                "sob.")
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
          print("'Figured if there was a way in, maybe there's a way\n"
                "out.'")
          print("He looks toward the fog where the threshold sits above\n"
                "them.")
          print("'There isn't.'")
          print("'It's a one way door.'")
          print("'Whatever brought you here doesn't bring you back.'")
          print("'We spent two days up here finding that out the hard\n"
                "way.'")
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
        print("'Couldn't make it work. Something about it knows what\n"
              "it wants.'")
        print("He holds it out.")
        print("'Maybe it wants you.'")
        print("\nItem acquired: Sort Rune")
        player.inventory.add("Sort Rune")
        player.flags['traveler_friend'] = True

      elif choice_3 == "4":
        print("\nYou say nothing.")
        print("The man shifts. Uncomfortable with the silence.")
        print("The woman speaks first. Soft. Like she's afraid of her\n"
              "own voice.")
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
      print("'They ring it when it's time to gather in the square\n"
            "and pay up.'")
      print("'Everyone in Vardeth stops what they're doing and\n"
            "goes.'")
      print("'Everyone.'")
      print("He looks at the woman. At you. At the slope below.")
      print("'For most people down there it's just another bad day.'")
      print("'For us...'")
      print("He glances up the slope where the swarm dissolved into\n"
            "nothing.")
      print("'When those things don't come back with what they were\n"
            "sent for...'")
      print("'...they'll know.'")
      print("'Nobody walks away from what they owe that town.\n"
            "Nobody.'")
      print("'Move. Or don't. But decide now.'")

      if player.flags.get('traveler_friend'):
        print("\n[1: 'Stay with me. We handle this together.']")
        print("[2: 'Go. Hide. When they send more — it's me they'll\n"
              "find waiting.']")
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
          print("'It won't.' He repeats it. Like he needs to hear it\n"
                "twice.")
          player.flags['companion_duo'] = True
          player.flags['companion'] = "Caleb and Mira"

        elif choice_5 == "2":
          print("\n'That's...' He stops.")
          print("Looks at you properly for the first time.")
          print("'Don't die for us, Pathwalker.'")
          print("He pulls her toward the slope.")
          print("'Ravens only come for those who've been through that\n"
                "gate.'")
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
          print("\n'The Tithe.' He almost laughs.")
          print("Almost.")
          print("'You'll learn more about it down there")
          print("than I could tell you in a year.'")
          print("\nThe bell tolls again. Closer somehow.")
          print("He glances up the slope. Then back at you.")
          print("\nMira steps forward before he can stop her.")
          print("'You're going down there.'")
          print("It isn't a question.")
          print("'My sister is in Vardeth. Somewhere.'")
          print("'We can't go back for her. The moment we pass that gate")
          print("they own us again.'")
          print("Her voice is steady.")
          print("Steady the way someone gets")
          print("when they've run out of room to fall apart.")
          print("'But you've never entered. You could listen.")
          print("Just — listen. For word of her.'")
          print("\nCaleb doesn't object.")
          print("That tells you how much it matters.")
          print("\n[1: 'I'll keep an ear out. I promise nothing more.']")
          print("[2: 'I have my own path. I'm not your errand runner.']")
          choice_5b = input("\nChoose: ")

          if choice_5b == "1":
            print("\nMira exhales.")
            print("Like she'd been holding that breath since the gate.")
            print("'That's all I'm asking.'")
            print("\nCaleb looks at you a moment longer than he needs to.")
            print("Then — deciding something — he points up the slope.")
            print("'East of the threshold. There's a fold in the rock —")
            print("an old herder's shelter built into it. Roof's half\n"
                  "gone.'")
            print("'A month out here teaches you where the wind doesn't\n"
                  "reach.'")
            print("'We hold near it at dusk. Every dusk.'")
            print("'You learn anything about Sera —'")
            print("\n'Sera.' Mira's voice, small. 'My sister's name is\n"
                  "Sera.'")
            print("'Older than me. Braver than me.'")
            print("'She'd want you to know her name.'")
            print("\nCaleb waits for that to pass. Then:")
            print("'Dusk. The fold. Don't be followed.'")
            print("\n'If you're smart — you'll forget the town has a name.'")
            print("He already knows you won't.")
            print("He doesn't waste another word on it.")
            player.flags['promised_sister_search'] = True
            player.flags['rendezvous_known'] = True

            print("\nThe raven bodies are still cooling on the slope")
            print("where you dropped them.")
            print("\nCaleb follows your glance.")
            print("\n'They'll be replaced by morning.")
            print("They always are.")
            print("Something keeps making more of them.'")
            print("\nHe doesn't ask.")
            print("Asking for two favors in one night")
            print("is a debt he can't carry.")

            print("\n[1] 'Whatever is spawning them — I'll deal with it.'")
            print("[2] Say nothing. One promise is enough.")

            vow_choice = input("\n> ").strip()

            if vow_choice == "1":
              print("\nMira and Caleb exchange a look.")
              print("You're not meant to read it yet.")
              print("\n'Then dusk can't come soon enough,'")
              print("Caleb says.")
              player.flags['promised_source'] = True
            else:
              print("\nThe slope says nothing either.")
          elif choice_5b == "2":
            print("\nMira flinches.")
            print("Small. Quickly buried.")
            print("But you saw it. So did he.")
            print("\nCaleb steps between you and her.")
            print("Not threatening. Just done.")
            print("'Right.' Cold now. 'Forget I let her ask.'")
            print("\nThe bell tolls. He doesn't look toward it.")
            print("He's looking at you.")
            print("'You'll fit right in down there.'")
            player.corruption += 1

          print("\nThey move up the slope. Fast.")
          print("The dark takes them the way it takes everything out\n"
                "here.")
          player.flags['travelers_fled'] = True

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
          player.flags['travelers_fled'] = True

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
              print("It comes out like a bellow and a wound at the same\n"
                    "time.")
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
              print("Markings that seem to shift when you're not looking\n"
                    "directly.")
              print("It hums in her hand.")
              print("Then hums louder.")
              print("She looks at you with something like wonder.")
              print("\nHer voice barely makes it out.")
              print("'I'm Mira.'")
              print("\nA pause.")
              print("'It never did that for him.'")
              print("She means the rune. She doesn't explain further.")
              print("\nShe holds it toward you.")
              print("The humming shifts the moment it gets close to your\n"
                    "hand.")
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
              print("Something inside it has been patient. It's done\n"
                    "waiting.)")
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
          player.flags['travelers_abandoned'] = True
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
    print("\nBehind you, somewhere up the slope —")
    print("a sound cuts off mid-note.")
    print("You couldn't say what it was.")
    print("You made sure of that.")

  if not player.inventory.has_item("Sort Rune") and "sort" not in player.spells:
    print("\n\nSomething catches your eye on the path ahead.")
    print("A small stone. Carved. Half-buried in the dirt.")
    print("It hums when you pick it up.")
    print("Louder when your hand closes around it.")
    print("You don't know what it is.")
    print("It doesn't have that problem.")
    player.inventory.add("Sort Rune")
    print("\nYou turn it over once.")
    print("Then slip it into your pack.")
    print("The hum fades against the cloth.")
    print("\nYou walk on.")

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
    print("Reveals common items. 10% chance of uncovering\n"
          "something rarer.)")
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
  save_checkpoint(player)
  print("\nAnd you see it.")
  print("\nVardeth.")
  print("\nThe sky above it stops you cold.")
  print("Behind you — stars. Infinite. Indifferent. Full of\n"
        "possibility.")
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
  print("People move through them the way water moves through\n"
        "cracks —")
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
  print("Always busy with something that matters to someone\n"
        "above them.")

  print("\nMetal grates line the street at irregular intervals.")
  print("You almost don't notice the first one.")
  print("Then you hear it.")
  print("\nA sound from below.")
  print("Distant. Muffled.")
  print("Human.")
  print("\nYou keep walking.")
  print("Everyone keeps walking.")
  print("That might be the worst thing about it.")

  if player.flags.get('companion_duo'):
    print("\nCaleb slows before the square opens up.")
    print("He's already counted the Enforcers at the corners.")
    print("You can tell by the way his eyes stopped moving.")
    print("\nHe doesn't say anything.")
    print("He reaches into his pack.")
    print("Pulls out a dark cloth — worn, shapeless, the kind of\n"
          "thing")
    print("that makes a person look like everyone else.")
    print("He pulls it over his shoulders without ceremony.")
    print("\nHe looks at Mira.")
    print("She's already adjusting — hood up, jacket reversed,")
    print("something about the way she carries herself\n"
          "deliberately flattened.")
    print("Less distinctive. More forgettable.")
    print("She's done this before.")
    print("\n'Once we're in there,' Caleb says quietly,")
    print("'we don't know each other.'")
    print("'Give it ten steps before you follow.'")
    print("He doesn't wait for a response.")
  elif player.flags.get('companion_mira'):
    print("\nMira stops before the square opens up.")
    print("You almost walk past her before you notice.")
    print("\nShe's seen the Enforcers at the corners.")
    print("Her hood comes up. Her jacket turns inside out.")
    print("The way she carries herself flattens —")
    print("smaller, slower, forgettable.")
    print("It takes her four seconds.")
    print("She's done this before.")
    print("That lands harder than anything she could have said.")
    print("\n'Walls have eyes here.' Barely a whisper.")
    print("'Once we're in there — you don't know me.'")
    print("'Ten steps. Then follow.'")
    print("She steps into the crowd and becomes part of it.")

  print("\nThe square opens up ahead.")
  print("Large. Too large for the town around it.")
  print("Like it was built for a different purpose")
  print("and this one grew up around it.")
  print("\nLines. Or what was left of lines.")
  print("The mass tithe ended roughly half an hour before you\n"
        "arrived.")
  print("You can tell by the way people are dispersing.")
  print("Slow. Careful.")
  print("Like moving too fast might draw attention.")
  print("\nAt the center — a device.")
  print("Larger than anything you'd expect.")
  print("A platform. Leather straps worn smooth from use.")
  print("Tubes that feed into containers")
  print("being carried away by people who don't make eye\n"
        "contact.")
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
  print("Stalls pressed up against the buildings that border it\n"
        "—")
  print("produce, cloth, dried things in bundles, a man with a\n"
        "cart of something")
  print("that smells like it was cooked this morning.")
  print("People moving between them.")
  print("Not the dispersing crowd. Different people.")
  print("The ones who have somewhere to be and something to\n"
        "trade.")
  print("Voices low. Business done quickly.")
  print("Eyes that flick to the center and flick away again.")
  print("\nThe buildings that ring the square are tall enough to\n"
        "lean.")
  print("Between them — gaps.")
  print("Narrow. Dark even now.")
  print("Alleyways that slot between the stone like\n"
        "afterthoughts,")
  print("running back into whatever Vardeth is behind its public\n"
        "face.")
  print("Mostly trash-filled corridors from the looks of it.")
  print("Others just as lonely and sad as the faces of most of\n"
        "the people in this square.")
  print("This is the whole town, more or less.")
  print("The square and the alleys feeding off it.")
  print("Everything else is just walls.")

  if player.flags.get('companion_duo'):
    print("\nThey're not beside you.")
    print("That was the arrangement.")
    print("But you find them anyway —")
    print("the man at a stall across the square,")
    print("handling a bundle of dried herbs he has no intention of\n"
          "buying.")
    print("His eyes haven't stopped working the corners.")
    print("\nThe woman is further off. Half-turned away.")
    print("Not looking at the device. Not the Enforcers.")
    print("Faces.")
    print("One by one.")
    print("Like she's looking for someone.")
    print("Even from here you can see it —")
    print("her hands have gone very still.")
  elif player.flags.get('companion_mira'):
    print("\nShe's exactly where she said she'd be.")
    print("Ten steps back. A stranger in the same crowd.")
    print("\nShe isn't looking at the device.")
    print("She isn't looking at the Enforcers.")
    print("She's looking at faces.")
    print("Moving through the crowd with her eyes the way someone\n"
          "does")
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

  print("\n[1: Approach an Enforcer. Get cleared — before they\n"
        "come asking.]")
  print("[2: Move through the square quietly. Find the\n"
        "alleyways.]")
  print("[3: Approach the Enforcers. Tell them you want in.]")
  if player.flags.get('companion_duo') or player.flags.get('companion_mira'):
    print("[4: Point them out. Tell the Enforcers what they're\n"
          "looking at.]")
  choice_9 = input("\nChoose: ")

  if choice_9 == "4" and (player.flags.get('companion_duo') or player.flags.get('companion_mira')):
    print("\nYou catch the nearest Enforcer's eye.")
    print("You nod — once — toward where they're standing.")
    print("\nThe Enforcer looks.")
    print("Then looks back at you.")
    print("Something passes between you that doesn't need words.")
    print("\nThree of them move at once.")
    print("Fast. Practiced.")
    print("The kind of coordinated that means they've done this\n"
          "many times.")

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
      print("They're dragging her and she's not even trying to stop\n"
            "them.")
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
    print("\nThe Enforcer who took your nod finds you")
    print("before you've decided where to go.")
    print("'The Collector pays for eyes like yours.'")
    print("'East end of the square. Tell them what you did today.'")
    print("'They'll understand.'")
    player.flags['enforcer_aligned'] = True

  if choice_9 == "1":
    print("\nThe Enforcer marks you before you reach him.")
    print("'New face.'")
    print("He says it the way someone reads a number off a list.")
    print("'New faces owe arrival levy. Everyone under this sky")
    print("pays for the privilege of standing under it.'")
    print("He nods toward a side building.")
    print("'Pay now. Get your token. Walk where you like.'")
    print("'Or wait until collection finds you.'")
    print("A pause that isn't really a pause.")
    print("'They're less gentle when they have to come looking.'")
    print("\n[1: Submit to private collection — costs 3 Mana and 2\n"
          "Manabda]")
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
      print("\nYou're halfway across the square when you feel it —")
      print("the weight of being watched by someone who knows you.")
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
      print("'Report to the Collector's office. East end of the\n"
            "square.'")
      print("'Tell them Reth sent you.'")
      print("He looks you over once more.")
      print("'Don't make me regret it.'")
      player.flags['enforcer_aligned'] = True
      player.corruption += 3
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


  if player.flags.get('enforcer_aligned'):
    player.corruption = max(player.corruption, 3)


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
    print("\nShe walks toward you — unhurried, like she has all the\n"
          "time in the world —")
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
      print("'You don't look like the usual recruits.'")
      print("Not an insult. More like she's working something out.")
      print("'Most of them come in here already angry about\n"
            "something.'")
      print("'You're not.'")
      print("\nA beat.")
      print("\n'Interesting.'")
      print("\nShe goes back to her desk.")
      print("Sits down. Picks up her pen.")
      print("'East corridor. Tomorrow morning. Someone will brief\n"
            "you.'")
      print("She's back to her papers.")
      print("But she doesn't tell you to leave.")
      player.flags['dara_romance'] = True
    else:
      print(f"\nYou give it.")
      print("\nThe tone registers. Something in her face closes.")
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


  print("\n\nYou find it almost by accident.")
  print("A door that doesn't announce itself.")
  print("No sign. No window.")

  if player.corruption >= 8:
    print("Just a door that's slightly warmer than the stone\n"
          "around it.")
    print("You've stopped noticing things like that.")
    print("Or maybe you've just stopped caring what they mean.")
  elif player.corruption >= 4:
    print("Just a door that's slightly warmer than the stone\n"
          "around it.")
    print("You notice it the way you notice everything now.")
    print("Cataloguing. Assessing. Old habits are softer than new\n"
          "ones.")
  else:
    print("Just a door that's slightly warmer than the stone\n"
          "around it.")
    print("In Vardeth, warmth from anywhere feels like it means\n"
          "something.")

  print("\nThrough a smeared window, a woman moves behind the\n"
        "counter.")
  print("Small shop. Cramped shelves.")
  print("The glass has cracks that were never worth fixing —")
  print("or maybe there was never money to.")
  print("The place looks like it made peace with its own decline\n"
        "a long time ago.")
  print("But the shelves have stock.")
  print("In Vardeth, that alone means something.")

  if player.flags.get('companion_mira'):
    if player.corruption >= 4:
      print("\nMira stops one step behind you at the threshold.")
      print("You don't see her face.")
      print("You don't need to.")
      print("She follows. She always follows.")
      print("But something in the set of her shoulders is different\n"
            "now.")
      print("Like she's carrying something she didn't have before.")
    else:
      print("\nMira glances at the window. Then at you.")
      print("She glances at the shelves the way someone does")
      print("when they haven't seen proper goods in a while.")
      print("Just for a second.")
      print("Then her face goes careful again.")
      print("She doesn't say anything. She just follows.")

  if player.flags.get('enforcer_aligned'):
    print("\nThe woman inside has seen you before you reach the\n"
          "door.")
    print("The way she straightens isn't welcome.")
    print("It's bracing.")
  else:
    print("\nSomething about the door makes you slow down.")
    print("Not fear. Something else.")
    print("Like it's been waiting. Quietly. Without making a fuss\n"
          "about it.")

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

  if player.flags.get('companion_duo'):
    print("\nOutside, the square has thinned.")
    print("The tithe crowd is long gone. The Enforcers at the\n"
          "corners")
    print("have settled into the bored half-attention of a slow\n"
          "shift.")
    print("\nCaleb drifts back to your side the way strangers don't\n"
          "—")
    print("without looking at you, without hurrying.")
    print("'Crowd's gone,' he says to the air. 'Eyes went with\n"
          "it.'")
    print("Mira appears at your other side a moment later.")
    print("As if she'd been there all along.")
    print("Maybe she had.")
  elif player.flags.get('companion_mira'):
    print("\nOutside, the square has thinned.")
    print("The Enforcers at the corners have gone bored and\n"
          "inward.")
    print("\nMira falls into step beside you.")
    print("No signal. No fuss.")
    print("Just close enough to talk")
    print("and far enough to deny it.")


  if (player.flags.get('companion_mira') or player.flags.get('companion_duo'))\
      and not player.flags.get('mira_ledger_moment_done'):

    if player.flags.get('companion_duo'):
      print("\nYou're crossing the square when Caleb speaks.")
      print("Not to anyone in particular.")
      print("\n'That voice.'")
      print("He says it the way someone mentions a sound they keep\n"
            "hearing in a wall.")
      print("Toneless. Like you've interrupted something.")
      print("'The one that comes from nowhere.'")
      print("'Talks like it already knows the answer to whatever\n"
            "it's about to say.'")
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
      print("Not troubled exactly. Somewhere between troubled and\n"
            "something else.")
      print("Like she's been thinking about the same thing for a\n"
            "long time")
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
      print("Because she isn't sure how to say it without sounding\n"
            "like she's lost her mind.")
      print("\n'That voice.' She drops her own voice lower.")
      print("'The bold one. It doesn't speak often.'")
      print("'Sometimes it offers something — advice, almost. Like\n"
            "it's trying to help.'")
      print("'Other times it...' She stops.")
      print("'...probes. Like it's testing something in you.'")
      print("'Deciding if you're worth the trouble before it commits\n"
            "to anything.'")
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


  print("\n\nYou're back in the square.")
  print("You know it differently now.")
  print("The first time it stopped you.")
  print("The device. The straps. The people who walked past\n"
        "without looking.")
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


  print("\n\nYou're about to move on.")
  print("\nThen — movement on the far side of the square.")
  print("\nTwo Enforcers.")
  print("Between them, three people.")
  print("Hands bound. Heads down.")
  print("Moving fast. Not dragged. Walking.")
  print("Like they've decided compliance is the last thing they\n"
        "have left.")
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
    print("\nA tug at the edge of your vision —")
    print("Mira. Pulling at the corner of Caleb's sleeve.")
    print("Twice. Quick. Right out in the open.")
    print("\nEvery rule they set on the way in — gone.")
    print("She's forgotten all of it.")
    print("\nCaleb's eyes snap to the corners first — Enforcers,")
    print("bored, not looking — then to her,")
    print("already wearing the face he saves for telling her no.")
    print("\nThen he sees hers.")
    print("\nThe hollowness she's carried since the slope is gone.")
    print("Burned off. Something fierce and bright underneath.")
    print("\n'What if Sera's down there?' Barely above a whisper —")
    print("but her grip on his sleeve doesn't loosen.")
    print("'Caleb. What if that's where they took her?'")
    print("\nHe looks at the door.")
    print("Then back at her.")
    print("You watch him reach for the careful, measured thing")
    print("he usually says.")
    print("\nHe doesn't find it.")
    print("\n'...Then we find out.' Quiet.")
    print("He nods toward the alley the guard took.")
    print("'Follow.'")
    print("\nMira turns to you.")
    print("The words come fast, like she's been holding them")
    print("since the gate.")
    print("'Sera. My older sister.'")
    print("'The brave one. She'd argue with an Enforcer")
    print("like it cost nothing — and somehow it never did.'")
    print("'People listened to her. People followed her.'")
    print("\n'It's true.' Caleb, quiet. Not arguing for once.")
    print("'When things got bad, she's the reason we thought")
    print("we could make it out here at all.'")
    print("'If Sera could do it — we could do it.'")
    print("'That was the whole plan.'")
    print("\n'She cries at everything.'")
    print("Mira says it almost to herself.")
    print("'Always has, ever since we were little.")
    print("Quick to feel it all — no matter how")
    print("strong her magic got.'")
    print("A breath that's almost a laugh and almost isn't.")
    print("'If she's down there — she's crying right now.")
    print("And arguing through it.'")
  elif player.flags.get('companion_mira'):
    print("\nFingers close around your sleeve.")
    print("\nMira.")
    print("You turn — and stop.")
    print("Because her face has changed.")
    print("The careful, flattened thing she wears in public is\n"
          "gone.")
    print("Her eyes are lit. Frightened and hopeful at once —")
    print("and the hope is winning.")
    print("\n'What if Sera's down there?'")
    print("She doesn't let go of your sleeve.")
    print("'They take people. That's a door people don't come out\n"
          "of.")
    print("If she's anywhere —'")
    print("She stops. Steadies herself.")
    print("'I have to know. Please.'")
    print("\nThen, quieter — because you've never met her:")
    print("'Sera. My older sister. The brave one.'")
    print("'She'd argue with an Enforcer like it cost nothing.'")
    print("'People followed her. I followed her.'")
    print("'She cries at everything. Always has,")
    print("ever since we were little —")
    print("no matter how strong her magic got.'")
    print("A breath that's almost a laugh and almost isn't.")
    print("'If she's down there — she's crying right now.")
    print("And arguing through it.'")
    print("\nShe tilts her head toward the alley the guard took.")
  elif player.flags.get('promised_sister_search'):
    print("\nA promise made on a dark slope stirs.")
    print("Bound hands. A door the town pretends not to see.")
    print("If Sera is anywhere in Vardeth —")
    print("it's somewhere like that.")
    print("You said you'd listen.")
    print("This is louder than listening.")
  else:
    print("\nPeople went through that door.")
    print("Nobody came back out of it.")
    print("And the whole square has agreed not to notice.")
    print("Whatever Vardeth keeps down there —")
    print("it's the kind of secret a town builds itself around.")

  print("\n[1: Follow him into the alley.]")
  print("[2: Hold. Watch where he goes from here.]")
  follow_choice = input("\nChoose: ").strip()

  if follow_choice == "2":
    print("\nYou wait.")
    print("He doesn't reappear on any side of the square you can\n"
          "see.")
    print("Whatever that back way connects to — it's not visible\n"
          "from here.")
    print("\nYou wait long enough to be certain.")
    print("Then you go anyway.")


  print("\n\nThe alley is narrow enough that the walls catch sound.")
  print("Smell of damp stone. Something old underneath it.")
  print("You move single file.")

  if player.flags.get('companion_duo'):
    print("\nCaleb goes first without being asked.")
    print("The kind of reflex that comes from experience, not\n"
          "bravery.")
  elif player.flags.get('companion_mira'):
    print("\nMira presses close to the wall. Practiced.")
    print("You match her without thinking about it.")


  print("\nYou're almost at the end of the alley when something\n"
        "moves above you.")
  print("Not wind.")
  print("\nYou look up.")
  print("\nRavens.")
  print("Sitting on a ledge near the roofline, set back from the\n"
        "square.")
  print("More than you'd expect.")
  print("Watching the square. Patient in a way birds aren't.")
  print("You don't know what to make of it yet.")
  print("You keep moving.")

  print("\nAt the far end, the alley opens onto a sunken little\n"
        "court —")
  print("and there he is.")
  print("The guard. Your guard. The one with the keys.")
  print("He shoulders through a low door under a guttering\n"
        "lantern.")
  print("A tavern. The kind that survives by not being worth\n"
        "robbing.")
  print("\nThe door swallows him.")
  print("Faint warmth. Faint noise. The clink of a man settling\n"
        "in")
  print("for a long appointment with a cup.")
  print("\nHe'll be there a while.")
  print("Long enough.")
  print("You mark the door and pull back up the alley.")
  player.flags['tavern_marked'] = True


  print("\n\nOutside. The alley mouth. Evening light going grey.")
  print("You stop.")

  if player.flags.get('companion_duo') and player.flags.get('companion_mira'):
    print("\nCaleb folds his arms.")
    print("'We know where they go in. We know the door.'")
    print("'We don't know the layout. We don't know the rotation.'")
    print("'And we don't know what we're walking into once we're\n"
          "past the first level.'")
    print("\nMira is quiet for a moment.")
    print("'A door the whole town pretends not to see,' she says.")
    print("'Whatever's behind it — they're not advertising it.'")
    print("'Which means it matters.'")
    print("\nCaleb nods once. Reluctant. Like agreeing costs him\n"
          "something.")
    print("'We need the transport record. The intake list.'")
    print("'Wherever they log who goes in — that's where the names\n"
          "are.'")
    print("\nA beat.")
    print("'Enforcer office,' Mira says.")
    print("'Has to be. They don't run something like this without\n"
          "documentation.'")
  elif player.flags.get('companion_mira'):
    print("\nMira leans against the wall.")
    print("'We know the door. We know it goes down.'")
    print("'We don't know who's in there. We don't know the\n"
          "rotation.'")
    print("She pauses.")
    print("'We need the intake record. Names. Dates. Where they\n"
          "put people.'")
    print("'The Enforcers document everything — they have to, at\n"
          "their scale.'")
    print("'There's an office somewhere in this district.'")
    print("'If there's a list, it's there.'")
  elif player.flags.get('companion_duo'):
    print("\nCaleb looks at the door from a distance.")
    print("'We're missing the intake record,' he says.")
    print("'Go in blind and we're guessing the whole way.'")
    print("'Enforcer office. There's always an office.'")
    print("'They run on paper. That's how you hold people\n"
          "accountable.'")
    print("'Or how you pretend to.'")
  else:
    print("\nYou think it through.")
    print("You know the door. You know it goes down.")
    print("You don't know the rotation. You don't know who's in\n"
          "there.")
    print("You don't know what they did with the three people you\n"
          "watched walk in.")
    print("\nA record exists somewhere. It has to.")
    print("Something that logs intake. Names. Assignments.")
    print("The Enforcers are an organization. Organizations\n"
          "document.")
    print("\nThere's an office in this district.")
    print("You're certain of it now.")

  player.flags['enforcer_office_known'] = True


  print("\n\nThe Enforcer office sits at the east end of the square.")
  print("Not hidden. Just unremarkable.")
  print("A building that doesn't want to be noticed and mostly\n"
        "succeeds.")
  print("\nYou approach.")

  moral_path = player.corruption < 4

  if moral_path:

    print("\nYou stop outside the window.")
    print("It's open. Not wide. Wide enough.")
    print("\nA voice inside. A woman's voice.")
    print("Dry delivery. Like she finds most things slightly\n"
          "obvious.")
    print("\nShe's talking to someone who isn't responding much.")
    print("Working through something. An intake record, by the\n"
          "sound of it.")
    print("\n'...Twilight gets the cipher, Ledger sets the key.'")
    print("She says it the way you'd say something you've been\n"
          "told to remember")
    print("and have remembered so many times it's lost all\n"
          "texture.")
    print("Bare. Built for use, not comfort.")
    print("'Two words. That's the whole thing. You'd think they'd\n"
          "make it harder.'")
    print("She flips a page.")
    print("'Twilight. Ledger. In that order. That's the door.'")
    print("\nA pause.")
    print("Then she laughs, very briefly, at something on the\n"
          "page.")
    print("'Honestly, it's embarrassing.'")
    print("\nSomething shifts in the room. A stool. She's standing.")
    print("You step back from the window.")
    player.flags['cipher_answer_known'] = True
    player.flags['cipher_answer_source'] = 'overheard'

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

    print("\nYou go in.")
    print("\nShe's behind a desk.")
    print("Late twenties, maybe early thirties — it's hard to tell\n"
          "in this light.")
    print("Dark hair. The kind of stillness that isn't calm so\n"
          "much as controlled.")
    print("She looks up when you enter.")
    print("She was expecting someone else.")
    print("She doesn't show it.")
    print("\n'This isn't a public office.'")
    print("Not aggressive. Just true.")
    print("\nShe studies you for a moment.")
    print("The way someone does when they're deciding which\n"
          "version of a situation this is.")
    print("Deciding whether you're a problem or something more\n"
          "interesting.")

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
      print("'If you already knew that, you didn't need to come\n"
            "here.'")
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


  print("\n\nYou're back in the square.")
  print("The stone tablet sits where it always has.")
  print("Twenty-six letters carved in order.")
  print("The question below them.")

  if player.flags.get('enforcer_aligned'):
    print("\nYou slow as you pass it.")
    print("An Enforcer peels off the nearest corner before you've\n"
          "even stopped.")
    print("'Twilight property.' He doesn't raise his voice.")
    print("'Recruits keep moving.'")
    print("\nYou keep moving.")
    print("Whatever the stone holds — it isn't for people on the\n"
          "payroll.")
    print("You chose a different reward.")
  elif not player.flags.get('cipher_answer_known'):
    print("\nYou stand in front of it.")
    print("The answer isn't there yet.")
    print("You can feel the gap where it should be.")
    print("You keep walking.")
  else:
    print("\nThis time you stop differently.")
    print("\nThe question waits where it has always waited:")
    print("\n  'What is the order that starts between light and dark")
    print("   and holds all of the names meant to lift the world?'")
    print("\nBetween light and dark. Twilight.")
    print("The names meant to lift the world. A ledger.")
    print("\nThe words from the office window slot into place")
    print("like they were cut for this stone all along.")
    print("Twilight. Ledger. In that order.")
    print("\nThe answer is two words.")
    print("Not the words themselves — the way they fit together.")
    print("The slot at the base is waiting.")

    print("\n[1: Attempt the cipher. (Costs: 2 Mana, 2 Manabda, 3\n"
          "Gold)]")
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
        print("The way it always speaks — like it was already there,\n"
              "waiting for you to be ready.")

        print("\n  ┌──────────────────────────────────────────────────────────┐")
        print("  │  LEDGER FOOTNOTE — Indexing and Concatenation            │")
        print("  └──────────────────────────────────────────────────────────┘")
        print("\n  'The alphabet is a list.'")
        print("  'Twenty-six elements. Each one has a position.'")
        print("  'The first element sits at index zero. Not one. Zero.'")
        print("'This is not a convention. It is the nature of the\n"
              "structure.'")
        print()
        print("'A cipher built on the alphabet is built on those\n"
              "positions.'")
        print("  'You take the letters you need. You join them.'")
        print("'That joining — one sequence appended to another — is\n"
              "concatenation.'")
        print()
        print("  'In the language of the world beneath this one:'")
        print()
        print("' elements =\n"
              "[\'A\',\'B\',\'C\',\'D\',\'E\',\'F\',\'G\',\'H\',\'I\',")
        print("'\n"
              "\'J\',\'K\',\'L\',\'M\',\'N\',\'O\',\'P\',\'Q\',\'R\',")
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
          print("\nMira watches the compartment close itself back into the\n"
                "stone.")
          print("'The letters,' she says quietly.")
          print("'They were always the answer. The order is what makes\n"
                "them mean something.'")
          print("She looks at you.")
          print("Something in her face you don't quite have a name for.")
        elif player.flags.get('companion_duo'):
          print("\nCaleb looks at the closed tablet.")
          print("'Hm.' That's all.")
          print("High praise from him.")


        print("\nThen you notice the quiet.")
        print("Not the usual Vardeth quiet. A new one.")
        print("\nThe nearest stalls have stopped mid-transaction.")
        print("A woman holding a bundle of cloth she's forgotten she's\n"
              "holding.")
        print("An old man who has taken his cap off")
        print("without appearing to know why.")
        print("Every face turned toward you.")
        print("\nThat stone has stood in this square longer")
        print("than anyone alive has been paying tithe beside it.")
        print("Nobody has ever opened it.")
        print("You can read that much in their faces.")
        print("\nAnd at the corners of the square —")
        print("the Enforcers are no longer bored.")
        print("Two of them are looking directly at you.")
        print("One says something to the other")
        print("without moving his eyes off you.")

        if not player.flags.get('dara_met'):
          print("\nThe office door at the east end opens.")
          print("\nA woman steps out. Late twenties, maybe early thirties.")
          print("Dark hair. The kind of stillness that isn't calm")
          print("so much as controlled.")
          print("She crosses the square unhurried —")
          print("and the Enforcers straighten as she passes them.")
          print("That tells you something before she says a word.")
          print("\nShe stops in front of the tablet. Looks at it.")
          print("Then at you.")
          print("\n'Eighty years.' She says it like a price.")
          print("'That stone has been asking its question for eighty\n"
                "years.'")
          print("'Collectors have tried. Clerks have tried.")
          print("People significantly more desperate than you have\n"
                "tried.'")
          print("\nShe studies you the way someone does when they're\n"
                "deciding")
          print("which version of a situation this is.")
          print("A problem. Or something more interesting.")
          print("\n'Dara.' She doesn't offer a hand.")
          print("'I keep the records you're not supposed to know exist.'")
          print("\nHer eyes drop to the seam in the stone —")
          print("the compartment, closed again, but she knows where to\n"
                "look.")
          print("Then back up to you.")
          print("\n'Here's my problem.'")
          print("'That answer is two words. Cipher words.'")
          print("'Maybe four people in this town know them.")
          print("I'm one. I know the other three by name.'")
          print("'And you walked in off a mountain this morning.'")
          print("\nShe lets that sit.")
          print("'So. Either you're something that stone")
          print("has been waiting eighty years for —")
          print("or somebody talked.'")
          print("'Which is it?'")
          print("\n[1: 'The stone told me what it needed.']")
          print("[2: 'Lucky guess.']")
          print("[3: Say nothing. Hold her gaze.]")
          dara_press = input("\nChoose: ").strip()

          if dara_press == "1":
            print("\nYou say it evenly. Because it's almost true.")
            print("Something did speak when your hand went in.")
            print("It just wasn't the stone.")
            print("\nShe studies you for a long moment.")
            print("Looking for the lie. Not finding the shape of one.")
            print("\n'...Huh.' Quiet. Genuinely thrown —")
            print("and visibly annoyed at being genuinely thrown.")
            print("'That's either the truth or the best answer")
            print("I've heard all year.'")
            print("'I haven't decided which is worse.'")
            player.flags['dara_intrigued'] = True
          elif dara_press == "2":
            print("\n'Lucky.' She repeats it flatly enough to bruise it.")
            print("'Eighty years of desperate people, and luck")
            print("picked the stranger with mountain dust on his boots.'")
            print("'No.'")
            print("\nShe steps half a pace closer.")
            print("'Somebody talked. And when I find out who —")
            print("I'll remember who they talked to.'")
          else:
            print("\nYou hold her gaze and give her nothing.")
            print("\nShe reads the nothing.")
            print("Files it.")
            print("\n'Quiet ones.' Almost to herself.")
            print("'The quiet ones are always worth a page of their own.'")

          player.flags['dara_suspicious'] = True
          print("\nA beat.")
          print("'I'd say keep your head down — but you opened the\n"
                "stone,")
          print("so apparently we're past that.'")
          print("\nShe glances once at the Enforcers. They unstiffen\n"
                "slightly.")
          print("'Don't do anything else interesting today.'")
          print("'I'd hate to have to write you down.'")
          print("\nShe walks back the way she came.")
          print("She doesn't look back.")
          print("She knows you're watching. That's enough for her.")
          player.flags['dara_met'] = True
          player.flags['dara_path'] = 'moral'
          if player.flags.get('companion_mira'):
            print("\nBeside you, Mira lets out a breath.")
            print("'That woman scares me,' she says.")
            print("'And she was being nice.'")
          elif player.flags.get('companion_duo'):
            print("\nCaleb watches her go.")
            print("'Records,' he says quietly.")
            print("'She just told us where the intake list lives.'")
            print("'Whether she meant to or not.'")

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


  print("\n\nThe evening still has hours in it.")
  print("And for the first time since the slope —")
  print("nothing is chasing you through them.")
  print("Vardeth, for better or worse, is open.")
  player.flags['maren_available'] = True
  from systems.hub import hub
  from location import Vardeth
  hub(player, Vardeth)


  print("\nNight has settled in properly by the time you head\n"
        "back.")
  print("Down the alley. Past the ledge — the ravens still\n"
        "there,")
  print("darker shapes against a dark sky. Still watching.")
  print("\nThe tavern door under the lantern. Warm light in the\n"
        "cracks.")
  print("If the guard kept to his schedule —")
  print("he's hours deep by now.")

  print("\n\nThe tavern receives you.")
  print("Low ceiling, propped by beams that have given up being\n"
        "straight.")
  print("Candle stubs in dishes. The smell of old smoke,")
  print("tallow, and something being reheated for the third\n"
        "time.")
  print("\nLightly peopled. Quieter than a tavern has any right to\n"
        "be.")
  print("The few patrons sit pressed to the walls —")
  print("high-legged tables, shoulders nearly touching the\n"
        "stone,")
  print("backs to nothing.")
  print("Nobody looks up. Looking up costs something in Vardeth.")
  print("\nThe man behind the bar is built like a cellar door —")
  print("wide as two of you, beard going grey in patches,")
  print("a belly that says the kitchen here feeds at least one\n"
        "person well.")
  print("In a town of mended clothes and hollow cheeks,")
  print("that belly is doing a lot of quiet talking.")
  print("\nHe spots you and his whole face gets involved.")
  print("'HA! New faces!'")
  print("It comes out like a small avalanche.")
  print("'Down MY alley, no less! You lot lost, brave, or\n"
        "thirsty?'")
  print("He's already reaching for cups.")
  print("'Don't answer — door's behind you either way, so it\n"
        "better be thirsty.'")
  if player.flags.get('companion_duo'):
    print("\nHe squints past you at the two finding a table.")
    print("'Three, then! Even better.'")
  print("\n'Name's Dovan. The tavern hasn't got one.")
  print("Folk just say the tavern, and I've made peace with it.'")
  print("A laugh that shakes the shelf behind him.")
  print("'And you are?'")
  print("\nYou give him a name. Maybe even yours.")

  print("\nA cup cracks against wood in the far corner.")
  print("'DOVAN! 'Nother!'")
  print("The guard. Jacket half-undone. Listing in his seat")
  print("like the room is on a slow tilt only he can feel.")
  print("The keys hang from a loop on his belt.")
  print("\nSomething crosses Dovan's face.")
  print("The guard is too far gone to read it.")
  print("You aren't.")
  if player.flags.get('companion_duo') or player.flags.get('companion_mira'):
    print("Neither is Mira — you catch her catching it too.")
  print("\nDovan leans across the bar. The big voice drops")
  print("to something just for this side of the counter.")
  print("'Every night, that one. End of every shift.'")
  print("'Drinks half my stock. Pays when he remembers how.'")
  print("A pause. He polishes a spot that doesn't need it.")
  print("'If he forgot the way here entirely —'")
  print("He doesn't finish. He just pours the man's drink.")
  print("'Let's say I wouldn't cry about it.'")

  if player.flags.get('companion_duo'):
    print("\nMira leans in, voice under the room's noise.")
    print("'He's already half gone.' A glance at the corner.")
    print("'If we sat with him... kept him company...'")
    print("She doesn't finish it. She doesn't have to.")
    print("\nCaleb, dry as the firewood:")
    print("'Kept him company. That's what we're calling it.'")
    print("'Fine. But you' — a look at you — 'do the reaching.")
    print("My hands shake around Enforcers. Old habit.'")
  elif player.flags.get('companion_mira'):
    print("\nMira leans in, voice under the room's noise.")
    print("'He's already half gone.'")
    print("'If we kept him company a while... talked to him...'")
    print("Her eyes flick to the keys. Back to you.")
    print("'People stop holding on to things")
    print("when they think they're among friends.'")
    print("She says it like someone who learned it the hard way.")
  else:
    print("\nYou take the measure of him from the bar.")
    print("Half gone already. The rest of the way is purchasable.")
    print("The keys are right there.")
    print("All it costs is patience. And gold.")


  drunk_level = 1
  talk_count = 0
  fail_count = 0
  keys_taken = False

  print("\nYou cross the room. Pull up a stool at his table.")
  print("He squints at you like you might be two people.")
  print("'...You buying?'")

  while not keys_taken and player.is_alive():
    print(f"\n  [He is {'tipsy' if drunk_level == 1 else 'properly drunk' if drunk_level == 2 else 'swaying in his seat' if drunk_level == 3 else 'one breeze from the floor'}.]")
    print("\n[1: Buy him another round. (1 gold)]")
    print("[2: Keep him talking.]")
    print("[3: Go for the keys.]")
    print("[4: Walk away. Not tonight.]")
    drink_choice = input("\nChoose: ").strip()

    if drink_choice == "1":
      if player.gold >= 1:
        player.gold -= 1
        if drunk_level < 4:
          drunk_level += 1
        print("\nYou signal Dovan. He pours without being told what.")
        if drunk_level == 2:
          print("\nThe guard toasts you.")
          print("Misses his own cup with the toast.")
          print("Finds it on the second try. Deeply satisfied about it.")
        elif drunk_level == 3:
          print("\nHe's explaining something important about doors.")
          print("'They're all — listen. LISTEN.'")
          print("'They're all just walls that gave up.'")
          print("He taps the table like he's said something profound.")
          print("He has no idea how right he is.")
        else:
          print("\nHe attempts to point at you")
          print("and selects the fireplace instead.")
          print("'You. You're alright. Not like — like THEM.'")
          print("He doesn't specify them.")
          print("The fireplace doesn't ask.")
      else:
        print("\nYou reach for gold that isn't there.")
        print("'Tab's a no, friend.' Dovan, from across the room.")
        print("Cheerful. Absolute.")

    elif drink_choice == "2":
      talk_count += 1
      if talk_count == 1:
        print("\nYou ask about the work. Vaguely. The way strangers do.")
        print("\n'The work.' He snorts into his cup.")
        print("'Nobody wants the under-floor shift.'")
        print("'Just me an' Berr down there nights.")
        print("An' Berr don't count.'")
        print("He laughs at something that isn't funny.")
        player.flags['guard_intel_thin_shift'] = True
        player.flags['sub_level_known'] = True
      elif talk_count == 2:
        print("\nYou keep him going. It doesn't take much.")
        print("\n'They sort 'em, y'know.'")
        print("His voice drops to a secret —")
        print("at a volume too drunk to keep one.")
        print("'Ones that can pay go back up.'")
        print("'Ones that can't...'")
        print("He waves vaguely at the floor.")
        print("He doesn't finish.")
        print("He doesn't need to.")
        player.flags['guard_intel_sorting'] = True
        if player.flags.get('companion_mira') or player.flags.get('companion_duo'):
          print("\nAcross the table, Mira has gone very still.")
          print("Her hands pressed flat to the wood.")
          print("Whatever she was hoping —")
          print("she's hoping it harder now.")
          print("And dreading it more.")
      else:
        print("\nHe's mostly weather and grievances now.")
        print("The well of useful things has run dry.")
        print("Only the cup is still producing.")

    elif drink_choice == "3":
      chance = {1: 25, 2: 50, 3: 75, 4: 95}[drunk_level]
      roll = random.randint(1, 100)
      print("\nThe keys dangle from the loop on his belt.")
      print("Tantalizing. Completely unaware of their future.")
      print("You let your hand drift off the table edge...")
      if roll <= chance:
        print("\nHis head dips toward the cup at exactly the right\n"
              "moment.")
        print("The loop gives. The keys come free without a sound.")
        print("Your pocket welcomes them like they were always going\n"
              "to end up there.")
        keys_taken = True
      else:
        fail_count += 1
        if fail_count == 1:
          print("\nOne eye opens.")
          print("He doesn't move otherwise. Just looks at you.")
          print("\n'Buy me a drink first.'")
          print("He closes the eye again.")
          print("\nYou withdraw the hand. Slowly.")
          print("Even drunk ones have instinct.")
        else:
          print("\nHis hand slaps down on the keys. Hard.")
          print("'OI.' Loud. Too loud.")
          print("The wall-sitters look up — looking up suddenly\n"
                "affordable.")
          print("\n'Easy, easy!' Dovan's voice rolls across the room")
          print("like a barrel over the noise.")
          print("'He's grabbing his OWN keys, you suspicious wreck.")
          print("Yours are on your belt, look down.'")
          print("\nThe guard looks down. Finds his keys.")
          print("Mollified by the discovery of his own belt.")
          print("'...S'right,' he mutters. 'S'mine.'")
          if fail_count == 2:
            print("\nDovan catches your eye on the way back to the bar.")
            print("Doesn't wink. Doesn't need to.")
            print("Get him drunker, the look says. You're embarrassing my\n"
                  "tavern.")
          else:
            print("\nBut there's no talking past it this time.")
            print("Something old and trained surfaces through the drink.")
            print("His chair goes over backwards. He's up —")
            print("swaying, red-eyed, and absolutely certain now.")
            print("\n'THIEF.'")
            print("The wall-sitters are already filing out the door.")
            print("They know what comes next better than you do.")
            print("\n'NOT THE TABLES!' Dovan, resigned, from somewhere\n"
                  "behind the bar.")
            print("\nThe guard swings first.")
            drunk_guard = Enforcer("Drunk Dungeon Guard")
            simple_combat(player, drunk_guard)
            if player.is_alive():
              print("\nHe goes down among the stools.")
              print("Breathing. Loudly. The drink claiming")
              print("whatever the fight left behind.")
              print("\nThe keys come off his belt without protest now.")
              player.flags['dungeon_keys'] = True
              player.flags['guard_brawled'] = True
              keys_taken = True
              print("\nDovan surveys the wreckage. Rights one chair.")
              print("'He swung first.' He says it to the empty room —")
              print("rehearsing it. Deciding it's even true.")
              print("'But you understand you drink somewhere else")
              print("until he forgets your face.'")
              print("A beat.")
              print("'Won't take long. He forgets his own.'")
            else:
              print("\nDarkness.")
              print("The Path ends here.")
              print("Beaten by a man who couldn't point at you an hour ago.")
              exit()

    elif drink_choice == "4":
      print("\nYou push back from the table.")
      print("Not tonight. Not like this.")
      print("'Wha— where's the party going?' The guard, to the room\n"
            "generally.")
      print("The room declines to answer.")
      break

  if keys_taken:
    print("\nYou settle back like nothing happened.")
    print("Finish your drink at a civilian pace.")
    print("Then you rise, nod to Dovan, and walk out.")
    print("\nThe night air takes you back.")
    print("The keys are a quiet new weight against your hip.")
    player.flags['dungeon_keys'] = True
    if player.flags.get('companion_duo'):
      print("\nOutside, Caleb exhales something close to approval.")
      print("'Didn't think you had the hands for it.'")
      print("From him, that's a parade.")
    elif player.flags.get('companion_mira'):
      print("\nOutside, Mira hugs her elbows against the cold.")
      print("But she's almost smiling.")
      print("'One step closer,' she says.")
      print("To Sera. She doesn't have to say it.")


  print("\n\nThe night stretches ahead.")
  print("Vardeth sleeps badly — but it sleeps.")
  print("What you do with the dark is up to you.")
  player.flags['vardeth_story_done'] = True
  hub(player, Vardeth)


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
              print("\nWhat this place has done to her,")
              print("and the sudden appearance of her sister,")
              print("cause rivulets of tears to branch")
              print("down her face in a steady stream.")
              print("\nOne thing they couldn't take from her")
              print("was her love — and the hope that someone")
              print("would come to her rescue.")
              print("\nThat hope was rewarded.")
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
              print("\nShe's looking at the ladder.")
              print("\nBefore you head toward it, she grabs")
              print("your shoulder and slightly turns you toward her.")
              print("\n'Let's just be careful.")
              print("We can't afford to lose any more.")
              print("Neither can I.'")
              print("\nYou climb first — going from one instance")
              print("of dark to a slightly less dark one,")
              print("but in no terms less dangerous.")
              print("\nMira pulls herself up beside you.")

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

            if player.flags.get('companion_mira'):
              print("\nBOOM.")
              print("\nBehind you, the hatch jumps in its frame.")
              print("Something on the dungeon side wants up.")
              print("\nThere's no time to care.")

            mother_raven = MotherRaven()
            if player.flags.get('companion_mira'):
              mother_raven.atk = max(1, mother_raven.atk - 2)
            simple_combat(player, mother_raven)

            if player.is_alive():
              player.gain_exp(mother_raven.exp_value)

              if player.flags.get('companion_mira'):
                print("\n\nThe last spell leaves your hand before")
                print("you've fully decided to throw it.")
                print("\nIt finds her in mid-flight —")
                print("as she's about to swoop down on you.")
                print("\nShe becomes a falling mass of black")
                print("ruffled feathers, tinged with blood.")
                print("\nShe squawks haphazardly —")
                print("more in terror than anger.")
                print("\nThe wall breaks outwards, splitting into")
                print("oh so many pieces from the impact")
                print("of her enormous body.")
                print("\nShe pushes away from tumbling with it")
                print("by great flaps of her wings,")
                print("as debris falls toward the square below,")
                print("and shouts of utter shock and anger,")
                print("combined with screams, reply back.")
                print("\nShe slightly regains her composure,")
                print("and starts trying to orient and fly in place —")
                print("\nas the hatch gives way behind you.")
                print("\nThe monstrous creature from before springs")
                print("into the air after escaping —")
                print("shooting out its tongue at what was")
                print("supposed to be you.")
                print("\nInstead, you step out of the way —")
                print("and it wraps around the middle of her body.")
                print("\nShe careens toward the opposite wall,")
                print("dragging the creature with her —")
                print("shrieking as it claws frantically at the driver")
                print("taking it down and away over the wall.")
                print("\nThe wall can't resist their combined weight —")
                print("and copies exactly what happened")
                print("to the one opposite of it.")
                print("\nTheir journey doesn't last long.")
                print("\nA final loud squawk.")
                print("Followed by a guttural roar.")
                print("\nYou look over the edge and see a tangle")
                print("of black fur and feathers, entwined")
                print("in a gross mound that's leaking blood.")
                player.flags['mother_raven_defeated'] = True
                print("\nThe ravens on every surface go still.")
                print("Then scatter.")
                print("Through gaps that are suddenly everywhere.")
                print("\nAmong the feathers on the floor —")
                print("one that's different from the others.")
                print("Longer. Darker.")
                print("It doesn't move when the others leave.")
                print("\nYou take it.")
                print("Raven Talon acquired.")
                player.inventory.add("Raven Talon")
                print("\nMira is already at the broken edge.")
                print("\n'Before anyone comes to investigate,' she says.")
                print("\nBelow — piled against the outside of the wall,")
                print("half-buried in new debris — hay.")
                print("\nYou both jump.")
                print("\n\nThe hay receives you.")
                print("Mira lands beside you a moment after.")
                print("\nYou barely stick the landing —")
                print("but when you do,")
                print("the human hand of the creature shoots out,")
                print("grabbing you.")
                print("\nMira screams as it happens.")
                print("\nYou prepare to finish the last of the horrors")
                print("standing in the way of your escape.")

                consequential = Consequential()
                consequential.hp = consequential.hp // 2
                consequential.max_hp = consequential.hp
                consequential.atk = max(1, consequential.atk - 2)
                simple_combat(player, consequential)

                if player.is_alive():
                  player.gain_exp(consequential.exp_value)
                  print("\nIt's hurled back from the last spell.")
                  print("\nIt starts to rise —")
                  print("as its body wobbles, unsure of its actions.")
                  print("\nIt gives one final groan as it collapses")
                  print("forward, snapping with its pincer in vain.")
                  print("\nBut it's meaningless —")
                  print("for you are well beyond its reach.")
                  print("\nMira looks at it with a mix")
                  print("of disgust and pity.")
                  print("\nThen at you.")
                  print("\nShe offers her hand.")
                  print("\n1. Take it")
                  print("2. Don't — but smile back and explain:")
                  print("   maybe in the future. You don't have")
                  print("   the luxury of what could be right now.")
                  hand_choice = input("> ").strip()

                  if hand_choice == "1":
                    player.flags['mira_hand_taken'] = True
                    print("\nYou take it.")
                    print("\nA lone tear makes its way down her face.")
                    print("\n'Let's get out of here,' she says,")
                    print("'and make sure my sister's death")
                    print("wasn't in vain.")
                    print("\nAnd let's put an end to the tyranny")
                    print("of the Twilight Ledger.'")
                  else:
                    player.flags['mira_deferred'] = True
                    print("\nMaybe in the future.")
                    print("You don't have the luxury")
                    print("of what could be right now.")
                    print("\n'I understand,' she says.")
                    print("\n'But let's commit the time to making sure")
                    print("Sera's death wasn't in vain.'")
                    print("\nYou return the smile, but weakly.")
                    print("\n'Gladly.'")

                  print("\nThe two of you head off to the east.")
                  player.flags['ch1_branch_complete'] = True
                  print("\n            [ CHAPTER 1 ENDS ]")

              else:
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