import cv2
from detectionPointsCles import gaussian_filter
from scipy.ndimage.filters import convolve
import matplotlib.pyplot as plt
import numpy as np

def display_img(img):
    plt.imshow(img)
    plt.show()

def difference_de_gaussiennes(image_initiale, s: int, nb_octave: int):
    # returns 
    #   Liste des matrices DoG
    #   Vect des sigma correspondant
    
    # TODO avant: avant : on normalisait l'image, mais je pense qu'elle est déjà norm (j'ai vérifié, mais à confirmer toute de même)
    # image_initiale_norm = np.array((image_initiale - np.min(image_initiale)) / (np.max(image_initiale) - np.min(image_initiale)))
    image_initiale_norm = image_initiale

    sigma_init = 1.6
    k = 2**(1/s)
    nb_image = s + 3
    gaussian_filtered_images = [[]]
    gaussian_filtered_images_sigmas = [[]]
    
    dogs = [] 
    sigmas = []

    # Octave 1 
    for image in range(nb_image):
        # TODO Vérifier si on a la bonne approche:
        sigma_img = sigma_init * (k**image)
        kernel = gaussian_filter(sigma_img)
        result = convolve(image_initiale_norm, kernel)
                        
        # TODO autre approche (inspiré de l'article sur medium): 
        # gaussian_filtered_images[0] = [image_initiale_norm]
        # for image in range(nb_image - 1):
        # sigma_img = sigma_init * k
        # kernel = gaussian_filter(sigma_img)
        # result = convolve(gaussian_filtered_images[0][-1], kernel)

        gaussian_filtered_images[0].append(result)
        gaussian_filtered_images_sigmas[0].append(sigma_img)

    # Octave 2 a nb_octave
    for i in range(1, nb_octave):
        temp = []
        for j in range(nb_image):
            temp.append(gaussian_filtered_images[i-1][j][::2, ::2])
        gaussian_filtered_images.append(temp)
        gaussian_filtered_images_sigmas.append([x * 2 for x in gaussian_filtered_images_sigmas[i-1]])

    # DoG tous les octaves
    for octave in range(nb_octave):
        dogs.append([])
        for i in range(len(gaussian_filtered_images[octave]) -1):
            # TODO (vérifier s'il faut que cette valeur soit en valeur absolue, je ne suis pas certain)
            diff = gaussian_filtered_images[octave][i + 1] - gaussian_filtered_images[octave][i]
            # TODO avant: on normalisait diff (vérifier s'il faut)
            # diff_norm = (diff - np.min(diff))/np.ptp(diff)

            dogs[octave].append(diff)
        sigmas.append(gaussian_filtered_images_sigmas[octave][:-1])

    return dogs, sigmas, gaussian_filtered_images, gaussian_filtered_images_sigmas


def test():
    img = cv2.imread("./images/lena_claire.jpg", cv2.IMREAD_COLOR).astype("float32")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    dogs, sigmas, gaussian_filtered_images, gaussian_filtered_images_sigmas = difference_de_gaussiennes(img, s=3, nb_octave=2)

    fig = plt.figure(figsize=(2,3))
    for i in range(1, 6+1):
        fig.add_subplot(2, 3, i)
        plt.imshow(gaussian_filtered_images[1][i-1])
    plt.show()

    fig = plt.figure(figsize=(2,3))
    for i in range(1, 6):
        fig.add_subplot(2, 3, i)
        plt.imshow(dogs[1][i-1])
    plt.show()

