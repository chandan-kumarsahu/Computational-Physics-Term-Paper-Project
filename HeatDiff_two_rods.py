import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Constants and parameters
L_rod1 = 1.0  # length of the first rod
L_rod2 = 1.0  # length of the second rod
alpha_rod1 = 0.01  # thermal diffusivity for rod 1
alpha_rod2 = 0.01  # thermal diffusivity for rod 2
dt = 0.001  # time step
dx = 0.01  # spatial step
duration = 50.0  # total simulation time

# Discretization
Nx_rod1 = int(L_rod1 / dx) + 1
Nx_rod2 = int(L_rod2 / dx) + 1
Nt = int(duration / dt) + 1

# Define spatial coordinates for each rod
x_values_rod1 = np.linspace(0, L_rod1, Nx_rod1)
x_values_rod2 = np.linspace(L_rod1, L_rod1 + L_rod2, Nx_rod2)
x_values_total = np.concatenate((x_values_rod1, x_values_rod2))

# Initialize temperature arrays for each rod
T_rod1 = np.zeros((Nt, Nx_rod1))
T_rod2 = np.zeros((Nt, Nx_rod2))

# Initial conditions for each rod
T_rod1[0, :] = -800 * (x_values_rod1 - 0.5)**2 + 1000
T_rod2[0, :] = -400 * (x_values_rod2 - 1.5)**2 + 800

# Boundary conditions
T_rod1[:, -1] = T_rod1[:, -2]  # Isolated boundary for rod 1
T_rod2[:, -1] = T_rod2[:, -2]  # Isolated boundary for rod 2

# Finite difference method for each rod
for n in range(0, Nt - 1):
    for i in range(1, Nx_rod1 - 1):
        T_rod1[n + 1, i] = T_rod1[n, i] + alpha_rod1 * dt / dx**2 * (T_rod1[n, i + 1] - 2 * T_rod1[n, i] + T_rod1[n, i - 1])

    for i in range(1, Nx_rod2 - 1):
        T_rod2[n + 1, i] = T_rod2[n, i] + alpha_rod2 * dt / dx**2 * (T_rod2[n, i + 1] - 2 * T_rod2[n, i] + T_rod2[n, i - 1])

    # Isolated boundary conditions for both rods
    T_rod1[n + 1, 0] = T_rod1[n, 1]
    T_rod2[n + 1, -1] = T_rod2[n, -2]

    # Boundary condition at the junction of the two rods
    T_rod1[n + 1, -1] = T_rod2[n, 0]
    T_rod2[n + 1, 0] = T_rod1[n, -1]

    

# Combine the temperatures of the two rods
T_total = np.concatenate((T_rod1, T_rod2), axis=1)

# Create a 3D surface plot for the total temperature
X_total, T_values_total = np.meshgrid(x_values_total, np.linspace(0, duration, Nt))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X_total, T_values_total, T_total, cmap='viridis')
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Time (s)')
ax.set_zlabel('Temperature (C)')
ax.set_title('Heat Diffusion in Two Connected Rods')
plt.show()