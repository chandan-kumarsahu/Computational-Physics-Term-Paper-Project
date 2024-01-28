####################################################################################################
# Solving heat diffusion for system with two grains of different material using 
# finite difference method initially heated to two different arbitrary concentration profiles 
# C(x, 0) = -800 * (x - 0.6)**2 + 1000  and 
# C(x, 0) = -600 * (x - 1.5)**2 + 600
# and then joined together while keeping their extreme ends isolated. 
# The heat flow balances in both grains to equilibriate. 
####################################################################################################

import matplotlib.pyplot as plt
import numpy as np
from numba import njit


@njit
def my_code():
    # Constants and parameters
    L_grain1 = 100.0  # length of the first grain
    L_grain2 = 100.0  # length of the second grain
    alpha_grain1 = 1  # thermal diffusivity for grain 1
    alpha_grain2 = 1  # thermal diffusivity for grain 2
    dt = 0.1  # time step
    dx = 1  # spatial step
    duration = 1000  # total simulation time

    gamma = 0.8

    # Discretization
    Nx_grain1 = int(L_grain1 / dx) + 1
    Nx_grain2 = int(L_grain2 / dx) + 1
    Nt = int(duration / dt) + 1

    # Define spatial coordinates for each grain
    x_values_grain1 = np.linspace(0, L_grain1, Nx_grain1)
    x_values_grain2 = np.linspace(L_grain1, L_grain1 + L_grain2, Nx_grain2)
    x_values_total = np.concatenate((x_values_grain1, x_values_grain2))

    # Initialize concentration arrays for each grain
    C_grain1 = np.zeros((Nt, Nx_grain1))
    C_grain2 = np.zeros((Nt, Nx_grain2))

    # Initial conditions for each grain
    C_grain1[0, :] = -0.04 * (x_values_grain1 - L_grain1/2)**2 + 200
    C_grain2[0, :] = -0.02 * (x_values_grain2 - int(L_grain2/2+L_grain1))**2 + 100

    # Boundary conditions
    C_grain1[:, 0] = C_grain1[:, 1]  # Isolated boundary for grain 1
    C_grain2[:, -1] = C_grain2[:, -2]  # Isolated boundary for grain 2

    # Finite difference method for each grain
    for n in range(0, Nt - 1):
        for i in range(1, Nx_grain1 - 1):
            C_grain1[n + 1, i] = C_grain1[n, i] + alpha_grain1 * dt / dx**2 * (C_grain1[n, i + 1] - 2 * C_grain1[n, i] + C_grain1[n, i - 1])

        for i in range(1, Nx_grain2 - 1):
            C_grain2[n + 1, i] = C_grain2[n, i] + alpha_grain2 * dt / dx**2 * (C_grain2[n, i + 1] - 2 * C_grain2[n, i] + C_grain2[n, i - 1])

        # Isolated boundary conditions for both grains
        C_grain1[n + 1, 0] = C_grain1[n, 1]
        C_grain2[n + 1, -1] = C_grain2[n, -2]

        # Boundary condition at the junction of the two grains
        C_grain1[n + 1, -1] = (alpha_grain1*C_grain1[n+1, -2] + alpha_grain1*C_grain2[n+1, 1]) / (alpha_grain1 + gamma*alpha_grain1)
        C_grain2[n + 1, 0] = (alpha_grain1*C_grain1[n+1, -2] + alpha_grain1*C_grain2[n+1, 1]) / (alpha_grain1/gamma + alpha_grain1)

    # Combine the concentrations of the two grains
    C_total = np.concatenate((C_grain1, C_grain2), axis=1)

    return C_total, x_values_total, duration, Nt

C_total, x_values_total, duration, Nt = my_code()

def plot_3D():
    # Create a 3D surface plot for the total concentration
    X_total, C_values_total = np.meshgrid(x_values_total, np.linspace(0, duration, Nt))
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X_total, C_values_total, C_total, cmap='viridis')
    ax.set_xlabel(r'Distance ($\mu$m)')
    ax.set_ylabel('Time (s)')
    ax.set_zlabel('Concentration (ppm)')
    ax.set_title('Heat Diffusion in Several Connected Rods of Different Materials')

    plt.savefig('Element_Partitioning_and_Diffusion/Plots/ElemPart_two_grains_mBC_3D.png', dpi=300)

def plot_2D():
    # Create a 2D plot for Concentration vs Length for every (Nt/10)th time step
    plt.figure(figsize=(12, 8))
    for i in range(0, Nt, int(Nt/10)):
        plt.plot(x_values_total, C_total[i, :], label='t = ' + str(i*duration/(Nt-1)) + ' s')
    plt.xlabel(r'Distance ($\mu$m)')
    plt.ylabel('Concentration (ppm)')
    plt.title('Heat Diffusion in Several Connected Rods of Different Materials')
    plt.legend()
    plt.savefig('Element_Partitioning_and_Diffusion/Plots/ElemPart_two_grains_mBC.png', dpi=300)


plot_3D()
plt.show()

