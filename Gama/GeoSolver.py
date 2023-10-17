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

def LatLon2XYZ(Lat : float, Lon : float, Height : int = 0) -> list[float]:
  output : list[float] = [0.0, 0.0, 0.0]
  output[0] = (EARTH_RADIUS + Height) * math.sin(math.radians(Lat)) * math.cos(math.radians(Lon))
  output[1] = (EARTH_RADIUS + Height) * math.sin(math.radians(Lat)) * math.sin(math.radians(Lon))
  output[2] = (EARTH_RADIUS + Height) * math.sin(math.radians(Lat))
  return output