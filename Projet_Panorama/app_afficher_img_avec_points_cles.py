


from difference_de_gaussiennes import difference_de_gaussiennes
from description_points_cles import description_points_cles
from detection_points_cles import detection_points_cles
from skimage.color import rgb2gray
from afficher_img_avec_points_cles import afficher_img_avec_points_cles
from skimage.io import imread

def run():

    img_color1 = imread("./images/droite.jpg")
    img1 = rgb2gray(img_color1)

    S = 3
    NB_OCTAVE = 3
    SEUIL_CONTRASTE = 0.03
    R_COURBURE_PRINCIPALE = 10
    RESOLUTION_OCTAVE = 0
    NB_K_LOWEST_PTS = 20


    # Obtenir pyramide de gaussienne pour Image 1
    dogs1, sigmas1, gaussian_filtered_images1, gaussian_filtered_images_sigmas1 = difference_de_gaussiennes(
                                                                                    image_initiale=img1, 
                                                                                    s=S, 
                                                                                    nb_octave=NB_OCTAVE)

    # Obtenir les points clés pour Image 1
    keypoints_octaves = []
    for resolution_octave in range(NB_OCTAVE):  
        keypoints = detection_points_cles(
                        dog=dogs1[resolution_octave], 
                        sigma=sigmas1[resolution_octave], 
                        seuil_contraste=SEUIL_CONTRASTE, 
                        r_courbure_principale=R_COURBURE_PRINCIPALE, 
                        resolution_octave=resolution_octave, 
                        gaussian_filtered_images=gaussian_filtered_images1[resolution_octave], 
                        gaussian_filtered_images_sigmas=gaussian_filtered_images_sigmas1[resolution_octave])

        keypoints_octaves.append(keypoints)


    afficher_img_avec_points_cles(img_color1, keypoints_octaves, True, "image_droite_avec_points_cles_et_theta")

run()