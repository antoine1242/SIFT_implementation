import numpy as np
import timeit

def obtenir_matrice_A(keypoints_matched1, keypoints_matched2):
    matrix_A = []

    for i in range(len(keypoints_matched1)):
        x1 = keypoints_matched1[i][0]
        y1 = keypoints_matched1[i][1]

        x2 = keypoints_matched2[i][0]
        y2 = keypoints_matched2[i][1]

        matrix_A.append([x1, y1, 1, 0, 0, 0, -x2*x1, -x2*y1, -x2])
        matrix_A.append([0, 0, 0, x1, y1, 1, -y2*x1, -y2*y1, -y2])

    matrix_A = np.array(matrix_A)

    return matrix_A


def calcul_matrice_H_avec_eig(keypoints_matched1, keypoints_matched2, verbose=False):
    matrix_A = obtenir_matrice_A(keypoints_matched1, keypoints_matched2)


    if verbose:
        start_time = timeit.default_timer()

    # (A.T)A
    matrix_A_quadratic = np.matmul((matrix_A.transpose()), matrix_A)
    
    # Décomposition en valeurs propres
    valeurs_propres, vecteurs_propres = np.linalg.eig(matrix_A_quadratic)

    if verbose:
        time_ = timeit.default_timer() - start_time
        print("--- np.linalg.eig in " + str(time_) + " seconds ---")

    idx_smallest_eigenvalue = np.argmin(valeurs_propres)

    H_flatten = vecteurs_propres[:, idx_smallest_eigenvalue]

    H_norm = H_flatten / H_flatten[-1]
    
    H_norm = np.reshape(H_norm, (3,3))  

    return H_norm, H_flatten


def calcul_matrice_H_avec_svd(keypoints_matched1, keypoints_matched2, verbose=False):
    matrix_A = obtenir_matrice_A(keypoints_matched1, keypoints_matched2)

    if verbose:
        start_time = timeit.default_timer()

    # SVD
    U, S, VT = np.linalg.svd(matrix_A)

    if verbose:        
        time_ = timeit.default_timer() - start_time
        print("--- np.linalg.svd in " + str(time_) + " seconds ---")


    H_flatten_svd = VT[-1]
    H_flatten_norm_svd = H_flatten_svd / H_flatten_svd[-1]


    H_norm_svd = np.reshape(H_flatten_norm_svd, (3,3))

    return H_norm_svd, H_flatten_svd


# Comparer dernier vecteur singulier vs vecteur propre A.T*A 
def vs_SDV_et_vp_ATA(keypoints_matched1, keypoints_matched2):
    _, H_flatten_svd = calcul_matrice_H_avec_svd(keypoints_matched1, keypoints_matched2)

    _, H_flatten_eig = calcul_matrice_H_avec_eig(keypoints_matched1, keypoints_matched2)

    print("H_flatten_svd", H_flatten_svd)
    print("H_flatten_eig", H_flatten_eig)

