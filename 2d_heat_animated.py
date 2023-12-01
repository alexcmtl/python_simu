# the 2d heat equation is given by
# U_t = D * (U_xx + U_yy)
# where D = diffusion constant
# U = U(x,y,t) is the temperature at point (x,y) at time t

# we want to set the boundary as the unit square [0,1]x[0,1]
# numerical solution to the heat equation:
# approximate U(x,y,t) by U(i,j,n) where x = i*dx , y = j*dy , t = n*dt
#
# The time derivative U_t is approximated by
# Ut = U(i,j,n+1) - U(i,j,n) / dt
# the derivatives Uxx and Uyy are given by the finite difference approximations
# Uxx = U(i+1,j,n) - 2*U(i,j,n) + U(i-1,j,n) / dx^2
# Uyy = U(i,j+1,n) - 2*U(i,j,n) + U(i,j-1,n) / dy^2
# in code:
# uxx = (u0[i+1,j] - 2*u0[i,j] + u0[i-1,j]) / dx2
# uyy = (u0[i,j+1] - 2*u0[i,j] + u0[i,j-1]) / dy2

# so we can write the discrete heat eq as 
# U(i,j,n+1) = U(i,j,n) + dt * D* [ uxx + uyy]

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

# define the constants of the problem
# plate size
w = h = 10
# dx , dy size
dx = dy = 0.1
# diffusivity constant
D = 10

# for colors
T_hot = 700
T_cool = 300

# define variables for loop
nx, ny = int((w / dx)), int((h / dy))
dx2, dy2 = dx * dx, dy * dy
dt = dx2 * dy2 / (2 * D * (dx2 + dy2))  # this is the correct formula for delta t

# set initial temperature of the plate
u0 = T_cool * np.ones((nx, ny))  # each dxdy tile starts with a temperature of 300
u = u0.copy()  # temperature

# to solve the heat equation, the initial conditions and boundary conditions must be specified
# we must set points in the plate where the initial temperature is hot so the heat will diffuse 
# form those tiles to nearby tiles as time passes

def set_heat_circle(u0):
    # define a circle of hot temperature (700)
    radius = 2
    cx, cy = 5, 5  # centered at (5,5) , plate size is 10x10
    rad2 = radius * radius
    for i in range(nx):
        for j in range(ny):
            p2 = (i * dx - cx) ** 2 + (j * dy - cy) ** 2
            if p2 < rad2:
                u0[i, j] = T_hot

set_heat_circle(u0)
# propagate the solution in time
def do_timestep(u0, u):
    # U(i,j,n+1) = U(i,j,n) + dt * D* [ uxx + uyy]
    uxx = (u0[2:, 1:-1] - 2 * u0[1:-1, 1:-1] + u0[:-2, 1:-1]) / dx2
    uyy = (u0[1:-1, 2:] - 2 * u0[1:-1, 1:-1] + u0[1:-1, :-2]) / dy2
    u[1:-1, 1:-1] = u0[1:-1, 1:-1] + D * dt * (uxx + uyy)
    u0 = u.copy()
    return u0, u


num_steps = 101

fig, ax = plt.subplots()
ax.set_xlim([0, 10])
ax.set_ylim([0, 10])

def animate(i):
    global ax ,u0, u
    if i == 0:
        u0 = T_cool * np.ones((nx, ny))  # each dxdy tile starts with a temperature of 300
        u = u0.copy()
        set_heat_circle(u0)
    ax.clear()
    ax.axis('off')
    u0, u = do_timestep(u0, u)
    ax.imshow(u.copy(), cmap=plt.get_cmap('hot'), vmin=T_cool, vmax=T_hot)
    ax.set_title('{:.1f} ms'.format(i * dt * 1000))
        

#fig.subplots_adjust(right=0.85)
#cbar_ax = fig.add_axes([0.9, 0.15, 0.03, 0.7])
#cbar_ax.set_xlabel('$T$ / K', labelpad=20)
#fig.colorbar(im, cax=cbar_ax)
ani = anim.FuncAnimation(fig,animate ,frames=num_steps*10, interval=10, repeat=True)
plt.show()

