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

    k_lowest_set = set()
   
    for i in range(0, m):
        for j in range(0, n):
            candidate = (descriptors_distance_matrix[i][j], i, j)
            candidate_coord = (i, j)

            if len(k_lowest) < k:
                k_lowest.append(candidate)
                k_lowest_set.add(candidate_coord)

            # Si les coordonnée du point clé candidat on ne l'ajoute pas  
            elif candidate_coord in k_lowest_set:
                continue

            # Si la distance du nouveau point candidat est plus petite que la distance maximale dans les k_lowest
            elif candidate[0] < k_lowest[0][0]:
                # On enlève valeur max
                removed_candidate = k_lowest.pop(0)
                # On l'enlève du set
                if removed_candidate is not None:
                    removed_candidate_coord = (removed_candidate[1], removed_candidate[2])
                    k_lowest_set.remove(removed_candidate_coord)

                # On ajoute nouveau point
                k_lowest.append(candidate)
                # On sort l'array
                sorted(k_lowest, key=lambda x: x[0], reverse = True)
                # On l'ajoute au set
                k_lowest_set.add(candidate_coord)

            
    print(k_lowest)

    return k_lowest