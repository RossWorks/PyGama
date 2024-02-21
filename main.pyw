import Gama
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

DefaultFontTuple = ("B612 mono", 10, "normal")
MenuFontTuple    = ("B612 mono",  9, "normal")
NumericFontTuple = ("B612", 10, "normal")

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
  RouteMesh = list()
  WorldMesh = Gama.MapRender.RenderWorld(LatRes=30,LonRes=30)
  World.plot_wireframe(WorldMesh['X'],WorldMesh['Y'],WorldMesh['Z'])
  if len(FlightPlan.Waypoints) > 1:
    RouteMesh = Gama.MapRender.RenderGamaFpl(FlightPlan.ExpandedWaypoints,
                                             Use3D=True)
  for segment in RouteMesh:
    marker = '--' if segment.Intended else ''
    World.plot(segment.Route[:,0],segment.Route[:,1], segment.Route[:,2],
               color=segment.Color, marker=marker)
    
  #2D Gama FPL
  RouteMesh.clear()
  if len(FlightPlan.Waypoints) > 1:
    RouteMesh = Gama.MapRender.RenderGamaFpl(FlightPlan.ExpandedWaypoints,
                                             Use3D=False)
  CdMap.clear()
  CdMap.set_theta_direction(-1)
  CdMap.set_theta_zero_location('N')
  for segment in RouteMesh:
    marker = '--' if segment.Intended else ''
    CdMap.plot(segment.Route[:,0],segment.Route[:,1]/1852,
               color=segment.Color, marker=marker, markersize=2)
  
  #Names in 2D FPLN
  GraphWps = list()
  if len(FlightPlan.Waypoints) > 1:
    GraphWps = Gama.MapRender.RenderWps(FlightPlan.Waypoints,is3D=False)
  for point in GraphWps:
    CdMap.plot(point.Theta, point.Rho/1852, marker=point.Marker, color = point.Color)
    CdMap.text(point.Theta, point.Rho/1852, point.Name)
  print("")
  print("")

ClassList : list[str] = []
TypeList  : list[str] = []

for key in Gama.FlightPlan.FplWaypoint.ClassDict:
  ClassList.append(Gama.FlightPlan.FplWaypoint.ClassDict[key])

for key in Gama.FlightPlan.FplWaypoint.TypeDict:
  TypeList.append(Gama.FlightPlan.FplWaypoint.TypeDict[key])

def DeleteFpl():
  print("Deactivation of Active Flight Plan")
  global FlightPlan
  FlightPlan = Gama.FlightPlan.FlightPlan(PposLat=45.5,
                                          PposLon=8.7)
  RefreshFpl()

def RemoveWpCallB():
  try:
    Index2BeRemoved = int(TxtDeleteIndex.get())
  except ValueError as InvalidIntCast:
    MyMessage = "Error from DELETE WP CALLBACK:\n"
    for element in InvalidIntCast.args:
      MyMessage += str(element) + "\n"
    messagebox.showerror(title="DELETE WP ERROR", message=MyMessage)
    return
  FlightPlan.RemoveWp(Index2BeRemoved)
  DeleteWpPopUp.withdraw()
  RefreshFpl()

def ShowInsertWpPopUp():
  InsertWpPopUp.deiconify()

def ShowDeleteWpPopUp():
  DeleteWpPopUp.deiconify()

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
  try:
    TmpId = int(TxtInsertIndex.get())
    TmpLat = float(TxtInsertLat.get())
    TmpLon = float(TxtInsertLon.get())
  except ValueError as InvalidIntCast:
    MyMessage = "Error from INSERT WP CALLBACK:\n"
    for element in InvalidIntCast.args:
      MyMessage += str(element) + "\n"
    messagebox.showerror(title="INSERT WP ERROR", message=MyMessage)
    return
  TmpWp = Gama.FlightPlan.FplWaypoint.FplWaypoint(Id= TmpId,
                                                  Name= TxtInsertName.get(),
                                                  Type=MyType,
                                                  Class=MyClass,
                                                  Lat=TmpLat,
                                                  Lon=TmpLon,
                                                  isFlyOver=WpIsFlyOver.get()==1)
  FlightPlan.InsertWp(Wpt=TmpWp, InsertInPos=int(TxtInsertIndex.get()))
  InsertWpPopUp.withdraw()
  RefreshFpl()

def ShowSetCdsCenterPopUp():
  SetCdsCenterPopUp.deiconify()
  TxtCenterIndex.config(to=len(FlightPlan.Waypoints))

def SetCdsCenter():
  Wp_index = int(TxtCenterIndex.get()) - 1
  try:
    NewLat  = FlightPlan.Waypoints[Wp_index].Lat
    NewLon  = FlightPlan.Waypoints[Wp_index].Lon
    Success = Gama.MapRender.SetCdsCenter(Lat_d=NewLat, Lon_d=NewLon)
  except IndexError:
    Success = False
  if Success:
    RefreshFpl()
  SetCdsCenterPopUp.withdraw()


home = tk.Tk()
home.title("PyGama")
home.geometry("1200x800")
tk.Grid.rowconfigure(home,0, weight=1)
tk.Grid.columnconfigure(home,0, weight=1)

DeactFPL_Icon = tk.PhotoImage(file="./Resources/DeactFpl.png")
InsertWp_Icon = tk.PhotoImage(file="./Resources/InsertWp.png")
DeleteWp_Icon = tk.PhotoImage(file="./Resources/DeleteWp.png")
SaveFpl_Icon  = tk.PhotoImage(file="./Resources/SaveFpl.png")
LoadFpl_Icon  = tk.PhotoImage(file="./Resources/LoadFpl.png")
DTO_Icon      = tk.PhotoImage(file="./Resources/D-TO.png")
SAR_Icon      = tk.PhotoImage(file="./Resources/SAR.png")

FplRepr = tk.StringVar(master = home)
WpIsFlyOver = tk.IntVar(master=home)
WpIndex  = tk.IntVar(master=home)

MainMenuBar = tk.Menu(master=home)
FplMenu     = tk.Menu(master=MainMenuBar, tearoff=0)
ProcMenu    = tk.Menu(master=MainMenuBar, tearoff=0)
ViewMenu    = tk.Menu(master=MainMenuBar, tearoff=0)
home.config(menu=MainMenuBar)

MainMenuBar.add_cascade(label="ACTIVE FLIGHT PLAN",menu=FplMenu,font=MenuFontTuple)
FplMenu.add_command(label="Deactivate FPL", command=DeleteFpl, image=DeactFPL_Icon, compound="left", font=MenuFontTuple)
FplMenu.add_command(label="Direct To...", state="disabled", image=DTO_Icon, compound="left", font=MenuFontTuple)
FplMenu.add_command(label="Insert Waypoint...", image=InsertWp_Icon, compound="left", font=MenuFontTuple, command=ShowInsertWpPopUp)
FplMenu.add_command(label="Delete Waypoint...", image=DeleteWp_Icon, compound="left", font=MenuFontTuple,command=ShowDeleteWpPopUp)
FplMenu.add_command(label="SAR...", state="disabled", image=SAR_Icon, compound="left", font=MenuFontTuple)
FplMenu.add_command(label="Save FPL...", state="disabled", image=SaveFpl_Icon, compound="left", font=MenuFontTuple)
FplMenu.add_command(label="Load FPL...", state="disabled", image=LoadFpl_Icon, compound="left", font=MenuFontTuple)

MainMenuBar.add_cascade(label="PROCEDURES",menu=ProcMenu,font=MenuFontTuple)
ProcMenu.add_command(label="Load SID...", state="disabled", font=MenuFontTuple)
ProcMenu.add_command(label="Load STAR...", state="disabled", font=MenuFontTuple)

MainMenuBar.add_cascade(label="VIEW CONTROL",menu=ViewMenu, font=MenuFontTuple)
ViewMenu.add_command(label="CENTER ON HELI",state="disabled")
ViewMenu.add_command(label="CENTER ON WPT...",state="normal",command=ShowSetCdsCenterPopUp)
ViewMenu.add_command(label="CENTER ON OBJECT...",state="disabled")

FplGroup = tk.LabelFrame(master = home, text="GRAPHICAL AREA", font=DefaultFontTuple)
FplGroup.columnconfigure(index= 0, weight=1)
FplGroup.rowconfigure(index=0,weight=1)
FplGroup.grid(row=0,column=0, rowspan=2, sticky="news")
FplWorkArea = ttk.Notebook(master = FplGroup)
FplWorkArea.grid(row=0, column=0, sticky="news")
FplList = tk.Text(master=FplWorkArea, width=120,state="disabled", font=DefaultFontTuple)
FplList.grid(row=0,column=0, sticky="news")
FplWorkArea.add(FplList, text="FLIGHT PLAN")
GamaList = tk.Text(master=FplWorkArea, width=120,state="disabled", font=DefaultFontTuple)
GamaList.grid(row=0,column=0, sticky="news")
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

InsertWpPopUp = tk.Toplevel(master=home)
InsertWpPopUp.protocol("WM_DELETE_WINDOW", InsertWpPopUp.withdraw)
InsertWpGroup = tk.LabelFrame(master = InsertWpPopUp, text = "INSERT WP CMD", font=DefaultFontTuple)
InsertWpGroup.grid(row=0, column=1, sticky='e')
LblInsertIndex = tk.Label(master = InsertWpGroup, text="INDEX:", font=DefaultFontTuple)
LblInsertIndex.grid(row=0,column=0, sticky='w')
LblInsertName = tk.Label(master = InsertWpGroup, text="NAME:", font=DefaultFontTuple)
LblInsertName.grid(row=1,column=0, sticky='w')
LblInsertType = tk.Label(master = InsertWpGroup, text="TYPE:", font=DefaultFontTuple)
LblInsertType.grid(row=2,column=0, sticky='w')
LblInsertClass = tk.Label(master = InsertWpGroup, text="CLASS:", font=DefaultFontTuple)
LblInsertClass.grid(row=3,column=0, sticky='w')
LblInsertLat = tk.Label(master = InsertWpGroup, text="LATITUDE:", font=DefaultFontTuple)
LblInsertLat.grid(row=4,column=0, sticky='w')
LblInsertLon = tk.Label(master = InsertWpGroup, text="LONGITUDE:", font=DefaultFontTuple)
LblInsertLon.grid(row=5,column=0, sticky='w')

CmdInsert = tk.Button(master = InsertWpGroup, text= "INSERT WP", font=DefaultFontTuple,
                      command=InsertWpCallB)
CmdInsert.grid(row=7, column=0)

TxtInsertIndex = tk.Spinbox(master= InsertWpGroup, width=8, font=NumericFontTuple, from_=0, to=200,justify="right")
TxtInsertIndex.grid(row=0,column=1)
TxtInsertName = tk.Entry(master= InsertWpGroup, width=8, font=NumericFontTuple)
TxtInsertName.grid(row=1,column=1)
TxtInsertType = ttk.Combobox(master= InsertWpGroup, width = 8, values= TypeList, font=NumericFontTuple)
TxtInsertType.current(0)
TxtInsertType.grid(row=2,column=1)
TxtInsertClass = ttk.Combobox(master= InsertWpGroup, width = 8,values=ClassList, font=NumericFontTuple)
TxtInsertClass.current(0)
TxtInsertClass.grid(row=3,column=1)
TxtInsertLat = tk.Entry(master= InsertWpGroup, width=8, font=NumericFontTuple)
TxtInsertLat.grid(row=4,column=1)
TxtInsertLon = tk.Entry(master= InsertWpGroup, width=8, font=NumericFontTuple)
TxtInsertLon.grid(row=5,column=1)
ChkInsertFlyOv = tk.Checkbutton(master= InsertWpGroup, text="FLY OVER",
                                variable=WpIsFlyOver, font=NumericFontTuple)
ChkInsertFlyOv.grid(row=6,column=1)

InsertWpPopUp.withdraw()

DeleteWpPopUp = tk.Toplevel(master=home)
DeleteWpPopUp.protocol("WM_DELETE_WINDOW", InsertWpPopUp.withdraw)
DeleteWpGroup = tk.LabelFrame(master = DeleteWpPopUp, text = "DELETE WP CMD", font=DefaultFontTuple)
DeleteWpGroup.grid(row=1, column=1)
LblDeleteIndex = tk.Label(master= DeleteWpGroup, text="DELETE WP INDEX:", font=DefaultFontTuple)
LblDeleteIndex.grid(row=0,column=0)
CmdDelete = tk.Button(master = DeleteWpGroup, text= "DELETE WP",
                      command=RemoveWpCallB, font=DefaultFontTuple)
CmdDelete.grid(row=1, column=0)
TxtDeleteIndex = tk.Spinbox(master= DeleteWpGroup, width=3, font=DefaultFontTuple, from_=0, to=200,justify="right")
TxtDeleteIndex.grid(row=0,column=1)
DeleteWpPopUp.withdraw()

SetCdsCenterPopUp = tk.Toplevel(master=home)
SetCdsCenterPopUp.protocol("WM_DELETE_WINDOW", InsertWpPopUp.withdraw)
SetCdsCenterGroup = tk.LabelFrame(master = SetCdsCenterPopUp, text = "SET CDS CENTER", font=DefaultFontTuple)
SetCdsCenterGroup.grid(row=1, column=1)
SetCdsCenterIndex = tk.Label(master= SetCdsCenterPopUp, text="WP INDEX:", font=DefaultFontTuple)
SetCdsCenterIndex.grid(row=0,column=0)
CmdSetCdsCenter = tk.Button(master = SetCdsCenterPopUp, text= "SET CENTER",
                            command=SetCdsCenter, font=DefaultFontTuple)
CmdSetCdsCenter.grid(row=1, column=0)
TxtCenterIndex = tk.Spinbox(master= SetCdsCenterPopUp, width=3, font=DefaultFontTuple, from_=1, to=200,justify="right")
TxtCenterIndex.grid(row=0,column=1)
SetCdsCenterPopUp.withdraw()


RefreshFpl()

home.mainloop()