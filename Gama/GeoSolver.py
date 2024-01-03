import math, numpy as np
TURN_RADIUS = 4*1852

EARTH_RADIUS = 6.371e6

class FlyByTransition:
  Pwp1_Lat     : float
  Pwp1_Lon     : float
  Pwp2_Lat     : float
  Pwp2_Lon     : float
  To_Lat       : float
  To_Lon       : float
  ArcRadius    : float
  LeftTurn     : bool
  TrkChange    : int
  InboundTrk   : int

  def __init__(self,
               Pwp1_Lat   : float, Pwp1_Lon   : float,
               Pwp2_Lat   : float, Pwp2_Lon   : float,
               To_Lat     : float, To_Lon     : float,
               ArcRadius  : float, TrkChange  : int,
               LeftTurn   :  bool, InboundTrk : int) -> None:
    self.Pwp1_Lat   = Pwp1_Lat
    self.Pwp1_Lon   = Pwp1_Lon
    self.Pwp2_Lat   = Pwp2_Lat
    self.Pwp2_Lon   = Pwp2_Lon
    self.To_Lat     = To_Lat
    self.To_Lon     = To_Lon
    self.ArcRadius  = ArcRadius
    self.LeftTurn   = LeftTurn
    self.TrkChange  = TrkChange
    self.InboundTrk = InboundTrk

def SolveFlyBy(LatFrom : float, LonFrom : float,
               LatTo   : float, LonTo   : float,
               LatNext : float, LonNext : float) -> FlyByTransition:
  '''This funcion takes three points and computes three points:
    1st pseudo-Wp, TO Waypoint and a second pseudo-Wp
    output comes as a specialized class carrying lat & lon of 
    the points along with other data
    the problem is a spherical triangle with:
    a = Turn radius side
    b = TO-arc_center side
    c = TO-pwp1 side
    alpha = half of track change
    beta = 90° because of tangency between TO leg & turn circle
    gamma is not useful
    see https://en.wikipedia.org/wiki/Solution_of_triangles#A_side,_one_adjacent_angle_and_the_opposite_angle_given_(spherical_AAS)
    for solution used'''
  print("computing Fly-By")
  FromVector = np.array(LatLon2XYZ(Lat=LatFrom,Lon=LonFrom),dtype=np.float64)
  ToVector   = np.array(LatLon2XYZ(Lat=LatTo,Lon=LonTo),dtype=np.float64)
  NextVector = np.array(LatLon2XYZ(Lat=LatNext,Lon=LonNext),dtype=np.float64)
  FromNormal = np.cross(ToVector,FromVector)
  NextNormal = np.cross(NextVector,ToVector)
  alpha = .5 * np.arccos(abs(np.dot(FromNormal,NextNormal)/(np.linalg.norm(NextNormal)*np.linalg.norm(FromNormal))))
  beta = np.radians(90)
  a = TURN_RADIUS / EARTH_RADIUS
  if True : #(a < np.radians(90)) and (alpha > beta):
    b = np.arcsin((np.sin(a)*np.sin(beta))/(np.sin(alpha)))
  else:
    b = np.pi - np.arcsin((np.sin(a)*np.sin(beta))/(np.sin(alpha)))
  sin_12_alpha_p_beta = np.sin(.5*(alpha+beta))
  sin_12_alpha_m_beta = np.sin(.5*(alpha-beta))
  c = 2*np.arctan(np.tan(.5*(a-b) * sin_12_alpha_p_beta/sin_12_alpha_m_beta))
  n = np.cross(FromVector,ToVector)
  n = n/np.sqrt(np.dot(n,n))
  i = ToVector/np.sqrt(np.dot(ToVector,ToVector))
  j = np.cross(i,n)
  B = EARTH_RADIUS*(np.cos(c)*i+np.sin(c)*j)
  n = np.cross(ToVector,NextVector)
  n = n/np.sqrt(np.dot(n,n))
  i = ToVector/np.sqrt(np.dot(ToVector,ToVector))
  j = np.cross(n,i) # the second pwp need the norm inverted: to be understood
  C = EARTH_RADIUS*(np.cos(c)*i+np.sin(c)*j)
  Pwp1 = XYZ2LatLonHeight(X=B[0], Y=B[1], Z=B[2])
  Pwp2 = XYZ2LatLonHeight(X=C[0], Y=C[1], Z=C[2])
  TrackChange = np.pi - (alpha * 2)
  n = np.cross(ToVector,FromVector)
  ArcIsLeft = np.dot(n, NextVector) < 0
  output = FlyByTransition(Pwp1_Lat=Pwp1[0], Pwp1_Lon=Pwp1[1],
                           Pwp2_Lat=Pwp2[0], Pwp2_Lon=Pwp2[1],
                           To_Lat=LatTo, To_Lon=LonTo, ArcRadius=a*EARTH_RADIUS,
                           LeftTurn=ArcIsLeft, TrkChange=TrackChange,
                           InboundTrk=0)
  return output
  
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

def XYZ2LatLonHeight(X : float, Y: float, Z : float) -> list[float]:
  output : list[float] = [1.0, 2.0, 3.0]
  output[2] = math.sqrt(X*X + Y*Y + Z*Z) # height = radius
  output[0] = math.degrees(math.asin(Z/output[2])) #Azimuth = lat
  output[1] = math.degrees(math.atan2(Y,X)) #Polar = Lon
  return output

def XY2ThetaRho(X : float, Y : float) -> list[float]:
  output = [0.0, 0.0]
  output[0] = math.atan2(X,Y)
  output[1] = math.sqrt(math.pow(X,2) + math.pow(Y,2))
  return output