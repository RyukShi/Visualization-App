import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations

figure = plt.figure(figsize=(10, 10), dpi=100)
axes = figure.add_subplot(111, projection='3d')
axes.set_xlabel('x')
axes.set_ylabel('y')
axes.set_zlabel('z')

# Functions to plot vector field


def funcU(x, y, z):
    return -3 + 6*x - 4*x*(y+1) - 4*z


def funcV(x, z):
    return 12*x - 4*x*x - 12*z + 4*z*z


def funcW(x, y, z):
    return 3 + 4*x - 4*x*(y+1) - 6*z + 4*(y+1)*z


def funcS(t):
    return np.sin(t)


def funcC(t):
    return np.cos(t)


def drawCube():
    r = [-1, 1]
    for s, e in combinations(np.array(list(product(r, r, r))), 2):
        if np.sum(np.abs(s-e)) == r[1]-r[0]:
            axes.plot3D(*zip(s, e), color="red")


def plot_3d_vectors(x_range: list = [-1, 1], y_range: list = [-1, 1], z_range: list = [-1, 1], step_size: float = 0.2):
    """
    Plot 3D vector field.
    """
    # Create a grid of points
    x_grid, y_grid, z_grid = np.meshgrid(
        np.arange(x_range[0], x_range[1], step_size),
        np.arange(y_range[0], y_range[1], step_size),
        np.arange(z_range[0], z_range[1], 0.4)
    )

    u = funcU(x_grid, y_grid, z_grid)
    v = funcV(x_grid, z_grid)
    w = funcW(x_grid, y_grid, z_grid)

    # Plot the vector field
    axes.quiver(x_grid, y_grid, z_grid, u, v, w, length=0.25, normalize=True)

    axes.set_xlim(x_range)
    axes.set_ylim(y_range)
    axes.set_zlim(z_range)
    plt.show()


def plot_3d_vectors_sin_cos(x_range: list = [-1, 1], y_range: list = [-1, 1], z_range: list = [-1, 1], step_size: float = 0.2):
    """
    Plot 3D vector field.
    """
    # Create a grid of points
    x_grid, y_grid, z_grid = np.meshgrid(
        np.arange(x_range[0], x_range[1], step_size),
        np.arange(y_range[0], y_range[1], step_size),
        np.arange(z_range[0], z_range[1], 0.4)
    )

    u = funcS(x_grid)
    v = funcC(y_grid)
    w = funcC(z_grid) * (u / v)

    # Plot the vector field
    axes.quiver(x_grid, y_grid, z_grid, u, v, w, length=0.25, normalize=True)
    axes.set_xlim(x_range)
    axes.set_ylim(y_range)
    axes.set_zlim(z_range)
    plt.show()


drawCube()

plot_3d_vectors()

# plot_3d_vectors_sin_cos()
