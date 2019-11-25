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
    
    # Liste comportant les k point avec la plus petite distance en ordre décroissant
    # Contient: Tuples représentant (valeur, index i, index j)
    k_lowest = []
    
    m = len(descriptors_distance_matrix)
    n = len(descriptors_distance_matrix[0])
    matrice_has_been_transposed = False
    
    if m > n:        
        descriptors_distance_matrix = descriptors_distance_matrix.transpose()
        m = len(descriptors_distance_matrix)
        n = len(descriptors_distance_matrix[0])
        matrice_has_been_transposed = True

    # Parcourir matrice sytmérique (évite d'avoir des dupliqués)
    for i in range(0, m):
        for j in range(i + 1, n):
            if not matrice_has_been_transposed:
                candidate = (descriptors_distance_matrix[i][j], i, j)
            else: 
                candidate = (descriptors_distance_matrix[i][j], j, i)

            if len(k_lowest) < k:
                k_lowest.append(candidate)
            # Si la distance du nouveau point candidat est plus petite que la distance maximale dans les k_lowest
            elif candidate[0] < k_lowest[0][0]:
                # On enlève valeur max
                k_lowest.pop(0)
                # On ajoute nouveau point
                k_lowest.append(candidate)
                # On sort l'array
                k_lowest.sort(reverse = True)

    return k_lowest


# Pour tester
# d_m = np.array([[ 1.,  2., 3.],
#                 [ 4.,  5., 6.],
#                 [ 7.,  8., 9.],
#                 [ 10.,  11., 12.]
                
#                 ])

# print(get_k_lowest(d_m, 1))

