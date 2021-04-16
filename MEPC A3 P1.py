 #========================================================================================#
"""
MEPC Engineering Mechanics Assignment-3 Problem-1

Problem Statement: Given the initial 2D position, speed and inclination angle with
horizontal of a projectile, produce ananimated graph of height against time using the
python programming language.

Author: S.Nishanth Vikraman
Roll Number: 111119120
Department: Mechanical Engineering
Degree: Bachelor of Technology
Batch: 2019-2023
"""
#========================================================================================#

#Importing necessary modules
import tkinter as tk
from math import ceil, sqrt, sin, pi
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

#Setting up variables
p = 0
y = 1.0

#Configuring the plot
plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
ax.set_xlabel("Time (s)")
ax.set_ylabel("Height (m)")
ax.set_title('2D Projectile Animation (Height vs Time)', fontsize = 12, fontweight ='bold') 
xdata, ydata = [], []
line, = ax.plot([], [], lw=2)
#line, = ax.plot(0,0)

#-----------------------------------------------------------------------------------------#

#|GRAPH ANIMATION CONTROL SECTION|#

#Start and Pause Graph
def start():
    global p
    global v
    global xdata
    global ydata
    global line
    global length
    v = float(entryVelocity.get())
    height = float(entryHeight.get())
    inclination = (float(entryInclination.get())*pi)/180

    #Negative height error check
    if(height<0):
        lblHeight["text"] = "Invalid height. Input a positive height value."
        btnStart["text"] = "Try again"
        return

    #Initiate graphing
    if(p==0):
        btnStart["text"] = "Pause"
        lblHeight["text"] = "Initial height from ground (m)"
        length = ceil((20.0/9.8)*(v*sin(inclination) + sqrt((v*sin(inclination))**2 + 19.6*height)))
        for frameIndex in range(length+1):
            xdata.append(frameIndex*0.05)
            ydata.append(height + v*(sin(inclination))*frameIndex*0.05 - 4.9*((frameIndex*0.05)**2))
        xdata.append(xdata[length])
        ydata.append(ydata[length])
        ax.set_xlim(0, length/20.0 + 1)
        ax.set_ylim(0, 1 + height + ((v*sin(inclination))**2)/19.6)
        p = 1
        anim = FuncAnimation(fig, func=run, frames=gen, fargs=(xdata, ydata), interval=20, repeat=False, blit=True)
        return

    #Close the application
    elif(p==2):
        btnStart["text"] = "Thank you!"
        window.after(800, window.destroy)
        return
            
    #Pause graphing 
    btnStart["text"] = "Continue"
    p = 0

#-----------------------------------------------------------------------------------------#

#|MAIN GRAPHING SECTION|#

frame = -1

#Generator function for providing time-frame numbers to Animator
def gen():
    global p
    global frame
    global length
    while(frame <= length):
        if(p==1):
            #Graphing in progress
            frame += 1
            yield frame
        elif(p==0):
            #Graph paused
            yield frame
        else:
            frame = 0
            break
    #Graph Over
    p = 2
    btnStart["text"] = "Simulation Over\nQuit?"
    btnStart["state"] = "active"
    yield frame

#Animator function to draw graph
def run(frame, xdata, ydata):
    lblY["text"] = "Height = " + str(round(ydata[frame], 3))
    lblTime["text"] = "Time Elapsed: " + str(round((frame*0.05),3))
    line.set_xdata(xdata[0:frame])
    line.set_ydata(ydata[0:frame])
    return line,

#-----------------------------------------------------------------------------------------#

#|INTERACTIVE MENU SETUP SECTION|#

window = tk.Tk()
window.title("Height-Time Animated Graph for a 2D Projectile")
window.configure(background='red')

frmDetails = tk.Frame(
    master = window, 
    background='red'
)

lblWelcome = tk.Label(master=frmDetails, text='Hello! Welcome to my MEPC Assignment-3 \
Problem-1 Applet!\n Enter the required details \
below for a 2D projectile to see the graph', bg='red')
lblWelcome.pack()

entryVelocity = tk.Entry(master=frmDetails)
entryVelocity.pack()

lblVelocity = tk.Label(master=frmDetails, text='Initial velocity magnitude (m/s)', bg='red')
lblVelocity.pack()

entryHeight = tk.Entry(master=frmDetails)
entryHeight.pack()

lblHeight = tk.Label(master=frmDetails, text='Initial height from ground (m)', bg='red')
lblHeight.pack()

entryInclination = tk.Entry(master=frmDetails)
entryInclination.pack()

lblInclination = tk.Label(master=frmDetails, text='Initial inclination with horizontal (degrees)', bg='red')
lblInclination.pack()

btnStart = tk.Button(master=frmDetails, text="Enter->", command=start)
btnStart.pack()

lblTime = tk.Label(master=frmDetails, bg='red')
lblTime.pack()

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

#-----------------------------------------------------------------------------------------#
