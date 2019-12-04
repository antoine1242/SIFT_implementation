import numpy as np
import matplotlib.pyplot as plt
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
from afficher_images_avec_point_cles_matched import afficher_images_avec_point_cles_matched

def obtenir_panorama(img_color1, img_color2):

    # Convertion des images initiales en images tons de gris
    img1 = rgb2gray(img_color1)
    img2 = rgb2gray(img_color2)


    # Initialisation des constantes
    S = 3
    NB_OCTAVE = 3
    SEUIL_CONTRASTE = 0.03
    R_COURBURE_PRINCIPALE = 10
    NB_K_LOWEST_PTS = 10
    
    #"""

    ##### 1. Obtenir descripteurs des points clés pour les deux images #####

    print("\nCalculs pour Image 1")
    # Obtenir pyramide de gaussienne pour Image 1
    dogs1, sigmas1, gaussian_filtered_images1, gaussian_filtered_images_sigmas1 = difference_de_gaussiennes(
                                                                                    image_initiale=img1, 
                                                                                    s=S, 
                                                                                    nb_octave=NB_OCTAVE)

    # Obtenir les points clés pour Image 1
    keypoints1 = []
    keypoints_descriptors1  = []
    keypoints1_par_octave = []

    for resolution_octave in range(NB_OCTAVE):  
        keypoints = detection_points_cles(
                    dog=dogs1[resolution_octave], 
                    sigma=sigmas1[resolution_octave], 
                    seuil_contraste=SEUIL_CONTRASTE, 
                    r_courbure_principale=R_COURBURE_PRINCIPALE, 
                    resolution_octave=resolution_octave, 
                    gaussian_filtered_images=gaussian_filtered_images1[resolution_octave], 
                    gaussian_filtered_images_sigmas=gaussian_filtered_images_sigmas1[resolution_octave])

        keypoints1.extend(keypoints)
        keypoints1_par_octave.append(len(keypoints))

        # Obtenir les descripteurs
        keypoints_descriptors = description_points_cles(
                                    initial_image=img1,
                                    keypoints=keypoints, 
                                    resolution_octave=resolution_octave, 
                                    gaussian_filtered_images=gaussian_filtered_images1[resolution_octave], 
                                    gaussian_filtered_images_sigmas=gaussian_filtered_images_sigmas1[resolution_octave])

        keypoints_descriptors1.extend(keypoints_descriptors)

    print("Nombre de points cles dans l'image 1:", len(keypoints1))
    print("len keypoints_descriptors1 ", len(keypoints_descriptors1))

    plot_graph(keypoints1_par_octave, 1)

    print("Points retires a cause du contraste dans l'image 1:")

    np.save("points_cles_image_gauche.npy", keypoints1)
    np.save("descripteurs_image_gauche.npy", keypoints_descriptors1)


    print("\nCalculs pour Image 2")
    # Obtenir pyramide de gaussienne pour Image 2
    dogs2, sigmas2, gaussian_filtered_images2, gaussian_filtered_images_sigmas2 = difference_de_gaussiennes(
                                                                                    image_initiale=img2,
                                                                                    s=S,
                                                                                    nb_octave=NB_OCTAVE)

    # Obtenir points clés pour Image 2
    keypoints2 = []
    keypoints_descriptors2  = []
    keypoints2_par_octave = []

    for resolution_octave in range(NB_OCTAVE):
        keypoints = detection_points_cles(
                    dog=dogs2[resolution_octave],
                    sigma=sigmas2[resolution_octave],
                    seuil_contraste=SEUIL_CONTRASTE,
                    r_courbure_principale=R_COURBURE_PRINCIPALE,
                    resolution_octave=resolution_octave,
                    gaussian_filtered_images=gaussian_filtered_images2[resolution_octave],
                    gaussian_filtered_images_sigmas=gaussian_filtered_images_sigmas2[resolution_octave])

        keypoints2.extend(keypoints)
        keypoints2_par_octave.append(len(keypoints))

        # Obtenir descripteurs pour points clés Image 2
        keypoints_descriptors = description_points_cles(
                                    initial_image=img2,
                                    keypoints=keypoints,
                                    resolution_octave=resolution_octave, 
                                    gaussian_filtered_images=gaussian_filtered_images2[resolution_octave],
                                    gaussian_filtered_images_sigmas=gaussian_filtered_images_sigmas2[resolution_octave])
        
        keypoints_descriptors2.extend(keypoints_descriptors)

    print("Nombre de points cles dans l'image 2:", len(keypoints2))
    print("len keypoints_descriptors2 ", len(keypoints_descriptors2))

    plot_graph(keypoints2_par_octave, 2)

    np.save("points_cles_image_droite.npy", keypoints2)
    np.save("descripteurs_image_droite.npy", keypoints_descriptors2)


    ##### 2. Trouver points clés de l'image 1 qui concordent avec ceux de l'image 2 #####

    print("\nCalcul de la matrice de distances")
    # Obtenir matrice de distances
    distance_matrix = distance_inter_points(
                        descriptors_image1=keypoints_descriptors1,
                        descriptors_image2=keypoints_descriptors2)
    
    print("distance_matrix.shape", distance_matrix.shape)

    np.save("matrice_D.npy", distance_matrix)

    print("\nCalcul de l'index des k plus petites distances")
    # Obtenir les k points avec la plus petite distance
    k_lowest = get_k_lowest(
                descriptors_distance_matrix=distance_matrix,
                k=NB_K_LOWEST_PTS)


    print("len k_lowest ", len(k_lowest))

    # Obtenir points clés qui match pour l'image 1 et l'image 2
    # à partir de l'index recueilli dans k_lowest
    keypoints_matched1, keypoints_matched2 = obtenir_points_clés_match(
                                                k_lowest=k_lowest,
                                                keypoints1=keypoints_descriptors1,
                                                keypoints2=keypoints_descriptors2)

    
    print("len keypoints_matched1 ", len(keypoints_matched1))
    print("len keypoints_matched2 ", len(keypoints_matched2))

    #"""

    # comparer_eig_vs_svd(keypoints_matched1, keypoints_matched2)

    # TODO temporaire à enlever:
    #keypoints_matched1 = [(444.0, 766.0), (503.0, 749.0), (494.0, 619.0), (229.0, 638.0), (437.0, 760.0), (277.0, 810.0), (355.0, 818.0), (398.0, 924.0), (109.0, 988.0), (368.0, 908.0), (177.0, 749.0), (363.0, 624.0), (440.0, 645.0)]
    #keypoints_matched2 = [(447.0, 164.0), (507.0, 147.0), (499.0, 15.0), (230.0, 32.0), (440.0, 157.0), (277.0, 207.0), (356.0, 216.0), (399.0, 323.0), (105.0, 386.0), (369.0, 307.0), (176.0, 144.0), (366.0, 19.0), (444.0, 41.0)]


    afficher_images_avec_point_cles_matched(img_color1, img_color2, keypoints_matched1, keypoints_matched2)

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

def plot_graph(keypoint_lens, num_image):
    x = []
    y = keypoint_lens
    
    # Avoir les points au bon octave
    for i in range(1, len(keypoint_lens) + 1):
        x.append(i)

    plt.plot(x, y, linestyle='None', marker='o', markerfacecolor='blue', markersize=5)

    plt.xlabel("Numero de l'octave")
    plt.ylabel("Nombre de points cles detectes")

    plt.title("Evolution du nombre de points-cles pour l'image " + str(num_image))

    plt.show()