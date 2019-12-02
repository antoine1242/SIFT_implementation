import numpy as np
from scipy.spatial import distance_matrix

def distance_inter_points(descriptors_image1, descriptors_image2):
    descriptors1 = []
    for i in range(len(descriptors_image1)):
        descriptors1.append(descriptors_image1[i][2:])

    descriptors2 = []
    for i in range(len(descriptors_image2)):
        descriptors2.append(descriptors_image2[i][2:])

    return distance_matrix(descriptors1, descriptors2)

def get_k_lowest(descriptors_distance_matrix, k):   
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

    for i in range(0, m):
        for j in range(0, n):
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
                k_lowest.sort(reverse = True, key=getKey)

    return k_lowest

def getKey(item):
    return item[0]



"""
k_lowest 1 octave
[(0.05294535922287039, 419, 470), (0.05250718522786104, 1379, 1385), (0.05010410116263206, 1125, 1153), 
(0.05000052979786348, 760, 778), (0.046431173495780825, 732, 762), (0.04517430485456253, 1399, 1402), 
(0.03952349631897787, 400, 449), (0.03659998014756905, 902, 949), (0.03615909829488879, 887, 930), (0.02809611919973084, 899, 945)]
"""

"""
k_lowest 2 octave
[(0.026173213628553675, 3189, 1445), (0.025970717262469904, 3426, 1460), (0.025508390192831264, 1460, 1445), 
(0.02545096469425073, 1467, 1460), (0.02451710141081692, 2615, 2680), (0.02188307085791383, 1452, 1460), 
(0.020965419175062224, 3552, 2823), (0.020226362162732683, 2779, 3622), (0.011178534952686597, 2768, 2818), (0.010613759395196666, 1882, 1913)]
"""