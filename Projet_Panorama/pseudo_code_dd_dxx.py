    # x = candidate_keypoint[0]
    # y = candidate_keypoint[1]

    # s = 1
    # dx = (stack_of_dog[s][x+1][y] - stack_of_dog[s][x-1][y]) / 2.
    # dy = (stack_of_dog[s][x][y+1] - stack_of_dog[s][x][y-1]) / 2.
    # ds = (stack_of_dog[s+1][x][y] - stack_of_dog[s-1][x][y]) / 2.

    # dxx = (stack_of_dog[s][x+1][y] - 2*stack_of_dog[s][x][y] + stack_of_dog[s][x-1][y]) 
    # dyy = (stack_of_dog[s][x][y+1] - 2*stack_of_dog[s][x][y] + stack_of_dog[s][x][y-1]) 
    # dss = (stack_of_dog[s+1][x][y] - 2*stack_of_dog[s][x][y] + stack_of_dog[s-1][x][y]) 

    # dxy = ((stack_of_dog[s][x+1][y+1] - stack_of_dog[s][x-1][y+1]) - (stack_of_dog[s][x+1][y-1] - stack_of_dog[s][x-1][y-1])) /4.
    # dxs = ((stack_of_dog[s+1][x+1][y] - stack_of_dog[s+1][x-1][y]) - (stack_of_dog[s-1][x+1][y] - stack_of_dog[s-1][x-1][y])) /4.
    # dys = ((stack_of_dog[s+1][x][y+1] - stack_of_dog[s+1][x][y-1]) - (stack_of_dog[s-1][x][y+1] - stack_of_dog[s-1][x][y-1])) /4.

    # d_dx = np.asarray([dx, dy, ds])
    # dd_dxx = np.asarray([
    #     [dxx, dxy, dxs],
    #     [dxy, dyy, dys],
    #     [dxs, dys, dss]
    # ])

    # X_2 = -np.linalg.inv(dd_dxx).dot(d_dx)
    # # print("X 2", X_2)
    # D_of_x = stack_of_dog[s][x][y] + 0.5 * (d_dx.dot(X_2))


    def dog_derivative(stack_of_dog, candidate_keypoint):
    x = candidate_keypoint[0]
    y = candidate_keypoint[1]
    s = 1 

    # 1. Obtenir évaluation de D au point candidat x (D(x))
    dx = (stack_of_dog[s][x+1][y] - stack_of_dog[s][x-1][y]) / 2.
    dy = (stack_of_dog[s][x][y+1] - stack_of_dog[s][x][y-1]) / 2.
    ds = (stack_of_dog[s+1][x][y] - stack_of_dog[s-1][x][y]) / 2.

    d_dx = np.array([dx, dy, ds])

    X = np.array(candidate_keypoint)

    D_of_x = stack_of_dog[s][x][y] + 0.5 * (d_dx.dot(X))


    # 2. Obtenir Ratio pour la courbature
    dxx = (stack_of_dog[s][x+1][y] - 2*stack_of_dog[s][x][y] + stack_of_dog[s][x-1][y]) 
    dyy = (stack_of_dog[s][x][y+1] - 2*stack_of_dog[s][x][y] + stack_of_dog[s][x][y-1]) 
    dxy = ((stack_of_dog[s][x+1][y+1] - stack_of_dog[s][x-1][y+1]) - (stack_of_dog[s][x+1][y-1] - stack_of_dog[s][x-1][y-1])) /4.

    traceH = dxx + dyy
    detH = dxx*dyy - dxy**2

    ratio = traceH**2 / detH 

    return abs(D_of_x), detH, ratio





# # Élimination de certains point clés candidats
# for candidate_keypoint in candidate_keypoints:
#     stack_of_dog = np.asarray([previous, current, next_])
#     # Obtenir informations nécessaires à partir des Différences de Gaussiennes
#     D_of_x, detH, ratio = dog_derivative(stack_of_dog, candidate_keypoint) 
#     # Élimination des points-clés de faible contraste avec D(x)
#     if D_of_x < seuil_contraste:
#         cnt_removed_extrema += 1
#     # Élimination des points situés sur les arêtes 
#     elif detH < 0 or ratio > (r_courbure_principale + 1)**2 / r_courbure_principale:
#         cnt_removed_edge += 1
#     # Si le point clé candidat respecte l'ensemble des restrictions on l'ajoute aux points clés 
#     else:
#         keypoints.append(candidate_keypoint)