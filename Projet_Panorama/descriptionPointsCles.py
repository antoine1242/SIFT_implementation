import numpy as np
from detectionPointsCles import gaussian_filter
import os

def descriptionPointsCles(keypoints, gaussian_filtered_images, gaussian_filtered_images_sigmas):
    print("Description des points cles")

    keypoints_descriptors = []
    
    nb_bins = 8
    nb_regions = 4
    region_length = 4
    window_length = region_length * nb_regions
    
    for keypoint in keypoints:
        x_kp = keypoint[0]
        y_kp = keypoint[1]
        sigma = keypoint[2]
        
        # On initialise le descripteur avec les coordonnées x,y du point clé
        keypoint_descriptor = [x_kp, y_kp]

        # gaussian_filter multiplie sigma par 3 donc on doit diviser par 6 ici pour avoir 0.5 sigma
        circular_gaussian_window = gaussian_filter(window_length / 6)

        # Sélection de l'image correspondant au sigma du point clé
        idx = gaussian_filtered_images_sigmas.index(sigma)
        L = gaussian_filtered_images[idx]
        
        # Parcours de la zone 16x16 autour du point clé pour calculer le gradient de chaque point
        range_zone = int(window_length / 2)
        # Besoin d'une liste pcq numpy array veut pas remplacer les ints par des tuples
        gradients_matrix = x = [[0 for i in range(window_length)] for j in range(window_length)]
        
        for dx_zone in range(-range_zone, range_zone):
            for dy_zone in range(-range_zone, range_zone):
                x = int(x_kp + dx_zone)
                y = int(y_kp + dy_zone)

                if x < 0 or x > L.shape[0] - 1 or y < 0 or y > L.shape[1] - 1: 
                    continue

                dx = L[min(L.shape[0]-1, x+1)][y] - L[max(x-1, 0)][y]
                dy = L[x][min(L.shape[1]-1, y+1)] - L[x][max(y-1, 0)]
                m = np.sqrt(dx**2 + dy**2)
                theta = (np.arctan2(dy, dx)) * 180/np.pi
                
                gradients_matrix[dx_zone + range_zone][dy_zone + range_zone] = (m, theta)

        histograms = []
        # Parcours de chaque sous-région. Création d'un histogramme des orientations des gradients de la sous-région
        for i in range(0, window_length, region_length):
            for j in range(0, window_length, region_length):
                hist = np.zeros(nb_bins, dtype=np.float32)
                for k in range(i, i + region_length):
                    for m in range(j, j + 4):
                        # Vaut 0 si le pixel est hors de l'image
                        if gradients_matrix[k][m] == 0:
                            continue
                        mag = gradients_matrix[k][m][0]
                        theta = gradients_matrix[k][m][1]
                
                        weight = circular_gaussian_window[dx_zone + range_zone][dy_zone + range_zone] * mag
                        bin_number = int(np.floor(theta) // (360 // nb_bins))
                        hist[bin_number] += weight
                histograms.extend(hist)
        
        # Le poids de chaque vecteur ne doit pas dépasser 0.2
        for value in histograms:
            value = min(value, 0.2)

        # Normalisation du vecteur de features
        s = sum(histograms)
        normalized_vector = [float(i)/s for i in histograms]

        # Ajout du vecteur dans le desctipteur
        keypoint_descriptor.extend(normalized_vector)

        # Ajout du descripteur à la liste des descripteurs
        keypoints_descriptors.append(keypoint_descriptor)
    
    return np.array(keypoints_descriptors)
  