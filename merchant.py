from items import HPPotion, ManaPotion, PassRune, Cloak, ExceptVial
from combat import simple_combat


class Merchant:
  def __init__(self, name, faction="Neutral", gold=0):
    self.name = name
    self.faction = faction
    self.gold = gold
    self.stock = []

  def build_stock(self):
    raise NotImplementedError("Each merchant must define their own stock.")

  def greet(self, player):
    raise NotImplementedError("Each merchant must define their own greeting.")

  def show_stock(self, player):
    raise NotImplementedError("Each merchant must define their own stock display.")

  def buy(self, player, choice):
    raise NotImplementedError("Each merchant must define their own buy logic.")

  def shop(self, player):
    raise NotImplementedError("Each merchant must define their own shop loop.")


class Maren(Merchant):
  def __init__(self):
    super().__init__(
      name="Maren",
      faction="Neutral",
      gold=0
    )
    self.build_stock()

  def build_stock(self):
    self.stock = [
      {
        "item": HPPotion("I"),
        "price": 20,
        "flavor": (
          "She slides a small vial across the counter without looking up.\n"
          "'Keeps you standing. Nothing more, nothing less.'\n"
          "(HP Potion I — restores 15 HP.)"
        )
      },
      {
        "item": ManaPotion("I"),
        "price": 25,
        "flavor": (
          "She glances at your palm. At the mark there.\n"
          "'For the well. When it runs low.' A pause. 'And it will.'\n"
          "(Mana Potion I — restores 10 Mana.)"
        )
      },
      {
        "item": PassRune(),
        "price": 40,
        "flavor": (
          "She holds it up briefly. A carved stone. Worn smooth on one side.\n"
          "'Sometimes... the smartest thing a person can do...'\n"
          "She sets it down. '...is simply not be there.'\n"
          "(Pass Rune — negates one incoming attack. Single use.)"
        )
      },
      {
        "item": Cloak(),
        "price": 30,
        "flavor": (
          "She nods toward a folded cloak on the shelf behind her.\n"
          "'Mended it myself. Twice.' Her hands don't shake when she says it.\n"
          "'Belonged to someone who thought they didn't need it.'\n"
          "She doesn't say what happened to them.\n"
          "(Traveler's Cloak — +2 Defense when equipped.)"
        )
      },
      {
        "item": ExceptVial(),
        "price": 120,
        "flavor": (
          "She reaches beneath the counter. Sets it down slowly.\n"
          "A small vial. The liquid inside moves like it's alive.\n"
          "'This one... I've had it a long time. Never needed it.'\n"
          "A breath. 'Almost did. Once.'\n"
          "'Something catches you before the fall. Don't ask me how.'\n"
          "She looks at you directly for the first time.\n"
          "'Don't waste it.'\n"
          "(Except Vial — restores 25% HP automatically when you drop to critical. Single use.)"
        )
      },
    ]

  def greet(self, player):
    if player.flags.get('enforcer_aligned'):
      print(f"\nThe old woman looks up from behind the counter.")
      print(f"Her face settles into something careful. Neutral.")
      print(f"'What do you need.'")
      print(f"Not a question. A transaction waiting to happen.")
    else:
      print(f"\nAn elderly woman stands behind a worn counter.")
      print(f"Her back is curved like something heavy has lived on it a long time.")
      print(f"She doesn't look up when you enter.")
      print(f"Then she does. Something shifts in her eyes.")
      print(f"She glances past you at the door. Then back.")
      print(f"'Pathwalker.' Her voice drops to almost nothing.")
      print(f"'Haven't seen one in...' She stops herself.")
      print(f"'Never mind. Come closer. I don't bite.'")
      print(f"She almost smiles. Almost.")
      if not player.flags.get('maren_spoke_freely'):
        print(f"\nShe leans forward. Eyes at the door again.")
        print(f"'You've seen them out there. The ones with the batons.'")
        print(f"'Good work, they call it.' She straightens a jar that doesn't need straightening.")
        print(f"'Good for someone, I'm sure. Just... never quite clear who.'")
        print(f"She meets your eyes. Holds them.")
        print(f"'You didn't hear that from me.'")
        player.flags['maren_spoke_freely'] = True

  def show_stock(self, player):
    discount = player.flags.get('enforcer_aligned', False)
    print(f"\n--- Maren's Wares ---")
    for i, entry in enumerate(self.stock):
      item = entry["item"]
      price = entry["price"] // 2 if discount else entry["price"]
      print(f"\n{i + 1}. {item.name} — {price} gold")
      print(f"   {entry['flavor']}")
    print(f"\n{len(self.stock) + 1}. Leave")
    if hasattr(player, 'gold'):
      print(f"\nYour gold: {player.gold}")

  def buy(self, player, choice):
    discount = player.flags.get('enforcer_aligned', False)
    if choice < 1 or choice > len(self.stock):
      print("She watches you. Waits.")
      return False
    entry = self.stock[choice - 1]
    item = entry["item"]
    price = entry["price"] // 2 if discount else entry["price"]
    if not hasattr(player, 'gold'):
      print("You have no gold.")
      return False
    if player.gold < price:
      print(f"\nShe glances at your hands.")
      print(f"'Not enough.' No judgment in it. Just fact.")
      return False
    try:
      player.inventory.add(item)
      player.gold -= price
      print(f"\nShe slides {item.name} across the counter.")
      if not player.flags.get('enforcer_aligned'):
        print(f"'Take care of yourself out there.'")
        print(f"'Vardeth...' She shakes her head slightly.")
        print(f"'It has a way of making people forget they ever had a choice.'")
      print(f"Gold remaining: {player.gold}")
      return True
    except OverflowError:
      print(f"\n'You're carrying too much already.' She pulls it back.")
      return False

  def shop(self, player):
    if not player.flags.get('paid_tithe') and not player.flags.get('enforcer_aligned'):
      print(f"\nShe looks at you carefully.")
      print(f"'You haven't paid tithe.' Not an accusation. A warning.")
      print(f"\nShe reaches beneath the counter.")
      print(f"Sets something down slowly. A small device.")
      print(f"Worn leather straps. A thin needle. Tubes leading to a dark bag.")
      print(f"The bag has seen use. Too much use.")
      print(f"'I don't ask about the square.' Her voice is barely anything.")
      print(f"'I don't report. I just...' She taps the device once.")
      print(f"'It's the only way I can help you. Safely.'")
      print(f"\n'It takes something from you. It always does.'")
      print(f"(Private tithe collection — costs 2 Mana and 2 Manabda)")
      print(f"\nYour Mana: {player.mana}/{player.max_mana} | Manabda: {player.manabda}/8")
      print(f"\n[1: Submit to the device]")
      print(f"[2: Refuse. Walk away.]")
      choice = input("Choose: ").strip()

      if choice == "1":
        if player.mana < 2 or player.manabda < 2:
          print(f"\nShe watches the device. Watches you.")
          print(f"'There's... not enough.' She says it gently.")
          print(f"'Come back when you're stronger.'")
          print(f"She puts the device away. Carefully.")
          return
        player.mana -= 2
        player.manabda -= 2
        print(f"\nYou strap your hand in. The needle finds its place.")
        print(f"A thin line of red travels down the tube. Into the bag.")
        print(f"She watches it. Not with pleasure. Never with pleasure.")
        print(f"'Done.' She unbuckles the strap herself. Doesn't make you do it.")
        print(f"She tucks the device away without looking at it.")
        print(f"'I'm sorry.' Barely a whisper. 'For what it's worth.'")
        print(f"Mana: {player.mana}/{player.max_mana} | Manabda: {player.manabda}/8")
        player.flags['paid_tithe_maren'] = True
        self.greet(player)
      else:
        print(f"\nShe nods. Puts the device away.")
        print(f"'I understand.' And she means it.")
        print(f"'Be careful out there.'")
        print(f"She turns back to her counter. The conversation is over.")
        return

    else:
      self.greet(player)

    while True:
      self.show_stock(player)
      try:
        choice = int(input("\nChoose [number]: ").strip())
      except ValueError:
        print("She waits patiently.")
        continue

      if choice == len(self.stock) + 1:
        print(f"\nShe nods as you turn to leave.")
        if not player.flags.get('enforcer_aligned'):
          print(f"'Watch the grates in the floor out there.'")
          print(f"'And... don't linger near them.'")
          print(f"She says nothing else. She doesn't have to.")
        break

      self.buy(player, choice)

  def on_attack(self, player):
    print(f"\nMaren stumbles backward. Knocks over a jar.")
    print(f"She doesn't scream. She just looks at you.")
    print(f"'I see.' Quiet. Resigned. Like she always knew.")
    print(f"\nThe door bursts open. Two Enforcers fill the frame.")
    print(f"'Pathwalker. Step away from the merchant.'")
    print(f"'Or don't.' The batons crackle.")
    from entities.humanoid import Enforcer
    enforcer1 = Enforcer("Town Enforcer")
    enforcer2 = Enforcer("Town Enforcer")
    simple_combat(player, enforcer1)
    if player.is_alive():
      simple_combat(player, enforcer2)
    if player.is_alive():
      print(f"\nMaren is gone. Slipped out while you fought.")
      print(f"The counter is empty. The Except Vial with it.")
      print(f"Some doors don't open twice.")
      player.flags['maren_gone'] = True