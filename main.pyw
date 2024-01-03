import Gama
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

FlightPlan = Gama.FlightPlan.FlightPlan(PposLat=45.5,
                                        PposLon=8.7)

def RefreshFpl():
  FplList.config(state="normal")
  FplList.delete('1.0',tk.END)
  FplList.insert('1.0',str(FlightPlan))
  FplList.config(state="disabled")
  GamaList.config(state="normal")
  GamaList.delete('1.0',tk.END)
  GamaList.insert('1.0',FlightPlan.__repr__(Gama=True))
  GamaList.config(state="disabled")

  #3D Flight map
  World.clear()
  WorldMesh = Gama.MapRender.RenderWorld(LatRes=30,LonRes=30)
  World.plot_wireframe(WorldMesh['X'],WorldMesh['Y'],WorldMesh['Z'])
  RouteMesh = Gama.MapRender.RenderGamaFpl(FlightPlan.ExpandedWaypoints,
                                           Use3D=True)
  for segment in RouteMesh:
    marker = '--' if segment.Intended else ''
    World.plot(segment.Route[:,0],segment.Route[:,1], segment.Route[:,2],
               color=segment.Color, marker=marker)
    
  #2D Gama FPL
  RouteMesh.clear()
  RouteMesh = Gama.MapRender.RenderGamaFpl(FlightPlan.ExpandedWaypoints,
                                           Use3D=False)
  CdMap.clear()
  CdMap.set_theta_direction(-1)
  CdMap.set_theta_zero_location('N')
  print(len(RouteMesh))
  for segment in RouteMesh:
    marker = '--' if segment.Intended else ''
    CdMap.plot(segment.Route[:,0],segment.Route[:,1]/1852,
               color=segment.Color, marker=marker, markersize=2)
  
  #Names in 2D FPLN
  GraphWps = Gama.MapRender.RenderWps(FlightPlan.Waypoints,is3D=False)
  for point in GraphWps:
    CdMap.plot(point.Theta, point.Rho/1852, marker=point.Marker, color = point.Color)
    CdMap.text(point.Theta, point.Rho/1852, point.Name)

ClassList : list[str] = []
TypeList  : list[str] = []

for key in Gama.FlightPlan.FplWaypoint.ClassDict:
  ClassList.append(Gama.FlightPlan.FplWaypoint.ClassDict[key])

for key in Gama.FlightPlan.FplWaypoint.TypeDict:
  TypeList.append(Gama.FlightPlan.FplWaypoint.TypeDict[key])

def RemoveWpCallB():
  Index2BeRemoved : int = int(TxtDeleteIndex.get())
  FlightPlan.RemoveWp(Index2BeRemoved)
  RefreshFpl()

def InsertWpCallB():
  '''This function calls for a new wp insertion in the active flightplan'''
  MyType  : int = -1
  MyClass : int = -1
  for key in Gama.FlightPlan.FplWaypoint.TypeDict:
    if Gama.FlightPlan.FplWaypoint.TypeDict[key] == TxtInsertType.get():
      MyType = key
  if MyType < 0:
    return
  for key in Gama.FlightPlan.FplWaypoint.ClassDict:
    if Gama.FlightPlan.FplWaypoint.ClassDict[key] == TxtInsertClass.get():
      MyClass = key
  if MyClass < 0:
    return
  TmpWp = Gama.FlightPlan.FplWaypoint.FplWaypoint(Id= int(TxtInsertIndex.get()),
                                                  Name= TxtInsertName.get(),
                                                  Type=MyType,
                                                  Class=MyClass,
                                                  Lat=float(TxtInsertLat.get()),
                                                  Lon=float(TxtInsertLon.get()),
                                                  isFlyOver=WpIsFlyOver.get()==1)
  FlightPlan.InsertWp(Wpt=TmpWp, InsertInPos=int(TxtInsertIndex.get()))
  RefreshFpl()


home = tk.Tk()
home.title("PyGama")

FplRepr = tk.StringVar(master = home)
WpIsFlyOver = tk.IntVar(master=home)

FplGroup = tk.LabelFrame(master = home, text="GRAPHICAL AREA")
FplGroup.grid(row=0,column=0, rowspan=2)
FplWorkArea = ttk.Notebook(master = FplGroup)
FplWorkArea.grid(row=0, column=0)
FplList = tk.Text(master=FplWorkArea, width=80,state="disabled")
FplList.grid(row=0,column=0)
FplWorkArea.add(FplList, text="FLIGHT PLAN")
GamaList = tk.Text(master=FplWorkArea, width=120,state="disabled")
GamaList.grid(row=0,column=0)
FplWorkArea.add(GamaList, text="GAMA PROTOCOL")
FplGraph = Figure(dpi=150.0, figsize=[5.0,5.0])
FplCanvas = FigureCanvasTkAgg(FplGraph, master = FplGroup)
World = FplGraph.add_subplot(projection='3d')
World.set_xlabel("X")
World.set_ylabel("Y")
World.set_zlabel("Z")
World.set_aspect("equal")
FplWorkArea.add(FplCanvas.get_tk_widget(), text="3D FLIGHT MAP")
Cds = Figure(dpi=150.0, figsize=[5.0,5.0])
Cdscreen = FigureCanvasTkAgg(Cds, master = FplWorkArea)
CdMap = Cds.add_subplot(projection='polar')
CdMap.set_theta_zero_location('N')
CdMap.set_theta_direction(-1)
#CdMap.set_facecolor('k')
CdMap.axes.clear()
FplWorkArea.add(Cdscreen.get_tk_widget(), text="CDS MAP")

InsertWpGroup = tk.LabelFrame(master = home, text = "INSERT WP CMD")
InsertWpGroup.grid(row=0, column=1)
LblInsertIndex = tk.Label(master = InsertWpGroup, text="WPT INDEX:")
LblInsertIndex.grid(row=0,column=0)
LblInsertName = tk.Label(master = InsertWpGroup, text="WPT NAME:")
LblInsertName.grid(row=1,column=0)
LblInsertType = tk.Label(master = InsertWpGroup, text="WPT TYPE:")
LblInsertType.grid(row=2,column=0)
LblInsertClass = tk.Label(master = InsertWpGroup, text="WPT CLASS:")
LblInsertClass.grid(row=3,column=0)
LblInsertLat = tk.Label(master = InsertWpGroup, text="WPT LATITUDE:")
LblInsertLat.grid(row=4,column=0)
LblInsertLon = tk.Label(master = InsertWpGroup, text="WPT LONGITUDE:")
LblInsertLon.grid(row=5,column=0)

CmdInsert = tk.Button(master = InsertWpGroup, text= "INSERT WP",
                      command=InsertWpCallB)
CmdInsert.grid(row=7, column=0)

TxtInsertIndex = tk.Entry(master= InsertWpGroup, width=8)
TxtInsertIndex.grid(row=0,column=1)
TxtInsertName = tk.Entry(master= InsertWpGroup, width=8)
TxtInsertName.grid(row=1,column=1)
TxtInsertType = ttk.Combobox(master= InsertWpGroup, width = 8, values= TypeList)
TxtInsertType.current(0)
TxtInsertType.grid(row=2,column=1)
TxtInsertClass = ttk.Combobox(master= InsertWpGroup, width = 8,values=ClassList)
TxtInsertClass.current(0)
TxtInsertClass.grid(row=3,column=1)
TxtInsertLat = tk.Entry(master= InsertWpGroup, width=8)
TxtInsertLat.grid(row=4,column=1)
TxtInsertLon = tk.Entry(master= InsertWpGroup, width=8)
TxtInsertLon.grid(row=5,column=1)
ChkInsertFlyOv = tk.Checkbutton(master= InsertWpGroup, text="WPT is FLY OVER:",
                                variable=WpIsFlyOver)
ChkInsertFlyOv.grid(row=6,column=0)



DeleteWpGroup = tk.LabelFrame(master = home, text = "DELETE WP CMD")
DeleteWpGroup.grid(row=1, column=1)
LblDeleteIndex = tk.Label(master= DeleteWpGroup, text="DELETE WP INDEX:")
LblDeleteIndex.grid(row=0,column=0)
CmdDelete = tk.Button(master = DeleteWpGroup, text= "DELETE WP",
                      command=RemoveWpCallB)
CmdDelete.grid(row=1, column=0)
TxtDeleteIndex = tk.Entry(master= DeleteWpGroup, width=3)
TxtDeleteIndex.grid(row=0,column=1)

RefreshFpl()

home.mainloop()