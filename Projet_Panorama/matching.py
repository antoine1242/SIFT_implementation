import numpy as np
from scipy.spatial import distance_matrix

def distance_inter_points(descriptors_image1, descriptors_image2):
    print("Calcul de la matrice de distance")

    descriptors1 = []
    for i in range(len(descriptors_image1)):
        descriptors1.append(descriptors_image1[i][2:])

    descriptors2 = []
    for i in range(len(descriptors_image2)):
        descriptors2.append(descriptors_image2[i][2:])

    return distance_matrix(descriptors1, descriptors2)

def get_k_lowest(descriptors_distance_matrix, k):
    print("Calcul de l'index des k plus petites distances")
    # Tuples représentant (valeur, index i, index j)
    k_lowest = [(float("inf"), 0, 0) for i in range(k)]

    for i in range(len(descriptors_distance_matrix)):
        for j in range(len(descriptors_distance_matrix[0])):
            for k in range(len(k_lowest)):
                if descriptors_distance_matrix[i][j] < k_lowest[k][0]:
                    k_lowest[k] = (descriptors_distance_matrix[i][j], i, j)
                    k_lowest.sort(reverse = True)
                    break

    print("K_lowest: ", k_lowest)
    return k_lowest
