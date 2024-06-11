import numpy as np
from ..Common import GeoSolver

MAX_BANK = np.deg2rad(25)

class SteerMachine:
    def __init__(self) -> None:
        self.MyLat = np.float64(0.0)
        self.MyLon = np.float64(0.0)
        self.MyHdg = np.float64(0.0)
        self.DestLat = np.float64(0.0)
        self.DestLon = np.float64(0.0)
        self.OriginLat = np.float64(0.0)
        self.OriginLon = np.float64(0.0)
        self.XTE = np.float64(0.0)
        self.Mode = np.int32(0) # 0=NAV, 1=TURN
        self.StartHdg = np.float64(0.0)
        self.Speed = np.float64(0.0)
        self.TurnRadius = np.float64(0.0)
        self.TargetTrack = np.float64(0.0)

    def UpdateDestination(self, DestLat, DestLon):
        self.DestLat = np.float64(DestLat)
        self.DestLon = np.float64(DestLon)

    def UpdateOrigin(self, OriginLat, OriginLon):
        self.OriginLat = np.float64(OriginLat)
        self.OriginLon = np.float64(OriginLon)

    def UpdatePpos(self, lat: np.float64, lon: np.float64, hdg: np.float64):
        self.MyHdg = hdg
        self.MyLat = lat
        self.MyLon = lon

    def GetRollSteer(self) -> np.float64:
      if self.Mode == 0:
        DesiredTrack = GeoSolver.GreatCircleInitAz(LatFrom=self.OriginLat,
                                                   LonFrom=self.OriginLon,
                                                   LatTo=self.DestLat,
                                                   LonTo=self.DestLon)
        XTE = GeoSolver.GreatCircleCrossDistance(LatFrom=self.OriginLat,
                                                 LonFrom=self.OriginLon,
                                                 LatTo=self.DestLat,
                                                 LonTo=self.DestLon,
                                                 PposLat=self.MyLat,
                                                 PposLon=self.MyLon)
        self.XTE = XTE
        DeltaHdg = DesiredTrack - self.MyHdg
        if DeltaHdg > np.pi:
            DeltaHdg -= 2 * np.pi
        elif DeltaHdg < (-1 * np.pi):
            DeltaHdg += 2 * np.pi
        DistParam = (-0.000424069 * XTE)
        if DistParam > np.deg2rad(45.0):
            DistParam = np.deg2rad(45.0)
        elif DistParam < np.deg2rad(-45.0):
            DistParam = np.deg2rad(-45.0)
        DeltaHdg += DistParam
        output = 0.5 * (DeltaHdg)
        if output > MAX_BANK:
            output = MAX_BANK
        elif output < -MAX_BANK:
            output = -MAX_BANK
        return output
      elif self.Mode == 1:
        AngSpeed = self.Speed / self.TurnRadius
        NormAcc = np.power(AngSpeed, 2) * self.TurnRadius
        output = NormAcc / 9.81
        DesiredTrack = GeoSolver.GreatCircleInitAz(LatFrom=self.OriginLat,
                                                   LonFrom=self.OriginLon,
                                                   LatTo=self.DestLat,
                                                   LonTo=self.DestLon)
        if np.absolute(self.MyHdg - DesiredTrack) < np.deg2rad(1):
            self.Mode = 0
        return output
      else:
          return np.float64(0.0)
