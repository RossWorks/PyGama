from CIVIL_GNSS import civil_gnss
from NAVIGATION import NAVIGATION
from AHRS import AHRS

import time

class FMS:

  def __init__(self) -> None:
    self.GPS1 = civil_gnss.civil_gnss()
    self.ahrs = AHRS.AHRS()
    self.INTNAV = NAVIGATION.navigation(self.GPS1, self.ahrs)
    self.timer1 = 0
  
  def ElaborationStep(self, minor: int):
      self.GPS1.ReceiveData()
      self.INTNAV.DoStep(minor)
      if self.timer1 % 2e6 == 0:
        print("FMS is alive")
      self.timer1 = self.timer1 + 1 % (2**32 - 1)
      time.sleep(0.02)


if __name__ == "__main__":
  print("FMS boot")
  
  minor_frame : int = 0
  FMS_instance = FMS()

  print("FMS: switch to operative phase")

  while(True):
    FMS_instance.ElaborationStep(minor_frame)
    minor_frame = (minor_frame + 1) % 32