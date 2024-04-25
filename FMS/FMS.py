from . import FlightPlan 
import numpy as np
from . import Steering


class BestData:
  lat : np.float64
  lon : np.float64
  Speed : np.float64
  Heading : np.float64
  SteerCmd : np.float64
  def __init__(self) -> None:
    self.lat = np.float64(0.0)
    self.lon = np.float64(0.0)
    self.Speed = np.float64(0.0)
    self.Heading = np.float64(0.0)
    self.SteerCmd = np.float64(0.0)

class FMS:

  def __init__(self) -> None:
    self.HeloState = BestData()
    self.FlightPlan = FlightPlan.FlightPlan(PposLat=self.HeloState.lat,
                                            PposLon=self.HeloState.lon)
    self.SteerMachine = Steering.SteerMachine()
  
  def ElaborationStep(self):
    if len(self.FlightPlan.ExpandedWaypoints) < 2:
      return 0
    self.SteerMachine.MyLat = self.HeloState.lat
    self.SteerMachine.MyLon = self.HeloState.lon
    self.SteerMachine.MyHdg = self.HeloState.Heading
    self.SteerMachine.UpdateDestination(DestLat=self.FlightPlan.ExpandedWaypoints[1].Lat,
                                        DestLon=self.FlightPlan.ExpandedWaypoints[1].Lon)
    self.HeloState.SteerCmd = self.SteerMachine.GetRollSteer()
    if self.SteerMachine.ToWptIsSeq():
      self.FlightPlan.Waypoints.pop(0)
      self.FlightPlan.RecomputeExpFp()
    

  def InsertWpInAfpl(self, Wpt : FlightPlan.FplWaypoint,
               InsertInPos : int = FlightPlan.APPEND_INDEX):
    self.FlightPlan.InsertWp(Wpt=Wpt, InsertInPos=InsertInPos)
  
  def RemoveWpFromAfpl(self,DeleteIndex : int):
    self.FlightPlan.RemoveWp(DeleteIndex=DeleteIndex)

  def DeselectAfpl(self):
    self.FlightPlan = FlightPlan.FlightPlan(PposLat=self.HeloState.lat,
                                            PposLon=self.HeloState.lon)
    
  def LoadUsrFpl(self, FilePath):
    FilePtr = open(file=FilePath, mode='r')
    self.DeselectAfpl()
    Index = 1
    for line in FilePtr:
      WpInfo=line.split(sep=';')
      MyWp = FlightPlan.FplWaypoint.FplWaypoint(Id = Index, Name=WpInfo[0], Type=int(WpInfo[1].strip()),
                                                Class=int(WpInfo[2].strip()),
                                                Lat=float(WpInfo[3]),
                                                Lon=float(WpInfo[4]),
                                                isFlyOver= WpInfo[5] == "FLY OV")
      self.FlightPlan.InsertWp(Wpt=MyWp, InsertInPos=Index)
      Index += 1
    FilePtr.close()

  def InternalDTO(self, WpIndex):
    self.FlightPlan.InternalDirTo(DtoIndex=WpIndex, PposLat=self.HeloState.lat,
                                  PposLon= self.HeloState.lon)

  def SaveAfpl(self, SaveFileName : str):
    FilePtr = open(SaveFileName, mode='w')
    FileContent = self.FlightPlan.FormatForFile()
    FilePtr.writelines(FileContent)
    FilePtr.close()

  def UpdateHeloState(self, Lat : float,
                      Lon : float,
                      Hdg : float,
                      Gs : float):
    self.HeloState.lat = np.float64(Lat)
    self.HeloState.lon = np.float64(Lon)
    self.HeloState.Heading = np.float64(Hdg)
    self.HeloState.Speed = np.float64(Gs)