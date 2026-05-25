class Inventory:
  def __init__(self) -> None:
    self.items: list[str] = []
    self.max_size: int = 12

  def add(self, item: str) -> str:
    if len(self.items) >= self.max_size:
      raise OverflowError("Inventory full, cant carry anymore!")
    self.items.append(item)
    return f"Added {item} to inventory"

  def remove(self, item: str) -> str:
    if item in self.items:
      self.items.remove(item)
      return f"Used {item}."
    raise ValueError(f"{item} not in Inventory.")

  def __str__(self) -> str:
    if not self.items:
      return "Inventory is empty."
    return "Inventory: "+", ".join(self.items)

  def __repr__(self) -> str:
    return f"Inventory({len(self.items)}/{self.max_size}"