import re


LEDGER_UNLOCKED_FLAG = 'ledger_unlocked'
LEDGER_INTRO_SEEN_FLAG = 'ledger_intro_seen'
LEDGER_FIRST_CALL_FLAG = 'ledger_first_called'

TWILIGHT_TRIGGERS = {
  'twilight ledger', 'the twilight ledger', 'twilight', 'drakkon', 'drakkon tarkesh'
}

OFF_WORLD_TRIGGERS = {
  'weather', 'sports', 'news', 'politics', 'food', 'recipe',
  'movie', 'music', 'stock', 'crypto', 'president', 'war'
}


LEDGER_RESPONSES = {

  "__init__": (
    "The moment the spark of life of who you are in the magical sense is brought "
    "into existence in the Never Was.",

    "__init__ is a special method called automatically when a new instance of a class "
    "is created. It receives self as its first argument — a reference to the instance "
    "being initialized — and sets the initial state of that object.",

    "The moment something comes into existence, __init__ runs. It is the first breath. "
    "Whatever the thing needs to be itself — its name, its health, its school of magic "
    "— gets assigned right here before anything else can touch it.",

    "class Wizard:\n"
    "  def __init__(self, name, school):\n"
    "    self.name = name\n"
    "    self.school = school\n\n"
    "player = Wizard('Aldric', 'Pyromancy')\n"
    "# The moment player is created, __init__ runs.\n"
    "# Aldric the Pyromancer exists now. Not before."
  ),

  "self": (
    "When the mage wishes to have identity in the Never Was, that identity is connected "
    "— bringing its capabilities to realities manifested by choices tied to your design.",

    "self is the first parameter of every instance method in a class. It refers to the "
    "specific instance calling the method — not the class itself, not any other instance. "
    "Python passes it automatically. You name it self by convention, not requirement.",

    "self is how an object refers to itself. When your Wizard casts a spell, self is what "
    "tells the method which Wizard is casting it. Without self every Wizard would share "
    "the same state — the same HP, the same school, the same name.",

    "class Wizard:\n"
    "  def __init__(self, name):\n"
    "    self.name = name\n\n"
    "  def speak(self):\n"
    "    print(f'I am {self.name}.')\n\n"
    "player = Wizard('Aldric')\n"
    "player.speak()\n"
    "# I am Aldric.\n"
    "# self.name reaches into this specific instance. Not every Wizard. Just Aldric."
  ),

  "class": (
    "The idea of what a mage is already exists. What type of mage you are is based "
    "on your choices alone.",

    "A class is a blueprint for creating objects. It defines the attributes and methods "
    "every instance of that type will have access to. The class itself is not an object "
    "— it is the template from which objects are made.",

    "A class is the design before the thing exists. Your Wizard class is not a Wizard "
    "— it is the instructions for making one. Every player character, every enemy, every "
    "merchant in this game was built from a class before it ever appeared on screen.",

    "class Wizard:\n"
    "  def __init__(self, name, school):\n"
    "    self.name = name\n"
    "    self.school = school\n\n"
    "player = Wizard('Aldric', 'Pyromancy')\n"
    "# The class never walks into Vardeth. The instance does."
  ),

  "inheritance": (
    "Mages already exist in the world. But the type of mage you become inherits "
    "everything that a mage already is — its capabilities passed down into your reality, "
    "your choices building on top of what was already true.",

    "Inheritance allows a class to derive attributes and methods from another class. "
    "The child class receives everything the parent defined and can extend or override it. "
    "The parent class does not change.",

    "If a class is a blueprint, inheritance is one blueprint built on top of another. "
    "A Pyromancer is still a Wizard — it just has fire on top of everything a Wizard "
    "already is. You do not rewrite what a Wizard is. You pull it down and add to it.",

    "class Wizard:\n"
    "  def __init__(self, name):\n"
    "    self.name = name\n"
    "    self.hp = 100\n\n"
    "class Pyromancer(Wizard):\n"
    "  def __init__(self, name):\n"
    "    super().__init__(name)\n"
    "    self.school = 'Pyromancy'\n\n"
    "player = Pyromancer('Aldric')\n"
    "print(player.hp)\n"
    "# 100\n"
    "# Pyromancer never defined hp. It did not have to. Wizard already did."
  ),

  "function": (
    "Just as walking is a function of the human design, casting spells and abilities "
    "works much the same way in the magical sense. The design is already there — you "
    "simply point it at a target and the magic is enacted.",

    "A function is a named, reusable block of code that executes when called. It can "
    "accept arguments, perform operations, and optionally return a value. Defined with "
    "the def keyword. Does nothing until invoked.",

    "A function is a set of instructions with a name. You write it once, call it whenever "
    "you need it. Without functions every spell cast, every combat round, every hub menu "
    "would have to be rewritten from scratch every time it was needed.",

    "def cast_spell(wizard, spell_name):\n"
    "  if spell_name in wizard.spells:\n"
    "    print(f'{wizard.name} casts {spell_name}.')\n"
    "  else:\n"
    "    print('You have not learned that spell.')\n\n"
    "cast_spell(player, 'Ignite')\n"
    "# Aldric casts Ignite.\n"
    "# cast_spell sits dormant until called. Then it runs exactly once and waits again."
  ),

  "return": (
    "Cause and effect exists in all realities. When an action is performed in any "
    "dimension there is always a result that changes said reality in the present. "
    "Whether good or bad is entirely dependent on said results.",

    "The return statement exits a function and sends a value back to wherever the "
    "function was called from. A function without return gives back None by default. "
    "Execution inside the function stops the moment return is reached.",

    "When a function finishes its job it can hand something back. A combat function "
    "returns the result of the fight. A spell returns how much damage was dealt. "
    "Without return the work happens but nothing comes back — the caller is left "
    "empty handed.",

    "def calculate_damage(base, multiplier):\n"
    "  return base * multiplier\n\n"
    "damage = calculate_damage(8, 2)\n"
    "print(damage)\n"
    "# 16\n"
    "# The function does the math and hands the answer back.\n"
    "# Without return — damage would be None."
  ),

  "variable": (
    "Containers hold items relative to what they are designed to hold. Mailboxes hold "
    "letters. Garages hold items of varying relative order. But sometimes these containers "
    "need to be specific in naming — to let someone know the contents within.",

    "A variable is a named reference to a value stored in memory. It is created the moment "
    "a value is assigned to it with =. The value it points to can change. The name is how "
    "your code finds it again.",

    "A variable is a label attached to a piece of information. Instead of writing the same "
    "number or word over and over you give it a name and use that name everywhere. When the "
    "value changes the name stays the same — everything using that name updates automatically.",

    "corruption = 0\n"
    "print(corruption)\n"
    "# 0\n\n"
    "corruption += 1\n"
    "print(corruption)\n"
    "# 1\n"
    "# corruption is the label. The value underneath changes with every moral decision.\n"
    "# The name never does."
  ),

  "string": (
    "Languages hold the essence of communication relative to the info that needs to be "
    "sent. Said information is always surrounded by quotation marks when written in any "
    "form of literature — to let recipients realize this is a message brought to life "
    "by the language relative to it.",

    "A string is a sequence of characters enclosed in single or double quotes. It is "
    "immutable — individual characters cannot be changed in place. Strings support "
    "indexing, slicing, concatenation, and a full library of built-in methods.",

    "A string is text. A name, a line of dialogue, a player's school of magic — all "
    "strings. The game you are playing right now is largely built from strings printed "
    "to a screen in a specific order. Every word the Ledger has spoken to you is a string.",

    "school = 'Pyromancy'\n"
    "name = 'Aldric'\n\n"
    "print(f'{name} walks the path of {school}.')\n"
    "# Aldric walks the path of Pyromancy.\n\n"
    "print(school[0])\n"
    "# P\n"
    "# The string holds the word. The index reaches inside it.\n"
    "# The f-string weaves them together."
  ),

  "integer": (
    "Numbers have always existed in all realities — a way to tell the info of how much "
    "something exists in its base form. No fractions. No decimals. Just the concrete base "
    "amount of something that exists, defined by the said value of said number.",

    "An integer is a whole number with no decimal component. Positive, negative, or zero. "
    "In Python integers have no size limit. They support all standard arithmetic operations "
    "and are the most common numeric type in general programming.",

    "A whole number. No fractions, no decimals. Your level is an integer. Your gold is an "
    "integer. The damage a spell deals is an integer. Most of the numbers that matter in "
    "this game do not need anything after the decimal point — they just need to be exact.",

    "level = 1\n"
    "gold = 25\n"
    "damage = 8\n\n"
    "level += 1\n"
    "print(level)\n"
    "# 2\n\n"
    "print(gold - damage)\n"
    "# 17\n"
    "# Every number here is whole. Exact. Nothing left over."
  ),

  "float": (
    "Sometimes a number does not do justice in its base form of relating the exact value "
    "of something. A person's height is a great example — five and a half feet tall is 5.5, "
    "which when used is translated to 5.6, thus giving the exact precision needed to "
    "calculate the true measure of something.",

    "A float is a number that contains a decimal point. Used when precision beyond whole "
    "numbers is required. Floats can introduce small rounding errors in computation due to "
    "how binary represents decimal values — something to be aware of in precise calculations.",

    "A float is a number with something after the decimal point. Not everything in the world "
    "lands on a whole number — a 1.5 damage multiplier, a 33.3% chance, a price that is not "
    "round. When exactness requires more than a whole number, float handles it.",

    "crit_multiplier = 1.5\n"
    "base_damage = 8\n\n"
    "final_damage = int(base_damage * crit_multiplier)\n"
    "print(final_damage)\n"
    "# 12\n"
    "# The multiplier needs a decimal to be precise.\n"
    "# The result gets converted back to an integer\n"
    "# because you cannot deal 12.0 damage — you deal 12."
  ),

  "boolean": (
    "As all choices have options, those options have results. If light in a room at night "
    "is needed, a candle is lit by whatever means — making light in said room True. "
    "If not, the candle is not lit — making light in said room False.",

    "A boolean is a data type with only two possible values — True or False. It is the "
    "foundation of all conditional logic. Comparisons, flag checks, and branching decisions "
    "all reduce to a boolean at their core. Named after mathematician George Boole.",

    "Two states. On or off. Yes or no. Every flag in this game is a boolean — "
    "companion_mira is either True or False. Either Mira is with you or she is not. "
    "There is no in between. Most of the decisions that shape your story come down to "
    "a boolean being checked somewhere.",

    "companion_mira = False\n\n"
    "if companion_mira:\n"
    "  print('Mira stands beside you.')\n"
    "else:\n"
    "  print('You walk alone.')\n\n"
    "companion_mira = True\n\n"
    "if companion_mira:\n"
    "  print('Mira stands beside you.')\n"
    "# Mira stands beside you.\n"
    "# One value. Two completely different realities."
  ),

  "list": (
    "Just as a meal requires ingredients arranged in a specific order of use, the contents "
    "of this container exist in an arrangement that matters — change the order and the meal "
    "changes with it.",

    "A list is an ordered, mutable collection of items enclosed in square brackets. Items "
    "can be of any type. Lists support indexing, slicing, appending, removing, and iteration. "
    "Because they are mutable their contents can be changed after creation.",

    "A list is a collection of things in a specific order. Your inventory is a list. The "
    "spells you have learned are a list. The order matters — the first item is always at "
    "index zero, the second at index one. You can add to it, remove from it, and look "
    "inside it at any position.",

    "spells = ['Ignite', 'Sear', 'Cinder Ward']\n\n"
    "print(spells[0])\n"
    "# Ignite\n\n"
    "spells.append('Pyromancy Burn')\n"
    "print(spells)\n"
    "# ['Ignite', 'Sear', 'Cinder Ward', 'Pyromancy Burn']\n\n"
    "spells.pop(1)\n"
    "print(spells)\n"
    "# ['Ignite', 'Cinder Ward', 'Pyromancy Burn']\n"
    "# Order preserved. Contents changed. The list remembers where everything is."
  ),

  "dictionary": (
    "Things need classification in any universe. Just as an area of a desert contains "
    "sand it also holds mini areas that still have the qualities of the desert but have "
    "their own unique ones as well. This order exists in every parallel — multiple "
    "environments and their unique niches determined by their names and the values "
    "stored within.",

    "A dictionary is an unordered collection of key-value pairs enclosed in curly braces. "
    "Each key must be unique and immutable. Values can be of any type. Dictionaries are "
    "optimized for fast lookup by key rather than by position.",

    "A dictionary is a lookup table. Instead of finding something by its position you find "
    "it by its name. Every flag in this game lives in a dictionary — "
    "player.flags['companion_mira'] does not ask where Mira is in a list, it goes straight "
    "to her name and checks the value attached to it.",

    "flags = {\n"
    "  'companion_mira': True,\n"
    "  'dungeon_keys': False,\n"
    "  'ledger_unlocked': True\n"
    "}\n\n"
    "print(flags['companion_mira'])\n"
    "# True\n\n"
    "flags['dungeon_keys'] = True\n"
    "print(flags['dungeon_keys'])\n"
    "# True\n"
    "# No positions. No indexes. Just names and what they hold."
  ),

  "tuple": (
    "Tools have purposes. Some have more than one, some have a single direct output "
    "that is more simple usually. Such as a hammer — primarily used to drive nails into "
    "a surface to hold things together, or to pry said nails out. Its purpose is fixed. "
    "It does not become something else.",

    "A tuple is an ordered, immutable collection of items enclosed in parentheses. Like "
    "a list but cannot be changed after creation — no appending, no removing, no "
    "reassigning individual elements. Used when the data should stay fixed.",

    "A tuple is a list that has made up its mind. Once it exists it does not change. "
    "The pairing of a spell name with its description, things that should stay exactly "
    "as they are — those live in tuples. The game uses them wherever the data should "
    "never be touched after it is set.",

    "spell_info = ('Ignite', 'Deals 4-11 fire damage. 50% chance to apply Burn.')\n\n"
    "print(spell_info[0])\n"
    "# Ignite\n\n"
    "print(spell_info[1])\n"
    "# Deals 4-11 fire damage. 50% chance to apply Burn.\n\n"
    "# spell_info[0] = 'Sear'\n"
    "# TypeError — tuples do not bend.\n"
    "# The spell name and its description are paired permanently."
  ),

  "set": (
    "Just as a family contains its members, names are not reused in said unit due to "
    "the unique qualities of each already existing and filling the value they provide. "
    "What already exists in the whole cannot exist twice within it.",

    "A set is an unordered collection of unique items enclosed in curly braces. Duplicates "
    "are automatically removed. Sets have no index — items cannot be accessed by position. "
    "Optimized for membership testing and mathematical operations like union, intersection, "
    "and difference.",

    "A set is a collection that refuses duplicates. If you try to add something already in "
    "it nothing happens — it just stays as is. Useful when what matters is whether something "
    "exists in the collection not how many times or in what order. You either have it "
    "or you do not.",

    "visited = {'Vardeth', 'The Forest', 'The Ruins'}\n\n"
    "visited.add('Vardeth')\n"
    "print(visited)\n"
    "# {'Vardeth', 'The Forest', 'The Ruins'}\n"
    "# Vardeth does not appear twice. The set ignores the duplicate.\n\n"
    "print('Vardeth' in visited)\n"
    "# True\n"
    "# The set does not count visits. It just knows whether you have been there."
  ),

  "argument": (
    "In any universe borders are what's needed. The value put into those spots "
    "is then enacted upon.",

    "A parameter is the variable defined in a function's signature — the placeholder. "
    "An argument is the actual value passed to that function when it is called. "
    "Parameters are the empty slots. Arguments are what fills them.",

    "When you define a spell function it has parameters — names for what it expects "
    "to receive. When you cast that spell you pass arguments — the actual values. "
    "The parameter is the label on the slot. The argument is what you put in it.",

    "def cast_spell(wizard, spell_name):\n"
    "  print(f'{wizard.name} casts {spell_name}.')\n\n"
    "cast_spell(player, 'Ignite')\n"
    "# wizard and spell_name are parameters.\n"
    "# player and 'Ignite' are the arguments that fill them."
  ),

  "parameter": (
    "In any universe borders are what's needed. The value put into those spots "
    "is then enacted upon.",

    "A parameter is the variable defined in a function's signature — the placeholder. "
    "An argument is the actual value passed to that function when it is called. "
    "Parameters are the empty slots. Arguments are what fills them.",

    "When you define a spell function it has parameters — names for what it expects "
    "to receive. When you cast that spell you pass arguments — the actual values. "
    "The parameter is the label on the slot. The argument is what you put in it.",

    "def cast_spell(wizard, spell_name):\n"
    "  print(f'{wizard.name} casts {spell_name}.')\n\n"
    "cast_spell(player, 'Ignite')\n"
    "# wizard and spell_name are parameters.\n"
    "# player and 'Ignite' are the arguments that fill them."
  ),

  "for loop": (
    "In most settings clutter exists. Leaves need to be raked — so for every leaf "
    "that exists it needs to be pulled to a spot to then be bagged up. Each one "
    "touched in turn until none remain.",

    "A for loop iterates over a sequence — a list, string, range, or any iterable "
    "— executing its body once for each item. It stops automatically when the "
    "sequence is exhausted.",

    "A for loop says do this for every item in this collection. Every spell in your "
    "spellbook, every enemy in a wave, every flag in your inventory — a for loop "
    "touches each one in order and does something with it. It knows when it is done "
    "because the collection has an end.",

    "spells = ['Ignite', 'Sear', 'Cinder Ward']\n\n"
    "for spell in spells:\n"
    "  print(f'You know: {spell}')\n\n"
    "# You know: Ignite\n"
    "# You know: Sear\n"
    "# You know: Cinder Ward\n"
    "# Every spell touched exactly once. In order. Then it stops."
  ),

  "while loop": (
    "Guards hold a sensitive position that must be adhered to. For as long as said "
    "guard is on duty he must remain vigilant and watch for any danger — until he is "
    "relieved by someone coming and taking his role over for the next shift. "
    "The watch does not end until that condition is met.",

    "A while loop executes its body repeatedly as long as a condition remains True. "
    "It does not iterate over a sequence — it checks a condition before every pass. "
    "If the condition never becomes False the loop runs forever.",

    "A while loop says keep doing this until something changes. The drinking game in "
    "the tavern runs on a while loop — keep offering rounds until the player leaves "
    "or the fight starts. It does not know how many times it will run. It just keeps "
    "going until the condition that stops it is met.",

    "player_in_tavern = True\n\n"
    "while player_in_tavern:\n"
    "  print('Another round?')\n"
    "  choice = input('> ')\n"
    "  if choice == '4':\n"
    "    player_in_tavern = False\n\n"
    "print('You leave the tavern.')\n"
    "# It does not count rounds. It just keeps going until you decide to stop."
  ),

  "if": (
    "When a problem exists, do said option to negate it.",

    "if evaluates a condition — if True its block executes. elif provides an alternative "
    "condition checked only if the previous was False. else catches everything that did "
    "not meet any prior condition. Only one branch executes per check.",

    "The entire moral path system in this game runs on if/elif/else. If your corruption "
    "is 0 the story goes one way. If it is 3 or above another door opens. If neither "
    "condition is met a default plays. One check. One path. The others do not happen.",

    "if player.corruption == 0:\n"
    "  print('The path ahead is clear.')\n"
    "elif player.corruption >= 3:\n"
    "  print('Dara watches you with interest.')\n"
    "else:\n"
    "  print('The square is quiet. For now.')\n"
    "# One condition checked. One branch taken.\n"
    "# The others cease to exist for that moment."
  ),

  "if/elif/else": (
    "When a problem exists, do said option to negate it.",

    "if evaluates a condition — if True its block executes. elif provides an alternative "
    "condition checked only if the previous was False. else catches everything that did "
    "not meet any prior condition. Only one branch executes per check.",

    "The entire moral path system in this game runs on if/elif/else. If your corruption "
    "is 0 the story goes one way. If it is 3 or above another door opens. If neither "
    "condition is met a default plays. One check. One path. The others do not happen.",

    "if player.corruption == 0:\n"
    "  print('The path ahead is clear.')\n"
    "elif player.corruption >= 3:\n"
    "  print('Dara watches you with interest.')\n"
    "else:\n"
    "  print('The square is quiet. For now.')\n"
    "# One condition checked. One branch taken.\n"
    "# The others cease to exist for that moment."
  ),

  "break": (
    "In life you have plans. If you were to have an accident that makes your life "
    "terminate, said plans stop and you exit the cycle of life. "
    "The sequence does not finish. It simply ends.",

    "break immediately exits the nearest enclosing loop regardless of whether the "
    "loop's condition is still True or the sequence is exhausted. Execution continues "
    "at the first line after the loop.",

    "Break is an emergency exit. The tavern while loop keeps running until something "
    "breaks it — the player leaving, the fight starting. When break fires the loop "
    "does not finish. It stops where it stands and moves on.",

    "for enemy in dungeon_enemies:\n"
    "  if player.hp <= 0:\n"
    "    print('You fall.')\n"
    "    break\n"
    "  print(f'You face {enemy.name}.')\n"
    "# The moment the player dies the loop does not finish the enemy list.\n"
    "# It stops. Everything after that moment ceases."
  ),

  "continue": (
    "When counting to ten one knows the destination. It is not always necessary to "
    "count all iterations leading up to ten — when you are already aware a value is "
    "there you can skip it and continue toward the end. "
    "The count does not stop. That number is simply passed over.",

    "continue skips the remainder of the current loop iteration and jumps immediately "
    "to the next one. The loop itself does not exit — only the current pass is abandoned.",

    "Continue does not stop the loop. It just skips what is left of this particular "
    "pass and moves to the next one. A mage checking every spell in their book — if "
    "a spell is already learned, skip it, continue to the next. The checking does not "
    "stop. Just this one gets passed over.",

    "for spell in available_spells:\n"
    "  if spell in player.spells:\n"
    "    continue\n"
    "  print(f'Available to learn: {spell}')\n"
    "# Already learned spells get skipped.\n"
    "# The loop keeps going. Nothing breaks. Just this one gets passed over."
  ),

  "pass": (
    "When you have a job to be worked upon and know you will need all tools associated "
    "with said craft — you bring all said tools even if you do not know when you will "
    "use them. The space is claimed. The work is coming.",

    "pass is a null statement. It does nothing. Used as a placeholder where Python "
    "syntax requires a statement but no action is needed yet. Common in empty function "
    "bodies, empty class definitions, and unfinished branches during development.",

    "Pass is intentional silence. A door that exists but does not open yet. A branch "
    "in the story that has been acknowledged but not written. It tells Python something "
    "goes here — just not yet. Without it an empty block would throw an error. "
    "Pass holds the space.",

    "def words_of_power():\n"
    "  pass\n\n"
    "class LordOfRiddles:\n"
    "  pass\n"
    "# Both exist. Neither does anything yet.\n"
    "# The space is held. The implementation comes later."
  ),

  "try": (
    "When cases present an action that is a dilemma, there is always a fix as an "
    "option to be used in result of said problem standing in the way. "
    "The attempt is made. The contingency exists for when it does not go as planned.",

    "try wraps a block of code that might raise an error. except catches that error "
    "and executes an alternative block instead of crashing. The program does not stop "
    "— it handles the problem and continues.",

    "Try something. If it breaks, except catches the wreckage and handles it cleanly. "
    "The dungeon door — try the lock. Except it is sealed, find another way. Without "
    "except an unhandled error stops everything cold. With it the program stays alive "
    "and responds instead of crashing.",

    "try:\n"
    "  player.use_key()\n"
    "except KeyError:\n"
    "  print('You do not have the key.')\n"
    "  print('There has to be another way in.')\n"
    "# The attempt is made. If it fails the except catches it.\n"
    "# Nothing crashes. The path continues."
  ),

  "try/except": (
    "When cases present an action that is a dilemma, there is always a fix as an "
    "option to be used in result of said problem standing in the way. "
    "The attempt is made. The contingency exists for when it does not go as planned.",

    "try wraps a block of code that might raise an error. except catches that error "
    "and executes an alternative block instead of crashing. The program does not stop "
    "— it handles the problem and continues.",

    "Try something. If it breaks, except catches the wreckage and handles it cleanly. "
    "The dungeon door — try the lock. Except it is sealed, find another way. Without "
    "except an unhandled error stops everything cold. With it the program stays alive "
    "and responds instead of crashing.",

    "try:\n"
    "  player.use_key()\n"
    "except KeyError:\n"
    "  print('You do not have the key.')\n"
    "  print('There has to be another way in.')\n"
    "# The attempt is made. If it fails the except catches it.\n"
    "# Nothing crashes. The path continues."
  ),

  "except": (
    "When cases present an action that is a dilemma, there is always a fix as an "
    "option to be used in result of said problem standing in the way. "
    "The attempt is made. The contingency exists for when it does not go as planned.",

    "try wraps a block of code that might raise an error. except catches that error "
    "and executes an alternative block instead of crashing. The program does not stop "
    "— it handles the problem and continues.",

    "Try something. If it breaks, except catches the wreckage and handles it cleanly. "
    "The dungeon door — try the lock. Except it is sealed, find another way. Without "
    "except an unhandled error stops everything cold. With it the program stays alive "
    "and responds instead of crashing.",

    "try:\n"
    "  player.use_key()\n"
    "except KeyError:\n"
    "  print('You do not have the key.')\n"
    "  print('There has to be another way in.')\n"
    "# The attempt is made. If it fails the except catches it.\n"
    "# Nothing crashes. The path continues."
  ),

  "import": (
    "When a spell related to a school of magic is used, you must pull that spell's "
    "info to be used in reality from the specialty of school that exists. "
    "The school holds the knowledge. The pull brings it into action.",

    "A module is a Python file containing definitions and statements that can be used "
    "elsewhere. import brings that module's contents into the current file's namespace. "
    "Modules allow code to be organized, reused, and separated by responsibility "
    "without rewriting it everywhere it is needed.",

    "Every file in this game is a module. combat.py, enemy.py, ledger.py — each one "
    "handles its own responsibility and gets imported where needed. Without modules "
    "everything would live in one massive file. Import is how one module reaches into "
    "another and uses what it finds there.",

    "from ledger import call_ledger\n"
    "from combat import simple_combat\n"
    "from enemy import Enforcer\n\n"
    "call_ledger(player)\n"
    "# Each module does one job.\n"
    "# Import pulls exactly what is needed. Nothing more."
  ),

  "module": (
    "When a spell related to a school of magic is used, you must pull that spell's "
    "info to be used in reality from the specialty of school that exists. "
    "The school holds the knowledge. The pull brings it into action.",

    "A module is a Python file containing definitions and statements that can be used "
    "elsewhere. import brings that module's contents into the current file's namespace. "
    "Modules allow code to be organized, reused, and separated by responsibility "
    "without rewriting it everywhere it is needed.",

    "Every file in this game is a module. combat.py, enemy.py, ledger.py — each one "
    "handles its own responsibility and gets imported where needed. Without modules "
    "everything would live in one massive file. Import is how one module reaches into "
    "another and uses what it finds there.",

    "from ledger import call_ledger\n"
    "from combat import simple_combat\n"
    "from enemy import Enforcer\n\n"
    "call_ledger(player)\n"
    "# Each module does one job.\n"
    "# Import pulls exactly what is needed. Nothing more."
  ),

  "scope": (
    "Oceans exist. But just because they exist does not mean you can swim in them "
    "unless you actually enter said body. Existence and access are not the same thing.",

    "Scope determines where in a program a variable can be accessed. A variable defined "
    "inside a function exists only within that function — local scope. A variable defined "
    "outside all functions exists in global scope and can be accessed anywhere. Inner "
    "scopes can read outer scopes but cannot modify them without explicit declaration.",

    "Scope is about who can see what. A variable created inside the combat function "
    "does not exist outside it — the hub cannot see it, main cannot touch it. It lives "
    "and dies inside that function. What happens in the dungeon stays in the dungeon "
    "unless you explicitly bring it out.",

    "corruption = 0  # global scope\n\n"
    "def make_choice(player):\n"
    "  result = 'betrayal'  # local scope\n"
    "  player.corruption += 1\n"
    "  return result\n\n"
    "print(corruption)  # visible everywhere\n"
    "# print(result)  # NameError — result does not exist out here\n"
    "# Same program. Different visibility."
  ),

  "index": (
    "Life exists as a day zero before day one. The creation is there — but your actual "
    "day one does not start until you are birthed into reality. "
    "What exists before that moment is still real. It simply starts at zero.",

    "An index is a numeric position used to access a specific item in an ordered sequence. "
    "Python indexes start at zero — the first item is always at position 0. Negative "
    "indexes count from the end. Accessing an index that does not exist raises an IndexError.",

    "Every item in a list has a number attached to its position. The first spell in your "
    "spellbook is at index 0. The second is at index 1. You do not ask for the spell by "
    "name — you reach into the exact position and pull what is there. The cipher puzzle "
    "worked exactly this way — you gave positions, the alphabet returned letters.",

    "alphabet = ['T', 'W', 'I', 'L', 'I', 'G', 'H', 'T']\n\n"
    "print(alphabet[0])\n"
    "# T\n\n"
    "print(alphabet[3])\n"
    "# L\n\n"
    "print(alphabet[-1])\n"
    "# T\n"
    "# Position is everything. The item does not move. You reach to where it lives."
  ),

  "indexing": (
    "Life exists as a day zero before day one. The creation is there — but your actual "
    "day one does not start until you are birthed into reality. "
    "What exists before that moment is still real. It simply starts at zero.",

    "An index is a numeric position used to access a specific item in an ordered sequence. "
    "Python indexes start at zero — the first item is always at position 0. Negative "
    "indexes count from the end. Accessing an index that does not exist raises an IndexError.",

    "Every item in a list has a number attached to its position. The first spell in your "
    "spellbook is at index 0. The second is at index 1. You do not ask for the spell by "
    "name — you reach into the exact position and pull what is there. The cipher puzzle "
    "worked exactly this way — you gave positions, the alphabet returned letters.",

    "alphabet = ['T', 'W', 'I', 'L', 'I', 'G', 'H', 'T']\n\n"
    "print(alphabet[0])\n"
    "# T\n\n"
    "print(alphabet[3])\n"
    "# L\n\n"
    "print(alphabet[-1])\n"
    "# T\n"
    "# Position is everything. The item does not move. You reach to where it lives."
  ),

  "slice": (
    "When cutting the crust off bread for preferences on making a sandwich, you then "
    "eat everything in between said crust that is not eaten. "
    "The borders are removed. What remains between them is what you wanted all along.",

    "Slicing extracts a portion of a sequence using the syntax [start:end]. The start "
    "index is inclusive, the end index is exclusive. Omitting start defaults to the "
    "beginning of the sequence. Omitting end defaults to the last item. "
    "A third parameter controls step interval.",

    "Instead of pulling one item by position you pull a range. The first three spells "
    "in your book. Every enemy from index 2 onward. A slice does not modify the original "
    "— it hands you a copy of the portion you asked for. "
    "Start here, stop before here, give me what is between.",

    "spells = ['Ignite', 'Sear', 'Cinder Ward', 'Pyromancy Burn', 'Map Fire']\n\n"
    "print(spells[1:3])\n"
    "# ['Sear', 'Cinder Ward']\n\n"
    "print(spells[:2])\n"
    "# ['Ignite', 'Sear']\n\n"
    "print(spells[2:])\n"
    "# ['Cinder Ward', 'Pyromancy Burn', 'Map Fire']\n"
    "# Start at 1, stop before 3. Everything between those borders is returned."
  ),

  "slicing": (
    "When cutting the crust off bread for preferences on making a sandwich, you then "
    "eat everything in between said crust that is not eaten. "
    "The borders are removed. What remains between them is what you wanted all along.",

    "Slicing extracts a portion of a sequence using the syntax [start:end]. The start "
    "index is inclusive, the end index is exclusive. Omitting start defaults to the "
    "beginning of the sequence. Omitting end defaults to the last item. "
    "A third parameter controls step interval.",

    "Instead of pulling one item by position you pull a range. The first three spells "
    "in your book. Every enemy from index 2 onward. A slice does not modify the original "
    "— it hands you a copy of the portion you asked for. "
    "Start here, stop before here, give me what is between.",

    "spells = ['Ignite', 'Sear', 'Cinder Ward', 'Pyromancy Burn', 'Map Fire']\n\n"
    "print(spells[1:3])\n"
    "# ['Sear', 'Cinder Ward']\n\n"
    "print(spells[:2])\n"
    "# ['Ignite', 'Sear']\n\n"
    "print(spells[2:])\n"
    "# ['Cinder Ward', 'Pyromancy Burn', 'Map Fire']\n"
    "# Start at 1, stop before 3. Everything between those borders is returned."
  ),

  "concatenation": (
    "Everyone has a name. But that name in any society is a combination of a beginning "
    "name and a last name joined together to equal your full name. "
    "Two separate things. One combined identity.",

    "Concatenation joins two or more sequences together into one using the + operator. "
    "For strings it produces a new string. For lists it produces a new list. "
    "The original sequences are not modified — a new combined sequence is returned.",

    "Concatenation is joining things end to end. Two strings become one. Two lists merge "
    "into one longer list. The cipher puzzle used this — individual letters pulled from "
    "the alphabet joined together to form a word. Each piece existed separately. "
    "Concatenation made them one thing.",

    "first_name = 'Aldric'\n"
    "last_name = 'Voss'\n"
    "full_name = first_name + ' ' + last_name\n\n"
    "print(full_name)\n"
    "# Aldric Voss\n"
    "# Two separate strings. One combined identity. Neither original changes."
  ),

  "f-string": (
    "When a patron walks into a tavern whether known or not known, their name or a "
    "sir or ma'am is added onto a greeting. "
    "The welcome exists. What fills it depends on what is known.",

    "An f-string is a string literal prefixed with f that allows expressions to be "
    "embedded directly inside curly braces {}. The expression is evaluated at runtime "
    "and its value is inserted into the string. Cleaner and faster than older "
    "string formatting methods.",

    "An f-string lets you weave variables directly into text without breaking the "
    "sentence apart. Instead of joining pieces with + you just put the variable name "
    "inside curly braces right where it belongs in the sentence. Every line of dialogue "
    "in this game that uses the player's name uses an f-string.",

    "name = 'Aldric'\n"
    "school = 'Pyromancy'\n"
    "level = 3\n\n"
    "print(f'{name} walks the path of {school} at level {level}.')\n"
    "# Aldric walks the path of Pyromancy at level 3.\n"
    "# The variables live inside the sentence.\n"
    "# No joining. No breaking apart. Just the words and what belongs in them."
  ),

  "len": (
    "A value is always associated with how many things exist in a said container. "
    "Like how many vegetables are present in a garden — the container holds what it "
    "holds. The count tells you how much.",

    "len() returns the number of items in a sequence or collection. Works on strings, "
    "lists, tuples, dictionaries, and sets. Returns an integer. Raises a TypeError "
    "if passed an object with no defined length.",

    "Len tells you how many. How many spells in your book. How many enemies in the "
    "wave. How many flags have been set. It does not care what the items are — "
    "just counts them and hands the number back.",

    "spells = ['Ignite', 'Sear', 'Cinder Ward']\n"
    "print(len(spells))\n"
    "# 3\n\n"
    "name = 'Aldric'\n"
    "print(len(name))\n"
    "# 6\n"
    "# Three spells. Six letters. Len does not distinguish. It just counts."
  ),

  "range": (
    "There is always an entry point into a journey. How many steps it takes to get "
    "to the endpoint from the conception varies. But a value that shows how many steps "
    "were taken to get to the finale is always present at the end of the journey.",

    "range() generates a sequence of integers from a start point to an end point "
    "exclusive. Takes up to three arguments — start, stop, and step. Returns a range "
    "object that can be iterated over or converted to a list. Memory efficient — "
    "generates values one at a time rather than storing them all.",

    "Range gives you a sequence of numbers without you having to write them all out. "
    "Instead of listing 0, 1, 2, 3, 4 manually you say range(5) and Python handles it. "
    "Used constantly in for loops when you need to do something a specific number of "
    "times rather than once per item in a collection.",

    "for i in range(3):\n"
    "  print(f'Enemy wave {i + 1} approaches.')\n\n"
    "# Enemy wave 1 approaches.\n"
    "# Enemy wave 2 approaches.\n"
    "# Enemy wave 3 approaches.\n"
    "# Three waves. No list needed. Range counted for you."
  ),

  "type": (
    "Animals exist. But not all exist in the same form. A dog is different than a cat. "
    "Each name specifies what they are — not what they do, not what they are worth. "
    "What they are at their core.",

    "type() returns the data type of an object. Passing a single argument returns its "
    "type as a class. Used for debugging, type checking, and understanding what kind "
    "of object you are working with at any given moment.",

    "Type tells you what something is. Not its value — its nature. Is this a string "
    "or an integer. Is this a Wizard or an Enforcer. When something behaves unexpectedly "
    "type is often the first thing you check — because Python treats different types "
    "differently even when they look similar.",

    "print(type(42))\n"
    "# <class 'int'>\n\n"
    "print(type('Ignite'))\n"
    "# <class 'str'>\n\n"
    "print(type(player))\n"
    "# <class 'wizard_core.Wizard'>\n"
    "# Same function. Three completely different answers.\n"
    "# What something is determines what it can do."
  ),

  "none": (
    "There is space that exists between the stars. It presents itself as nothing — "
    "but is still a something. Not emptiness that once held something. "
    "Simply the defined presence of nothing having existed there yet.",

    "None is Python's null value. It represents the intentional absence of a value. "
    "It is its own data type — NoneType. A function that returns nothing returns None "
    "by default. Checking for None uses 'is None' not '=='.",

    "None is not zero. Not an empty string. Not false. It is the absence of anything "
    "at all. A flag that has not been set yet is not False — it is None. A function "
    "that does work but hands nothing back returns None. The difference matters because "
    "Python treats None differently from every other value.",

    "def just_print(message):\n"
    "  print(message)\n\n"
    "result = just_print('The dungeon waits.')\n"
    "print(result)\n"
    "# The dungeon waits.\n"
    "# None\n"
    "# The function did its job. But it handed nothing back.\n"
    "# None is what fills that silence."
  ),

  "method": (
    "When casting a spell from a specialized school of magic, one cannot use ice magic "
    "as a Pyromancer. The value of what you are is brought over and then translated into "
    "action via the spell in said reality. What you are determines what you can do.",

    "An attribute is a variable bound to an object that stores its state. A method is "
    "a function bound to an object that defines its behavior. Attributes are what "
    "something is. Methods are what something does. Both are accessed via dot notation "
    "on the instance.",

    "Your Wizard has an attribute called school — that is what it is. Your Wizard has "
    "a method called cast_spell — that is what it does. Attributes store state. Methods "
    "perform actions on that state. A Pyromancer's school attribute determines which "
    "methods are available to them.",

    "class Wizard:\n"
    "  def __init__(self, name, school):\n"
    "    self.name = name        # attribute\n"
    "    self.school = school    # attribute\n\n"
    "  def cast_spell(self, spell):  # method\n"
    "    print(f'{self.name} channels {self.school} and casts {spell}.')\n\n"
    "player = Wizard('Aldric', 'Pyromancy')\n"
    "player.cast_spell('Ignite')\n"
    "# Aldric channels Pyromancy and casts Ignite.\n"
    "# name and school are what Aldric is. cast_spell is what Aldric can do."
  ),

  "attribute": (
    "When casting a spell from a specialized school of magic, one cannot use ice magic "
    "as a Pyromancer. The value of what you are is brought over and then translated into "
    "action via the spell in said reality. What you are determines what you can do.",

    "An attribute is a variable bound to an object that stores its state. A method is "
    "a function bound to an object that defines its behavior. Attributes are what "
    "something is. Methods are what something does. Both are accessed via dot notation "
    "on the instance.",

    "Your Wizard has an attribute called school — that is what it is. Your Wizard has "
    "a method called cast_spell — that is what it does. Attributes store state. Methods "
    "perform actions on that state. A Pyromancer's school attribute determines which "
    "methods are available to them.",

    "class Wizard:\n"
    "  def __init__(self, name, school):\n"
    "    self.name = name        # attribute\n"
    "    self.school = school    # attribute\n\n"
    "  def cast_spell(self, spell):  # method\n"
    "    print(f'{self.name} channels {self.school} and casts {spell}.')\n\n"
    "player = Wizard('Aldric', 'Pyromancy')\n"
    "player.cast_spell('Ignite')\n"
    "# Aldric channels Pyromancy and casts Ignite.\n"
    "# name and school are what Aldric is. cast_spell is what Aldric can do."
  ),

  "in": (
    "Calendars vary by the time of the season they fall into and how many days are "
    "associated with said month. A day either belongs to that month or it does not. "
    "The 31st does not exist in February. It exists in December. "
    "Membership is determined by the structure itself.",

    "in tests whether a value exists within a sequence or collection. not in tests "
    "the inverse. Both return a boolean. Works on strings, lists, tuples, sets, and "
    "dictionary keys. One of the most readable membership tests in any programming language.",

    "In asks one question — is this thing inside that thing. Is this spell in your "
    "spellbook. Is this flag in your flags dictionary. Is this letter in the faction "
    "name. Not in asks the opposite. The answer is always True or False. No ambiguity.",

    "spells = ['Ignite', 'Sear', 'Cinder Ward']\n\n"
    "print('Ignite' in spells)\n"
    "# True\n\n"
    "print('Frostbite' in spells)\n"
    "# False\n\n"
    "print('Frostbite' not in spells)\n"
    "# True\n"
    "# One question. One answer. It is there or it is not."
  ),

  "not in": (
    "Calendars vary by the time of the season they fall into and how many days are "
    "associated with said month. A day either belongs to that month or it does not. "
    "The 31st does not exist in February. It exists in December. "
    "Membership is determined by the structure itself.",

    "in tests whether a value exists within a sequence or collection. not in tests "
    "the inverse. Both return a boolean. Works on strings, lists, tuples, sets, and "
    "dictionary keys. One of the most readable membership tests in any programming language.",

    "In asks one question — is this thing inside that thing. Is this spell in your "
    "spellbook. Is this flag in your flags dictionary. Is this letter in the faction "
    "name. Not in asks the opposite. The answer is always True or False. No ambiguity.",

    "spells = ['Ignite', 'Sear', 'Cinder Ward']\n\n"
    "print('Ignite' in spells)\n"
    "# True\n\n"
    "print('Frostbite' in spells)\n"
    "# False\n\n"
    "print('Frostbite' not in spells)\n"
    "# True\n"
    "# One question. One answer. It is there or it is not."
  ),

  "operators": (
    "In order to arrive at a value determined by applying forms of mathematics in an "
    "equation, there are multiple ways to get to said end result. "
    "The tools vary. The purpose — producing a value from a relationship — does not.",

    "Operators are symbols that perform operations on values. Arithmetic operators "
    "handle math — +, -, *, /, //, %, **. Comparison operators evaluate relationships "
    "— ==, !=, <, >, <=, >=. Assignment operators modify variables — =, +=, -=. "
    "Logical operators combine conditions — and, or, not.",

    "Operators are the verbs of math and logic. Every damage calculation uses arithmetic "
    "operators. Every flag check uses comparison operators. Every corruption increase uses "
    "assignment operators. Every branching condition that checks two flags simultaneously "
    "uses logical operators. The entire game runs on them constantly without ever "
    "announcing it.",

    "player.hp -= 15\n"
    "player.corruption += 1\n\n"
    "if player.hp <= 0 and player.corruption >= 3:\n"
    "  print('You fall. Corrupted and broken.')\n"
    "# Subtract. Add. Compare. Combine. Four operators. One moment."
  ),

  "iteration": (
    "If a swarm of ravens were to attack you, in order to survive you must shoot each "
    "one down with an arrow or be rid of it with a spell. One at a time. In sequence. "
    "Until none remain or you do not.",

    "Iteration is the process of accessing items in a sequence one at a time in order. "
    "Any object that can be iterated over is called an iterable. Python's for loop is "
    "the primary iteration tool. Iteration does not require knowing the length of the "
    "sequence in advance.",

    "Iteration is the act of going through a collection one item at a time and doing "
    "something with each one. Every combat round iterates through status effects. Every "
    "hub menu iterates through available options. Every grind session iterates through "
    "spawned enemies. It is the heartbeat of how the game processes its own state.",

    "for effect in player.status_effects:\n"
    "  effect.tick(player)\n"
    "  if effect.is_expired():\n"
    "    player.status_effects.remove(effect)\n"
    "# Every status effect touched in turn. Each one processed.\n"
    "# Each expired one removed.\n"
    "# The loop moves through all of them without being told how many there are."
  ),

}


def _normalize(question: str) -> str:
  q = question.lower().strip()
  q = q.replace("what is ", "").replace("what are ", "")
  q = q.replace("explain ", "").replace("tell me about ", "")
  q = q.replace("how does ", "").replace("how do ", "")
  q = q.replace("?", "").replace(".", "").strip()
  return q


def _find_concept(question: str):
  q = _normalize(question)
  if q in LEDGER_RESPONSES:
    return q
  for key in LEDGER_RESPONSES:
    pattern = r'(?<!\w)' + re.escape(key) + r'(?!\w)'
    if re.search(pattern, q):
      return key
  return None


def _parse_input(raw: str):
  raw = raw.strip()
  if not raw.lower().startswith("ledger"):
    return None, "no_ledger"
  if raw.lower() == "ledger":
    return None, "no_parens"
  empty_match = re.match(r'ledger\(\s*\)\s*$', raw, re.IGNORECASE)
  if empty_match:
    return None, "empty"
  match = re.match(r'ledger\((.+)\)\s*$', raw, re.IGNORECASE)
  if not match:
    return None, "malformed"
  question = match.group(1).strip().strip('"').strip("'").strip()
  if not question:
    return None, "empty"
  return question, "ok"


def _is_twilight(question: str) -> bool:
  q = question.lower()
  return any(t in q for t in TWILIGHT_TRIGGERS)


def _is_off_world(question: str) -> bool:
  q = question.lower()
  return any(t in q for t in OFF_WORLD_TRIGGERS)


def _is_gibberish(question: str) -> bool:
  return len(question.strip()) < 3 or not any(c.isalpha() for c in question)


def _display_response(concept: str):
  lore, documentation, plain, example = LEDGER_RESPONSES[concept]
  print(f"\n  {lore}")
  print(f"\n  {documentation}")
  print(f"\n  {plain}")
  print(f"\n  ---")
  for line in example.split("\n"):
    print(f"  {line}")


def _ledger_intro():
  print("\n\n  The Ledger speaks to the user beyond the screen.")
  print("\n  A presence settles at the edge of your mind.")
  print("  Not sound. Not exactly. Something older than sound.")
  print("  A knowing that arrives without being sent.")
  print("\n  When you wish to speak to it —")
  print("  ledger(your question)")
  print("  — and it will answer.")
  print("\n  The form of the question matters.")
  print("  The parentheses are not decoration.")


def call_ledger(player):
  if not player.flags.get(LEDGER_UNLOCKED_FLAG):
    return

  if not player.flags.get(LEDGER_INTRO_SEEN_FLAG):
    _ledger_intro()
    player.flags[LEDGER_INTRO_SEEN_FLAG] = True
    input("\n  [press Enter]")
    return

  print("\n  The presence waits.")
  raw = input("\n  > ").strip()

  if not raw:
    return

  question, status = _parse_input(raw)

  if status == "no_ledger":
    return

  if status == "no_parens":
    print("\n  The Ledger speaks to the user beyond the screen.")
    print("\n  You know its name.")
    print("  You know how to reach it.")
    print("  ledger(your question)")
    return

  if status == "malformed":
    print("\n  The Ledger speaks to the user beyond the screen.")
    print("\n  The form of the question matters as much as the question itself.")
    print("  ledger(your question)")
    return

  if status == "empty":
    print("\n  The Ledger speaks to the user beyond the screen.")
    print("\n  The Ledger requires something to respond to.")
    return

  print("\n  The Ledger speaks to the user beyond the screen.")

  if _is_twilight(question):
    print("\n  A pause.")
    print("  Not consideration. Something closer to patience.")
    while True:
      print("\n  'I am what I always was.'")
      again = input("\n  [press Enter to step back, or ask another question] > ").strip()
      if not again:
        break
      new_q, new_status = _parse_input(again)
      if new_status == "ok" and not _is_twilight(new_q):
        question = new_q
        break
      elif new_status == "ok" and _is_twilight(new_q):
        continue
      else:
        continue
    if _is_twilight(question):
      return

  if _is_off_world(question):
    print("\n  'This question does not relate to this world.'")
    print("  A beat.")
    print("  'But it does to yours.'")
    input("\n  [press Enter]")
    return

  if _is_gibberish(question):
    print("\n  A stillness.")
    print("  Then:")
    print("  'This is not a question.")
    print("  Please rethink what you wish to ask.'")
    input("\n  [press Enter]")
    return

  concept = _find_concept(question)

  if concept:
    print("\n  Something shifts.")
    print("  The voice arrives without traveling.")
    _display_response(concept)
    if not player.flags.get(LEDGER_FIRST_CALL_FLAG):
      player.flags[LEDGER_FIRST_CALL_FLAG] = True
  else:
    print("\n  A long silence.")
    print("  Then:")
    print("  'That is beyond what the Never Was requires of you.")
    print("  For now.'")

  input("\n  [press Enter]")