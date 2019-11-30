import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from difference_de_gaussiennes import difference_de_gaussiennes
from description_points_cles import description_points_cles
from detection_points_cles import detection_points_cles, isExtremum
from gaussian_filter import gaussian_filter
from matching import distance_inter_points, get_k_lowest
from homographie import calcul_matrice_H_avec_eig, calcul_matrice_H_avec_svd
import cv2
from skimage.io import imread
from skimage.color import rgb2gray
from matplotlib.patches import Circle, Arrow
import math 

def run():

    keypoints_matched1 =  [(494.0, 619.0), (229.0, 638.0), (398.0, 924.0), (363.0, 624.0), (444.0, 766.0), (440.0, 645.0), (355.0, 818.0), (109.0, 988.0), (277.0, 810.0), (177.0, 749.0), (503.0, 749.0), (437.0, 760.0), (368.0, 908.0)]
    keypoints_matched2 =  [(277.0, 207.0), (440.0, 157.0), (369.0, 307.0), (176.0, 144.0), (447.0, 164.0), (399.0, 323.0), (105.0, 386.0), (366.0, 19.0), (444.0, 41.0), (507.0, 147.0), (230.0, 32.0), (499.0, 15.0), (356.0, 216.0)]


    H_norm_svd_eig, H_flatten_eig = calcul_matrice_H_avec_eig(keypoints_matched1, keypoints_matched2, verbose=True)

    H_norm_svd_svd, H_flatten_svd = calcul_matrice_H_avec_svd(keypoints_matched1, keypoints_matched2, verbose=True)

    print(H_flatten_eig)
    print(H_flatten_svd)

    """
    [ 8.08662327e-04  7.67589919e-04 -9.04723553e-01  2.87430802e-04
    4.13015656e-04 -4.25991886e-01  1.84305192e-06  1.89270783e-06
    -2.17004795e-03]

    [ 8.08662270e-04  7.67589921e-04 -9.04723531e-01  2.87430823e-04
    4.13015706e-04 -4.25991933e-01  1.84305181e-06  1.89270790e-06
    -2.17004796e-03]
    """
    
run()