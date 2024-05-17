import math, numpy as np
TURN_RADIUS = 4*1852
FLYBY_THRESHOLD = np.radians(15)
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
  ArcCenterLat : float
  ArcCenterLon : float
  Valid        : bool

  def __init__(self,
               Pwp1_Lat   : float, Pwp1_Lon   : float,
               Pwp2_Lat   : float, Pwp2_Lon   : float,
               To_Lat     : float, To_Lon     : float,
               ArcRadius  : float, TrkChange  : int,
               LeftTurn   :  bool, InboundTrk : int,
               ArcCenterLat : float, ArcCenterLon : float,
               Validity : bool) -> None:
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
    self.ArcCenterLat = ArcCenterLat
    self.ArcCenterLon = ArcCenterLon
    self.Valid      = Validity

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
    alpha = 90° - track change / 2
    beta = 90° because of tangency between TO leg & turn circle
    gamma is not useful
    see https://en.wikipedia.org/wiki/Solution_of_triangles#A_side,_one_adjacent_angle_and_the_opposite_angle_given_(spherical_AAS)
    for solution used'''
  FromVector = np.array(LatLon2XYZ(Lat=LatFrom,Lon=LonFrom),dtype=np.float64)
  ToVector   = np.array(LatLon2XYZ(Lat=LatTo,Lon=LonTo),dtype=np.float64)
  NextVector = np.array(LatLon2XYZ(Lat=LatNext,Lon=LonNext),dtype=np.float64)
  FromNormal = np.cross(ToVector,FromVector)
  NextNormal = np.cross(NextVector,ToVector)
  InvalidateResult : bool = False
  TrackChange = np.arccos(np.inner(FromNormal,NextNormal)/(np.linalg.norm(NextNormal)*np.linalg.norm(FromNormal)))
  print("Track change   = " + str(np.degrees(TrackChange)) + "°")
  alpha = np.pi / 2 - .5 * TrackChange
  beta = np.radians(90)
  a = TURN_RADIUS / EARTH_RADIUS
  if (a < np.radians(90)) and (alpha > beta):
    #this condition should never be true
    b = np.pi - np.arcsin((np.sin(a)*np.sin(beta))/(np.sin(alpha)))
  else:
    b = np.arcsin((np.sin(a)*np.sin(beta))/(np.sin(alpha)))
  sin_12_alpha_p_beta = np.sin(.5*(alpha+beta))
  sin_12_alpha_m_beta = np.sin(.5*(alpha-beta))
  c = 2*np.arctan(np.tan(.5*(a-b)) * sin_12_alpha_p_beta/sin_12_alpha_m_beta)
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
  n = np.cross(ToVector,FromVector)
  ArcIsLeft = np.dot(n, NextVector) < 0
  IncomingTrack = GreatCircleFinalAz(LatFrom=LatFrom, LonFrom=LonFrom, 
                                     LatTo=Pwp1[0], LonTo=Pwp1[1])
  print("Incoming track = " + str(int(np.degrees(IncomingTrack))) + "°")
  if TrackChange < FLYBY_THRESHOLD:
    print("Invalidating Fly-by due to track change = "+ str(np.degrees(TrackChange)) +" < " + str(np.degrees(FLYBY_THRESHOLD)) + "°")
    InvalidateResult = True
  Faz_to_center = IncomingTrack + np.pi/2 * (-1 if ArcIsLeft else 1)
  ArcCenter = GreatCircleDirect(LatFrom=Pwp1[0], LonFrom=Pwp1[1],
                                Faz=Faz_to_center,
                                Distance= a*EARTH_RADIUS)
  output = FlyByTransition(Pwp1_Lat=Pwp1[0], Pwp1_Lon=Pwp1[1],
                           Pwp2_Lat=Pwp2[0], Pwp2_Lon=Pwp2[1],
                           To_Lat=LatTo, To_Lon=LonTo, ArcRadius=a*EARTH_RADIUS,
                           LeftTurn=ArcIsLeft, TrkChange=TrackChange,
                           InboundTrk=IncomingTrack, ArcCenterLat=ArcCenter[0],
                           ArcCenterLon=ArcCenter[1], Validity= not InvalidateResult)
  return output

def LatLon2XYZ(Lat : float, Lon : float, Height : int = 0) -> list[float]:
  output : list[float] = [1.0, 2.0, 3.0]
  output[0] = (EARTH_RADIUS + Height) * math.cos(Lat) * math.cos(Lon)
  output[1] = (EARTH_RADIUS + Height) * math.cos(Lat) * math.sin(Lon)
  output[2] = (EARTH_RADIUS + Height) * math.sin(Lat)
  return output

def XYZ2LatLonHeight(X : float, Y: float, Z : float) -> list[float]:
  output : list[float] = [1.0, 2.0, 3.0]
  output[2] = math.sqrt(X*X + Y*Y + Z*Z) # height = radius
  output[0] = math.asin(Z/output[2]) #Azimuth = lat
  output[1] = math.atan2(Y,X) #Polar = Lon
  return output

def GreatCircleDistance(LatFrom : float, LonFrom : float,
                        LatTo   : float, LonTo   : float) -> np.float64:
  if np.abs(LatFrom - LatTo) < 1e-8 and np.abs(LonFrom - LonTo) < 1e-8:
    return np.float64(0.0)
  sin_phi1 = np.sin(LatFrom)
  cos_phi1 = np.cos(LatFrom)
  sin_phi2 = np.sin(LatTo)
  cos_phi2 = np.cos(LatTo)
  delta_lambda = LonTo - LonFrom
  delta_sigma  = np.arccos(sin_phi1*sin_phi2 + cos_phi1*cos_phi2*np.cos(delta_lambda))
  distance = EARTH_RADIUS * delta_sigma
  return distance

def GreatCircleInitAz(LatFrom : float, LonFrom : float,
                      LatTo   : float, LonTo   : float) -> float:
  sin_phi1 = math.sin(LatFrom)
  cos_phi1 = math.cos(LatFrom)
  sin_phi2 = math.sin(LatTo)
  cos_phi2 = math.cos(LatTo)
  sin_delta_lambda = math.sin(LonTo - LonFrom)
  cos_delta_lambda = math.cos(LonTo - LonFrom)
  N = (cos_phi2 * sin_delta_lambda)
  D = (cos_phi1*sin_phi2 - sin_phi1*cos_phi2*cos_delta_lambda)
  return math.atan2(N,D)

def GreatCircleFinalAz(LatFrom : float, LonFrom : float,
                       LatTo   : float, LonTo   : float) -> float:
  sin_phi1 = math.sin(LatFrom)
  cos_phi1 = math.cos(LatFrom)
  sin_phi2 = math.sin(LatTo)
  cos_phi2 = math.cos(LatTo)
  sin_delta_lambda = math.sin(LonTo - LonFrom)
  cos_delta_lambda = math.cos(LonTo - LonFrom)
  N = (cos_phi1 * sin_delta_lambda)
  D = (-1*cos_phi2*sin_phi1 + sin_phi2*cos_phi1*cos_delta_lambda)
  T = math.atan2(N,D)
  if math.isnan(T):
    print("T = " + str(T))
    print("N = " + str(N))
    print("D = " + str(D))
  return T

def GreatCircleDirect(LatFrom : float, LonFrom : float,
                      Faz     : float, Distance: float) -> list[float]:
  sin_phi1 = math.sin(LatFrom)
  cos_phi1 = math.cos(LatFrom)
  sigma_12 = Distance / EARTH_RADIUS
  sin_sigma_12 = math.sin(sigma_12)
  cos_sigma_12 = math.cos(sigma_12)
  cos_faz = math.cos(Faz)
  sin_faz = math.sin(Faz)
  N = sin_phi1*cos_sigma_12 + cos_phi1*sin_sigma_12*cos_faz
  D = math.pow(cos_phi1*cos_sigma_12 - sin_phi1*sin_sigma_12*cos_faz,2)
  D+= math.pow(sin_sigma_12*sin_faz,2)
  D = math.sqrt(D)
  LatDest = math.atan2(N,D)
  N = sin_sigma_12*sin_faz
  D = cos_phi1*cos_sigma_12 - sin_phi1*sin_sigma_12*cos_faz
  LonDest = LonFrom + math.atan2(N,D)
  return [LatDest, LonDest]


def GreatCircleCrossDistance(LatFrom: np.float64, LonFrom: np.float64,
                             LatTo: np.float64, LonTo:np.float64,
                             PposLat: np.float64, PposLon: np.float64) -> np.float64:
    delta_13 = GreatCircleDistance(LatFrom=LatFrom, LonFrom=LonFrom,
                                   LatTo=PposLat, LonTo=PposLon) / EARTH_RADIUS
    theta_13 = GreatCircleInitAz(LatFrom=LatFrom, LonFrom=LonFrom,
                                 LatTo=PposLat, LonTo=PposLon)
    theta_12 = GreatCircleInitAz(LatFrom=LatFrom, LonFrom=LonFrom,
                                 LatTo=LatTo, LonTo=LonTo)

    XTE = np.arcsin(np.sin(delta_13) * np.sin(theta_13 - theta_12)) * EARTH_RADIUS
    return XTE

if __name__ == "__main__":
  import os
  print("Initiating self test for " + os.path.basename(__file__))
  A = [np.deg2rad(45.0), np.deg2rad(8.0)]
  B = [np.deg2rad(46.0), np.deg2rad(8.0)]
  C = [np.deg2rad(45.5), np.deg2rad(8.0)]
  X = [np.deg2rad(45.5), np.deg2rad(7.0)]
  Y = [np.deg2rad(45.5), np.deg2rad(9.0)]
  print("A = " + str(np.rad2deg(A[0])) + " " + str(np.rad2deg(A[1])))
  print("B = " + str(np.rad2deg(B[0])) + " " + str(np.rad2deg(B[1])))
  print("C = " + str(np.rad2deg(C[0])) + " " + str(np.rad2deg(C[1])))
  print("X = " + str(np.rad2deg(X[0])) + " " + str(np.rad2deg(X[1])))
  print("Y = " + str(np.rad2deg(Y[0])) + " " + str(np.rad2deg(Y[1])))
  print()
  print("XTD of X from A-B")
  print(GreatCircleCrossDistance(A[0],A[1],B[0],B[1],X[0],X[1])/1852.0)
  print("XTD of Y from A-B")
  print(GreatCircleCrossDistance(A[0],A[1],B[0],B[1],Y[0],Y[1])/1852.0)
  print("Distance C-X")
  print(GreatCircleDistance(C[0],C[1],X[0],X[1])/1852.0)
