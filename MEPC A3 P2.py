#========================================================================================#
"""
MEPC Engineering Mechanics Assignment-3 Problem-2

Problem Statement: Given the initial 2D position and velocity of a projectile, produce
ananimated graph of its trajectory using the python programming language.

Author: S.Nishanth Vikraman
Roll Number: 111119120
Department: Mechanical Engineering
Degree: Bachelor of Technology
Batch: 2019-2023
"""
#========================================================================================#

#Importing necessary modules
import tkinter as tk
from math import ceil, sqrt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

#Setting up necessary global variables
p = 0
length = 0

#Setting up the plot
plt.style.use('seaborn-darkgrid')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel('X Axis (m)')
ax.set_ylabel('Y Axis (m)')
ax.set_title('2D Projectile Animation (x vs y)', fontsize = 12, fontweight ='bold')
xdata, ydata = [], []
line, = ax.plot(0,0)

#-----------------------------------------------------------------------------------------#

#|GRAPH ANIMATION CONTROL SECTION|#

#Start and Pause Graph
def start():
    global p
    global length
    VXi = float(entryVelocityX.get())
    VYi = float(entryVelocityY.get())
    Xi = float(entryXi.get())
    Yi = float(entryYi.get())

    #Negative height error check
    if(Yi<0):
        lblYi["text"] = "Invalid initial Y coordinate. Input a positive height value."
        btnStart["text"] = "Try again"
        return

    #Initiate graphing
    if(p==0):
        btnStart["text"] = "Pause"
        lblYi["text"] = "Initial Y coordinate (m):"
        p = 1
        length = ceil((20.0/9.8)*(VYi + sqrt(VYi**2 + 19.6*Yi)))
        for frameIndex in range(length):
            xdata.append(Xi + VXi*(frameIndex)*0.05)
            ydata.append(Yi + VYi*frameIndex*0.05 - 4.95*((frameIndex*0.05)**2))
        xdata.append(xdata[length-1])
        ydata.append(ydata[length-1])
        ax.set_xlim(Xi-3, 1 + Xi + VXi*((VYi/4.9) + sqrt(Yi/4.9)))
        ax.set_ylim(0, 1 + Yi + (VYi**2)/19.6)
        plt.annotate(s='Starting Point: (' + str(Xi) + ',' + str(Yi) + ')', xy=(Xi, Yi), xytext=(Xi, Yi-1))
        anim = FuncAnimation(fig, func=run, frames=gen, fargs=(xdata, ydata), interval=20, blit=True)
        return

    #Close the application
    elif(p==2):
        btnStart["text"] = "Thank you!"
        window.after(800, window.destroy)
        return
    
    #Pause graphing
    p = 0
    btnStart["text"] = "Continue"

#-----------------------------------------------------------------------------------------#

#|MAIN GRAPHING SECTION|# 

frame = -1

#Generator function for providing time-frame numbers to Animator
def gen():
    global p
    global length
    global frame
    while(frame < length): 
        if(p==1):
            #Graphing in progress
            frame += 1
            yield frame
        elif(p==0):
            #Graph paused
            yield frame
    #Graph Over
    p = 2
    btnStart["text"] = "Simulation Over\nQuit?"
    btnStart["state"] = "active"
    yield frame

#Animator function to draw graph
def run(frame, xdata, ydata):
    lblX["text"] = "X = " + str(round(xdata[frame], 3))
    lblY["text"] = "Y = " + str(round(ydata[frame], 3))
    lblTime["text"] = "Time Elapsed: " + str(round((frame*0.05), 3))
    line.set_xdata(xdata[0:frame])
    line.set_ydata(ydata[0:frame])
    return line,    

#-----------------------------------------------------------------------------------------#

#|INTERACTIVE MENU SETUP SECTION|#

window = tk.Tk()
window.title("Animated Graph of the trajectory of a 2D Projectile")
window.configure(background='red')

frmDetails = tk.Frame(
    master = window, 
    background='red'
)

lblWelcome = tk.Label(master=frmDetails, text='Hello! Welcome to my MEPC \
Assignment-3 Problem-2 Applet! \nEnter the required details below for a \
3D projectile to see the graph: \n\n', bg='red')
lblWelcome.pack()

entryVelocityX = tk.Entry(master=frmDetails)
entryVelocityX.pack()
lblVelocityX = tk.Label(master=frmDetails, text='Initial X component of velocity\'s magnitude (m/s)', bg='red')
lblVelocityX.pack()

entryVelocityY = tk.Entry(master=frmDetails)
entryVelocityY.pack()
lblVelocityY = tk.Label(master=frmDetails, text='Initial Y component of velocity\'s magnitude (m/s)', bg='red')
lblVelocityY.pack()

entryXi = tk.Entry(master=frmDetails)
entryXi.pack()
lblXi = tk.Label(master=frmDetails, text='Initial X coordinate (m):', bg='red')
lblXi.pack()

entryYi = tk.Entry(master=frmDetails)
entryYi.pack()
lblYi = tk.Label(master=frmDetails, text='Initial Y coordinate (m):', bg='red')
lblYi.pack()

btnStart = tk.Button(master=frmDetails, text="Enter->", command=start)
btnStart.pack()

lblTime = tk.Label(master=frmDetails, bg='red')
lblTime.pack()

lblX = tk.Label(master=frmDetails, bg='red')
lblX.pack()

lblY = tk.Label(master=frmDetails, bg='red')
lblY.pack()

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().grid(column=1, row=1)
canvas.draw()

frmDetails.grid(column=2, row=1)

toolbarFrame = tk.Frame(
    master = window, 
    relief = tk.RAISED,
    borderwidth = 2, 
    background='red'
)
toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
toolbar.update()
toolbarFrame.grid(row=2, column=1)


window.mainloop()

#Code End.
#-----------------------------------------------------------------------------------------#
