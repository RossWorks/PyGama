import math
TURN_RADIUS = 2e3

EARTH_RADIUS = 6.371e6

def SolveFlyBy(LatFrom : float, LonFrom : float,
               LatTo   : float, LonTo   : float,
               LatNext : float, Lonnext : float) -> list[float]:
  CourseToB = 125
  CourseFromB = 97
  TrackChange = CourseFromB - CourseToB
  ReducedTurnRadius = 2 * math.pi() / EARTH_RADIUS
  return None

def LatLon2XY(Lat : float, Lon : float,
              OriginLat : float, OriginLon : float) -> list[float]:
  if Lat == OriginLat and Lon == OriginLon:
    return [0.0,0.0]
  output : list[float] = [1.0, 2.0]
  cos_phi0  = math.cos(math.radians(OriginLat))
  cos_phi   = math.cos(math.radians(Lat))
  sin_phi0  = math.sin(math.radians(OriginLat))
  sin_phi   = math.sin(math.radians(Lat))
  cos_rho_R = sin_phi0 * sin_phi + cos_phi0 * cos_phi * math.cos(math.radians(Lon-OriginLon))
  rho       = EARTH_RADIUS * math.acos(cos_rho_R)
  tan_theta = cos_phi * math.cos(math.radians(Lon-OriginLon)) /\
             (cos_phi0*sin_phi - sin_phi0*cos_phi* math.cos(math.radians(Lon-OriginLon)))
  theta     = math.atan(tan_theta)
  output[0] = rho * math.sin(theta)
  output[1] = rho * math.cos(theta) * -1
  return output

def LatLon2XYZ(Lat : float, Lon : float, Height : int = 0) -> list[float]:
  output : list[float] = [1.0, 2.0, 3.0]
  output[0] = (EARTH_RADIUS + Height) * math.cos(math.radians(Lat)) * math.cos(math.radians(Lon))
  output[1] = (EARTH_RADIUS + Height) * math.cos(math.radians(Lat)) * math.sin(math.radians(Lon))
  output[2] = (EARTH_RADIUS + Height) * math.sin(math.radians(Lat))
  return output