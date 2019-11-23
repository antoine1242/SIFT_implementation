import numpy as np

def calcul_matrice_H(keypoints_matched1, keypoints_matched2):
    matrix_A = []

    for i in range(len(keypoints_matched1)):
        x1 = keypoints_matched1[i][0]
        y1 = keypoints_matched1[i][1]

        x2 = keypoints_matched2[i][0]
        y2 = keypoints_matched2[i][1]

        matrix_A.append([x1, y1, 1, 0, 0, 0, -x2*x1, -x2*y1, -x2])
        matrix_A.append([0, 0, 0, x1, y1, 1, -y2*x1, -y2*y1, -y2])

    matrix_A = np.array(matrix_A)

    # (A.T)A
    matrix_A_quadratic = np.matmul((matrix_A.transpose()), matrix_A)

    valeurs_propres, vecteurs_propres = np.linalg.eig(matrix_A_quadratic)

    idx_smallest_eigenvalue = np.argmin(valeurs_propres)

    H_flatten = vecteurs_propres[idx_smallest_eigenvalue]

    H_flatten_norm = H_flatten / H_flatten[-1]

    H_norm = np.reshape(H_flatten_norm, (3,3))

    # SVD
    U, S, VT = np.linalg.svd(matrix_A)

    H_flatten_svd = VT.transpose()[-1]
    H_flatten_norm_svd = H_flatten_svd / H_flatten_svd[-1]
    H_norm_svd = np.reshape(H_flatten_norm_svd, (3,3))

    print("H_flatten")
    print(H_flatten)

    # On obtient presque le même vecteur propre... certaines valeurs ont un signe inversé (mais pas toutes !?)
    print("VT")
    print(VT.transpose()[-1])

    return H_norm_svd

    """
    print("H_norm: ")
    print(H_norm)

    print("H_norm_svd")
    print(H_norm_svd)
    """