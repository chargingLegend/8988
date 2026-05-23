import random

class inventory:
  def __init__(self):
    self.items = []
    self.max_size = 12

  def add(self, item):
    if len(self.items) >= self.max_size:
      raise Exception("Inventory full, cant carry anymore!")
    self.items.append(item)
    return f"Added {item} to inventory"

  def remove(self, item):
    if item in self.items:
      self.items.remove(item)
      return f"Used {item}."
    raise ValueError(f"{item} not in inventory.")

  def __str__(self):
    if not self.items:
      return "Inventory is empty."
    return "Inventory: "+", ".join(self.items)

class Monster:
  def __init__(self, name="Unknown", hp=10, desc="A creature.", exp_value=0):
    self.name = name
    self.hp = hp
    self.desc = desc
    self.status = []
    self.exp_value = exp_value

  def __repr__(self):
    return f"{self.name} - HP: {self.hp} - {self.desc}"

  def is_alive(self):
    return self.hp > 0

  def take_damage(self, dmg, dmg_type="physical"):
    self.hp -= dmg
    if self.hp < 0:
      self.hp = 0
    print(f"{self.name} takes {dmg} {dmg_type} damage! HP: {self.hp}")
    if not self.is_alive():
      print(f"{self.name} falls.")

class RavenSwarm(Monster):
  def __init__(self, name="Raven Swarm", hp=15, desc="Not birds. Too many eyes. Too much hunger."):
    super().__init__(name, hp, desc, exp_value=50)
    self.attack_dmg = (1, 4)
    self.dmg_type = "piercing"

  def attack(self, target):
    dmg = random.randint(*self.attack_dmg)
    print(f"{self.name} swarms! Beaks and claws rake for {dmg}!")
    target.take_damage(dmg, self.dmg_type)

Mountain = {
  "name" : "Moutainside",
  "common" : ["Rock", "Snow", "Stick"],
  "uncommon" : ["Mountain Herb"],
  "rare" : ["Ancient coin"],
}

class Wizard:
  def __init__(self, name, level=1, hp=100, school="Undecided", spells=None, manabda=8):
    self.name = name
    self.level = level
    self.hp = hp
    self.school = school
    self.manabda = manabda
    self.spells = spells if spells is not None else []
    self.spell_data = {}


  def __repr__(self):
    return f"Wizard({self.name}) - HP: {self.hp} - School: {self.school} - Spells: {len(self.spells)}/5 - Manabda: {self.manabda}"

  def is_alive(self):
    return self.hp > 0

  def take_damage(self, dmg, dmg_type="physical"):
    self.hp -= dmg
    if self.hp < 0:
      self.hp = 0
    print(f"{self.name} takes {dmg} {dmg_type} damage! HP: {self.hp}")
    if not self.is_alive():
      print(f"{self.name} falls.")

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
      print("A whisper you didn’t think brushes the back of your skull.")
      print("Death recognizes you. And waits.")
      self.spells = ["Rattle", "Wither", "Gravechill"]
      self.spell_data = {
        "Rattle": (2, 7, "necrotic", "{target}'s bones remember the grave. They protest."),
        "Wither": (1, 6, "necrotic", "vitality flees {target} like startled crows."),
        "Gravechill": (3, 6, "necrotic", "the cold of tombs settles in {target}.")
      }
    elif school == "Enhancement":
      print("Muscle fibers sing. Bones feel dense as iron.")
      print("The mountain air tastes thin. You don’t care.")
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
      print("Whispers you don’t recognize brush your thoughts.")
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
    if "sort" not in self.known_spells:
      self.known_spells.append("sort")
      self.sort_acquired_by = method
      return "The runes on your palm shift. You understand how to use the rune to 'sort' now."
    return "You already understand the sort spell"

  def sort(self, location: dict):
    if "sort" not in self.spells:
      raise AttributeError("You trace the rune to be able to use the 'sort' ability, but it doesnt mean anything to you.not yet")
    found = random.sample(location["common"], k=2)

    if random.random() < 0.10:
      found.append(random.choice(location["uncommon"]))

    for item in found:
      self.inventory.add(item)

    print(f"you focus on the Rune of sort")
    print(f"Found: {', ' .join(found)}")
    print(self.inventory)

  def cast_manabda(self, spell_name, target=None):
    if spell_name not in self.spells:
      print("The spell fizzles. You don't know it.")
      return False
    if self.manabda == 0:
      print("Nothing happens. The well, from which you draw your power is dry.")
      return False

    self.manabda -= 1
    print(f"*Manabda burns. One less in the well.* Manabda left: {self.manabda}")

    min_dmg, max_dmg, dmg_type, desc = self.spell_data.get(spell_name, (1, 3, "arcane", "power lashes {target}."))




    if min_dmg == 0 and max_dmg == 0:
      print(f"{self.name} weaves: '{spell_name}'.")
      if target:
        print(desc.format(target=target.name))
      else:
        print(desc.format(target="the empty air"))
      return True

    if not target:
      print(f"{self.name} weaves '{spell_name}' but there is no target. Power dissipates.")
      return True

    dmg = random.randint(min_dmg, max_dmg)
    print(f"{self.name} weaves: '{spell_name}'!")
    print(desc.format(target=target.name))
    target.take_damage(dmg, dmg_type)
    return True

def simple_combat(player, enemy):
  print(f"\n=== COMBAT: {player.name} vs {enemy.name} ===")
  while player.is_alive() and enemy.is_alive():
    print(f"\n{player}")
    print(f"{enemy}")
    print(f"Your spells: {player.spells} | Manabda: {player.manabda}")
    action = input("Cast a spell by name, or type 'flee': ").strip()
    if action.lower() == 'flee':
      print(f"{player.name} flees.The path teaches cowardice has a price: no exp gained!")
      break
    spell_hit = player.cast_manabda(action, enemy)
    if not enemy.is_alive():
      break
    if spell_hit:
      print()
      enemy.attack(player)
      if not player.is_alive():
        break
  print("\n=== COMBAT ENDS ===")
if __name__ == "__main__":
  print("A voice, not your own, scrapes the inside of your skull: 'The ledger awakens.'")

  # --- The Ritual Begins ---
  print("The  stone terminal in front you is cold. Dark. Silent.")
  print("it waits,just a few steps in front of you,the start of your career as a true wizard,aiming to rule the path")
  print("A prompt blinks across the top of it in red letters, It wants a name.")
  player_name = input("Enter True Name: ")
  player = Wizard(name=player_name)
  print(f"\nSpellbook opens: {player.spells} | Manabda: {player.manabda}")
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
  print("a booming voice speaks in your head: he is here, you look up as the end of the words trail off into nothingness.")
  print("An older wizard stands where none stood before. He speaks no greeting.")
  print("He stares, casting a critical eye as if appraising your value... and barely nods.")
  print("He pulls a ledger from his robe. Bound in obsidian.it flips open without him making it do so,then It vanishes again.")
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
      print("\nThe ravens scatter... for now.")
      print("The man stands. Medium build, average height. Mop of messy blonde hair hides his eyes.")
      print("The woman cowers behind him. Homely. Quiet. Hands over her head.")
      print("The man does not thank you. He glares. 'You. Pathwalker. Here to rob us?'")
  elif choice_2 == "2":
    print("\nYou do not help. The wail cuts short. Silence returns.")
    print("A lesson unlearned. Manabda unspent. Is that wise?")
    print("You turn away. The mountain air feels colder.")
  elif choice_2 == "3":
    print("\nYou ignore the screams. The town below calls louder.")
    print("Your goal is to rule all wizarding kind. Not save strays.")
    print("This is why none speak of it. It is not the same world.")
  print("\nYour School stirs within you. Your choices echo.")
  print(f"Current state: {player}")