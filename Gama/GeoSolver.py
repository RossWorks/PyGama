import math
TURN_RADIUS = 2e3

EARTH_RADIUS = 6e6

def SolveFlyBy(LatFrom : float, LonFrom : float,
               LatTo   : float, LonTo   : float,
               LatNext : float, Lonnext : float) -> list[float]:
  CourseToB = 125
  CourseFromB = 97
  TrackChange = CourseFromB - CourseToB
  ReducedTurnRadius = 2 * math.pi() / EARTH_RADIUS
  return None
