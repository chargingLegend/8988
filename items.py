class Item:
    def __init__(self, name, rarity="common", description="", value=0):
        self.name = name
        self.rarity = rarity
        self.description = description
        self.value = value

    def inspect(self):
        return f"{self.name} [{self.rarity}] — {self.description}"

    def use(self, player, context=None):
        raise NotImplementedError(f"{self.name} has no use() defined.")


class Consumable(Item):
    def __init__(self, name, rarity="common", description="", value=0):
        super().__init__(name, rarity, description, value)

    def use(self, player, context=None):
        raise NotImplementedError(f"{self.name} has no use() defined.")


class PassRune(Consumable):
    def __init__(self):
        super().__init__(
            name="Pass Rune",
            rarity="uncommon",
            description="A carved rune that negates what comes next.",
            value=40
        )

    def use(self, player, context=None):
        print("\nYou trace the Pass Rune. It crumbles to dust.")
        print("pass  # the attack finds nothing.")
        print("The strike moves through the space where you were.")
        return "negated"


class ExceptVial(Consumable):
    def __init__(self):
        super().__init__(
            name="Except Vial",
            rarity="rare",
            description="Catches you before the fall. Not a guarantee. Just a catch.",
            value=120
        )
        self.restore_percent = 0.25

    def use(self, player, context=None):
        restore = int(player.max_hp * self.restore_percent)
        player.hp = min(player.max_hp, player.hp + restore)
        print(f"\nYour vision blacks out.")
        print(f"Then — something catches.")
        print(f"A vial at your hip shatters on its own.")
        print(f"except — caught before the fall.")
        print(f"+{restore} HP restored. [{player.hp}/{player.max_hp}]")
        return True


class FinallyFlask(Consumable):
    def __init__(self):
        super().__init__(
            name="Finally Flask",
            rarity="legendary",
            description="finally — this always runs. Even after death.",
            value=500
        )

    def use(self, player, context=None):
        player.hp = player.max_hp
        player.mana = player.max_mana
        player.manabda = 8
        print(f"\nYou die.")
        print(f"For a moment there is nothing.")
        print(f"Then the Flask pulses once. Brilliant. Absolute.")
        print(f"finally — this always runs.")
        print(f"Death finds no purchase here.")
        print(f"HP: {player.hp}/{player.max_hp} | "
              f"Mana: {player.mana}/{player.max_mana} | "
              f"Manabda: {player.manabda}")
        return "resurrected"


class HPPotion(Consumable):
    TIERS = {
        "I":   {"restore": 15, "value": 20},
        "II":  {"restore": 35, "value": 45},
        "III": {"restore": 60, "value": 90},
        "IV":  {"restore": 100, "value": 200},
    }

    def __init__(self, tier="I"):
        self.tier = tier
        data = self.TIERS[tier]
        super().__init__(
            name=f"HP Potion {tier}",
            rarity="common" if tier == "I" else "uncommon",
            description=f"Restores {data['restore']} HP.",
            value=data["value"]
        )
        self.restore = data["restore"]

    def use(self, player, context=None):
        player.hp = min(player.max_hp, player.hp + self.restore)
        print(f"\n{player.name} drinks {self.name}.")
        print(f"+{self.restore} HP. [{player.hp}/{player.max_hp}]")
        return True


class ManaPotion(Consumable):
    TIERS = {
        "I":   {"restore": 10, "value": 25},
        "II":  {"restore": 25, "value": 60},
        "III": {"restore": 45, "value": 110},
        "IV":  {"restore": 70, "value": 220},
    }

    def __init__(self, tier="I"):
        self.tier = tier
        data = self.TIERS[tier]
        super().__init__(
            name=f"Mana Potion {tier}",
            rarity="common" if tier == "I" else "uncommon",
            description=f"Restores {data['restore']} Mana.",
            value=data["value"]
        )
        self.restore = data["restore"]

    def use(self, player, context=None):
        player.mana = min(player.max_mana, player.mana + self.restore)
        print(f"\n{player.name} drinks {self.name}.")
        print(f"+{self.restore} Mana. [{player.mana}/{player.max_mana}]")
        return True


class ManabdaPotion(Consumable):
    TIERS = {
        "I":   {"restore": 2, "value": 150},
        "II":  {"restore": 4, "value": 350},
        "III": {"restore": 6, "value": 700},
    }

    def __init__(self, tier="I"):
        self.tier = tier
        data = self.TIERS[tier]
        super().__init__(
            name=f"Manabda Potion {tier}",
            rarity="rare",
            description=f"Restores {data['restore']} Manabda. Handle carefully.",
            value=data["value"]
        )
        self.restore = data["restore"]

    def use(self, player, context=None):
        player.manabda = min(8, player.manabda + self.restore)
        print(f"\n{player.name} drinks {self.name}.")
        print(f"The lambda stirs. Power returns.")
        print(f"+{self.restore} Manabda. [{player.manabda}/8]")
        return True


class Equipment(Item):
    def __init__(self, name, rarity="common", description="", value=0,
                 defense_bonus=0, atk_bonus=0, mana_bonus=0):
        super().__init__(name, rarity, description, value)
        self.defense_bonus = defense_bonus
        self.atk_bonus = atk_bonus
        self.mana_bonus = mana_bonus
        self.equipped = False

    def equip(self, player):
        self.equipped = True
        player.defense += self.defense_bonus
        player.mana += self.mana_bonus
        print(f"\n{player.name} equips {self.name}.")
        if self.defense_bonus:
            print(f"+{self.defense_bonus} Defense.")
        if self.mana_bonus:
            print(f"+{self.mana_bonus} Mana.")

    def unequip(self, player):
        self.equipped = False
        player.defense -= self.defense_bonus
        player.mana -= self.mana_bonus
        print(f"\n{player.name} unequips {self.name}.")


class Cloak(Equipment):
    def __init__(self, name="Traveler's Cloak", rarity="common",
                 description="A worn cloak.", value=30,
                 defense_bonus=2):
        super().__init__(name, rarity, description, value,
                        defense_bonus=defense_bonus)


class LegendaryCloak(Cloak):
    def __init__(self, name="Cloak of Unmaking",
                 description="Light bends away from it.",
                 defense_bonus=15, value=800):
        super().__init__(name, rarity="legendary",
                        description=description,
                        value=value,
                        defense_bonus=defense_bonus)


class Staff(Equipment):
    def __init__(self, name="Gnarled Staff", rarity="common",
                 description="A basic focusing rod.", value=50,
                 defense_bonus=0, atk_bonus=2, mana_bonus=5):
        super().__init__(name, rarity, description, value,
                        defense_bonus=defense_bonus,
                        atk_bonus=atk_bonus,
                        mana_bonus=mana_bonus)


class Rod(Equipment):
    def __init__(self, name="Apprentice Rod", rarity="common",
                 description="Channels raw mana cleanly.", value=40,
                 mana_bonus=3):
        super().__init__(name, rarity, description, value,
                        mana_bonus=mana_bonus)


class Scepter(Equipment):
    def __init__(self, name="Iron Scepter", rarity="uncommon",
                 description="Authority made physical.", value=120,
                 defense_bonus=3, atk_bonus=3, mana_bonus=3):
        super().__init__(name, rarity, description, value,
                        defense_bonus=defense_bonus,
                        atk_bonus=atk_bonus,
                        mana_bonus=mana_bonus)