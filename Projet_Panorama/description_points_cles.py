import numpy as np
import cv2
from gaussian_filter import gaussian_filter
from scipy.ndimage.filters import convolve
from gaussian_filter import gaussian_filter

def description_points_cles(initial_image, keypoints, resolution_octave, gaussian_filtered_images, gaussian_filtered_images_sigmas):
    print("Description des points cles")

    # Dictionnaire d'images filtrées avec sigma donné:
    # Key: sigma
    # Value: image initiale convoluée avec filtre gaussien de valeur sigma
    keypoints_descriptors = []
    filtered_images_dict = {}
    for keypoint in keypoints:
        descriptor = calculate_descriptors(initial_image, filtered_images_dict, keypoint, resolution_octave, gaussian_filtered_images, gaussian_filtered_images_sigmas)
        
        if len(descriptor) > 0:
            keypoints_descriptors.append(descriptor)

    return np.array(keypoints_descriptors)

def calculate_descriptors(initial_image, filtered_images_dict, keypoint, resolution_octave, gaussian_filtered_images, gaussian_filtered_images_sigmas):
    nb_bins = 8
    nb_regions = 4
    region_length = 4
    window_length = region_length * nb_regions
    

    # gaussian_filter multiplie sigma par 3 donc on doit diviser par 6 ici pour avoir 0.5 sigma
    circular_gaussian_window = gaussian_filter(window_length / 6)

    # TODO ajuster position aussi lorsqu'on va mettre bonne version de L
    x_kp = int(round(keypoint[0]/(2**resolution_octave))) #keypoint[0] # int(round(keypoint[0]/(2**resolution_octave)))
    y_kp = int(round(keypoint[1]/(2**resolution_octave))) #keypoint[1] # int(round(keypoint[1]/(2**resolution_octave)))
    sigma = keypoint[2]
    
    # On initialise le descripteur avec les coordonnées x,y du point clé
    keypoint_descriptor = [keypoint[0], keypoint[1]]

    # Sélection de l'image correspondant au sigma du point clé


    # TODO : Revoir quelle image on doit prendre 
    idx = gaussian_filtered_images_sigmas.index(sigma)
    L = gaussian_filtered_images[idx]

    # if sigma in filtered_images_dict:
    #     L = filtered_images_dict[sigma]
    # else:
    #     kernel = gaussian_filter(sigma)
    #     result = convolve(initial_image, kernel)
    #     filtered_images_dict[sigma] = result
    #     L = result

    
    L = rotate(L, keypoint[3], (y_kp, x_kp))

    # Parcours de la zone 16x16 autour du point clé pour calculer le gradient de chaque point
    range_zone = int(window_length / 2)

    # Initialisation de la matrice de gradients
    # Note: Besoin d'une liste pcq numpy array veut pas remplacer les ints par des tuples
    gradients_matrix = x = [[0 for i in range(window_length)] for j in range(window_length)]
    
    # Calcul des gradients dans la matrice de gradients
    for dx_zone in range(-range_zone, range_zone):
        for dy_zone in range(-range_zone, range_zone):
            x = int(x_kp + dx_zone)
            y = int(y_kp + dy_zone)

            # Si coordonnée est à l'extérieur de l'image on ne la considère pas
            if x < 0 or x > L.shape[0] - 1 or y < 0 or y > L.shape[1] - 1: 
                continue

            if L[x][y] == 0:
                return []

            # Calcul du gradient (norme + orientation)
            dx = 0.5 * (L[min(L.shape[0]-1, x+1)][y] - L[max(x-1, 0)][y])
            dy = 0.5 * (L[x][min(L.shape[1]-1, y+1)] - L[x][max(y-1, 0)])
            m = np.sqrt(dx**2 + dy**2)
            theta = (np.arctan2(dy, dx)) * 180/np.pi
            
            # Ajouter gradient à la matrice de gradients
            gradients_matrix[dx_zone + range_zone][dy_zone + range_zone] = (m, theta)

    histograms = []
    # Parcours de chaque sous-région. 
    # Création d'un histogramme des orientations des gradients de la sous-région
    for i in range(0, window_length, region_length):
        for j in range(0, window_length, region_length):
            hist = np.zeros(nb_bins, dtype=np.float32)
            for k in range(i, i + region_length):
                for m in range(j, j + region_length):
                    # Vaut 0 si le pixel est hors de l'image
                    if gradients_matrix[k][m] == 0:
                        continue

                    mag = gradients_matrix[k][m][0]
                    theta = gradients_matrix[k][m][1]
                    weight = circular_gaussian_window[k][m] * mag

                    bin_number = int(np.floor(theta) // (360 // nb_bins))
                    hist[bin_number] += weight
                            
            histograms.extend(hist)
    
    # Normalisation du vecteur de features
    norm = np.linalg.norm(histograms)
    normalized_vector_1 = [float(i)/norm for i in histograms]

    # Le poids de chaque vecteur ne doit pas dépasser 0.2
    for index, value in enumerate(normalized_vector_1):
        normalized_vector_1[index] = min(value, 0.2)

    # Normalisation du vecteur de features
    norm_1 = np.linalg.norm(normalized_vector_1)
    normalized_vector_2 = [float(i)/norm_1 for i in normalized_vector_1]

    # Ajout du vecteur d'histogrammes dans le desctipteur
    keypoint_descriptor.extend(normalized_vector_2)

    return keypoint_descriptor

def rotate(image, angle, center = None, scale = 1.0):
    (h, w) = image.shape[:2]

    if center is None:
        center = (w / 2, h / 2)

    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated