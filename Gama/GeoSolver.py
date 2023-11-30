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
  '''This function is derived from the formulas depicted in:
  \"An album of map projections\", by 
  John P. Snyder, ; U.S. Geological Survey,
  and
  Philip M. Voxland,University of Minnesota
  page 228.
  This function applies azimuthal equidistant projection, same used in UN flag
  '''
  output = [0.0, 0.0]
  sin_phi1 = math.sin(math.radians(OriginLat))
  cos_phi1 = math.cos(math.radians(OriginLat))
  sin_phi  = math.sin(math.radians(Lat))
  cos_phi  = math.cos(math.radians(Lat))
  cos_delta_lambda = math.cos(math.radians(Lon-OriginLon))
  sin_delta_lambda = math.sin(math.radians(Lon-OriginLon))
  cos_z = sin_phi1 * sin_phi + cos_phi1 * cos_phi * cos_delta_lambda
  if cos_z < 0:
    return [math.nan, math.nan] #the point must be rejected
  if cos_z == 1:
    K = 1
  else:
    sin_z = math.sqrt(1 - math.pow(cos_z,2))
    K = math.acos(cos_z) / sin_z

  output[0] = EARTH_RADIUS * K * cos_phi * sin_delta_lambda
  output[1] = EARTH_RADIUS * K * (cos_phi1 * sin_phi - sin_phi1 * cos_phi * cos_delta_lambda)
  return output

def LatLon2XYZ(Lat : float, Lon : float, Height : int = 0) -> list[float]:
  output : list[float] = [1.0, 2.0, 3.0]
  output[0] = (EARTH_RADIUS + Height) * math.cos(math.radians(Lat)) * math.cos(math.radians(Lon))
  output[1] = (EARTH_RADIUS + Height) * math.cos(math.radians(Lat)) * math.sin(math.radians(Lon))
  output[2] = (EARTH_RADIUS + Height) * math.sin(math.radians(Lat))
  return output

def XY2ThetaRho(X : float, Y : float) -> list[float]:
  output = [0.0, 0.0]
  output[0] = math.atan2(X,Y)
  output[1] = math.sqrt(math.pow(X,2) + math.pow(Y,2))
  return output