import numpy as np
import CIVIL_GNSS, AHRS
import socket, struct

class navigation:
  def __init__(self, GNSSsensor: CIVIL_GNSS.civil_gnss,
                     AHRSsensor: AHRS.AHRS) -> None:
    self.GPS_status = 0
    self.HeloLatitude = np.float64(0.0)
    self.HeloLongitude = np.float64(0.0)
    self.GNSSptr : CIVIL_GNSS.civil_gnss = GNSSsensor
    self.ahrs_ptr : AHRS.AHRS = AHRSsensor
    self.NAV_SENS_DATA = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.NAV_SENS_DATA.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    self.Socket_destination = ('255.255.255.255', 35000)
    self.pitch = np.float64(0.0)
    self.roll = np.float64(0.0)
    self.mag_heading = np.int32(0)
    self.HeloTrack = 0

  def SelectBestData(self) -> None:
    pass


  def GetSensorData(self, sensor: str):
    if sensor == "GPS":
      self.GPS_status = self.GNSSptr.getEnum("OPMODE")
      self.HeloLatitude = self.GNSSptr.getFloat("LATITUDE")
      self.HeloLongitude = self.GNSSptr.getFloat("LONGITUDE")
      self.HeloTrack = self.GNSSptr.getInteger("TRACK")
    if sensor == "AHRS":
      self.pitch = self.ahrs_ptr.getFloat("PITCH")
      self.roll = self.ahrs_ptr.getFloat("ROLL")
      self.mag_heading = self.ahrs_ptr.getInteger("MAG_HEADING")


  def SendData(self, minor: int) -> None:
    message = struct.pack('>i',0) #SSM array
    message = message + struct.pack('>f', self.HeloLatitude) # GNSS latitude --> before consolidation
    message = message + struct.pack('>f', self.HeloLongitude) # GNSS longitude --> before consolidation
    message = message + struct.pack('>i', self.HeloTrack) # GNSS track
    message = message + struct.pack('>i', 0) # GNSS altitude
    message = message + struct.pack('>i', self.GPS_status) # GNSS ground speed
    message = message + struct.pack('>i', 0) # GNSS sensor status
    message = message + struct.pack('>B', 0) # GNSS satellites
    message = message + struct.pack('>H', 0) # Spare
    message = message + struct.pack('>f', self.pitch) # AHRS pitch
    message = message + struct.pack('>f', self.roll) # AHRS roll
    message = message + struct.pack('>I', self.mag_heading) # AHRS MAG HDG
    message = message + struct.pack('>I', self.mag_heading) # AHRS MAG HDG
    self.NAV_SENS_DATA.sendto(message, self.Socket_destination)

  def DoStep(self, minor: int) -> None:
    match minor:
      case 0:
        self.GetSensorData("GPS")
      case 1:
        return
        self.GetSensorData("AHRS")
      case 10:
        self.SendData(minor)

