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
  Id            : int    # unit: N/A
  Name          : str    # unit: N/A
  Type          : int    # unit: N/A
  Class         : int    # unit: N/A
  Lat           : float  # unit: degrees
  Lon           : float  # unit: degrees
  GapFollows    : bool   # unit: N/A
  ConicApp      : bool   # unit: N/A
  ArcRadius     : float  # unit: m
  ArcCenterLat  : float  # unit: degrees
  ArcCenterLon  : float  # unit: degrees
  TrackChange   : int    # unit: degrees
  isGraphical   : bool   # unit: N/A
  InboundCrs    : int    # unit: degrees
  ArcIsLeftHand : bool   # unit: N/A
  LegIntended   : bool   # unit: N/A
  ArcIntended   : bool   # unit: N/A

  def __init__(self, Id : int = 0,
               Name : str = "******",
               Type : int = 0,
               Class : int = 0,
               Lat : float = 0.0,
               Lon : float = 0.0,
               GapFollows : bool = False,
               ConicApp : bool = False,
               ArcRadius : float = 0.0,
               ArcCenterLat : float = 0.0,
               ArcCenterLon : float = 0.0,
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
    self.ArcCenterLat  = ArcCenterLat
    self.ArcCenterLon  = ArcCenterLon
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
    output += "{:6.6f}".format(math.degrees(self.Lat)).rjust(9) + ";" 
    output += "{:6.6f}".format(math.degrees(self.Lon)).rjust(9) + ";"
    output += "{:2.1f}".format(self.ArcRadius).rjust(8) + ";"
    output += str(int(math.degrees(self.InboundCrs))).rjust(4) + ";"
    output += str(int(math.degrees(self.TrackChange))).rjust(4) + ";"
    output += (ARC if self.ConicApp else STRAIGHT).rjust(9) + ";"
    output += TurnDirection[self.ArcIsLeftHand].rjust(5) + ";"
    output += ("LEG " + SegmentDisplay[self.LegIntended]).rjust(12) + ";"
    output += ("CONIC " + SegmentDisplay[self.LegIntended]).rjust(12) + ";"
    output += ("GAP" if self.GapFollows else "NO GAP").rjust(6) + ";"
    output += WpDisplay[self.isGraphical].rjust(10) + ";"
    output += "\n"
    return output