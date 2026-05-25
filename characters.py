import random
from Inventory import Inventory
from systems.status_effects import Burn

class Wizard:
  def __init__(self, name, level=1, hp=100, school="Undecided", spells=None, manabda=8, inventory=None):
    self.name = name
    self.level = level
    self.hp = hp
    self.school = school
    self.manabda = manabda
    self.spells = spells if spells is not None else []
    self.spell_data = {}
    self.inventory = inventory if inventory is not None else Inventory()
    self.status_effects = []

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

  def add_status(self, status_effect):
        self.status_effects.append(status_effect)

  def tick_status_effects(self):
    messages = []
    for effect in self.status_effects[:]:
      result = effect.tick(self)
      if result:
        messages.append(result)
      if effect.is_expired():
        self.status_effects.remove(effect)
    return "\n".join(messages)

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
    if "sort" not in self.spells:
      self.spells.append("sort")
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
    if spell_name == "Ignite" and random.random() < 0.5:
      burn = Burn(duration=3, damage_per_turn=5)
      target.add_status(burn)
      print(f"{target.name} catches fire!")
    return True

def simple_combat(player, enemy):
  print(f"\n=== COMBAT: {player.name} vs {enemy.name} ===")
  while player.is_alive() and enemy.is_alive():

    player_msgs = player.tick_status_effects()
    if player_msgs: print(player_msgs)
    if not player.is_alive(): break

    enemy_msgs = enemy.tick_status_effects()
    if enemy_msgs: print(enemy_msgs)
    if not enemy.is_alive(): break

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
