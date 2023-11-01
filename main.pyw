import Gama
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

FlightPlan = Gama.FlightPlan.FlightPlan(PposLat=0.0,
                                        PposLon=0.0)

def RefreshFpl():
  FplList.config(state="normal")
  FplList.delete('1.0',tk.END)
  FplList.insert('1.0',str(FlightPlan))
  FplList.config(state="disabled")
  GamaList.config(state="normal")
  GamaList.delete('1.0',tk.END)
  GamaList.insert('1.0',FlightPlan.__repr__(Gama=True))
  GamaList.config(state="disabled")
  World.clear()
  WorldMesh = Gama.MapRender.RenderWorld(LatRes=30,LonRes=30)
  World.plot_wireframe(WorldMesh['X'],WorldMesh['Y'],WorldMesh['Z'])
  RouteMesh = Gama.MapRender.RenderGamaFpl(FlightPlan.ExpandedWaypoints)
  for segment in RouteMesh:
    marker = '--' if segment.Intended else ''
    World.plot(segment.Route[:,0],segment.Route[:,1], segment.Route[:,2],
               color=segment.Color, marker=marker)
  


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
GamaList = tk.Text(master=FplWorkArea, width=80,state="disabled")
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