import numpy as np
import socket, struct


class civil_gnss:
    def __init__(self) -> None:
        self.lat = np.float64(0.0)
        self.lon = np.float64(0.0)
        self.altitude = np.float64(0.0)
        self.speed = np.float64(0.0)
        self.track = np.float64(0.0)
        self.LinkFail = self.InitSockets()
        self.payload = bytes(0)
        self.opmode = np.int32(0)
        self.satellites = np.int32(0)
        self.LostPackets = 0

    def ReceiveData(self) -> None:
      try:
        self.payload, _ = self.Socket.recvfrom(1500)
        self.LinkFail = False
        self.LostPackets = 0
      except BlockingIOError:
        self.LostPackets += 1
        self.LinkFail = self.LostPackets > 15
      self.ParseData()

    def ParseData(self) -> None:
       index = 0
       while index < len(self.payload):
         message = struct.unpack('>i',self.payload[index:index+4])[0]
         label = int(f"{(message & 0xFF) & 0xFF:08b}"[::-1], 2) # this reverses the incoming label bits
         if label == 0o1:
           self.opmode = (message & 0x1C00) >> 10
           self.satellites = (message & 0xE000) >> 14
         elif label == 0o110:
           self.lat = float((message & 0x1FFFFF00) >> 8) / 2**21 * 180
         elif label == 0o111:
           self.lon = float((message & 0x1FFFFF00) >> 8) / 2**21 * 180
         elif label == 0o45:
           self.track = float((message & 0x1FF00000) >> 20)
         elif label == 0o76:
           self.altitude = 0.0
         index += 4

    def InitSockets(self) -> bool:
      fails : int = 0
      try:
        self.Socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.Socket.bind(("0.0.0.0",11111))
        self.Socket.setblocking(False)
        print("GNSS socket OK")
      except:
        fails += 1
      return fails > 0
    
    def getBoolean(self, key: str) -> bool:
       if key == "LINK_FAIL":
          return self.LinkFail
       else:
          return False
       
    def getEnum(self, key: str) -> int:
       if key == "OPMODE":
          return int(self.opmode)
       else:
          return 0
       
    def getInteger(self, key: str) -> int:
       if key=="SATELLITES":
          return int(self.satellites)
       elif key == "TRACK":
          return int(self.track)
       elif key == "ALTITUDE":
          return int(self.altitude)
       else:
          return 0
       
    def getFloat(self, key: str) -> float:
       if key == "LATITUDE":
          return float(self.lat)
       elif key == "LONGITUDE":
          return float(self.lon)
       else:
          return 0.0