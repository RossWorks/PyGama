from . import FlightPlan as Fp, GeoSolver, FplWaypoint, GamaSettings
import numpy as np

CDScenter = [45.5, 8.7]

#this dict hold the conversion factor from meters to [key]
Length_conversion_factor : dict[str:float] = {"METERS" : 1,
                                              "NAUTICAL_MILES" : 0.00053996,
                                              "STATUTE_MILES" : 0.000621504,
                                              "KILOMETERS" : 0.001,
                                              "FEET" : 3}

CDSsettings = GamaSettings.CDSsettings("./Settings/New.ini")

def DecDeg2DDMM_MM(Degrees : float) -> str:
  output = ""
  Deg = int(Degrees)
  Min = (Degrees - Deg) * 60
  output = str(Deg) + "° " + str(Min) + "\'"
  return output

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
    self.Marker = CDSsettings.MARKER_NULL
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
                                    OriginLat=CDScenter[0], OriginLon=CDScenter[1]))
  print("p1 = " + str(p1))
  p2 = np.array(GeoSolver.LatLon2XY(Lat=EndPoint.Lat, Lon=EndPoint.Lon,
                                    OriginLat=CDScenter[0], OriginLon=CDScenter[1]))
  print("p2 = " + str(p2))
  pre_output[:,0] = np.linspace(p1[0],p2[0],100)
  pre_output[:,1] = np.linspace(p1[1],p2[1],100)
  output[:,0] = np.arctan2(pre_output[:,0],pre_output[:,1])
  output[:,1] = np.sqrt(np.power(pre_output[:,1],2)+np.power(pre_output[:,0],2))\
                * Length_conversion_factor[CDSsettings.GetLengthSetting()]
  print(output)
  return output

def DrawGreatCircle(StartPoint : Fp.GamaWaypoints.GamaFplWaypoint, 
                    EndPoint   : Fp.GamaWaypoints.GamaFplWaypoint) -> np.ndarray:
  output = np.zeros(shape=(100,3))
  Xyz = GeoSolver.LatLon2XYZ(Lat=StartPoint.Lat, Lon=StartPoint.Lon)
  p1 = np.array(Xyz)
  print("p1 = " + str(p1))
  Xyz = GeoSolver.LatLon2XYZ(Lat=EndPoint.Lat, Lon=EndPoint.Lon)
  p2 = np.array(Xyz)
  print("p2 = " + str(p2))
  n = (np.cross(p1,p2))
  n = n/np.sqrt(np.dot(n,n))
  print("n = " + str(n))
  i = p1/np.sqrt(np.dot(p1,p1))
  j = np.cross(n,i)
  print("i = " + str(i)+ "\nj = " + str(j))
  delta_angle = np.arccos(np.dot(p1,p2)/(np.linalg.norm(p1)*np.linalg.norm(p2)))
  t = np.resize(a=np.linspace(start=0,stop=delta_angle,num=100),
                new_shape=(100,1))
  output = GeoSolver.EARTH_RADIUS*(np.cos(t)*i+np.sin(t)*j)
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
      TmpSegment.Color = 'm' if index == 0 else 'k'
      NextSegIsArc = (Fp.GamaWaypoints.ConnectionType[GamaFpl[index].NextSeg] == Fp.GamaWaypoints.ARC)
      TmpSegment.Intended = False
      if NextSegIsArc:
        pass
      else:
        if Use3D:
          print("calculating 3D great circle #" + str(index))
          TmpSegment.Route = DrawGreatCircle(StartPoint = GamaFpl[index],
                                             EndPoint   = GamaFpl[index+1])
        else:
          print("calculating 2D straight line #" + str(index))
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
                                OriginLat=CDScenter[0],
                                OriginLon=CDScenter[1])
    Theta,Rho = GeoSolver.XY2ThetaRho(X=X,Y=Y)
    Rho = Rho * Length_conversion_factor[CDSsettings.GetLengthSetting()]
    TmpGraphWp.SetPolarPosition(Rho=Rho,Theta=Theta)
    Marker, Color = CDSsettings.GetWpMarker_Color(Point=point)
    TmpGraphWp.SetMarker(Marker=Marker)
    TmpGraphWp.SetColor(Color=Color)
    TmpGraphWp.SetName(Name=point.Name)
    output.append(TmpGraphWp)
  return output
  