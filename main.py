# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 19:36:24 2020

@author: Manuel
"""

import os
# import all classes/methods 
# from the tkinter module 
import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import pandas as pd


class plot_window():
    def __init__(self,title = "Title",x_label = "Time in sec", y_label = "Value"):
        # Generate some start/example data
        self.X = 0
        self.Y = 0
        # Setup the graph
        self.fig = Figure(figsize = (7, 5), dpi = 100)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.line1, = self.ax.plot(self.X, self.Y)
        
        self.ax.set_title(title)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.set_xlim(0,10)
        self.ax.set_ylim(0,10)
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, window)
        self.canvas.get_tk_widget().grid(row = 0, column = 0, sticky="nsew")
            
    def updateData(self,df):
        print(df.head())
        self.X = df.X
        self.Y = df.Y
        # pl1.line1.set_xdata(df.X)
        # pl1.line1.set_ydata(df.Y)
        self.line1.set_data(df.X,df.Y)
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, window)
        self.canvas.get_tk_widget().grid(row = 0, column = 0, sticky="nsew")
        # self.canvas.draw()
        

# def get_data_from_new_file(path):
#     print("In here")
#     print(path)
    
#     raw_path=os.path.join(path.split("\\"))
#     print(raw_path)
#     df = pd.read_csv(path,sep=";")

#     return df


def _watch(root,pl1):

    class handler(FileSystemEventHandler):
        def on_moved(self, event):
            
            print("----------Jetzt--------------------")
            print(event)
            # try:
            print("dest Path: " + event.dest_path)
            
            global newFile
            newFile = r"{0}".format(event.dest_path)
            
            print("Newfile: " + newFile)
            df = pd.read_csv(newFile,sep=";")#get_data_from_new_file(event.dest_path)
            # print(df.head())
            # pl1.X = df.X
            # pl1.Y =df.Y
            pl1.updateData(df)
            # except:
                # print("Other event then fileMovedEvent")
 

    observer = Observer()
    observer.schedule(handler(), root, recursive=True)
    observer.start()

    print("Watching '{0}' ...".format(root))
    return observer 

  
# The main tkinter window 
window = tk.Tk() 
  
# setting the title and  
window.title('Plotting in Tkinter') 
  
# setting the dimensions of  
# the main window 
window.geometry("900x700") 



# set up 1 plotting window
pl1 = plot_window()


  
# button that would displays the plot 
switch_variable = tk.StringVar(value="auto")

automatic_button = tk.Radiobutton(window, text="Automatic", variable=switch_variable,
                            indicatoron=False, value="auto", width=8)
manual_button = tk.Radiobutton(window, text="Manual", variable=switch_variable,
                            indicatoron=False, value="manual", width=8)

# place the button 
# into the window 
automatic_button.grid(row = 1, column = 0) 
manual_button.grid(row = 2, column = 0) 



path = r"C:\Users\Manuel\Desktop\github\plotter\plotter\Test"
    
observer = _watch(path,pl1)


try:
    # run the gui 
    window.mainloop()
finally:
    observer.stop()
    observer.join()


