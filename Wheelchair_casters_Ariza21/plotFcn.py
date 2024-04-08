
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button
import math

def plotCasters(simX):
    th_c1=simX[:,5]
    th_c2=simX[:,6]
    t = range(simX.shape[0])
    fig, (ax,ax1) = plt.subplots(1,2, subplot_kw={'projection': 'polar'})
    fig.subplots_adjust(bottom=0.25)
    line, = ax.plot([th_c1[0], th_c1[0]], [0, 1], ls = '-')
    line1, = ax1.plot([th_c2[0], th_c2[0]], [0, 1], ls = '-')
    axiter = fig.add_axes([0.25, 0.1, 0.65, 0.03])
    iter_slider = Slider(
        ax=axiter,
        label='iteration',
        valmin=1,
        valmax=simX.shape[0],
        valinit=0,
    )
    def update(iter):
        line.set_xdata([th_c1[round(iter-1)], th_c1[round(iter-1)]])
        line1.set_xdata([th_c2[round(iter-1)], th_c2[round(iter-1)]])
        fig.canvas.draw_idle()
    iter_slider.on_changed(update)
    plt.show()

def plotTrackProj(simX, T_opt=None):
    x=simX[:,0]
    y=simX[:,1]
    v=np.sqrt(simX[:,3]+simX[:,4])
    plt.figure()
    plt.ylabel('y[m]')
    plt.xlabel('x[m]')

    # Draw driven trajectory
    heatmap = plt.scatter(x,y, c=v, cmap=cm.rainbow, edgecolor='none', marker='o')
    cbar = plt.colorbar(heatmap, fraction=0.035)
    cbar.set_label("velocity in [m/s]")
    ax = plt.gca()
    ax.set_aspect('equal', 'box')

def plotRes(simX,simU,t):
    # plot results
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.step(t, simU[:,0], color='r')
    plt.step(t, simU[:,1], color='g')
    plt.title('closed-loop simulation')
    plt.legend(['a','aW'])
    plt.ylabel('u')
    plt.xlabel('t')
    plt.grid(True)
    plt.subplot(2, 1, 2)
    plt.plot(t, simX[:,:])
    plt.ylabel('x')
    plt.xlabel('t')
    plt.legend(['x','y','theta','v','w','th_cl','th_cr'])
    plt.grid(True)

def plotalat(simX,simU,constraint,t):
    Nsim=t.shape[0]
    plt.figure()
    alat=np.zeros(Nsim)
    for i in range(Nsim):
        alat[i]=constraint.alat(simX[i,:],simU[i,:])
    plt.plot(t,alat)
    plt.plot([t[0],t[-1]],[constraint.alat_min, constraint.alat_min],'k--')
    plt.plot([t[0],t[-1]],[constraint.alat_max, constraint.alat_max],'k--')
    plt.legend(['alat','alat_min/max'])
    plt.xlabel('t')
    plt.ylabel('alat[m/s^2]')

