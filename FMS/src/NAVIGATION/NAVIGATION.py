import numpy as np
import CIVIL_GNSS
import socket, struct

class navigation:
  def __init__(self, GNSSsensor: CIVIL_GNSS.civil_gnss) -> None:
    self.GPS_status = 0
    self.HeloLatitude = np.float64(0.0)
    self.HeloLongitude = np.float64(0.0)
    self.GNSSptr : CIVIL_GNSS.civil_gnss = GNSSsensor
    self.NAV_SENS_DATA = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.Socket_destination = ('127.0.0.1', 35000)

  def SelectBestData(self) -> None:
    pass


  def GetSensorData(self, sensor: str):
    if sensor == "GPS":
      self.GPS_status = self.GNSSptr.getEnum("OPMODE")
      self.HeloLatitude = self.GNSSptr.getFloat("LATITUDE")
      self.HeloLongitude = self.GNSSptr.getFloat("LONGITUDE")

  def SendData(self) -> None:
    message = struct.pack('>iff',
                          0,
                          self.HeloLatitude,
                          self.HeloLongitude)
    self.NAV_SENS_DATA.sendto(message, self.Socket_destination)

  def DoStep(self, minor: int) -> None:
    if minor % 4 == 1:
      self.GetSensorData("GPS")
    elif minor % 32 == 0:
      self.SendData()
