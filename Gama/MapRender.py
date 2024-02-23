from . import FlightPlan as Fp, GeoSolver, FplWaypoint, GamaWaypoints
import numpy as np

MapCenter = [np.radians(45.5), np.radians(8.7)]
MapOrientation = np.pi/2

MARKER_APT = "^"
MARKER_NDB = "o"
MARKER_USR = "*"
MARKER_VHF = "h"
MARKER_WPT = "D"
MARKER_NULL = "."
Type_marker_dict : dict[str:str] = {"APT" : MARKER_APT,
                                    "NDB" : MARKER_NDB,
                                    "USR" : MARKER_USR,
                                    "VHF" : MARKER_VHF,
                                    "WPT" : MARKER_WPT}

Type_color_dict : dict[str:str] = {"APT" : "cyan",
                                   "NDB" : "orange",
                                   "USR" : "yellow",
                                   "VHF" : "green",
                                   "WPT" : "pink"}

def SetCdsCenter(Lat : float, Lon : float) -> bool:
  global MapCenter
  if abs(Lat) > (np.pi/2):
    return False
  if abs(Lon) > np.pi:
    return False
  MapCenter = [Lat, Lon]
  return True

def SetMapRotation(NewHeading : float = 0) -> bool:
  global MapOrientation
  MapOrientation = NewHeading
  return True

class GraphFpSegment:
  Intended : bool
  Route : np.ndarray
  Color : str

  def __init__(self) -> None:
    self.Intended = False
    self.Route = 0.0 * np.zeros(shape=(100,3), dtype=np.float64)
    self.Color = 'k'

class GraphWpMarker:
  Name  : str
  Color : str
  Marker: str
  Theta : float
  Rho : float
  X : float
  Y : float
  Z : float

  def __init__(self) -> None:
    self.Name = "******"
    self.Color = 'k'
    self.Marker = MARKER_NULL
    self.X = 0.0
    self.Y = 0.0
    self.Z = 0.0
    self.Theta = 0.0
    self.Rho = 0.0
  
  def SetPolarPosition(self, Rho : float, Theta : float):
    self.Rho = Rho
    self.Theta = Theta

  def SetMarker(self, Marker : str):
    self.Marker = Marker
  
  def SetColor(self, Color : str):
    self.Color = Color

  def SetName(self, Name : str):
    self.Name = Name

def RenderWorld(LatRes : int = 20, LonRes : int = 20) -> dict[str : np.ndarray]:
  output : dict[str:np.ndarray] = {}
  u = np.linspace(0, 2 * np.pi, LonRes)
  v = np.linspace(0, np.pi, LatRes)
  output['X'] = GeoSolver.EARTH_RADIUS * np.outer(np.cos(u), np.sin(v))
  output['Y'] = GeoSolver.EARTH_RADIUS * np.outer(np.sin(u), np.sin(v))
  output['Z'] = GeoSolver.EARTH_RADIUS * np.outer(np.ones(np.size(u)), np.cos(v))
  return output

def DrawPolarStraightLine(StartPoint : Fp.GamaWaypoints.GamaFplWaypoint, 
                          EndPoint   : Fp.GamaWaypoints.GamaFplWaypoint) -> np.ndarray:
  pre_output = np.zeros(shape=(100,2))
  output = np.zeros(shape=(100,2))
  p1 = np.array(GeoSolver.LatLon2XY(Lat=StartPoint.Lat, Lon=StartPoint.Lon,
                                    OriginLat=MapCenter[0], OriginLon=MapCenter[1]))
  p2 = np.array(GeoSolver.LatLon2XY(Lat=EndPoint.Lat, Lon=EndPoint.Lon,
                                    OriginLat=MapCenter[0], OriginLon=MapCenter[1]))
  pre_output[:,0] = np.linspace(p1[0],p2[0],100)
  pre_output[:,1] = np.linspace(p1[1],p2[1],100)
  output[:,0] = np.arctan2(pre_output[:,0],pre_output[:,1])
  output[:,1] = np.sqrt(np.power(pre_output[:,1],2)+np.power(pre_output[:,0],2))
  return output

def DrawGreatCircle(StartPoint : Fp.GamaWaypoints.GamaFplWaypoint, 
                    EndPoint   : Fp.GamaWaypoints.GamaFplWaypoint) -> np.ndarray:
  output = np.zeros(shape=(100,3))
  Xyz = GeoSolver.LatLon2XYZ(Lat=StartPoint.Lat, Lon=StartPoint.Lon)
  p1 = np.array(Xyz)
  Xyz = GeoSolver.LatLon2XYZ(Lat=EndPoint.Lat, Lon=EndPoint.Lon)
  p2 = np.array(Xyz)
  n = (np.cross(p1,p2))
  n = n/np.sqrt(np.dot(n,n))
  i = p1/np.sqrt(np.dot(p1,p1))
  j = np.cross(n,i)
  delta_angle = np.arccos(np.dot(p1,p2)/(np.linalg.norm(p1)*np.linalg.norm(p2)))
  t = np.resize(a=np.linspace(start=0,stop=delta_angle,num=100),
                new_shape=(100,1))
  output = GeoSolver.EARTH_RADIUS*(np.cos(t)*i+np.sin(t)*j)
  return output

def DrawPolarArc(StartPoint : Fp.GamaWaypoints.GamaFplWaypoint,
                 EndPoint   : Fp.GamaWaypoints.GamaFplWaypoint) -> np.ndarray:
  output = np.zeros(shape=(100,2))
  Pwp1Vector = np.array(GeoSolver.LatLon2XY(Lat=StartPoint.Lat, Lon= StartPoint.Lon,
                                            OriginLat=MapCenter[0], OriginLon=MapCenter[1]))
  Pwp1Vector = Pwp1Vector.reshape((2,1))
  ArcCenter = GeoSolver.LatLon2XY(Lat=StartPoint.ArcCenterLat, Lon= StartPoint.ArcCenterLon,
                                  OriginLat=MapCenter[0], OriginLon=MapCenter[1])
  ArcCenterVector = np.array(ArcCenter).reshape((2,1))
  Angle = np.linspace(start=0,stop=StartPoint.TrackChange, num=100).reshape((100,1))
  Center2PwpVector = Pwp1Vector - ArcCenterVector
  theta = np.pi * (.5 if StartPoint.ArcIsLeftHand else -.5) #behaviour is inverted from Fly-By computation because a rot matrix follow anticlockwise angle rule
  rot_matrix = np.matrix([[np.cos(theta), -np.sin(theta)],
                          [np.sin(theta),  np.cos(theta)]])
  otherVector = rot_matrix @ Center2PwpVector
  for step in range(0,len(Angle)):
    Dummy = ArcCenterVector + (Center2PwpVector * np.cos(Angle[step]) + otherVector * np.sin(Angle[step]))
    output_theta    = np.arctan2(Dummy[0],Dummy[1])
    output_rho      = np.sqrt(np.power(Dummy[0],2)+np.power(Dummy[1],2))
    output[step, 0] = output_theta
    output[step, 1] = output_rho
  return output

def RenderGamaFpl(GamaFpl : list[Fp.GamaWaypoints.GamaFplWaypoint],
                  Use3D   : bool = True) -> list[GraphFpSegment]:
  print("Updating "+ ("3" if Use3D else "2") +"D Flight plan")
  output = list()
  TmpSegment = GraphFpSegment()
  FpSize = len(GamaFpl)
  if FpSize == 1:
    TmpSegment.Color = 'k'
    TmpSegment.Route[0,0] = GamaFpl[0].Lat
    output.append(TmpSegment)
  else:
    for index in range(0,FpSize-1):
      TmpSegment = GraphFpSegment()
      EndOfArcPoint = GamaWaypoints.GamaFplWaypoint()
      TmpSegment.Color = 'm' if index == 0 else 'k'
      TmpSegment.Intended = False
      if Use3D:
        print("calculating 3D great circle from " + str(GamaFpl[index].Name) + " to " + str(GamaFpl[index+1].Name))
        TmpSegment.Route = DrawGreatCircle(StartPoint = GamaFpl[index],
                                           EndPoint   = GamaFpl[index+1])
        output.append(TmpSegment)
      else:
        if GamaFpl[index].ConicApp:
          print("Calculating 2D Arc from " + str(GamaFpl[index].Name) + " to " + str(GamaFpl[index+1].Name))
          TmpSegment.Route = DrawPolarArc(StartPoint = GamaFpl[index],
                                          EndPoint   = EndOfArcPoint)
          output.append(TmpSegment)
          if not GamaFpl[index].GapFollows:
            continue
            print("calculating 2D straight line from " + str(GamaFpl[index].Name) + " to " + str(GamaFpl[index+1].Name))
            TmpSegment.Route = DrawPolarStraightLine(StartPoint = EndOfArcPoint,
                                                   EndPoint   = GamaFpl[index+1])
        elif not GamaFpl[index].GapFollows:
          print("calculating 2D straight line from " + str(GamaFpl[index].Name) + " to " + str(GamaFpl[index+1].Name))
          TmpSegment.Route = DrawPolarStraightLine(StartPoint = GamaFpl[index],
                                                   EndPoint   = GamaFpl[index+1])
          output.append(TmpSegment)
  return output

def RenderWps(WpList : list[FplWaypoint.FplWaypoint],
              is3D : bool = True) -> list[GraphWpMarker]:
  output : list[GraphWpMarker] = []
  for point in WpList:
    TmpGraphWp = GraphWpMarker()
    X,Y = GeoSolver.LatLon2XY(Lat=point.Lat,
                                Lon=point.Lon,
                                OriginLat=MapCenter[0],
                                OriginLon=MapCenter[1])
    Theta,Rho = GeoSolver.XY2ThetaRho(X=X,Y=Y)
    TmpGraphWp.SetPolarPosition(Rho=Rho,Theta=Theta)
    try:
      TmpGraphWp.SetMarker(Marker=Type_marker_dict[point.GetType()])
    except KeyError:
      TmpGraphWp.Marker = MARKER_NULL
    try:
      TmpGraphWp.SetColor(Color=Type_color_dict[point.GetType()])
    except KeyError:
      TmpGraphWp.Color = "k"
    TmpGraphWp.SetName(Name=point.Name)
    output.append(TmpGraphWp)
  return output
  