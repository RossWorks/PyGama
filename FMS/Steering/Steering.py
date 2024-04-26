import numpy as np
from ..Common import GeoSolver

class SteerMachine:
    
  def __init__(self) -> None:
    self.MyLat = np.float64(0.0)
    self.MyLon = np.float64(0.0)
    self.MyHdg = np.float64(0.0)
    self.DestLat = np.float64(0.0)
    self.DestLon = np.float64(0.0)

  def UpdateDestination(self, DestLat, DestLon):
    self.DestLat = np.float64(DestLat)
    self.DestLon = np.float64(DestLon)

  def UpdatePpos(self, lat : np.float64, lon : np.float64, hdg : np.float64):
    self.MyHdg = hdg
    self.MyLat = lat
    self.MyLon = lon

  def GetRollSteer(self) -> np.float64:
    TgtHdg = GeoSolver.GreatCircleInitAz(LatFrom= self.MyLat, LonFrom= self.MyLon,
                                         LatTo= self.DestLat, LonTo= self.DestLon)
    DeltaHdg = TgtHdg - self.MyHdg
    if DeltaHdg > np.pi:
      DeltaHdg -= 2*np.pi
    elif DeltaHdg <  (-1 * np.pi):
      DeltaHdg += 2*np.pi
    output = .5 * (DeltaHdg)
    if output > np.deg2rad(25):
      output = np.deg2rad(25)
    elif output < np.deg2rad(-25):
      output = np.deg2rad(-25)
    return output
  
  def ToWptIsSeq(self) -> bool:
    Distance2Go = GeoSolver.GreatCircleDistance(LatFrom= self.MyLat, LonFrom= self.MyLon,
                                                LatTo= self.DestLat, LonTo= self.DestLon)
    return Distance2Go < (0.8 * 1852)