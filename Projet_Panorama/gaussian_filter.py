import numpy as np

def gaussian_filter(sigma):
    length = 2 * np.ceil(3*sigma) + 1

    ax = np.linspace(-(length - 1) / 2, (length - 1) / 2, length)
    xx, yy = np.meshgrid(ax, ax)

    kernel = np.exp(-0.5 * (np.square(xx) + np.square(yy)) / np.square(sigma))

    return kernel / np.sum(kernel)
