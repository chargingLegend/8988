import random
from characters import Wizard, simple_combat


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