import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from difference_de_gaussiennes import difference_de_gaussiennes
from description_points_cles import description_points_cles
from detection_points_cles import detection_points_cles
from matching import distance_inter_points
from matching import get_k_lowest
import cv2
from skimage.io import imread
from skimage.color import rgb2gray
from matplotlib.patches import Circle, Arrow
import math 
from gaussian_filter import gaussian_filter
from scipy.ndimage.filters import convolve
from afficher_img_avec_points_cles import afficher_img_avec_points_cles

def run():
    print("Projet Pano is running App 2!")
    
    img_color1 = imread("./images/droite.jpg")
    img1 = rgb2gray(img_color1)

    # TODO: revoir s<il faut convoluer image initialement...
    # s0=1.3
    # img1 = convolve(img1, gaussian_filter(s0))

    dogs, sigmas, gaussian_filtered_images, gaussian_filtered_images_sigmas = difference_de_gaussiennes(img1, 3, 2)

    # for dog in dogs:
    #    print("dogs", dogs)

    keypoints1 = detection_points_cles(dogs[0], sigmas[0], 0.03, 10, 0, gaussian_filtered_images[0], gaussian_filtered_images_sigmas[0])

    keypoints_descriptors1 = description_points_cles(keypoints1, gaussian_filtered_images[0], gaussian_filtered_images_sigmas[0])

    afficher_img_avec_points_cles(img_color1, keypoints1)
    
