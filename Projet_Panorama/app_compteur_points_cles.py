import cv2
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.color import rgb2gray
from difference_de_gaussiennes import difference_de_gaussiennes
from detection_points_cles import detection_points_cles
from gaussian_filter import gaussian_filter

def run():
    print("Project Pano is running - Compteur points clés.")
   
    img = imread("./images/gauche.jpg")
    img = rgb2gray(img)

    dogs, sigmas, gaussian_filtered_images, gaussian_filtered_images_sigmas = difference_de_gaussiennes(img, s=3, nb_octave=2)

    # Octave 1
    print("Octave 1 image gauche")
    detection_points_cles(dogs[0], sigmas[0], 0.03, 10, 0, gaussian_filtered_images[0], gaussian_filtered_images_sigmas[0])

    # Octave 2
    print("Octave 2 image gauche")
    detection_points_cles(dogs[1], sigmas[1], 0.03, 10, 0, gaussian_filtered_images[1], gaussian_filtered_images_sigmas[1])



    img = imread("./images/droite.jpg")
    img = rgb2gray(img)

    dogs, sigmas, gaussian_filtered_images, gaussian_filtered_images_sigmas = difference_de_gaussiennes(img, s=3, nb_octave=2)

    # Octave 1
    print("Octave 1 image droite")
    detection_points_cles(dogs[0], sigmas[0], 0.03, 10, 0, gaussian_filtered_images[0], gaussian_filtered_images_sigmas[0])

    # Octave 2
    print("Octave 2 image droite")
    detection_points_cles(dogs[1], sigmas[1], 0.03, 10, 0, gaussian_filtered_images[1], gaussian_filtered_images_sigmas[1])

run()
