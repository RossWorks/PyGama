from . import GamaWaypoint
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

MARKER_APT = "^"
MARKER_NDB = "o"
MARKER_USR = "*"
MARKER_VHF = "h"
MARKER_WPT = "D"
MARKER_NULL = "."
Type_marker_dict : dict[str:str] = {"APT" : MARKER_APT,
                                    "NDB" : MARKER_NDB,
                                    "USR" : MARKER_USR,
                                    "VHF" : MARKER_VHF,
                                    "WPT" : MARKER_WPT}

Type_color_dict : dict[str:str] = {"APT" : "cyan",
                                   "NDB" : "orange",
                                   "USR" : "yellow",
                                   "VHF" : "green",
                                   "WPT" : "pink"}

EARTH_RADIUS = 6.371e6

class GraphFpSegment:
  Intended : bool
  Route : np.ndarray
  Color : str

  def __init__(self) -> None:
    self.Intended = False
    self.Route = 0.0 * np.zeros(shape=(100,3), dtype=np.float64)
    self.Color = 'k'

class GraphWpMarker:
  Name  : str
  Color : str
  Marker: str
  Theta : float
  Rho : float
  X : float
  Y : float
  Z : float

  def __init__(self) -> None:
    self.Name = "******"
    self.Color = 'k'
    self.Marker = MARKER_NULL
    self.X = 0.0
    self.Y = 0.0
    self.Z = 0.0
    self.Theta = 0.0
    self.Rho = 0.0
  
  def SetPolarPosition(self, Rho : float, Theta : float):
    self.Rho = Rho
    self.Theta = Theta

  def SetMarker(self, Marker : str):
    self.Marker = Marker
  
  def SetColor(self, Color : str):
    self.Color = Color

  def SetName(self, Name : str):
    self.Name = Name

class Display:
  
  def __init__(self, MasterWidget : tk.Widget) -> None:
    self.Cds = Figure(dpi=150.0, figsize=[5.0,5.0])
    self.Cdscreen = FigureCanvasTkAgg(self.Cds, master = MasterWidget)
    self.CdMap = self.Cds.add_subplot(projection='polar')
    self.CdMap.set_theta_zero_location('N')
    self.CdMap.set_theta_direction(-1)
    #CdMap.set_facecolor('k')
    self.CdMap.axes.clear()
    self.DisplayWidget  = self.Cdscreen.get_tk_widget()
    self.MapCenter      = [np.radians(45.5), np.radians(8.7)]
    self.MapOrientation = np.pi/2
    self.StoredFpl : list[GamaWaypoint.GamaWaypoint] = []

  def GetTkinterWidget(self) -> tk.Widget:
    return self.DisplayWidget

  def RefreshFpl(self, Fpl : list[GamaWaypoint.GamaWaypoint]):
    self.CdMap.clear()
    self.CdMap.set_theta_direction(-1)
    self.CdMap.set_theta_offset(self.MapOrientation)
    if len(Fpl) < 1:
      return
    RouteMesh : list[GraphFpSegment] = self._RenderGamaFpl(GamaFpl=Fpl)
    for segment in RouteMesh:
      marker = '--' if segment.Intended else ''
      self.CdMap.plot(segment.Route[:,0],segment.Route[:,1]/1852,
                      color=segment.Color, marker=marker, markersize=2)
    #Names in 2D FPLN
    GraphWps = self._RenderWps(WpList=Fpl)
    for point in GraphWps:
      self.CdMap.plot(point.Theta, point.Rho/1852, marker=point.Marker, color = point.Color)
      self.CdMap.text(point.Theta, point.Rho/1852, point.Name)
    print("")
    print("")
    self.Cdscreen.draw()

  def SetCdsCenter(self, Lat : float, Lon : float, DelayUpdate : bool = False) -> bool:
    if abs(Lat) > (np.pi/2):
      return False
    if abs(Lon) > np.pi:
      return False
    self.MapCenter = [Lat, Lon]
    if not DelayUpdate:
      self.RefreshFpl(Fpl=self.StoredFpl)
    return True
  
  def SetMapRotation(self, NewHeading : float = 0) -> bool:
    self.MapOrientation = NewHeading
    return True

  def _RenderGamaFpl(self, GamaFpl : list[GamaWaypoint.GamaWaypoint]) -> list[GraphFpSegment]:
    self.StoredFpl = GamaFpl.copy()
    print("CDS: Updating Flight plan")
    output = list()
    TmpSegment = GraphFpSegment()
    FpSize = len(GamaFpl)
    if FpSize == 1:
      TmpSegment.Color = 'k'
      TmpSegment.Route[0,0] = GamaFpl[0].Lat
      output.append(TmpSegment)
    else:
      for index in range(0,FpSize-1):
        TmpSegment = GraphFpSegment()
        EndOfArcPoint = GamaWaypoint.GamaWaypoint()
        TmpSegment.Color = 'm' if index == 0 else 'k'
        TmpSegment.Intended = False
        if GamaFpl[index].ConicApp:
          print("Calculating 2D Arc from " + str(GamaFpl[index].Name) + " to " + str(GamaFpl[index+1].Name))
          TmpSegment.Route = self._DrawPolarArc(StartPoint = GamaFpl[index],
                                           EndPoint   = EndOfArcPoint)
          output.append(TmpSegment)
          if not GamaFpl[index].GapFollows:
            continue
            print("calculating 2D straight line from " + str(GamaFpl[index].Name) + " to " + str(GamaFpl[index+1].Name))
            TmpSegment.Route = self._DrawPolarStraightLine(StartPoint = EndOfArcPoint,
                                                           EndPoint   = GamaFpl[index+1])
        elif not GamaFpl[index].GapFollows:
          print("calculating 2D straight line from " + str(GamaFpl[index].Name) + " to " + str(GamaFpl[index+1].Name))
          TmpSegment.Route = self._DrawPolarStraightLine(StartPoint = GamaFpl[index],
                                                         EndPoint   = GamaFpl[index+1])
          output.append(TmpSegment)
    return output
  
  def _DrawPolarStraightLine(self, StartPoint : GamaWaypoint.GamaWaypoint, 
                             EndPoint   : GamaWaypoint.GamaWaypoint) -> np.ndarray:
    pre_output = np.zeros(shape=(100,2))
    output = np.zeros(shape=(100,2))
    p1 = np.array(self._LatLon2XY(Lat=StartPoint.Lat, Lon=StartPoint.Lon,
                                  OriginLat=self.MapCenter[0], OriginLon=self.MapCenter[1]))
    p2 = np.array(self._LatLon2XY(Lat=EndPoint.Lat, Lon=EndPoint.Lon,
                                  OriginLat=self.MapCenter[0], OriginLon=self.MapCenter[1]))
    pre_output[:,0] = np.linspace(p1[0],p2[0],100)
    pre_output[:,1] = np.linspace(p1[1],p2[1],100)
    output[:,0] = np.arctan2(pre_output[:,0],pre_output[:,1])
    output[:,1] = np.sqrt(np.power(pre_output[:,1],2)+np.power(pre_output[:,0],2))
    return output
  
  def _LatLon2XY(self, Lat : float, Lon : float,
                 OriginLat : float, OriginLon : float) -> list[float]:
    '''This function is derived from the formulas depicted at page 228 of:\n
\"An album of map projections\",\nby 
    John P. Snyder, ; U.S. Geological Survey,\n
    Philip M. Voxland,University of Minnesota\n    
This function applies azimuthal equidistant projection, same used in UN flag
    '''
    output = [0.0, 0.0]
    sin_phi1 = np.sin(OriginLat)
    cos_phi1 = np.cos(OriginLat)
    sin_phi  = np.sin(Lat)
    cos_phi  = np.cos(Lat)
    cos_delta_lambda = np.cos(Lon-OriginLon)
    sin_delta_lambda = np.sin(Lon-OriginLon)
    cos_z = sin_phi1 * sin_phi + cos_phi1 * cos_phi * cos_delta_lambda
    if cos_z < 0:
      return [np.nan, np.nan] #the point must be rejected
    if cos_z == 1:
      K = 1
    else:
      sin_z = np.sqrt(1 - np.power(cos_z,2))
      K = np.arccos(cos_z) / sin_z
  
    output[0] = EARTH_RADIUS * K * cos_phi * sin_delta_lambda
    output[1] = EARTH_RADIUS * K * (cos_phi1 * sin_phi - sin_phi1 * cos_phi * cos_delta_lambda)
    return output
  
  def _DrawPolarArc(self, StartPoint : GamaWaypoint.GamaWaypoint,
                    EndPoint : GamaWaypoint.GamaWaypoint) -> np.ndarray:
    output = np.zeros(shape=(100,2))
    Pwp1Vector = np.array(self._LatLon2XY(Lat=StartPoint.Lat, Lon= StartPoint.Lon,
                                              OriginLat=self.MapCenter[0], OriginLon=self.MapCenter[1]))
    Pwp1Vector = Pwp1Vector.reshape((2,1))
    ArcCenter = self._LatLon2XY(Lat=StartPoint.ArcCenterLat, Lon= StartPoint.ArcCenterLon,
                                    OriginLat=self.MapCenter[0], OriginLon=self.MapCenter[1])
    ArcCenterVector = np.array(ArcCenter).reshape((2,1))
    Angle = np.linspace(start=0,stop=StartPoint.TrackChange, num=100).reshape((100,1))
    Center2PwpVector = Pwp1Vector - ArcCenterVector
    theta = np.pi * (.5 if StartPoint.ArcIsLeftHand else -.5) #behaviour is inverted from Fly-By computation because a rot matrix follow anticlockwise angle rule
    rot_matrix = np.matrix([[np.cos(theta), -np.sin(theta)],
                            [np.sin(theta),  np.cos(theta)]])
    otherVector = rot_matrix @ Center2PwpVector
    for step in range(0,len(Angle)):
      Dummy = ArcCenterVector + (Center2PwpVector * np.cos(Angle[step]) + otherVector * np.sin(Angle[step]))
      output_theta    = np.arctan2(Dummy[0],Dummy[1])
      output_rho      = np.sqrt(np.power(Dummy[0],2)+np.power(Dummy[1],2))
      output[step, 0] = output_theta
      output[step, 1] = output_rho
    return output
  
  def _XY2ThetaRho(self, X : float, Y : float) -> list[float]:
    output = [0.0, 0.0]
    output[0] = np.arctan2(X,Y)
    output[1] = np.sqrt(np.power(X,2) + np.power(Y,2))
    return output

  def _RenderWps(self, WpList : list[GamaWaypoint.GamaWaypoint]) -> list[GraphWpMarker]:
    output : list[GraphWpMarker] = []
    for point in WpList:
      if not point.isGraphical:
        continue
      TmpGraphWp = GraphWpMarker()
      X,Y = self._LatLon2XY(Lat=point.Lat,
                            Lon=point.Lon,
                            OriginLat=self.MapCenter[0],
                            OriginLon=self.MapCenter[1])
      Theta,Rho = self._XY2ThetaRho(X=X,Y=Y)
      TmpGraphWp.SetPolarPosition(Rho=Rho,Theta=Theta)
      try:
        TmpGraphWp.SetMarker(Marker=Type_marker_dict[point.GetType()])
      except KeyError:
        TmpGraphWp.Marker = MARKER_NULL
      try:
        TmpGraphWp.SetColor(Color=Type_color_dict[point.GetType()])
      except KeyError:
        TmpGraphWp.Color = "k"
      TmpGraphWp.SetName(Name=point.Name)
      output.append(TmpGraphWp)
    return output
  