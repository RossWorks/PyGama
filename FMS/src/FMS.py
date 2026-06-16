from CIVIL_GNSS import civil_gnss
from NAVIGATION import NAVIGATION


class FMS:

  def __init__(self) -> None:
    self.GPS1 = civil_gnss.civil_gnss()
    self.INTNAV = NAVIGATION.navigation(self.GPS1)
  
  def ElaborationStep(self, minor: int):
      self.GPS1.ReceiveData()
      self.INTNAV.DoStep(minor)


if __name__ == "__main__":
  print("FMS boot")
  
  minor_frame : int = 0
  FMS_instance = FMS()

  print("FMS: switch to operative phase")

  while(True):
    FMS_instance.ElaborationStep(minor_frame)
    minor_frame = (minor_frame + 1) % 32