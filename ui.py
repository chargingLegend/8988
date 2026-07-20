import builtins

_lines_since_pause = 0
PAGE_HEIGHT = 25

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
  answer = builtins.input(prompt)
  while answer.strip() == "":
    answer = builtins.input(prompt)
  return answer