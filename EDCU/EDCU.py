if __name__ == "__main__":
  print("Standalone operation not permitted!")
  exit()

import tkinter as tk

class EDCUdata:

  def __init__(self, Lat, Lon, Hdg, GS, BankCmd) -> None:
    self.Lat = Lat 
    self.Lon = Lon
    self.Hdg = Hdg
    self.GS = GS
    self.BankCmd = BankCmd


class EDCU:
  
  def __init__(self, master : tk.Widget) -> None:
    self.DefaultFontTuple = ("B612 mono", 12, "normal")
    self.Screen = tk.Frame(master=master)

    self.PposLat = tk.StringVar(master=self.Screen, value= "N 0.0".ljust(6,'0'))
    self.PposLon = tk.StringVar(master=self.Screen, value="E 0.0".ljust(6,'0'))
    self.Gs = tk.StringVar(master=self.Screen, value="0" + " KTS")
    self.Hdg = tk.StringVar(master=self.Screen, value="0" + " °")

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
    self.GsDataFrame = tk.LabelFrame(master=self.Screen, text= "GROUND SPEED", font=self.DefaultFontTuple)
    self.GsDataFrame.grid(row=1,column=0, padx=10, pady=10)
    self.LblGs = tk.Label(master=self.GsDataFrame, text="0 KT", font=self.DefaultFontTuple, foreground='black', textvariable=self.Gs)
    self.LblGs.grid(row=0,column=0, padx=10, pady=10)
    self.HdgDataFrame = tk.LabelFrame(master=self.Screen, text= "HEADING", font=self.DefaultFontTuple)
    self.HdgDataFrame.grid(row=1,column=1, padx=10, pady=10)
    self.LblHdg = tk.Label(master=self.HdgDataFrame, text="0 °", font=self.DefaultFontTuple, foreground='black', textvariable=self.Hdg)
    self.LblHdg.grid(row=0,column=0, padx=10, pady=10)
    self.LblRoll = tk.Label(master=self.HdgDataFrame, text="0 °", font=self.DefaultFontTuple, foreground='black', textvariable=self.Hdg)
    self.LblRoll.grid(row=0,column=1, padx=10, pady=10)
    self.FplList = tk.Text(master=self.Screen, width=70,state="disabled", font=self.DefaultFontTuple)
    self.FplList.grid(row=0,column=2, rowspan=4, sticky="news")

  def Update(self, Data : EDCUdata):
    self.PposLat.set(value = str(180/3.14 * Data.Lat)[0:6])
    self.PposLon.set(str(180/3.14 *Data.Lon)[0:6])
    self.Gs.set(str(Data.GS/1852*3600)[0:4])
    self.Hdg.set(str(180/3.14 *Data.Hdg)[0:4])
