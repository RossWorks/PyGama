if __name__ == "__main__":
  print("FlightPlan module for Gama package")
  print("Standalone operation NOT ALLOWED")
  exit()

from . import FplWaypoint
from CDS import GamaWaypoint
from FMS.Common import GeoSolver
import numpy as np

FPL_MAX_SIZE : int = 200
ACHIEVEMENT_THRS : float = 0.5 * 1852
APPEND_INDEX : int = 0

class FlightPlan:
  Waypoints : list[FplWaypoint.FplWaypoint]
  ExpandedWaypoints : list[GamaWaypoint.GamaWaypoint]

  def __init__(self, PposLat : float, PposLon : float) -> None:
    self.Waypoints : list[FplWaypoint.FplWaypoint] = []
    self.ExpandedWaypoints : list[GamaWaypoint.GamaFplWaypoint] = []
    NewFromWpt = FplWaypoint.FplWaypoint(Id=0,
                                         Name="*PPOS*",
                                         Type=5,
                                         Class=0,
                                         Lat=PposLat,
                                         Lon=PposLon,
                                         isFlyOver=True)
    self.Waypoints.append(NewFromWpt)
    self.AttributesComputation()
    self.RecomputeExpFp()

  def __str__(self) -> str:
    output : str = ""
    Counter : int = 1
    for Waypoint in self.ExpandedWaypoints:
      output += str(Counter).rjust(3) + " --> " + str(Waypoint)
      Counter += 1
    return output
  
  def CheckAchievement(self, PposLat : float, PposLon : float) -> dict:
    output = dict()
    if len(self.Waypoints) < 2:
      output["valid"] = False
      return output
    Distance2Go = GeoSolver.GreatCircleDistance(PposLat,PposLon, self.Waypoints[1].Lat,self.Waypoints[1].Lon)
    if Distance2Go > (ACHIEVEMENT_THRS + self.Waypoints[1].TurnAnticipation):
      output["valid"] = False
      return output
    output["turnradius"] = self.Waypoints[1].TurnRadius
    output["trackchange"] = self.Waypoints[1].TrackChange
    output["valid"] = True
    self.RemoveWp(DeleteIndex=1)
    return output 
  
  def FormatForFile(self) -> str:
    output : str = ""
    for Waypoint in self.Waypoints:
      output += Waypoint.PrintForFile()
    return output
  
  def InsertWp(self, Wpt : FplWaypoint.FplWaypoint,
               InsertInPos : int = APPEND_INDEX):
    '''This function inserts Wpt @ InsertInPos position (default is 0 for append)
    Asking for InsertInPos = 1 means replacing the first Wp'''
    if (InsertInPos > FPL_MAX_SIZE):
      print("Flight Plan is not that big: " + str(InsertInPos) + " > " + str(FPL_MAX_SIZE))
      return
    elif (InsertInPos <= 0 or InsertInPos > len(self.Waypoints)):
      print("Waypoint insertion @ line " + str(InsertInPos))
      if InsertInPos == 2:
        Wpt.WpReprCat = 1
        if len(self.Waypoints) > 1:
          self.Waypoints[1].WpReprCat = 2
      self.Waypoints.append(Wpt)
    elif (InsertInPos == 1):
      print("Substitution of FROM waypoint")
      self.Waypoints.insert(1,Wpt)
      self.Waypoints.pop(0)
      self.Waypoints[0].WpReprCat = 0
    else:
      print("Waypoint insertion @ line " + str(InsertInPos))
      self.Waypoints.insert(InsertInPos-1, Wpt)
    self.AttributesComputation()
    self.RecomputeExpFp()
    
  def RemoveWp(self, DeleteIndex : int):
    if (DeleteIndex < 1 or DeleteIndex > len(self.Waypoints)):
      print("Flight Plan is not that big: " + str(DeleteIndex) + " > " + str(len(self.Waypoints)))
      return
    print("Waypoint deletion from line " + str(DeleteIndex))
    self.Waypoints.pop(DeleteIndex-1)
    self.AttributesComputation()
    self.RecomputeExpFp()

  def InternalDirTo(self, DtoIndex : int, PposLat : float, PposLon : float):
    self.Waypoints =self.Waypoints[DtoIndex:]
    PPOS = FplWaypoint.FplWaypoint(Id=0,Name="*PPOS*", Type=5, Class=0,
                                     Lat=PposLat,
                                     Lon=PposLon,
                                     isFlyOver=True)
    self.Waypoints.insert(0, PPOS)
    self.Waypoints[0].WpReprCat = 0
    self.Waypoints[1].WpReprCat = 1
    self.AttributesComputation()
    self.RecomputeExpFp()

  
  def AttributesComputation(self):
    self.Waypoints[0].SetFlyOver(FlyOver=True)
    for index in range(1, len(self.Waypoints) - 1):
        FlyByData = GeoSolver.SolveFlyBy(LatFrom=self.Waypoints[index-1].Lat,
                                         LonFrom=self.Waypoints[index-1].Lon,
                                         LatTo=self.Waypoints[index].Lat,
                                         LonTo=self.Waypoints[index].Lon,
                                         LatNext=self.Waypoints[index+1].Lat,
                                         LonNext=self.Waypoints[index+1].Lon)
        if FlyByData.Valid:
            self.Waypoints[index].TurnAnticipation = GeoSolver.GreatCircleDistance(LatFrom=self.Waypoints[index].Lat,
                                                                                   LonFrom=self.Waypoints[index].Lon,
                                                                                   LatTo=FlyByData.Pwp1_Lat,
                                                                                   LonTo=FlyByData.Pwp1_Lon)
            self.Waypoints[index].TurnRadius = 4 * 1852
        else:
            self.Waypoints[index].TurnAnticipation = 0
            self.Waypoints[index].TurnRadius = 4 * 1852 * 0
        for element in self.Waypoints:
          print("Turn anticipation for " + element.Name + " WP = " + str(element.TurnAnticipation))
        self.Waypoints[index].TrackChange = FlyByData.TrkChange * (-1 if FlyByData.LeftTurn else 1)
        

  def RecomputeExpFp(self):
    print("Recompute of Gama Flight Plan")
    PseudoCounter : int = 1
    self.ExpandedWaypoints.clear()
    if len(self.Waypoints) == 1:
      NewGamaWp = GamaWaypoint.GamaWaypoint(Id=1,
                                               Name=self.Waypoints[0].Name,
                                               Type=self.Waypoints[0].Type,
                                               Class=self.Waypoints[0].Class,
                                               Lat = self.Waypoints[0].Lat,
                                               Lon = self.Waypoints[0].Lon,
                                               GapFollows=True,
                                               ConicApp=False,
                                               isGraphical=True)
      self.ExpandedWaypoints.append(NewGamaWp)
      return
    for Index in range(0, len(self.Waypoints)):
      if Index == len(self.Waypoints):
        print("Inserting last waypoint: " + self.Waypoints[Index].Name)
        NewGamaWp = GamaWaypoint.GamaFplWaypoint(Id=1,
                                                  Name  = self.Waypoints[Index].Name,
                                                  Type  = self.Waypoints[Index].Type,
                                                  Class = self.Waypoints[Index].Class,
                                                  Lat = self.Waypoints[Index].Lat,
                                                  Lon = self.Waypoints[Index].Lon,
                                                  GapFollows=True,
                                                  ConicApp=0)
        self.ExpandedWaypoints.append(NewGamaWp)
      else:
        if (not self.Waypoints[Index].FlyOver) and (Index > 0) and (Index < (len(self.Waypoints)-1)):
          print("computing Fly-By on " + self.Waypoints[Index].Name)
          FlyByData   = GeoSolver.SolveFlyBy(LatFrom = self.Waypoints[Index-1].Lat,
                                             LonFrom = self.Waypoints[Index-1].Lon,
                                             LatTo   = self.Waypoints[Index].Lat,
                                             LonTo   = self.Waypoints[Index].Lon,
                                             LatNext = self.Waypoints[Index+1].Lat,
                                             LonNext = self.Waypoints[Index+1].Lon)
          
          GamaPwp1 = GamaWaypoint.GamaWaypoint(Id=1,
                                                   Name  = "Pwp" + str(PseudoCounter),
                                                   Type  = 0,
                                                   Class = 0,
                                                   Lat   = FlyByData.Pwp1_Lat,
                                                   Lon   = FlyByData.Pwp1_Lon,
                                                   GapFollows=True,
                                                   ConicApp=False,
                                                   isGraphical=False)
          GamaPwp1_2=GamaWaypoint.GamaWaypoint(Id=1,
                                                   Name          = "Pwp" + str(PseudoCounter),
                                                   Type          = 0,
                                                   Class         = 0,
                                                   Lat           = FlyByData.Pwp1_Lat,
                                                   Lon           = FlyByData.Pwp1_Lon,
                                                   GapFollows    = False,
                                                   ConicApp      = True,
                                                   isGraphical   = False,
                                                   ArcRadius     = FlyByData.ArcRadius,
                                                   ArcIsLeftHand = FlyByData.LeftTurn,
                                                   TrackChange   = FlyByData.TrkChange,
                                                   ArcCenterLat  = FlyByData.ArcCenterLat,
                                                   ArcCenterLon  = FlyByData.ArcCenterLon)
          PseudoCounter += 1
          GamaToWp = GamaWaypoint.GamaWaypoint(Id=1,
                                                   Name        = self.Waypoints[Index].Name,
                                                   Type        = self.Waypoints[Index].Type,
                                                   Class       = self.Waypoints[Index].Class,
                                                   Lat         = FlyByData.To_Lat,
                                                   Lon         = FlyByData.To_Lon,
                                                   GapFollows  = FlyByData.Valid,
                                                   ConicApp    = False,
                                                   isGraphical = True)
          GamaPwp2 = GamaWaypoint.GamaWaypoint(Id=1,
                                                   Name  = "Pwp" + str(PseudoCounter),
                                                   Type  = 0,
                                                   Class = 0,
                                                   Lat   = FlyByData.Pwp2_Lat,
                                                   Lon   = FlyByData.Pwp2_Lon,
                                                   GapFollows=False,
                                                   ConicApp=False,
                                                   isGraphical=False)
          PseudoCounter += 1
          if FlyByData.Valid:
            self.ExpandedWaypoints.append(GamaPwp1)
          self.ExpandedWaypoints.append(GamaToWp)
          if FlyByData.Valid:
            self.ExpandedWaypoints.append(GamaPwp1_2)
            self.ExpandedWaypoints.append(GamaPwp2)
          
        else:
          print("Crossing " + self.Waypoints[Index].Name + " as Fly-Over")
          NewGamaWp = GamaWaypoint.GamaWaypoint(Id=1,
                                                  Name  = self.Waypoints[Index].Name,
                                                  Type  = self.Waypoints[Index].Type,
                                                  Class = self.Waypoints[Index].Class,
                                                  Lat = self.Waypoints[Index].Lat,
                                                  Lon = self.Waypoints[Index].Lon,
                                                  GapFollows=False,
                                                  ConicApp=0,
                                                  isGraphical=True)
          self.ExpandedWaypoints.append(NewGamaWp)
