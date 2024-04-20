import numpy as np
from . import FCS

Gravity : np.float64 = 9.80665
EARTH_RADIUS : np.float64 = 6.371e6

class Helicopter:
  Lat : np.float64
  Lon : np.float64
  Hdg : np.float64
  VNS : np.float64
  VEW : np.float64
  bank: np.float64
  SimStep : np.uint32
  DeltaTime = np.float64(0.001)

  def __init__(self, Lat : float, Lon : float) -> None:
    self.Lat = np.float64(Lat)
    self.Lon = np.float64(Lon)
    self.Hdg = np.float64(0.0)
    self.VNS = np.float64(0.0)
    self.VEW = np.float64(0.0)
    self.bank = np.float64(0.0)
    self.SimStep = np.uint32(0)

  def __str__(self) -> str:
    output : str =  "Step #" + str(self.SimStep) + '\n'
    output += "Latitude  = " + str(np.rad2deg(self.Lat)) + '\n'
    output += "Longitude = " + str(np.rad2deg(self.Lon)) + '\n'
    output += "Heading   = " + str(np.rad2deg(self.Hdg)) + '\n'
    output += "Bank      = " + str(np.rad2deg(self.bank)) + '\n'
    return output
  
  def SetInitialValues(self, Lat : float, Lon :float) -> None:
    self.Lat = Lat
    self.Lon = Lon

  def SetRollAngle(self, NewRoll) -> None:
    self.bank = NewRoll

  def SetSpeed(self, NewSpeed) -> None:
    self.VEW = NewSpeed * np.sin(self.Hdg)
    self.VNS = NewSpeed * np.cos(self.Hdg)

  def SetHeading(self, NewHeading) -> None:
    self.Hdg = NewHeading

  def SimulationStep(self) -> None:
    self.VNS += Gravity * np.tan(self.bank) * self.DeltaTime * np.cos(self.Hdg)
    self.VEW += Gravity * np.tan(self.bank) * self.DeltaTime * np.sin(self.Hdg)
    self.Lat += self.VNS * self.DeltaTime / EARTH_RADIUS
    self.Lon += self.VEW * self.DeltaTime / (EARTH_RADIUS * np.cos(self.Lat))
    self.Hdg = np.arctan2(self.VEW, self.VNS)
    self.SimStep += 1