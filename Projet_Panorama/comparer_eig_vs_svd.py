from homographie import calcul_matrice_H_avec_eig, calcul_matrice_H_avec_svd

def comparer_eig_vs_svd(keypoints_matched1, keypoints_matched2):
    H_norm_svd_eig, H_flatten_eig = calcul_matrice_H_avec_eig(keypoints_matched1, keypoints_matched2, verbose=True)

    H_norm_svd_svd, H_flatten_svd = calcul_matrice_H_avec_svd(keypoints_matched1, keypoints_matched2, verbose=True)


    print("H_flatten_eig", H_flatten_eig)
    print("H_flatten_svd", H_flatten_svd)

    return H_norm_svd_eig, H_flatten_eig, H_norm_svd_svd, H_flatten_svd