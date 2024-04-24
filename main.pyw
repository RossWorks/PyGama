import EDCU.EDCU
import CDS, FMS, HELO, EDCU
import math, os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import HELO.FCS
import HELO.Helicopter

DefaultFontTuple = ("B612 mono", 10, "normal")
MenuFontTuple    = ("B612 mono",  9, "normal")
NumericFontTuple = ("B612", 10, "normal")
KillApp : bool = False
SimulationActive : bool = False
minor : int = 0

FlightPlan = FMS.FlightPlan.FlightPlan(PposLat=math.radians(45.5),
                            PposLon=math.radians(8.7))

FlightController = HELO.FCS.FCS(Mode=1, P=0.5, I=0.0, D=0.0)

FlyingThing = HELO.Helicopter.Helicopter(Lat = math.radians(45.5),
                                         Lon = math.radians(8.70))
FlyingThing.VNS = 60 * 1852 / 3600
FlyingThing.VEW = .5* 60 * 1852 / 3600

def SimulationStep():
  global minor, FlightController, FlyingThing
  FlightController.SetCurrHdg(CurrHdg=FlyingThing.Hdg)
  NewRoll = FlightController.ExecuteStep()
  FlyingThing.SetRollAngle(NewRoll=NewRoll)
  FlyingThing.SimulationStep()
  DisplayUnit.MapCenter = [FlyingThing.Lat, FlyingThing.Lon]
  FMS2EDCUData = EDCU.EDCU.EDCUdata(Lat=FlyingThing.Lat,
                                    Lon=FlyingThing.Lon,
                                    Hdg=FlyingThing.Hdg,
                                    GS=math.sqrt(FlyingThing.VEW**2 + FlyingThing.VNS**2),
                                    BankCmd=FlyingThing.bank)
  ProgressReport.Update(FMS2EDCUData)
  if minor % 1000 == 0:
    DisplayUnit.RefreshFpl(FlightPlan.ExpandedWaypoints)

def SetNewHdgCmd():
  FlightController.SelHdg = math.radians(float(TxtSelHdg.get()))
  FlightController.Mode = 1

def ShowFcs():
  FcsPanel.deiconify()

def StartSimulation():
  global SimulationActive
  SimulationActive = True

def StopSimulation():
  global SimulationActive
  SimulationActive = False

def SetMapAspect():
  #Gama.MapRender.SetCdsCenter(Lat=math.radians(FlightPlan.Waypoints[0].Lat),
  #                            Lon=math.radians(FlightPlan.Waypoints[0].Lon))
  TmpHeading_rad = math.radians(int(TxtNewBearing.get()) + 90)
  DisplayUnit.SetMapRotation(NewHeading=TmpHeading_rad)
  SetCdsRotationPopUp.withdraw()
  RefreshFpl()

def RefreshFpl():
  GamaList.config(state="normal")
  GamaList.delete('1.0',tk.END)
  GamaList.insert('1.0',FlightPlan.__repr__(Gama=True))
  GamaList.config(state="disabled")   
  #2D Gama FPL
  DisplayUnit.RefreshFpl(Fpl=FlightPlan.ExpandedWaypoints)
  
ClassList : list[str] = []
TypeList  : list[str] = []

for key in FMS.FplWaypoint.ClassDict:
  ClassList.append(FMS.FplWaypoint.ClassDict[key])

for key in FMS.FplWaypoint.TypeDict:
  TypeList.append(FMS.FplWaypoint.TypeDict[key])

def DeleteFpl():
  print("Deactivation of Active Flight Plan")
  global FlightPlan
  FlightPlan = FMS.FlightPlan.FlightPlan(PposLat=math.radians(45.5),
                                         PposLon=math.radians(8.7))
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

def ShowDtoPopUp():
  global WpsNames
  TmpList = []
  for point in FlightPlan.Waypoints:
    TmpList.append(point.Name)
  WpsNames.set(TmpList)
  DtoPopUp.deiconify()

def MakeInternalDirTo():
  IndexOfDto = DtoList.curselection()
  print("Selected Wp #" + str(IndexOfDto[0]) + " for D-TO")
  FlightPlan.InternalDirTo(DtoIndex=IndexOfDto[0])
  DtoPopUp.withdraw()
  RefreshFpl()

def ShowCdsAspectPopUp():
  SetCdsRotationPopUp.deiconify()

def InsertWpCallB():
  '''This function calls for a new wp insertion in the active flightplan'''
  MyType  : int = -1
  MyClass : int = -1
  for key in FMS.FlightPlan.FplWaypoint.TypeDict:
    if FMS.FlightPlan.FplWaypoint.TypeDict[key] == TxtInsertType.get():
      MyType = key
  if MyType < 0:
    return
  for key in FMS.FlightPlan.FplWaypoint.ClassDict:
    if FMS.FlightPlan.FplWaypoint.ClassDict[key] == TxtInsertClass.get():
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
  TmpWp = FMS.FlightPlan.FplWaypoint.FplWaypoint(Id= TmpId,
                                                  Name= TxtInsertName.get(),
                                                  Type=MyType,
                                                  Class=MyClass,
                                                  Lat=math.radians(TmpLat),
                                                  Lon=math.radians(TmpLon),
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
    Success = DisplayUnit.SetCdsCenter(Lat=NewLat, Lon=NewLon)
  except IndexError:
    Success = False
  if Success:
    RefreshFpl()
  SetCdsCenterPopUp.withdraw()

def SaveFPL():
  NamePrefix = "FPL"
  termiantion = ".fp"
  SaveDir = "./storage/"
  if not os.path.isdir(SaveDir):
    os.mkdir(SaveDir)
  FileList = os.listdir(SaveDir)
  ProposedFileName = (NamePrefix + '999'.rjust(3,'0') + termiantion)
  for number in range(1,31):
    if (NamePrefix + str(number).rjust(3,'0') + termiantion) not in FileList:
      ProposedFileName = (NamePrefix + str(number).rjust(3,'0') + termiantion)
      break
  FileContent = FlightPlan.FormatForFile()
  FileName = filedialog.asksaveasfilename(confirmoverwrite=True, initialdir=SaveDir, initialfile=ProposedFileName)
  if len(FileName) < 1:
    return
  FilePtr = open(FileName, mode='w')
  FilePtr.writelines(FileContent)
  FilePtr.close()
  return

def LoadFPL():
  FileName = filedialog.askopenfilename(defaultextension='fp', initialdir="./storage/")
  FilePtr = open(file=FileName, mode='r')
  global FlightPlan
  FlightPlan = FMS.FlightPlan.FlightPlan(PposLat=math.radians(45.5),
                                          PposLon=math.radians(8.7))
  Index = 1
  for line in FilePtr:
    WpInfo=line.split(sep=';')
    MyWp = FMS.FlightPlan.FplWaypoint.FplWaypoint(Id = Index, Name=WpInfo[0], Type=int(WpInfo[1].strip()),
                                                   Class=int(WpInfo[2].strip()),
                                                   Lat=float(WpInfo[3]),
                                                   Lon=float(WpInfo[4]),
                                                   isFlyOver= WpInfo[5] == "FLY OV")
    FlightPlan.InsertWp(Wpt=MyWp, InsertInPos=Index)
    Index += 1
  FilePtr.close()
  RefreshFpl()

def TerminateApp():
  global KillApp
  KillApp = True
  home.destroy()
  exit()

home = tk.Tk()
home.protocol("WM_DELETE_WINDOW", TerminateApp)
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
WpsNames = tk.StringVar(master = home)

MainMenuBar = tk.Menu(master=home)
FplMenu     = tk.Menu(master=MainMenuBar, tearoff=0)
ProcMenu    = tk.Menu(master=MainMenuBar, tearoff=0)
ViewMenu    = tk.Menu(master=MainMenuBar, tearoff=0)
SimMenu     = tk.Menu(master=MainMenuBar, tearoff=0)
home.config(menu=MainMenuBar)

MainMenuBar.add_cascade(label="ACTIVE FLIGHT PLAN",menu=FplMenu,font=MenuFontTuple)
FplMenu.add_command(label="Deactivate FPL", command=DeleteFpl, image=DeactFPL_Icon, compound="left", font=MenuFontTuple)
FplMenu.add_command(label="Direct To...", state="active", image=DTO_Icon, compound="left", font=MenuFontTuple,command=ShowDtoPopUp)
FplMenu.add_command(label="Insert Waypoint...", image=InsertWp_Icon, compound="left", font=MenuFontTuple, command=ShowInsertWpPopUp)
FplMenu.add_command(label="Delete Waypoint...", image=DeleteWp_Icon, compound="left", font=MenuFontTuple,command=ShowDeleteWpPopUp)
FplMenu.add_command(label="SAR...", state="disabled", image=SAR_Icon, compound="left", font=MenuFontTuple)
FplMenu.add_command(label="Save FPL...", state="active", image=SaveFpl_Icon, compound="left", font=MenuFontTuple, command=SaveFPL)
FplMenu.add_command(label="Load FPL...", state="active", image=LoadFpl_Icon, compound="left", font=MenuFontTuple, command=LoadFPL)

MainMenuBar.add_cascade(label="PROCEDURES",menu=ProcMenu,font=MenuFontTuple)
ProcMenu.add_command(label="Load SID...", state="disabled", font=MenuFontTuple)
ProcMenu.add_command(label="Load STAR...", state="disabled", font=MenuFontTuple)

MainMenuBar.add_cascade(label="VIEW CONTROL",menu=ViewMenu, font=MenuFontTuple)
ViewMenu.add_command(label="CENTER ON HELI",state="active", font= MenuFontTuple, command=SetMapAspect)
ViewMenu.add_command(label="CENTER ON WPT...",state="normal",command=ShowSetCdsCenterPopUp)
ViewMenu.add_command(label="CENTER ON OBJECT...",state="disabled")
ViewMenu.add_command(label="ROTATE MAP...",state="normal",command=ShowCdsAspectPopUp)

MainMenuBar.add_cascade(label="HELO CONTROL",menu=SimMenu, font=MenuFontTuple)
SimMenu.add_command(label="START SIMULATION",state="normal", font= MenuFontTuple,command=StartSimulation)
SimMenu.add_command(label="STOP SIMULATION",state="normal", font= MenuFontTuple, command=StopSimulation)
SimMenu.add_command(label="SIM STEP",state="normal", command=SimulationStep)
SimMenu.add_command(label="FCS PANEL",state="normal",command=ShowFcs)

FplGroup = tk.LabelFrame(master = home, text="GRAPHICAL AREA", font=DefaultFontTuple)
FplGroup.columnconfigure(index= 0, weight=1)
FplGroup.rowconfigure(index=0,weight=1)
FplGroup.grid(row=0,column=0, rowspan=2, sticky="news")
FplWorkArea = ttk.Notebook(master = FplGroup)
FplWorkArea.grid(row=0, column=0, sticky="news")
ProgressReport = EDCU.EDCU.EDCU(master=FplWorkArea)
FplWorkArea.add(ProgressReport.Screen, text="EDCU")
GamaList = tk.Text(master=FplWorkArea, width=120,state="disabled", font=DefaultFontTuple)
GamaList.grid(row=0,column=0, sticky="news")
FplWorkArea.add(GamaList, text="GAMA PROTOCOL")
DisplayUnit = CDS.Display.Display(MasterWidget=FplWorkArea)
FplWorkArea.add(DisplayUnit.DisplayWidget, text="CDS MAP")

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
DeleteWpPopUp.protocol("WM_DELETE_WINDOW", DeleteWpPopUp.withdraw)
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

FcsPanel = tk.Toplevel(master=home)
FcsPanel.protocol("WM_DELETE_WINDOW", FcsPanel.withdraw)
LnavGroup = tk.LabelFrame(master = FcsPanel, text = "LNAV", font=DefaultFontTuple)
LnavGroup.grid(row=1, column=1)
LblSelHdg = tk.Label(master= LnavGroup, text="SELECTED HDG", font=DefaultFontTuple)
LblSelHdg.grid(row=0,column=0)
CmdHdgMode = tk.Button(master = LnavGroup, text= "SET HDG",
                      command=SetNewHdgCmd, font=DefaultFontTuple)
CmdHdgMode.grid(row=1, column=0)
TxtSelHdg = tk.Spinbox(master= LnavGroup, width=3, font=DefaultFontTuple, from_=0, to=359,justify="center")
TxtSelHdg.grid(row=0,column=1)
FcsPanel.withdraw()

SetCdsCenterPopUp = tk.Toplevel(master=home)
SetCdsCenterPopUp.protocol("WM_DELETE_WINDOW", SetCdsCenterPopUp.withdraw)
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

SetCdsRotationPopUp = tk.Toplevel(master=home)
SetCdsRotationPopUp.protocol("WM_DELETE_WINDOW", SetCdsRotationPopUp.withdraw)
SetCdsRotationGroup = tk.LabelFrame(master = SetCdsRotationPopUp, text = "SET MAP ROTATION", font=DefaultFontTuple)
SetCdsRotationGroup.grid(row=1, column=1)
SetCdsRotationIndex = tk.Label(master= SetCdsRotationGroup, text="NEW BEARING:", font=DefaultFontTuple)
SetCdsRotationIndex.grid(row=0,column=0)
CmdSetCdsRotation = tk.Button(master = SetCdsRotationGroup, text= "ROTATE MAP",
                            command=SetMapAspect, font=DefaultFontTuple)
CmdSetCdsRotation.grid(row=1, column=0)
TxtNewBearing = tk.Spinbox(master= SetCdsRotationGroup, width=3, font=DefaultFontTuple, from_=1, to=360, justify="right")
TxtNewBearing.grid(row=0,column=1)
SetCdsRotationPopUp.withdraw()

DtoPopUp = tk.Toplevel(master=home)
DtoPopUp.protocol("WM_DELETE_WINDOW", DtoPopUp.withdraw)
InternalDtoGroup = tk.LabelFrame(master=DtoPopUp, text="INTERNAL D-TO", font=DefaultFontTuple)
InternalDtoGroup.grid(row=0,column=0)
DtoList = tk.Listbox(master=InternalDtoGroup, font=DefaultFontTuple, listvariable=WpsNames,
                     selectmode=tk.SINGLE)
DtoList.grid(row=0,column=0)
CmdIntDto = tk.Button(master=DtoPopUp, text="D-TO", font=DefaultFontTuple, command=MakeInternalDirTo)
CmdIntDto.grid(row=1,column=1)
CmdExtDto = tk.Button(master=DtoPopUp, state="disabled", text="EXT D-TO", font=DefaultFontTuple)
CmdExtDto.grid(row=0,column=1)
DtoPopUp.withdraw()

RefreshFpl()

while(not KillApp):
  if SimulationActive:
    SimulationStep()
  home.update()
  minor += 1
