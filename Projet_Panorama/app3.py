import numpy as np
import cv2
from matching import distance_inter_points, get_k_lowest
from skimage.color import rgb2gray
from afficher_img_avec_points_cles import afficher_img_avec_points_cles
from combiner_images_avec_points_cles import combiner_images_avec_points_cles
from hist_match import equalize_hist
from skimage.io import imread

from scipy import ndimage

def rotate(image, angle, center = None, scale = 1.0):
    (h, w) = image.shape[:2]

    if center is None:
        center = (w / 2, h / 2)

    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated

img_color1 = imread("./images/gauche.jpg")
img_color2 = imread("./images/droite.jpg")

#keypoints_matched1 =  [(224.0, 880.0), (203.0, 950.0), (54.0, 483.0), (306.0, 121.0), (233.0, 774.0), (353.0, 907.0), (237.0, 841.0), (58.0, 494.0), (214.0, 733.0)]
#keypoints_matched2 =  [(223.0, 278.0), (201.0, 349.0), (52.0, 182.0), (248.0, 939.0), (233.0, 170.0), (354.0, 306.0), (236.0, 238.0), (56.0, 193.0), (214.0, 128.0)]

keypoints_matched1 = [(169.0, 753.0), (516.0, 753.0), (444.0, 766.0), (503.0, 749.0), (494.0, 619.0), (229.0, 638.0), (277.0, 810.0), (355.0, 818.0), (398.0, 924.0), (109.0, 988.0), (177.0, 749.0), (363.0, 624.0), (440.0, 645.0)]
keypoints_matched2 = [(168.0, 148.0), (520.0, 151.0), (447.0, 164.0), (507.0, 147.0), (499.0, 15.0), (230.0, 32.0), (277.0, 207.0), (356.0, 216.0), (399.0, 323.0), (105.0, 386.0), (176.0, 144.0), (366.0, 19.0), (444.0, 41.0)]

#afficher_img_avec_points_cles(img_color1, keypoints_matched1, False)
#afficher_img_avec_points_cles(img_color2, keypoints_matched2, False)


#rotation angle in degree
rotated = rotate(img_color1, 45, (300, 300))
afficher_img_avec_points_cles(rotated, [], False)


img_color2_v2 = equalize_hist(img_color2, img_color1)

print("Combinaison des deux images pour former panorama.")
pano_img = combiner_images_avec_points_cles(
                keypoints_matched1=keypoints_matched1, 
                keypoints_matched2=keypoints_matched2, 
                img_color1=img_color1, 
                img_color2=img_color2_v2)

afficher_img_avec_points_cles(pano_img, [], False)
