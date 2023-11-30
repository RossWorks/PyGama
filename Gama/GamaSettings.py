from . import FplWaypoint
import configparser as ini

class GamaSettings:
  MARKER_APT  : str
  MARKER_NDB  : str
  MARKER_USR  : str
  MARKER_VHF  : str
  MARKER_WPT  : str
  MARKER_NULL : str
  Type_marker_dict : dict[str:str] = {}
  Type_color_dict : dict[str:str] = {}

  def __init__(self, SettingFile : str) -> None:
    self.LoadDefaultSettings()
    Config = ini.ConfigParser()
    ReadFiles = Config.read(filenames=SettingFile)
    if len(ReadFiles) == 0:
      print("Setting file unavailable: loading default settings")
      return
    self.Type_color_dict["APT"]  = "#" + Config["CDS"]["APT_COLOR"]
    self.Type_color_dict["VHF"]  = "#" + Config["CDS"]["VHF_COLOR"]
    self.Type_color_dict["NDB"]  = "#" + Config["CDS"]["NDB_COLOR"]
    self.Type_color_dict["WPT"]  = "#" + Config["CDS"]["WPT_COLOR"]
    self.Type_color_dict["USR"]  = "#" + Config["CDS"]["USR_COLOR"]
    self.Type_marker_dict["APT"] = Config["CDS"]["APT_MARKER"]
    self.Type_marker_dict["VHF"] = Config["CDS"]["VHF_MARKER"]
    self.Type_marker_dict["NDB"] = Config["CDS"]["NDB_MARKER"]
    self.Type_marker_dict["WPT"] = Config["CDS"]["WPT_MARKER"]
    self.Type_marker_dict["USR"] = Config["CDS"]["USR_MARKER"]

  def LoadDefaultSettings(self) -> None:
    self.MARKER_APT = "^"
    self.MARKER_NDB = "o"
    self.MARKER_USR = "*"
    self.MARKER_VHF = "h"
    self.MARKER_WPT = "D"
    self.MARKER_NULL = "."
    self.Type_marker_dict : dict[str:str] = {"APT" : self.MARKER_APT,
                                             "NDB" : self.MARKER_NDB,
                                             "USR" : self.MARKER_USR,
                                             "VHF" : self.MARKER_VHF,
                                             "WPT" : self.MARKER_WPT}
         
    self.Type_color_dict : dict[str:str] = {"APT" : "cyan",
                                            "NDB" : "orange",
                                            "USR" : "yellow",
                                            "VHF" : "green",
                                            "WPT" : "pink"}

  def GetWpMarker_Color(self, Point : FplWaypoint.FplWaypoint) -> list[str]:
    output = list()
    try:
      Marker = self.Type_marker_dict[Point.GetType()]
      Color  = self.Type_color_dict[Point.GetType()]
    except KeyError:
      Marker = self.MARKER_NULL
      Color = 'k'
    output = [Marker, Color]
    return output
