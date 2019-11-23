import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from difference_de_gaussiennes import difference_de_gaussiennes
from descriptionPointsCles import descriptionPointsCles
from detectionPointsCles import detectionPointsCles, isExtremum, gaussian_filter
from matching import distance_inter_points, get_k_lowest
from homographie import calcul_matrice_H
import cv2
from skimage.io import imread
from skimage.color import rgb2gray
from matplotlib.patches import Circle, Arrow
import math 

# TODO: si on veut: le chargé fit contraste avant extremum

def display_gaussian_window(s):
    kernel = gaussian_filter(s)
    #print(kernel.shape)
    plt.imshow(kernel)
    plt.show()

def run():
    print("Project Pano is running!")
    
    print("Image 1")
    img_color1 = imread("./images/gauche.jpg")
    img1 = rgb2gray(img_color1)


    dogs, sigmas, gaussian_filtered_images, gaussian_filtered_images_sigmas = difference_de_gaussiennes(img1, 3, 2)

    keypoints1 = detectionPointsCles(dogs[0], sigmas[0], 0.03, 10, 0, gaussian_filtered_images[0], gaussian_filtered_images_sigmas[0])
    # for k in keypoints:
    #    print(k)
    # display_img_with_keypoints(img_color, keypoints)

    keypoints_descriptors1 = descriptionPointsCles(keypoints1, gaussian_filtered_images[0], gaussian_filtered_images_sigmas[0])

    print("Image 2")
    img_color2 = imread("./images/droite.jpg")
    img2 = rgb2gray(img_color2)

    dogs, sigmas, gaussian_filtered_images, gaussian_filtered_images_sigmas = difference_de_gaussiennes(img2, 3, 2)

    keypoints2 = detectionPointsCles(dogs[0], sigmas[0], 0.03, 10, 0, gaussian_filtered_images[0], gaussian_filtered_images_sigmas[0])

    keypoints_descriptors2 = descriptionPointsCles(keypoints2, gaussian_filtered_images[0], gaussian_filtered_images_sigmas[0])

    print("Matrice de distance")
    distance_matrix = distance_inter_points(keypoints_descriptors1, keypoints_descriptors2)

    k_lowest = get_k_lowest(distance_matrix, 2*10)

    keypoints_matched1 = []
    keypoints_matched2 = []

    for k in range(len(k_lowest)):
        idx_image1 = k_lowest[k][1]
        idx_image2 = k_lowest[k][2]
        keypoints_matched1.append((keypoints1[idx_image1][0], keypoints1[idx_image1][1], keypoints1[idx_image1][2], keypoints1[idx_image1][3]))
        keypoints_matched2.append((keypoints2[idx_image2][0], keypoints1[idx_image2][1], keypoints1[idx_image2][2], keypoints1[idx_image1][3]))

    keypoints_matched1 = list(set(keypoints_matched1))
    keypoints_matched2 = list(set(keypoints_matched2))

    print("keypoints_matched1: ", keypoints_matched1)
    print("keypoints_matched2: ", keypoints_matched2)

    display_img_with_keypoints(img_color1, keypoints_matched1)
    display_img_with_keypoints(img_color2, keypoints_matched2)

    H = calcul_matrice_H(keypoints_matched1, keypoints_matched2)

    """
    fig = plt.figure(figsize=(2,3))
    for i in range(1, 6+1):
        fig.add_subplot(2, 3, i)
        plt.imshow(gaussian_filtered_images[1][i-1], cmap='gray', vmin=0, vmax=1)
    plt.show()

    fig = plt.figure(figsize=(2,3))
    for i in range(1, 6):
        fig.add_subplot(2, 3, i)
        plt.imshow(dogs[1][i-1], cmap='gray', vmin=0, vmax=1)
    plt.show()
    """

    """
    previous = np.array([[9, 9, 9], [9, 9, 9], [9, 9, 9]])
    current = np.array([[9, 9, 9], [9, 8, 9], [9, 9, 9]])
    suivant = np.array([[9, 9, 9], [9, 9, 9], [9, 9, 9]])

    print(isExtremum(previous, current, suivant, 1, 1))
    """

def display_img_with_keypoints(img, keypoints):
    # Create a figure. Equal aspect so circles look circular
    fig,ax = plt.subplots(1)
    ax.set_aspect('equal')

    # Show the image
    ax.imshow(img)

    # Now, loop through coord arrays, and create a circle at each x,y pair
    for keypoint in keypoints:
        x = keypoint[0]
        y = keypoint[1]
        r = 5 * keypoint[2]
        angle = math.radians(keypoint[3])
        dx = r * np.cos(angle)
        dy = r * np.sin(angle)

        line = Arrow(y, x, dx, dy, width=2.0)
        circ = Circle((y,x), r, fill=False)
        ax.add_patch(circ)
        ax.add_patch(line)

    # Show the image
    plt.show()

run()

"""
#Pour pas avoir à tout exécuter pour trouver les keypoints

img_color1 = imread("./images/gauche.jpg")
img_color2 = imread("./images/droite.jpg")

keypoints_matched1 =  [(437.0, 760.0, 3.2, 198.00000000000188), (109.0, 988.0, 2.5398416831491195, 162.00000000000904), (177.0, 749.0, 2.5398416831491195, 162.00000000000583), (363.0, 624.0, 2.015873679831797, 18.000000000002533), (355.0, 818.0, 2.015873679831797, 198.00000000000117), (277.0, 810.0, 2.5398416831491195, 305.9999999999992), (494.0, 619.0, 2.5398416831491195, 54.000000000000014), (177.0, 749.0, 2.5398416831491195, 342.0000000000004), (277.0, 810.0, 2.5398416831491195, 342.0000000000003), (398.0, 924.0, 2.015873679831797, 342.0000000000004), (368.0, 908.0, 2.5398416831491195, 342.0000000000002), (440.0, 645.0, 2.5398416831491195, 342.0000000000002), (444.0, 766.0, 2.015873679831797, 162.0000000000075), (440.0, 645.0, 2.5398416831491195, 18.000000000003773), (229.0, 638.0, 2.5398416831491195, 305.9999999999999), (503.0, 749.0, 2.5398416831491195, 198.00000000000907)]
keypoints_matched2 =  [(444.0, 619.0, 2.5398416831491195, 18.000000000003773), (447.0, 437.0, 2.015873679831797, 162.0000000000075), (176.0, 891.0, 2.5398416831491195, 162.00000000000583), (399.0, 55.0, 2.015873679831797, 342.0000000000004), (507.0, 428.0, 2.5398416831491195, 198.00000000000907), (277.0, 908.0, 2.5398416831491195, 305.9999999999992), (176.0, 891.0, 2.5398416831491195, 342.0000000000004), (366.0, 784.0, 2.015873679831797, 18.000000000002533), (277.0, 816.0, 2.5398416831491195, 305.9999999999992), (277.0, 816.0, 2.5398416831491195, 342.0000000000003), (105.0, 189.0, 2.5398416831491195, 162.00000000000904), (440.0, 858.0, 3.2, 198.00000000000188), (277.0, 908.0, 2.5398416831491195, 342.0000000000003), (369.0, 176.0, 2.5398416831491195, 342.0000000000002), (230.0, 154.0, 2.5398416831491195, 305.9999999999999), (356.0, 18.0, 2.015873679831797, 198.00000000000117), (444.0, 619.0, 2.5398416831491195, 342.0000000000002), (499.0, 92.0, 2.5398416831491195, 54.000000000000014)]

H = calcul_matrice_H(keypoints_matched1, keypoints_matched2)

print(H)

x_max_droite = len(img_color1)
y_max_droite = len(img_color1[0])
print(x_max_droite)
print(y_max_droite)

# x_y_max_droite = np.matmul(H, np.array([x_max_droite, y_max_droite, 1]))
x_y_max_droite = H.dot(np.array([x_max_droite, y_max_droite, 1]))

print(x_y_max_droite)
"""
