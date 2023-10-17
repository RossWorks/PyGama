from . import FplWaypoint, GamaWaypoints, GeoSolver

FPL_MAX_SIZE : int = 200

APPEND_INDEX : int = 0

class FlightPlan:
  Waypoints : list[FplWaypoint.FplWaypoint]
  ExpandedWaypoints : list[GamaWaypoints.GamaFplWaypoint]

  def __init__(self, PposLat : float, PposLon : float) -> None:
    self.Waypoints : list[FplWaypoint.FplWaypoint] = []
    NewFromWpt = FplWaypoint.FplWaypoint(Id=0,
                                         Name="*PPOS*",
                                         Type=5,
                                         Class=0,
                                         Lat=PposLat,
                                         Lon=PposLon,
                                         isFlyOver=True)
    self.Waypoints.append(NewFromWpt)

  def __repr__(self) -> str:
    output : str = ""
    for Waypoint in self.Waypoints:
      output += str(Waypoint)
    return output
  
  def InsertWp(self, Wpt : FplWaypoint.FplWaypoint,
               InsertInPos : int = APPEND_INDEX):
    if (InsertInPos > FPL_MAX_SIZE):
      return
    elif (InsertInPos <= 0 or InsertInPos > len(self.Waypoints)):
      self.Waypoints.append(Wpt)
    elif (InsertInPos == 1):
      self.Waypoints.insert(1,Wpt)
      self.Waypoints.pop(0)
    else:
      self.Waypoints.insert(InsertInPos, Wpt)
    
  def RemoveWp(self, DeleteIndex : int):
    if (DeleteIndex < 1 or DeleteIndex > len(self.Waypoints)):
      return
    self.Waypoints.pop(DeleteIndex-1)

  def UpdateExpFp(self):
    self.ExpandedWaypoints.clear()
    if len(self.Waypoints) == 1:
      NewGamaWp = GamaWaypoints.GamaFplWaypoint(Id=1,
                                                Name=self.Waypoints[0].Name,
                                                Type=self.Waypoints[0].Type,
                                                Class=self.Waypoints[0].Class,
                                                Lat=self.Waypoints[0].Lat,
                                                Lon=self.Waypoints[0].Lon,
                                                GapFollows=True,
                                                NextConnect=0)
      self.ExpandedWaypoints.append(NewGamaWp)
      return
    for Index in range(1, len(self.Waypoints)+1):
      if Index == len(self.Waypoints):
        NewGamaWp = GamaWaypoints.GamaFplWaypoint(Id=1,
                                                  Name  = self.Waypoints[Index].Name,
                                                  Type  = self.Waypoints[Index].Type,
                                                  Class = self.Waypoints[Index].Class,
                                                  Lat   = self.Waypoints[Index].Lat,
                                                  Lon   = self.Waypoints[Index].Lon,
                                                  GapFollows=True,
                                                  NextConnect=0)
        self.ExpandedWaypoints.append(NewGamaWp)
      else:
        if not self.Waypoints[Index].FlyOver:
          TmpListOfWp = GeoSolver.SolveFlyBy(LatFrom = self.Waypoints[Index-1].Lat,
                                             LonFrom = self.Waypoints[Index-1].Lon,
                                             LatTo   = self.Waypoints[Index].Lat,
                                             LonTo   = self.Waypoints[Index].Lon,
                                             LatNext = self.Waypoints[Index+1].Lat,
                                             LonNext = self.Waypoints[Index+1].Lon)
          self.ExpandedWaypoints.append(TmpListOfWp)
        else:
          NewGamaWp = GamaWaypoints.GamaFplWaypoint(Id=1,
                                                  Name  = self.Waypoints[Index].Name,
                                                  Type  = self.Waypoints[Index].Type,
                                                  Class = self.Waypoints[Index].Class,
                                                  Lat   = self.Waypoints[Index].Lat,
                                                  Lon   = self.Waypoints[Index].Lon,
                                                  GapFollows=True,
                                                  NextConnect=0)
          self.ExpandedWaypoints.append(NewGamaWp)
    