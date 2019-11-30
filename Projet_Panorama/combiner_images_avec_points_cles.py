import numpy as np
from homographie import calcul_matrice_H_avec_svd

def combiner_images_avec_points_cles(keypoints_matched1, keypoints_matched2, img_color1, img_color2):
    H, _ = calcul_matrice_H_avec_svd(keypoints_matched1, keypoints_matched2)
    
    H_inv = np.linalg.inv(H)

    shape_img2 = np.array([len(img_color2), len(img_color2[0]), 1])
    shape_pano_img = H_inv@shape_img2

    # Ajouter image de droite
    pano_img = np.zeros((int(shape_pano_img[0]), int(shape_pano_img[1]), 3), dtype=np.float32)
    
    for i in range(len(pano_img)):
        for j in range(len(pano_img[0])):
            img_target_coord = np.array([i, j, 1])

            img_droite_coord = H@img_target_coord

            img_droite_x = int(round(img_droite_coord[0]))
            img_droite_y = int(round(img_droite_coord[1]))

            # Si coordonnée est à l'extérieur de l'image on ne la considère pas
            if img_droite_x < 0 or img_droite_x > len(img_color2) - 1 or img_droite_y < 0 or img_droite_y > len(img_color2[0]) - 1: 
                continue

            pano_img[i][j] = img_color2[img_droite_x][img_droite_y]/255.


    # Ajouter image de gauche
    for i in range(len(img_color1)):
        for j in range(len(img_color1[0])):
            if i < 0 or i > shape_pano_img[0] - 1 or j < 0 or j > shape_pano_img[1] - 1:
                continue
            pano_img[i][j] = img_color1[i][j]/255.

    return pano_img