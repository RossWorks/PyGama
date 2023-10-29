from . import FlightPlan as Fp, GeoSolver
import math, numpy as np

class GraphFpSegment:
  Intended : bool
  Route : np.ndarray
  Color : str

  def __init__(self) -> None:
    self.Intended = False
    self.Route = 0.0 * np.zeros(shape=(100,3), dtype=np.float64)
    self.Color = 'k'


def RenderWorld(LatRes : int = 20, LonRes : int = 20) -> dict[str : np.ndarray]:
  output : dict[str:np.ndarray] = {}
  u = np.linspace(0, 2 * np.pi, LonRes)
  v = np.linspace(0, np.pi, LatRes)
  output['X'] = GeoSolver.EARTH_RADIUS * np.outer(np.cos(u), np.sin(v))
  output['Y'] = GeoSolver.EARTH_RADIUS * np.outer(np.sin(u), np.sin(v))
  output['Z'] = GeoSolver.EARTH_RADIUS * np.outer(np.ones(np.size(u)), np.cos(v))
  return output

def DrawGreatCircle(StartPoint : Fp.GamaWaypoints.GamaFplWaypoint, 
                    EndPoint : Fp.GamaWaypoints.GamaFplWaypoint) -> np.ndarray:
  output = np.zeros(shape=(100,1))
  p1 = np.array([StartPoint.X,StartPoint.Y, StartPoint.Z])
  p2 = np.array([EndPoint.X,EndPoint.Y, EndPoint.Z])
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


def RenderGamaFpl(GamaFpl : list[Fp.GamaWaypoints.GamaFplWaypoint]) -> list[GraphFpSegment]:
  output = list()
  TmpSegment = GraphFpSegment()
  FpSize = len(GamaFpl)
  NextSegIsArc : bool = False
  if FpSize == 1:
    TmpSegment.Color = 'k'
    TmpSegment.Route[0,0] = GamaFpl[0].X
    output.append(TmpSegment)
  else:
    for index in range(0,FpSize-1):
      TmpSegment = GraphFpSegment()
      NextSegIsArc = (Fp.GamaWaypoints.ConnectionType[GamaFpl[index].NextSeg] == Fp.GamaWaypoints.ARC)
      TmpSegment.Intended = False
      if NextSegIsArc:
        pass
      else:
       try:
        TmpSegment.Route = DrawGreatCircle(StartPoint = GamaFpl[index],
                                           EndPoint   = GamaFpl[index+1])
       except IndexError:
         print("Failed @ Index = " + str(index))
      output.append(TmpSegment)
  return output
  