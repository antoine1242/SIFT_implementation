
import numpy as np
from difference_de_gaussiennes import difference_de_gaussiennes
from description_points_cles import description_points_cles
from detection_points_cles import detection_points_cles
from gaussian_filter import gaussian_filter
from matching import distance_inter_points, get_k_lowest
from skimage.color import rgb2gray
from afficher_img_avec_points_cles import afficher_img_avec_points_cles
from obtenir_points_clés_match import obtenir_points_clés_match
from combiner_images_avec_points_cles import combiner_images_avec_points_cles
from hist_match import equalize_hist
from comparer_eig_vs_svd import comparer_eig_vs_svd

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
    NB_K_LOWEST_PTS = 20

    #"""

    ##### 1. Obtenir descripteurs des points clés pour les deux images #####

    print("\nCalculs pour Image 1")
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


    print("\nCalculs pour Image 2")
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

    print("\nCalcul de la matrice de distances")   
    # Obtenir matrice de distances    
    distance_matrix = distance_inter_points(
                        descriptors_image1=keypoints_descriptors1, 
                        descriptors_image2=keypoints_descriptors2)


    print("\nCalcul de l'index des k plus petites distances")
    # Obtenir les k points avec la plus petite distance
    k_lowest = get_k_lowest(
                descriptors_distance_matrix=distance_matrix, 
                k=NB_K_LOWEST_PTS)


    # Obtenir points clés qui match pour l'image 1 et l'image 2 
    # à partir de l'index recueilli dans k_lowest
    keypoints_matched1, keypoints_matched2 = obtenir_points_clés_match(
                                                k_lowest=k_lowest,
                                                keypoints1=keypoints1, 
                                                keypoints2=keypoints2)

    #"""

    comparer_eig_vs_svd(keypoints_matched1, keypoints_matched2)

    # TODO temporaire à enlever:
    #keypoints_matched1 = [(444.0, 766.0), (503.0, 749.0), (494.0, 619.0), (229.0, 638.0), (437.0, 760.0), (277.0, 810.0), (355.0, 818.0), (398.0, 924.0), (109.0, 988.0), (368.0, 908.0), (177.0, 749.0), (363.0, 624.0), (440.0, 645.0)]
    #keypoints_matched2 = [(447.0, 164.0), (507.0, 147.0), (499.0, 15.0), (230.0, 32.0), (440.0, 157.0), (277.0, 207.0), (356.0, 216.0), (399.0, 323.0), (105.0, 386.0), (369.0, 307.0), (176.0, 144.0), (366.0, 19.0), (444.0, 41.0)]


    ##### 3. Reconstitution du panorama #####

    img_color2_v2 = equalize_hist(img_color2, img_color1)

    print("Combinaison des deux images pour former panorama.")
    pano_img = combiner_images_avec_points_cles(
                    keypoints_matched1=keypoints_matched1, 
                    keypoints_matched2=keypoints_matched2, 
                    img_color1=img_color1, 
                    img_color2=img_color2_v2)
    
    afficher_img_avec_points_cles(pano_img, [], False)

    return pano_img
