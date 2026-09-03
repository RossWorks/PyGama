import socket
import struct
from time import sleep

class GNSSemul:

   def __init__(self, port: int) -> None:
      self.IP = '255.255.255.255'
      self.port = port
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

      self.latitude = 45.0
      self.longitude = 12.0
      self.track = 300
      self.opmode = 4

   def preparelabel(self, datum: str, Extended: bool = False) -> int:
      output = 0
      LSB = 8
      if datum == "LATITUDE":
         LSB = 8
         payload = int(self.latitude / 180.0 * 2**21)
         ssm = 3
         label = int(f"{0o110 & 0xFF:08b}"[::-1], 2)
         parity = 1
      elif datum == "LONGITUDE":
         LSB = 8
         payload = int(self.longitude / 180.0 * 2**21)
         ssm = 3
         label = int(f"{0o111 & 0xFF:08b}"[::-1], 2)
         parity = 1
      elif datum == "OPMODE":
         LSB = 10
         payload = self.opmode
         ssm = 3
         label = int(f"{0o1 & 0xFF:08b}"[::-1], 2)
         parity = 1
      elif datum == "TRACK":
         LSB = 20
         payload = self.track
         ssm = 3
         label = int(f"{0o45 & 0xFF:08b}"[::-1], 2)
         parity = 1
      else:
         print("UNRECOGNIZED ELEMENT: " + key)
      output = (label | (payload << LSB) | (ssm << 29) | (parity << 31))
      return output


   def loopStep(self):
      messaggio = struct.pack('>I', self.preparelabel("LATITUDE", True))
      messaggio = messaggio + struct.pack('>I', self.preparelabel("LONGITUDE", True))
      messaggio = messaggio + struct.pack('>I', self.preparelabel("OPMODE", True))
      messaggio = messaggio + struct.pack('>I', self.preparelabel("TRACK", True))
      self.socket.sendto(messaggio, (self.IP, self.port))

if __name__ == "__main__":
   localInstance = GNSSemul(11111)
   while (True):
      localInstance.loopStep()
      sleep(5)