from items import (Item, Consumable, Equipment, HPPotion, ManaPotion,
  ManabdaPotion, PassRune, ExceptVial, FinallyFlask,
  Cloak, Staff, Rod, Scepter)

class Inventory:
  def __init__(self) -> None:
    self.items: list = []
    self.max_size: int = 12

  def add(self, item) -> str:
    if len(self.items) >= self.max_size:
      raise OverflowError("Inventory full, can't carry anymore!")
    self.items.append(item)
    name = item.name if hasattr(item, 'name') else item
    return f"Added {name} to inventory"

  def remove(self, item_name: str) -> str:
    for item in self.items:
      target = item.name if hasattr(item, 'name') else item
      if target == item_name:
        self.items.remove(item)
        return f"Used {item_name}."
    raise ValueError(f"{item_name} not in Inventory.")

  def get_item(self, item_name: str):
    for item in self.items:
      target = item.name if hasattr(item, 'name') else item
      if target == item_name:
        return item
    return None

  def has_item(self, item_name: str) -> bool:
    return self.get_item(item_name) is not None

  def get_consumables(self):
    return [i for i in self.items if isinstance(i, Consumable)]

  def get_equipment(self):
    return [i for i in self.items if isinstance(i, Equipment)]

  def __str__(self) -> str:
    if not self.items:
      return "Inventory is empty."
    lines = []
    for item in self.items:
      if hasattr(item, 'rarity'):
        lines.append(f"  - {item.name} [{item.rarity}]")
      else:
        lines.append(f"  - {item}")
    return f"Inventory ({len(self.items)}/{self.max_size}):\n" + "\n".join(lines)

  def __repr__(self) -> str:
    return f"Inventory({len(self.items)}/{self.max_size})"