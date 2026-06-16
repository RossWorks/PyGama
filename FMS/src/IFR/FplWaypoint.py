import numpy as np

NONE_TYPE = 0
USR_TYPE = 1
APT_TYPE = 2
VHF_TYPE = 3
NDB_TYPE = 4
WPT_TYPE = 5
PPOS_TYPE = 6

TypeDict : dict [int : str] = {NONE_TYPE : "------",
                               USR_TYPE : "USR",
                               APT_TYPE : "APT",
                               VHF_TYPE : "VHF",
                               NDB_TYPE : "NDB",
                               WPT_TYPE : "WPT",
                               PPOS_TYPE : "PPOS"}


CLASS_NONE = 0
CLASS_VOR = 1
CLASS_DME = 2
CLASS_VORDME = 3
CLASS_TACAN = 4
CLASS_VORTAC  =5

ClassDict : dict [int : str] = {CLASS_NONE : "------",
                                CLASS_VOR : "VOR",
                                CLASS_DME : "DME",
                                CLASS_VORDME : "VORDME",
                                CLASS_TACAN : "TACAN",
                                CLASS_VORTAC : "VORTAC"}


ERROR_NO_ERROR = 0
ERROR_INVALID_TYPE = 1
ErrorDict : dict [int : str] = {ERROR_NO_ERROR : "NO ERROR",
                                ERROR_INVALID_TYPE : "INVALID TYPE"}


class FplWaypoint:

  def __init__(self, Id: np.int32 = 0,
               Name: str = "******",
               Type: np.int32 = NONE_TYPE,
               Class: np.int32 = 0,
               Lat: np.float64 = 0.0,
               Lon: np.float64 = 0.0,
               isFlyOver: bool = False,
               WpCat: np.int32 = 2,
               TurnAnticipation: np.float64 = 0.0,
               TrackChange: np.int32 = 0,
               TurnRadius: np.float64 = 0.0) -> None:
    self.Id      = Id
    self.Name    = Name
    self.Type    = Type
    self.Class   = Class
    self.Lat     = Lat
    self.Lon     = Lon
    self.FlyOver = isFlyOver
    self.WpReprCat = WpCat
    self.TurnAnticipation = TurnAnticipation
    self.TrackChange = TrackChange
    self.TurnRadius = TurnRadius

  def __repr__(self) -> str:
    output : str = ""
    output += self.Name.rjust(6) + ";"
    output += TypeDict[self.Type].rjust(6) + ";"
    output += ClassDict[self.Class].rjust(6) + ";"
    output += "{:6.6f}".format(np.rad2deg(self.Lat)).rjust(9) + ";"
    output += "{:6.6f}".format(np.rad2deg(self.Lon)).rjust(9) + ";"
    output += "FLY OV" if self.FlyOver else "FLY BY"
    output += "\n"
    return output
  
  def PrintForFile(self) -> str:
    output : str = ""
    output += self.Name      + ";"
    output += str(self.Type) + ";"
    output += str(self.Class)+ ";"
    output += str(self.Lat)  + ";"
    output += str(self.Lon)  + ";"
    output += str(self.FlyOver)
    output += "\n"
    return output
  
  def GetClass(self) -> str:
    return ClassDict[self.Class]
  
  def GetType(self) -> str:
    return TypeDict[self.Type]
  

  def SetFlyOver(self, FlyOver: bool):
    self.FlyOver = FlyOver

  def SetType(self, Type) -> int:
    output = ERROR_INVALID_TYPE
    if type in TypeDict.keys():
      self.Type = Type
      output = ERROR_NO_ERROR
    return output
