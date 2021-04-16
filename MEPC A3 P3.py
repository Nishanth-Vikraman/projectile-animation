#========================================================================================#
"""
MEPC Engineering Mechanics Assignment-3 Problem-3

Problem Statement: Given the initial position and velocity of a particle, produce the
animated trajectory using the python programming language.

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
from numpy import empty
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

#Setting up necessary global variables
length = 0.0
p = 0

#Setting up the plot
fig = plt.figure(facecolor = 'black')
ax = p3.Axes3D(fig)
#plt.style.use('seaborn-darkgrid')
ax.set_title('3D Projectile Animation (x vs y vs z)', fontsize = 12, fontweight ='bold')
ax.set_xlabel('X Axis (m)')
ax.set_ylabel('Z Axis (m)')
ax.set_zlabel('Y Axis (m)')

#-----------------------------------------------------------------------------------------#

#|GRAPH ANIMATION CONTROL SECTION|#

#Start and Pause Graph
def start():
    global p
    global length
    VXi = float(entryVelocityX.get())
    VYi = float(entryVelocityY.get())
    VZi = float(entryVelocityZ.get())
    Xi = float(entryXi.get())
    Yi = float(entryYi.get())
    Zi = float(entryZi.get())

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
        ax.set_xlim(Xi-3, 1 + Xi + VXi*((VYi/4.9) + sqrt(Yi/4.9)))
        ax.set_zlim(0, 1 + Yi + (VYi**2)/19.6)
        ax.set_ylim(Zi-1, 1 + Zi + VZi*((VYi/4.9) + sqrt(Yi/4.9)))
        length = ceil((20.0/9.8)*(VYi + sqrt(VYi**2 + 19.6*Yi)))
        ax.view_init(elev=20, azim=135)
        lineData = empty((3, length+1))
        for frameIndex in range(length):
            lineData[0, frameIndex] = Xi + VXi*(frameIndex*0.05)
            lineData[2, frameIndex] = Yi + VYi*frameIndex*0.05 - 4.95*((frameIndex*0.05)**2)
            lineData[1, frameIndex] = Zi + VZi*(frameIndex*0.05)
        lineData[:, length] = lineData[:, length-1]
        line = ax.plot(lineData[0, 0:1], lineData[1, 0:1], lineData[2, 0:1])[0]
        anim = FuncAnimation(fig, func=run, frames=gen, fargs=(line, lineData), interval=20, blit=True)
        #plt.show()
        return

    #Close the application
    elif(p==2):
        ax.set_title('Thank You!', fontsize = 12, fontweight ='bold')
        window.after(800, window.destroy)

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
            lblTime["text"] = "Time Elapsed: " + str(round((frame*0.05), 3))
            yield frame
        elif(p==0):
            #Graph paused
            yield frame
    #Graph Over
    btnStart["text"] = "Simulation Over. Quit? "
    btnStart["state"] = "active"
    p = 2
    yield frame

#Animator function to draw graph
def run(frame, line, lineData):
    lblX["text"] = "X = " + str(round(lineData[0, frame], 3))
    lblY["text"] = "Y = " + str(round(lineData[2, frame], 3))
    lblZ["text"] = "Z = " + str(round(lineData[1, frame], 3))
    line.set_data(lineData[0:2, :frame])
    line.set_3d_properties(lineData[2, :frame])
    return line,
    
                
#-----------------------------------------------------------------------------------------#

#|INTERACTIVE MENU SETUP SECTION|#

window = tk.Tk()
window.configure(background='red')
window.title("Animated Graph of the trajectory of a 3D Projectile")

frmDetails = tk.Frame(
    master = window, 
    background='red'
)

lblWelcome = tk.Label(master=frmDetails, text='Hello! Welcome to my MEPC \
Assignment-3 Problem-3 Applet! \nEnter the required details below for a \
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

entryVelocityZ = tk.Entry(master=frmDetails)
entryVelocityZ.pack()
lblVelocityZ = tk.Label(master=frmDetails, text='Initial Z component of velocity\'s magnitude (m/s)', bg='red')
lblVelocityZ.pack()


entryXi = tk.Entry(master=frmDetails)
entryXi.pack()
lblXi = tk.Label(master=frmDetails, text='Initial X coordinate (m):', bg='red')
lblXi.pack()

entryYi = tk.Entry(master=frmDetails)
entryYi.pack()
lblYi = tk.Label(master=frmDetails, text='Initial Y coordinate (m):', bg='red')
lblYi.pack()

entryZi = tk.Entry(master=frmDetails)
entryZi.pack()
lblZi = tk.Label(master=frmDetails, text='Initial Z coordinate (m):', bg='red')
lblZi.pack()

btnStart = tk.Button(master=frmDetails, text="Enter->", command=start)
btnStart.pack()

lblTime = tk.Label(master=frmDetails, bg='red')
lblTime.pack()

lblX = tk.Label(master=frmDetails, bg='red')
lblX.pack()

lblY = tk.Label(master=frmDetails, bg='red')
lblY.pack()

lblZ = tk.Label(master=frmDetails, bg='red')
lblZ.pack()

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
