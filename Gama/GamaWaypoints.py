from . import FplWaypoint as FpWp

ConnectionType : dict[int : str] = {0 : "STRAIGHT",
                                    1 : "ARC"}

class GamaFplWaypoint:
  Id      : int
  Name    : str
  Type    : int
  Class   : int
  X       : float
  Y       : float
  Z       : float
  GapFoll : bool
  NextSeg : int
  ArcRad  : int
  ArcCenterX : float
  ArcCenterY : float
  ArcAngle   : float

  def __init__(self, Id : int = 0,
               Name : str = "******",
               Type : int = 0,
               Class : int = 0,
               X : float = 0.0,
               Y : float = 0.0,
               Z : float = 0.0,
               GapFollows : bool = False,
               NextConnect : int = 0,
               ArcRadius : int = 0,
               ArcCenterX : float = 0.0,
               ArcCenterY : float = 0.0,
               ArcAngle : float = 0.0) -> None:
    self.Id         = Id
    self.Name       = Name
    self.Type       = Type
    self.Class      = Class
    self.X          = X
    self.Y          = Y
    self.Z          = Z
    self.GapFoll    = GapFollows
    self.NextSeg    = NextConnect
    self.ArcRad     = ArcRadius
    self.ArcCenterX = ArcCenterX
    self.ArcCenterY = ArcCenterY
    self.ArcAngle   = ArcAngle

  def __repr__(self) -> str:
    output : str = ""
    output += self.Name.rjust(6) + ";"
    output += FpWp.TypeDict[self.Type].rjust(6) + ";"
    output += FpWp.ClassDict[self.Class].rjust(6) + ";"
    output += "GAP" if self.GapFoll else "NO GAP"
    output += "\n"
    return output