from . import FlightPlan, Steering, Common
from EDCU import EDCU
import numpy as np


class BestData:

  def __init__(self) -> None:
    self.lat = np.float64(0.0)
    self.lon = np.float64(0.0)
    self.Speed = np.float64(0.0)
    self.Heading = np.float64(0.0)
    self.SteerCmd = np.float64(0.0)
    self.Time2Go_To = np.int32(0)
    self.Distance2Go_To = np.float64(0.0)
    self.Time2Go_Next = np.int32(0)
    self.Distance2Go_Next = np.float64(0.0)
    self.Time2Go_Dest = np.int32(0)
    self.Distance2Go_Dest = np.float64(0.0)
    self.XTE = np.float64(0.0)


class FMS:

  def __init__(self) -> None:
    self.HeloState = BestData()
    self.FlightPlan = FlightPlan.FlightPlan.FlightPlan(PposLat=self.HeloState.lat,
                                                       PposLon=self.HeloState.lon)
    self.SteerMachine = Steering.Steering.SteerMachine()
  
  def ElaborationStep(self):
    self.FlightPlan.CheckAchievement(PposLat=self.HeloState.lat,
                                     PposLon=self.HeloState.lon)
    self.HeloState.SteerCmd = self.SteerExecutionStep()    

  def InsertWpInAfpl(self, Wpt : FlightPlan.FplWaypoint,
                     InsertInPos : int = FlightPlan.FlightPlan.APPEND_INDEX):
    self.FlightPlan.InsertWp(Wpt=Wpt, InsertInPos=InsertInPos)
  
  def RemoveWpFromAfpl(self,DeleteIndex : int):
    self.FlightPlan.RemoveWp(DeleteIndex=DeleteIndex)

  def DeselectAfpl(self):
    self.FlightPlan = FlightPlan.FlightPlan.FlightPlan(PposLat=self.HeloState.lat,
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

  def SwitchFlyByState(self, Index):
    self.FlightPlan.Waypoints[Index].FlyOver = not self.FlightPlan.Waypoints[Index].FlyOver
    self.FlightPlan.RecomputeExpFp()

  def GetFlyByState(self, Index) -> bool:
    return self.FlightPlan.Waypoints[Index].FlyOver

  def UpdateHeloState(self, Lat : float,
                      Lon : float,
                      Hdg : float,
                      Gs : float):
    self.HeloState.lat = np.float64(Lat)
    self.HeloState.lon = np.float64(Lon)
    self.HeloState.Heading = np.float64(Hdg)
    self.HeloState.Speed = np.float64(Gs)

  def SteerExecutionStep(self) -> np.float64:
    if len(self.FlightPlan.ExpandedWaypoints) < 2:
      return np.float64(0.0)
    self.SteerMachine.UpdatePpos(lat = self.HeloState.lat,
                                 lon = self.HeloState.lon,
                                 hdg = self.HeloState.Heading)
    self.SteerMachine.UpdateDestination(DestLat=self.FlightPlan.ExpandedWaypoints[1].Lat,
                                        DestLon=self.FlightPlan.ExpandedWaypoints[1].Lon)
    self.SteerMachine.UpdateOrigin(OriginLat=self.FlightPlan.ExpandedWaypoints[0].Lat,
                                   OriginLon=self.FlightPlan.ExpandedWaypoints[0].Lon)
    SteerCmd = self.SteerMachine.GetRollSteer()
    self.HeloState.XTE = self.SteerMachine.XTE
    return SteerCmd

  def DataForEDCU(self) -> EDCU.EDCUdata:
    output = EDCU.EDCUdata()
    output.Lat = self.HeloState.lat
    output.Lon = self.HeloState.lon
    output.GS  = self.HeloState.Speed
    output.Hdg = self.HeloState.Heading
    output.Distance2Go_To   = self.HeloState.Distance2Go_To
    output.Distance2Go_Next = self.HeloState.Distance2Go_Next
    output.Distance2Go_Dest = self.HeloState.Distance2Go_Dest
    output.Time2Go_To   = self.HeloState.Time2Go_To
    output.Time2Go_Next = self.HeloState.Time2Go_Next
    output.Time2Go_Dest = self.HeloState.Time2Go_Dest
    output.Fpl = self.FlightPlan.Waypoints
    output.XTE = self.HeloState.XTE
    return output

  def PerfoStep(self):
    if len(self.FlightPlan.Waypoints) < 2:
      self.HeloState.Distance2Go_To = np.NaN
      self.HeloState.Distance2Go_Next = np.NaN
      self.HeloState.Distance2Go_Dest = np.NaN
      self.HeloState.Time2Go_To = np.NaN
      self.HeloState.Time2Go_Next = np.NaN
      self.HeloState.Time2Go_Dest = np.NaN
      return  
    PposLat = self.HeloState.lat
    PposLon = self.HeloState.lon
    ToLat   = self.FlightPlan.Waypoints[1].Lat
    ToLon   = self.FlightPlan.Waypoints[1].Lon
    self.HeloState.Distance2Go_To = Common.GeoSolver.GreatCircleDistance(LatFrom=PposLat, LonFrom=PposLon, LatTo=ToLat, LonTo=ToLon)
    self.HeloState.Time2Go_To = self.HeloState.Distance2Go_To / self.HeloState.Speed
    if len(self.FlightPlan.Waypoints) > 2:
      NextLat   = self.FlightPlan.Waypoints[2].Lat
      NextLon   = self.FlightPlan.Waypoints[2].Lon
      self.HeloState.Distance2Go_Next = Common.GeoSolver.GreatCircleDistance(LatFrom=ToLat, LonFrom=ToLon, LatTo=NextLat, LonTo=NextLon)
      self.HeloState.Time2Go_Next = self.HeloState.Distance2Go_Next / self.HeloState.Speed
    self.HeloState.Time2Go_Dest = np.NaN
    self.HeloState.Distance2Go_Dest = np.NaN