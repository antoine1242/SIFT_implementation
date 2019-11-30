
import numpy as np
from difference_de_gaussiennes import difference_de_gaussiennes
from description_points_cles import description_points_cles
from detection_points_cles import detection_points_cles
from gaussian_filter import gaussian_filter
from matching import distance_inter_points, get_k_lowest
from homographie import calcul_matrice_H_avec_eig, calcul_matrice_H_avec_svd
from skimage.color import rgb2gray
from afficher_img_avec_points_cles import afficher_img_avec_points_cles

def obtenir_panorama(img_color1, img_color2):

    # Convertion des images initiales en images tons de gris
    img1 = rgb2gray(img_color1)
    img2 = rgb2gray(img_color2)


    # Initialisation des constantes
    S = 3
    NB_OCTAVE = 2
    SEUIL_CONTRASTE = 0.03
    R_COURBURE_PRINCIPALE = 10
    RESOLUTION_OCTAVE = 0


    ##### 1. Obtenir descripteurs des points clés pour les deux images #####

    print("Calculs pour Image 1")
    # Obtenir pyramide de gaussienne pour Image 1
    dogs1, sigmas1, gaussian_filtered_images1, gaussian_filtered_images_sigmas1 = difference_de_gaussiennes(
                                                                                    image_initiale=img1, 
                                                                                    s=S, 
                                                                                    nb_octave=NB_OCTAVE)

    # Obtenir points clés pour Image 1
    keypoints1 = detection_points_cles(
                    dog=dogs1[0], 
                    sigma=sigmas1[0], 
                    seuil_contraste=SEUIL_CONTRASTE, 
                    r_courbure_principale=R_COURBURE_PRINCIPALE, 
                    resolution_octave=RESOLUTION_OCTAVE, 
                    gaussian_filtered_images=gaussian_filtered_images1[0], 
                    gaussian_filtered_images_sigmas=gaussian_filtered_images_sigmas1[0])

    # Obtenir descripteurs pour points clés Image 1
    keypoints_descriptors1 = description_points_cles(
                                keypoints=keypoints1, 
                                gaussian_filtered_images=gaussian_filtered_images1[0], 
                                gaussian_filtered_images_sigmas=gaussian_filtered_images_sigmas1[0])


    print("Calculs pour Image 2")
    # Obtenir pyramide de gaussienne pour Image 2
    dogs2, sigmas2, gaussian_filtered_images2, gaussian_filtered_images_sigmas2 = difference_de_gaussiennes(
                                                                                    image_initiale=img2, 
                                                                                    s=S, 
                                                                                    nb_octave=NB_OCTAVE)

    # Obtenir points clés pour Image 2
    keypoints2 = detection_points_cles(
                    dog=dogs2[0], 
                    sigma=sigmas2[0], 
                    seuil_contraste=SEUIL_CONTRASTE, 
                    r_courbure_principale=R_COURBURE_PRINCIPALE, 
                    resolution_octave=RESOLUTION_OCTAVE, 
                    gaussian_filtered_images=gaussian_filtered_images2[0], 
                    gaussian_filtered_images_sigmas=gaussian_filtered_images_sigmas2[0])

    # Obtenir descripteurs pour points clés Image 2
    keypoints_descriptors2 = description_points_cles(
                                keypoints=keypoints2, 
                                gaussian_filtered_images=gaussian_filtered_images2[0], 
                                gaussian_filtered_images_sigmas=gaussian_filtered_images_sigmas2[0])



    ##### 2. Trouver points clés de l'image 1 qui concordent avec ceux de l'image 2 #####

    print("Calcul de la matrice de distances")   
    # Obtenir matrice de distances    
    distance_matrix = distance_inter_points(
                        descriptors_image1=keypoints_descriptors1, 
                        descriptors_image2=keypoints_descriptors2)


    print("Calcul de l'index des k plus petites distances")
    # Obtenir les k points avec la plus petite distance
    k_lowest = get_k_lowest(
                descriptors_distance_matrix=distance_matrix, 
                k=20)


    # Obtenir points clés qui match pour l'image 1 et l'image 2 
    # à partir de l'index recueilli dans k_lowest
    keypoints_matched1 = []
    keypoints_matched2 = []

    for k in range(len(k_lowest)):
        idx_image1 = k_lowest[k][1]
        idx_image2 = k_lowest[k][2]
        
        keypoints_matched1.append((keypoints1[idx_image1][0], keypoints1[idx_image1][1]))
        keypoints_matched2.append((keypoints2[idx_image2][0], keypoints2[idx_image2][1]))

    # Rejection des points clés matched de même coordonnée
    coordinates_set = set()
    kept_indexes = []
    for i in range(len(keypoints_matched1)):    
        point = (keypoints_matched1[i][0], keypoints_matched1[i][1])    
        if point not in coordinates_set:
            kept_indexes.append(i)
            coordinates_set.add(point)

    keypoints_no_duplicates1 = []
    keypoints_no_duplicates2 = []

    for i in range(len(kept_indexes)):
        keypoints_no_duplicates1.append(keypoints_matched1[kept_indexes[i]])
        keypoints_no_duplicates2.append(keypoints_matched2[kept_indexes[i]])

    keypoints_matched1 = keypoints_no_duplicates1
    keypoints_matched2 = keypoints_no_duplicates2


    ##### 3. Reconstitution du panorama #####

    H, _ = calcul_matrice_H_avec_svd(keypoints_matched1, keypoints_matched2)
    
    H_inv = np.linalg.inv(H)
    H_inv = H_inv / H_inv[2][2]
    print()
    print("H_inv", H_inv)



    print()
    print("m nb_rows", len(img2))
    print("n nb_columns", len(img2[0]))

    coor_temp = np.array([1, 1, 1])
    print()
    print("coor_temp", coor_temp)
    print()
    print("H_inv@coor_temp", H_inv@coor_temp)

    coor_temp = np.array([277, 207, 1])
    print()
    print("coor_temp", coor_temp)
    print()
    print("H_inv@coor_temp", H_inv@coor_temp)


    coor_temp = np.array([494, 619, 1])
    print()
    print("coor_temp", coor_temp)
    print()
    print("H_inv@coor_temp", H_inv@coor_temp)

    coor_temp = np.array([len(img2), len(img2[0]), 1])
    print()
    print("coor_temp", coor_temp)
    print()
    shape_new_img = H_inv@coor_temp
    print("H_inv@coor_temp", H_inv@coor_temp)

    print("y", int(shape_new_img[0]))
    print("x", int(shape_new_img[1]))

    new_img = np.zeros((int(shape_new_img[0]), int(shape_new_img[1]), 3), dtype=np.float32)
    for i in range(len(img2)):
        for j in range(len(img2[0])):
            old_coord = np.array([i, j, 1])
            new_coord = H_inv@old_coord

            new_x = int(new_coord[0])
            new_y = int(new_coord[1])

            # Si coordonnée est à l'extérieur de l'image on ne la considère pas
            if new_x < 0 or new_x > shape_new_img[0] - 1 or new_y < 0 or new_y > shape_new_img[1] - 1: 
                continue

            new_img[new_x][new_y] = img_color2[i][j]/255.

    
    for i in range(len(img1)):
        for j in range(len(img1[0])):
            if i < 0 or i > shape_new_img[0] - 1 or j < 0 or j > shape_new_img[1] - 1:
                continue
            new_img[i][j] = img_color1[i][j]/255.

    
    afficher_img_avec_points_cles(new_img, [], False)

    return new_img
