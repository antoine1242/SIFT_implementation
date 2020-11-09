from gaussian_filter import gaussian_filter
from scipy.ndimage.filters import convolve
import matplotlib.pyplot as plt
import numpy as np

def difference_de_gaussiennes(image_initiale, s: int, nb_octave: int):

    image_initiale_norm = np.array((image_initiale - np.min(image_initiale)) / (np.max(image_initiale) - np.min(image_initiale)))

    sigma_init = 1.6
    k = 2**(1/s)
    nb_image = s + 3
    gaussian_filtered_images = [[]]
    gaussian_filtered_images_sigmas = [[]]
    
    dogs = [] 
    sigmas = []

    # Octave 1 
    for image in range(nb_image):
        # Traitement différent pour première image  de la première octave
        # afin de considérer le flou intrinsèque de 1
        if image == 0:
            sigma_img = np.sqrt(sigma_init**2 - 1)
            gaussian_filtered_images_sigmas[0].append(sigma_init)
        else:
            sigma_img = sigma_init * (k**image)
            gaussian_filtered_images_sigmas[0].append(sigma_img)

        kernel = gaussian_filter(sigma_img)
        result = convolve(image_initiale_norm, kernel)
                       
        gaussian_filtered_images[0].append(result)

    # Octave 2 a nb_octave
    for i in range(1, nb_octave):
        temp = []
        for j in range(nb_image):
            temp.append(gaussian_filtered_images[i-1][j][::2, ::2])
        gaussian_filtered_images.append(temp)
        gaussian_filtered_images_sigmas.append([x * 2 for x in gaussian_filtered_images_sigmas[i-1]])

    # DoG de tous les octaves
    for octave in range(nb_octave):
        dogs.append([])
        for i in range(len(gaussian_filtered_images[octave]) -1):
            diff = gaussian_filtered_images[octave][i + 1] - gaussian_filtered_images[octave][i]
            dogs[octave].append(diff)

        sigmas.append(gaussian_filtered_images_sigmas[octave][:-1])

    return dogs, sigmas, gaussian_filtered_images, gaussian_filtered_images_sigmas
