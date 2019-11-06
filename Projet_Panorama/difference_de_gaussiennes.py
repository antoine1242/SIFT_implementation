import cv2
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import numpy as np

def display_img(img):
    plt.imshow(img)
    plt.show()

def difference_de_gaussiennes(image_initiale, s: int, nb_octave: int):
    # returns 
    #   Liste des matrices DoG
    #   Vect des sigma correspondant
    image_initiale_norm = (image_initiale - np.min(image_initiale))/np.ptp(image_initiale)

    sigma_init = 1.6
    k = 2**(1/s)
    nb_image = s + 3
    gaussian_filtered_images = [[]]
    gaussian_filtered_images_sigmas = [[]]
    
    dogs = [] #
    sigmas = []

    # Octave 1 
    for image in range(nb_image):
        sigma_img = sigma_init * (k**image)
        result = gaussian_filter(image_initiale_norm, sigma=sigma_img) 
        gaussian_filtered_images[0].append(result)
        gaussian_filtered_images_sigmas[0].append(sigma_img)
        print(type(result))

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
            diff = gaussian_filtered_images[octave][i + 1] - gaussian_filtered_images[octave][i]
            diff_norm = (diff - np.min(diff))/np.ptp(diff)
            dogs[octave].append(diff_norm)
        sigmas.append(gaussian_filtered_images_sigmas[octave][:-1])


    return dogs, sigmas, gaussian_filtered_images, gaussian_filtered_images_sigmas
    
# TODO les traitements doivent etre fait avec image noire et blanche
img = cv2.imread("./images/lena_claire.jpg", cv2.IMREAD_COLOR).astype("float32")

#display_img(img)
dogs, sigmas, gaussian_filtered_images, gaussian_filtered_images_sigmas = difference_de_gaussiennes(img, 3, 2)

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

print(np.amax(dogs[0][0]))

#print(gaussian_filtered_images[0][0])
#print(dogs[0][1])
#display_img(dogs[0][1])

