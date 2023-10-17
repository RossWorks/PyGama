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
    self.UpdateExpFp()

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
      self.Waypoints.insert(InsertInPos-1, Wpt)
    self.UpdateExpFp()
    
  def RemoveWp(self, DeleteIndex : int):
    if (DeleteIndex < 1 or DeleteIndex > len(self.Waypoints)):
      return
    self.Waypoints.pop(DeleteIndex-1)
    self.UpdateExpFp()

  def UpdateExpFp(self):
    self.ExpandedWaypoints.clear()
    X = 0.0
    Y = 0.0
    Z = 0.0
    if len(self.Waypoints) == 1:
      X, Y, Z = GeoSolver.LatLon2XYZ(Lat = self.Waypoints[0].Lat,
                                     Lon = self.Waypoints[0].Lon)
      NewGamaWp = GamaWaypoints.GamaFplWaypoint(Id=1,
                                                Name=self.Waypoints[0].Name,
                                                Type=self.Waypoints[0].Type,
                                                Class=self.Waypoints[0].Class,
                                                X=X, Y=Y, Z=Z,
                                                GapFollows=True,
                                                NextConnect=0)
      self.ExpandedWaypoints.append(NewGamaWp)
      return
    for Index in range(0, len(self.Waypoints)):
      if Index == len(self.Waypoints):
        X, Y, Z = GeoSolver.LatLon2XYZ(Lat = self.Waypoints[0].Lat,
                                       Lon = self.Waypoints[0].Lon)
        NewGamaWp = GamaWaypoints.GamaFplWaypoint(Id=1,
                                                  Name  = self.Waypoints[Index].Name,
                                                  Type  = self.Waypoints[Index].Type,
                                                  Class = self.Waypoints[Index].Class,
                                                  X=X, Y=Y, Z=Z,
                                                  GapFollows=True,
                                                  NextConnect=0)
        self.ExpandedWaypoints.append(NewGamaWp)
      else:
        if False: #not self.Waypoints[Index].FlyOver:
          X, Y, Z = GeoSolver.LatLon2XYZ(Lat = self.Waypoints[0].Lat,
                                         Lon = self.Waypoints[0].Lon)
          TmpListOfWp = GeoSolver.SolveFlyBy(LatFrom = self.Waypoints[Index-1].Lat,
                                             LonFrom = self.Waypoints[Index-1].Lon,
                                             LatTo   = self.Waypoints[Index].Lat,
                                             LonTo   = self.Waypoints[Index].Lon,
                                             LatNext = self.Waypoints[Index+1].Lat,
                                             LonNext = self.Waypoints[Index+1].Lon)
          self.ExpandedWaypoints.append(TmpListOfWp)
        else:
          X, Y, Z = GeoSolver.LatLon2XYZ(Lat = self.Waypoints[0].Lat,
                                         Lon = self.Waypoints[0].Lon)
          NewGamaWp = GamaWaypoints.GamaFplWaypoint(Id=1,
                                                  Name  = self.Waypoints[Index].Name,
                                                  Type  = self.Waypoints[Index].Type,
                                                  Class = self.Waypoints[Index].Class,
                                                  X=X, Y=Y, Z=Z,
                                                  GapFollows=True,
                                                  NextConnect=0)
          self.ExpandedWaypoints.append(NewGamaWp)
    
  def GetGraphicalGamaPoints(self) -> list[list[float]]:
    output : list[list[float]] = []
    for Point in self.ExpandedWaypoints:
      output.append([Point.X,Point.Y, Point.Z])
    return output