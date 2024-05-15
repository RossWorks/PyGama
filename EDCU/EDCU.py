if __name__ == "__main__":
  print("Standalone operation not permitted!")
  exit()

import tkinter as tk
import math
from FMS.FlightPlan import FplWaypoint

class EDCUdata:

  def __init__(self) -> None:
    self.Lat = 0.0
    self.Lon = 0.0
    self.Hdg = 0.0
    self.GS = 0.0
    self.Time2Go_To = 0
    self.Distance2Go_To = 0.0
    self.Time2Go_Next = 0
    self.Distance2Go_Next = 0.0
    self.Time2Go_Dest = 0
    self.Distance2Go_Dest = 0.0
    self.Fpl : list[FplWaypoint.FplWaypoint] = []

class FplEntryWidget:
  
  def __init__(self, master : tk.Widget) -> None:
    self.DefaultFontTuple = ("B612 mono", 12, "normal")
    self.NeutralBgColor = '#2c3e50'


    self.Slot = tk.Frame(master=master, background=self.NeutralBgColor, padx=5, pady=15)
    self.WpName = tk.Label(master=self.Slot, font=self.DefaultFontTuple, width=6, anchor='w', background=self.NeutralBgColor)
    self.WpName.grid(row=0,column=0, padx=10, sticky='w')
    self.FlyOverFlag = tk.Label(master=self.Slot, text=' ', font=self.DefaultFontTuple, background=self.NeutralBgColor)
    self.FlyOverFlag.grid(row=0,column =1, padx=10)

  def SetAsFrom(self):
    self.WpName.config(foreground='yellow')

  def SetAsTo(self):
    self.WpName.config(foreground='magenta')

  def SetFlyOver(self):
    self.FlyOverFlag.config(text='F', background='cyan')

  def SetFlyBy(self):
    self.FlyOverFlag.config(text=' ', background=self.NeutralBgColor)

  def SetAsBlank(self):
    self.FlyOverFlag.config(text=' ', background=self.NeutralBgColor)
    self.WpName.config(text=6*' ', background=self.NeutralBgColor)



class EDCU:
  
  def __init__(self, master : tk.Widget) -> None:
    self.DefaultFontTuple = ("B612 mono", 12, "normal")
    self.Screen = tk.Frame(master=master)

    self.PposLat          = tk.StringVar(master=self.Screen, value= "N 0.0".ljust(6,'0'))
    self.PposLon          = tk.StringVar(master=self.Screen, value= "E 0.0".ljust(6,'0'))
    self.Gs               = tk.StringVar(master=self.Screen, value= "0" + " KTS")
    self.Hdg              = tk.StringVar(master=self.Screen, value= "0" + " °")
    self.Time2Go_To       = tk.StringVar(master=self.Screen, value= "0" + " °")
    self.Distance2Go_To   = tk.StringVar(master=self.Screen, value= "0" + " NM")
    self.Time2Go_Next     = tk.StringVar(master=self.Screen, value= "0" + " °")
    self.Distance2Go_Next = tk.StringVar(master=self.Screen, value= "0" + " NM")
    self.Time2Go_Dest     = tk.StringVar(master=self.Screen, value= "0" + " °")
    self.Distance2Go_Dest = tk.StringVar(master=self.Screen, value= "0" + " NM")

    self.PposFrame = tk.LabelFrame(master=self.Screen, text="PRESENT POSITION", font=self.DefaultFontTuple)
    self.PposFrame.grid(row=0,column=0, columnspan=2,padx=10, pady=10, sticky='ew')
    self.LblLat = tk.Label(master=self.PposFrame, textvariable=self.PposLat, font=self.DefaultFontTuple)
    self.LblLat.grid(row=0, column=0, padx=10, pady=0)
    self.LblLon = tk.Label(master=self.PposFrame, textvariable=self.PposLon, font=self.DefaultFontTuple)
    self.LblLon.grid(row=0, column=1, padx=10, pady=0)
    self.Fplprogress = tk.LabelFrame(master=self.Screen, text= "PROGRESS", font=self.DefaultFontTuple)
    self.Fplprogress.grid(row=3,column=0, columnspan=2, padx=10, pady=10, sticky='news')
    self.LblTo = tk.Label(master=self.Fplprogress, text="TO", font=self.DefaultFontTuple, foreground='magenta')
    self.LblTo.grid(row=0,column=0, padx=10, pady=10, sticky='w')
    self.LblNext = tk.Label(master=self.Fplprogress, text="NEXT", font=self.DefaultFontTuple, foreground='black')
    self.LblNext.grid(row=1,column=0, padx=10, pady=10, sticky='w')
    self.LblDest = tk.Label(master=self.Fplprogress, text="DEST", font=self.DefaultFontTuple, foreground='black')
    self.LblDest.grid(row=2,column=0, padx=10, pady=10, sticky='w')
    self.LblTime2To = tk.Label(master=self.Fplprogress, textvariable=self.Time2Go_To, font=self.DefaultFontTuple, foreground='magenta')
    self.LblTime2To.grid(row=0,column=1, padx=10, pady=10, sticky='w')
    self.LblTime2Next = tk.Label(master=self.Fplprogress, textvariable=self.Time2Go_Next, font=self.DefaultFontTuple, foreground='black')
    self.LblTime2Next.grid(row=1,column=1, padx=10, pady=10, sticky='w')
    self.LblTime2Dest = tk.Label(master=self.Fplprogress, textvariable=self.Time2Go_Dest, font=self.DefaultFontTuple, foreground='black')
    self.LblTime2Dest.grid(row=2,column=1, padx=10, pady=10, sticky='w')
    self.LblDistance2To = tk.Label(master=self.Fplprogress, textvariable=self.Distance2Go_To, font=self.DefaultFontTuple, foreground='magenta')
    self.LblDistance2To.grid(row=0,column=2, padx=10, pady=10, sticky='w')
    self.LblDistance2Next = tk.Label(master=self.Fplprogress, textvariable=self.Distance2Go_Next, font=self.DefaultFontTuple, foreground='black')
    self.LblDistance2Next.grid(row=1,column=2, padx=10, pady=10, sticky='w')
    self.LblDistance2Dest = tk.Label(master=self.Fplprogress, textvariable=self.Distance2Go_Dest, font=self.DefaultFontTuple, foreground='black')
    self.LblDistance2Dest.grid(row=2,column=2, padx=10, pady=10, sticky='w')

    self.GsDataFrame = tk.LabelFrame(master=self.Screen, text= "GROUND SPEED", font=self.DefaultFontTuple)
    self.GsDataFrame.grid(row=1,column=0, padx=10, pady=10)
    self.LblGs = tk.Label(master=self.GsDataFrame, text="0 KT", font=self.DefaultFontTuple, foreground='black', textvariable=self.Gs)
    self.LblGs.grid(row=0,column=0, padx=10, pady=10)
    self.HdgDataFrame = tk.LabelFrame(master=self.Screen, text= "HEADING", font=self.DefaultFontTuple)
    self.HdgDataFrame.grid(row=1,column=1, padx=10, pady=10)
    self.LblHdg = tk.Label(master=self.HdgDataFrame, text="0 °", font=self.DefaultFontTuple, foreground='black', textvariable=self.Hdg)
    self.LblHdg.grid(row=0,column=0, padx=10, pady=10)

    self.FplList = tk.LabelFrame(master=self.Screen, width=70, font=self.DefaultFontTuple, text="FLIGHT PLAN")
    self.TmpList = []
    for index in range(5):
      self.TmpList.append(FplEntryWidget(master=self.FplList))
      self.TmpList[index].Slot.grid(row=index, column=0)
    self.FplList.grid(row=0,column=2, rowspan=4, sticky="news")

  def Update(self, Data : EDCUdata):
    self.PposLat.set(value = Rad2Coords(Data.Lat, True))
    self.PposLon.set(Rad2Coords(Data.Lon,False))
    self.Gs.set(str(Data.GS/1852*3600)[0:4])
    self.Hdg.set(str(180/3.14 *Data.Hdg)[0:4] + ' °')
    if Data.Distance2Go_To == Data.Distance2Go_To :
      self.Distance2Go_To.set(str(Data.Distance2Go_To/1852)[0:str(Data.Distance2Go_Dest/1852).find('.') + 2] + " NM")
    self.Time2Go_To.set(Sec2hh_mm(Data.Time2Go_To))
    if Data.Distance2Go_Next == Data.Distance2Go_Next:
      self.Distance2Go_Next.set(str(Data.Distance2Go_Next/1852)[0:str(Data.Distance2Go_Dest/1852).find('.') + 2] + " NM")
    self.Time2Go_Next.set(Sec2hh_mm(Data.Time2Go_Next))
    if Data.Distance2Go_Dest == Data.Distance2Go_Dest:
      self.Distance2Go_Dest.set(str(Data.Distance2Go_Dest/1852)[0:str(Data.Distance2Go_Dest/1852).find('.') + 2] + " NM")
    self.Time2Go_Dest.set(Sec2hh_mm(Data.Time2Go_Dest))
    for index in range(5):
      if index < len(Data.Fpl):
        self.TmpList[index].WpName.config(text=Data.Fpl[index].Name)
        if Data.Fpl[index].WpReprCat == 0:
          self.TmpList[index].SetAsFrom()
        elif Data.Fpl[index].WpReprCat == 1:
          self.TmpList[index].SetAsTo()
        else:
          self.TmpList[index].WpName.config(foreground='black')
        if not Data.Fpl[index].FlyOver or Data.Fpl[index].WpReprCat == 0:
          self.TmpList[index].SetFlyBy()
        else:
          self.TmpList[index].SetFlyOver()
      else:
        self.TmpList[index].SetAsBlank()

def Sec2hh_mm(seconds : int) -> str:
  if seconds != seconds:
    return 4 * '-'
  hours = int(seconds) // 3600
  minutes = int(((seconds/3600) - hours) * 60)
  return str(hours) + ":" + str(minutes)

def Rad2Coords(radians : float, isLat : bool) -> str:
  raw_degrees = math.degrees(radians)
  degrees = int(raw_degrees)
  minutes = (raw_degrees - degrees) * 60
  minutes_str = str(minutes)
  dotIndex = minutes_str.find('.')
  if isLat:
    output = 'N' if degrees >= 0 else 'S'
  else:
    output = 'E' if degrees >= 0 else 'W'
  output += str(degrees) + "°" + minutes_str[0:dotIndex+3] + '\''
  return output 
  
