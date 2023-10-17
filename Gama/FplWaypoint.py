TypeDict : dict [int : str] = {0 : "------",
                               1 : "USR",
                               2 : "APT",
                               3 : "VHF",
                               4 : "NDB",
                               5 : "WPT"}

ClassDict : dict [int : str] = {0 : "------",
                                1 : "VOR",
                                2 : "DME",
                                3 : "VORDME",
                                4 : "TACAN",
                                5 : "VORTAC"}

class FplWaypoint:
  Id      : int
  Name    : str
  Type    : int
  Class   : int
  Lat     : float
  Lon     : float
  FlyOver : bool

  def __init__(self, Id : int = 0,
               Name : str = "******",
               Type : int = 0,
               Class : int = 0,
               Lat : float = 0.0,
               Lon : float = 0.0,
               isFlyOver : bool = False) -> None:
    self.Id      = Id
    self.Name    = Name
    self.Type    = Type
    self.Class   = Class
    self.Lat     = Lat
    self.Lon     = Lon
    self.FlyOver = isFlyOver

  def __repr__(self) -> str:
    output : str = ""
    output += self.Name.rjust(6) + ";"
    output += TypeDict[self.Type].rjust(6) + ";"
    output += ClassDict[self.Class].rjust(6) + ";"
    output += str(self.Lat).rjust(9) + ";"
    output += str(self.Lon).rjust(9) + ";"
    output += "FLY OV" if self.FlyOver else "FLY BY"
    output += "\n"
    return output