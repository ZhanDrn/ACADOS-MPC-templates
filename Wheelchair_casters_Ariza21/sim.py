

import time, os
import numpy as np
from solversetup import *
from plotFcn import *
import matplotlib.pyplot as plt


Tf = 3.5  # prediction horizon
N = 70  # number of discretization steps
T = 9*3.5  # maximum simulation time[s]
sref_N = 3  # reference for final reference progress

# load model
constraint, model, acados_solver = acados_settings(Tf, N)

# dimensions
nx = model.x.size()[0]
nu = model.u.size()[0]
ny = nx + nu
Nsim = int(T * N / Tf)

# initialize data structs
simX = np.ndarray((Nsim, nx))
simU = np.ndarray((Nsim, nu))
tcomp_sum = 0
tcomp_max = 0
#Intial state
thcl0 = -np.pi/4
thcr0 = -np.pi/4
#x0 states: 
#x0 = [x position, y position, orientation, linear velocity, angular velocity, left caster orientation, right caster orientation]
x0 = np.array([0,0,0,0,0,thcl0,thcr0])
acados_solver.set(0, "lbx", x0)
acados_solver.set(0, "ubx", x0)
status = acados_solver.solve()
# simulate
i = 0
while i<Nsim:#replace with simulation running condition
    #Set target
    yref=np.array([5,5,0,0,0,0,0,0,0])
    for j in range(N-1):
        acados_solver.set(j, "yref", yref)
    acados_solver.set(N, "yref", yref[:7])
    # update initial state
    # Replace x0 with data from simulator (linear and angular velocities can be left if not available in simulator)
    x0 = acados_solver.get(1, "x")
    acados_solver.set(0, "lbx", x0)
    acados_solver.set(0, "ubx", x0)

    # solve ocp
    t = time.time()

    status = acados_solver.solve()

    elapsed = time.time() - t

    # manage timings
    tcomp_sum += elapsed
    if elapsed > tcomp_max:
        tcomp_max = elapsed

    # get solution
    x1 = acados_solver.get(1, "x")
    u0 = acados_solver.get(0, "u")
    v = x1[3]#linear velocity
    w = x1[4]#angular velocity
    av = u0[0]#linear acceleration
    aw = u0[1]#angular acceleration
    for j in range(nx):
        simX[i, j] = x1[j]
    for j in range(nu):
        simU[i, j] = u0[j]
    i+=1

    

# Plot
t = np.linspace(0.0, Nsim * Tf / N, Nsim)
plotRes(simX, simU, t)
plotTrackProj(simX)
plotCasters(simX)
#plotalat(simX, simU, constraint, t)

# Print
acados_solver.print_statistics()
print(acados_solver.get(12, "x"))
print("Average computation time: {}".format(tcomp_sum / Nsim))
print("Maximum computation time: {}".format(tcomp_max))
print("Average speed:{}m/s".format(np.average(simX[:, 3])))
plt.show()
