if __name__ == "__main__":
  print("FlightPlan module for Gama package")
  print("Standalone operation NOT ALLOWED")
  exit()

from . import FplWaypoint, GamaWaypoints, GeoSolver

FPL_MAX_SIZE : int = 200

APPEND_INDEX : int = 0

class FlightPlan:
  Waypoints : list[FplWaypoint.FplWaypoint]
  ExpandedWaypoints : list[GamaWaypoints.GamaFplWaypoint]

  def __init__(self, PposLat : float, PposLon : float) -> None:
    self.Waypoints : list[FplWaypoint.FplWaypoint] = []
    self.ExpandedWaypoints : list[GamaWaypoints.GamaFplWaypoint] = []
    NewFromWpt = FplWaypoint.FplWaypoint(Id=0,
                                         Name="*PPOS*",
                                         Type=5,
                                         Class=0,
                                         Lat=PposLat,
                                         Lon=PposLon,
                                         isFlyOver=True)
    self.Waypoints.append(NewFromWpt)
    self.RecomputeExpFp()

  def __repr__(self, Gama : bool = False) -> str:
    output : str = ""
    if Gama:
      for Waypoint in self.ExpandedWaypoints:
        output += str(Waypoint)
    else:
      for Waypoint in self.Waypoints:
        output += str(Waypoint)
    return output
  
  def InsertWp(self, Wpt : FplWaypoint.FplWaypoint,
               InsertInPos : int = APPEND_INDEX):
    '''This function inserts Wpt @ InsertInPos position (default is 0 for append)
    Asking for InsertInPos = 1 means replacing the first Wp'''
    if (InsertInPos > FPL_MAX_SIZE):
      return
    elif (InsertInPos <= 0 or InsertInPos > len(self.Waypoints)):
      self.Waypoints.append(Wpt)
    elif (InsertInPos == 1):
      self.Waypoints.insert(1,Wpt)
      self.Waypoints.pop(0)
    else:
      self.Waypoints.insert(InsertInPos-1, Wpt)
    self.RecomputeExpFp()
    
  def RemoveWp(self, DeleteIndex : int):
    if (DeleteIndex < 1 or DeleteIndex > len(self.Waypoints)):
      return
    self.Waypoints.pop(DeleteIndex-1)
    self.RecomputeExpFp()

  def RecomputeExpFp(self):
    PseudoCounter : int = 1
    self.ExpandedWaypoints.clear()
    if len(self.Waypoints) == 1:
      NewGamaWp = GamaWaypoints.GamaFplWaypoint(Id=1,
                                                Name=self.Waypoints[0].Name,
                                                Type=self.Waypoints[0].Type,
                                                Class=self.Waypoints[0].Class,
                                                Lat = self.Waypoints[0].Lat,
                                                Lon = self.Waypoints[0].Lon,
                                                GapFollows=True,
                                                NextConnect=0)
      self.ExpandedWaypoints.append(NewGamaWp)
      return
    for Index in range(0, len(self.Waypoints)):
      if Index == len(self.Waypoints):
        NewGamaWp = GamaWaypoints.GamaFplWaypoint(Id=1,
                                                  Name  = self.Waypoints[Index].Name,
                                                  Type  = self.Waypoints[Index].Type,
                                                  Class = self.Waypoints[Index].Class,
                                                  Lat = self.Waypoints[Index].Lat,
                                                  Lon = self.Waypoints[Index].Lon,
                                                  GapFollows=True,
                                                  NextConnect=0)
        self.ExpandedWaypoints.append(NewGamaWp)
      else:
        if (not self.Waypoints[Index].FlyOver) and (Index > 0) and (Index < (len(self.Waypoints)-1)):
          TmpListOfWp = GeoSolver.SolveFlyBy(LatFrom = self.Waypoints[Index-1].Lat,
                                             LonFrom = self.Waypoints[Index-1].Lon,
                                             LatTo   = self.Waypoints[Index].Lat,
                                             LonTo   = self.Waypoints[Index].Lon,
                                             LatNext = self.Waypoints[Index+1].Lat,
                                             LonNext = self.Waypoints[Index+1].Lon)
          
          GamaPwp1 = GamaWaypoints.GamaFplWaypoint(Id=1,
                                                   Name  = "Pwp" + str(PseudoCounter),
                                                   Type  = self.Waypoints[Index].Type,
                                                   Class = self.Waypoints[Index].Class,
                                                   Lat   = TmpListOfWp[0],
                                                   Lon   = TmpListOfWp[1],
                                                   GapFollows=True,
                                                   NextConnect=0)
          GamaPwp1_2=GamaWaypoints.GamaFplWaypoint(Id=1,
                                                   Name  = "Pwp" + str(PseudoCounter),
                                                   Type  = self.Waypoints[Index].Type,
                                                   Class = self.Waypoints[Index].Class,
                                                   Lat   = TmpListOfWp[0],
                                                   Lon   = TmpListOfWp[1],
                                                   GapFollows=False,
                                                   NextConnect=0)
          PseudoCounter += 1
          GamaToWp = GamaWaypoints.GamaFplWaypoint(Id=1,
                                                   Name  = self.Waypoints[Index].Name ,
                                                   Type  = self.Waypoints[Index].Type,
                                                   Class = self.Waypoints[Index].Class,
                                                   Lat   = TmpListOfWp[2],
                                                   Lon   = TmpListOfWp[3],
                                                   GapFollows=True,
                                                   NextConnect=0)
          GamaPwp2 = GamaWaypoints.GamaFplWaypoint(Id=1,
                                                   Name  = "Pwp" + str(PseudoCounter),
                                                   Type  = self.Waypoints[Index].Type,
                                                   Class = self.Waypoints[Index].Class,
                                                   Lat   = TmpListOfWp[4],
                                                   Lon   = TmpListOfWp[5],
                                                   GapFollows=False,
                                                   NextConnect=0)
          PseudoCounter += 1
          self.ExpandedWaypoints.append(GamaPwp1)
          self.ExpandedWaypoints.append(GamaToWp)
          self.ExpandedWaypoints.append(GamaPwp1_2)
          self.ExpandedWaypoints.append(GamaPwp2)
          
        else:
          NewGamaWp = GamaWaypoints.GamaFplWaypoint(Id=1,
                                                  Name  = self.Waypoints[Index].Name,
                                                  Type  = self.Waypoints[Index].Type,
                                                  Class = self.Waypoints[Index].Class,
                                                  Lat = self.Waypoints[Index].Lat,
                                                  Lon = self.Waypoints[Index].Lon,
                                                  GapFollows=False,
                                                  NextConnect=0)
          self.ExpandedWaypoints.append(NewGamaWp)
