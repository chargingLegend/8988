from ch0 import prologue
from ch1 import (mountain_descent, vardeth_arrival, town_threads,
                 enforcer_office, cipher_tablet, vardeth_evening,
                 the_dungeon)
from systems.checkpoint import (RestartGame, CheckpointReload,
                                register_resume_point, RESUME_POINTS)


def resolve_ch1_route(flags):
  promise = flags.get('promised_sister_search', False)
  mira = flags.get('companion_mira', False)
  duo = flags.get('companion_duo', False)
  dara = flags.get('dara_dungeon', False)
  if mira and duo:
    return 'duo'
  if promise and not mira and not duo and not dara:
    return 'solo_promise'
  return 'default'


register_resume_point("vardeth_arrival", lambda p: vardeth_arrival(p))
register_resume_point("dungeon_entrance", lambda p: the_dungeon(p))

if __name__ == "__main__":
  while True:
    try:
      player = prologue()
      mountain_descent(player)
      vardeth_arrival(player)
      town_threads(player)
      enforcer_office(player)
      cipher_tablet(player)
      vardeth_evening(player)
      the_dungeon(player)
      break
    except RestartGame:
      continue
    except CheckpointReload as reload:
      resume = RESUME_POINTS.get(reload.location_id)
      if resume:
        resume(player)
      break