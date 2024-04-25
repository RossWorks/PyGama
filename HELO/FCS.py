import numpy as np

FcsModes : dict[np.int32 : str] = {0 : "NO_STEER",
                                   1 : "HDG_MODE"}

class FCS:
  P : np.float64
  I : np.float64
  D : np.float64
  Mode : np.int32
  SelHdg : np.int32
  FmsRollSteer : np.float64

  def __init__(self, P : float, I : float, D : float, Mode : int) -> None:
    self.P = P
    self.I = I
    self.D = D
    self.Mode = Mode
    self.SelHdg = np.int32(0)
    self.CurrHdg = np.float64(0.0)
    self.SteerCmd = np.float64(0.0)
    self.FmsRollSteer = np.float64(0.0)
  
  def __str__(self) -> str:
    output   = "Selected HDG = " + str(np.rad2deg(self.SelHdg)) + '\n'
    output += "Current HDG   = " + str(np.rad2deg(self.CurrHdg)) + '\n'
    output += "Roll Steering = " + str(np.rad2deg(self.SteerCmd)) + '\n'
    return output
  
  def GetHdgModeRollCmd(self) -> float:
    DeltaHdg = self.SelHdg - self.CurrHdg
    if DeltaHdg > np.pi:
      DeltaHdg -= 2*np.pi
    elif DeltaHdg <  (-1 * np.pi):
      DeltaHdg += 2*np.pi
    RawData = self.P * (DeltaHdg)
    if RawData > np.deg2rad(25):
      RawData = np.deg2rad(25)
    elif RawData < np.deg2rad(-25):
      RawData = np.deg2rad(-25)
    return RawData
  
  def SetCurrHdg(self, CurrHdg : float):
    self.CurrHdg = CurrHdg
  
  def SetSelectedHdg(self, NewHdg : float):
    self.SelHdg = np.float64(NewHdg)
  
  def SetFmsRollSteer(self, CmdFromFms : float):
    self.FmsRollSteer = CmdFromFms

  def ExecuteStep(self):
    if self.Mode == 0:
      self.SteerCmd = 0.0
    elif self.Mode == 1:
      self.SteerCmd = self.GetHdgModeRollCmd()
    elif self.Mode == 2:
      return self.FmsRollSteer
    return self.SteerCmd