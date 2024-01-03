from . import FplWaypoint as FpWp

import math

STRAIGHT : str = "STRAIGHT"
ARC      : str = "CONIC"

LEFT  : str = "LEFT"
RIGHT : str = "RIGHT"

INTENDED     : str = "INTENDED"
NOT_INTENDED : str = "NOT INTENDED"

GRAPHICAL     : str = "GRAPHICAL"
NOT_GRAPHICAL : str = "INVISIBLE"

ConnectionType : dict[bool : str] = {False : STRAIGHT,
                                     True  : ARC}

TurnDirection : dict[bool : str] = {False : RIGHT,
                                    True  : LEFT}

SegmentDisplay : dict[bool : str] = {False : NOT_INTENDED,
                                     True  : INTENDED}

WpDisplay : dict[bool : str] = {False : NOT_GRAPHICAL,
                                True  : GRAPHICAL}

class GamaFplWaypoint:
  Id            : int
  Name          : str
  Type          : int
  Class         : int
  Lat           : float
  Lon           : float
  GapFollows    : bool
  ConicApp      : bool
  ArcRadius     : float
  ArcCenterX    : float
  ArcCenterY    : float
  TrackChange   : int
  isGraphical   : bool
  InboundCrs    : int
  ArcIsLeftHand : bool
  LegIntended   : bool
  ArcIntended   : bool

  def __init__(self, Id : int = 0,
               Name : str = "******",
               Type : int = 0,
               Class : int = 0,
               Lat : float = 0.0,
               Lon : float = 0.0,
               GapFollows : bool = False,
               ConicApp : bool = False,
               ArcRadius : float = 0.0,
               ArcCenterX : float = 0.0,
               ArcCenterY : float = 0.0,
               TrackChange : int = 0,
               isGraphical : bool = False,
               InboundCrs : int = 0,
               ArcIsLeftHand : bool = False,
               LegIntended : bool = True,
               ArcIntended : bool = True) -> None:
    self.Id            = Id
    self.Name          = Name
    self.Type          = Type
    self.Class         = Class
    self.Lat           = Lat
    self.Lon           = Lon
    self.GapFollows    = GapFollows
    self.ConicApp      = ConicApp
    self.ArcRadius     = ArcRadius
    self.ArcCenterX    = ArcCenterX
    self.ArcCenterY    = ArcCenterY
    self.TrackChange   = TrackChange
    self.isGraphical   = isGraphical
    self.InboundCrs    = InboundCrs
    self.ArcIsLeftHand = ArcIsLeftHand
    self.LegIntended   = LegIntended
    self.ArcIntended   = ArcIntended

  def __repr__(self) -> str:
    output : str = ""
    output += self.Name.rjust(6) + ";"
    output += FpWp.TypeDict[self.Type].rjust(6) + ";"
    output += FpWp.ClassDict[self.Class].rjust(6) + ";"
    output += "{:6.6f}".format(self.Lat).rjust(9) + ";" 
    output += "{:6.6f}".format(self.Lon).rjust(9) + ";"
    output += "{:2.1f}".format(self.ArcRadius).rjust(8) + ";"
    output += str(self.InboundCrs).rjust(4) + ";"
    output += str(int(math.degrees(self.TrackChange))).rjust(4) + ";"
    output += (STRAIGHT if self.ConicApp == 0 else ARC).rjust(9) + ";"
    output += TurnDirection[self.ArcIsLeftHand] + ";"
    output += ("LEG " + SegmentDisplay[self.LegIntended]).rjust(12) + ";"
    output += ("CONIC " + SegmentDisplay[self.LegIntended]).rjust(12) + ";"
    output += ("GAP" if self.GapFollows else "NO GAP").rjust(6) + ";"
    output += WpDisplay[self.isGraphical].rjust(10) + ";"
    output += "\n"
    return output