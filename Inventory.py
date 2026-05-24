class Inventory:
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
    raise ValueError(f"{item} not in Inventory.")

  def __str__(self):
    if not self.items:
      return "Inventory is empty."
    return "Inventory: "+", ".join(self.items)