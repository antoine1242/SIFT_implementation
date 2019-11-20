import numpy as np

def detectionPointsCles(dog, sigma, seuil_contraste, r_courbure_principale, resolution_octave, gaussian_filtered_images, gaussian_filtered_images_sigmas):
    print("detectionPointsCles")
    cnt_candidates_curr = 0
    cnt_candidates_octave = []
    cnt_removed_contrast = 0
    cnt_removed_edge = 0
    keypoints = []
    nb_bins = 10
    bin_size = 360 // nb_bins


    for i in range(1, len(dog)-1):
        previous = dog[i-1]
        current = dog[i]
        nextDog = dog[i+1]
        candidate_keypoints = []
        for x in range(1, len(previous)-1):
            for y in range(1, len(previous[0])-1):
                if isExtremum(previous, current, nextDog, x, y):
                    candidate_keypoints.append((x,y,sigma[i]))
                    cnt_candidates_curr += 1
        
        # Élimination point clés faible constraste
        for candidate_keypoint in candidate_keypoints:
            stack_of_dog = np.asarray([previous, current, nextDog])

            D_of_x, detH, ratio = dogDerivative(stack_of_dog, candidate_keypoint) 

            if D_of_x < seuil_contraste:
                cnt_removed_contrast += 1
            elif detH < 0 or ratio > (r_courbure_principale + 1)**2 / r_courbure_principale:
                cnt_removed_edge += 1
            else:
                keypoints.append(candidate_keypoint)

        cnt_candidates_octave.append(cnt_candidates_curr)
        cnt_candidates_curr = 0

    cnt_candidates = sum(cnt_candidates_octave)

    check_val = set()
    keypoints_filtered = []
    for x, y, s in keypoints:
        if (x, y) not in check_val:
            keypoints_filtered.append((x, y, s))

    print(cnt_removed_contrast)
    print(cnt_removed_edge)
    print(cnt_candidates)
    keypoints_m_and_theta = []
    for keypoint in keypoints_filtered:
        # TODO est-ce que le sigma est suppose etre "proche" ou exact
        x_kp = keypoint[0]
        x_kp = keypoint[1]
        sigma = keypoint[2]
        
        range_zone = int(2*np.ceil(sigma) + 1)

        # s = np.clip(s, 0, octave.shape[2] - 1) ???
        # TODO: 
        #kernel = gaussian_filter(image_initiale_norm, sigma=sigma) 

        # TODO: Comment trouver le bon L
        # TODO: Comment trouver le nombre de pixels a observer autour

        idx = gaussian_filtered_images_sigmas.index(sigma)
        L = gaussian_filtered_images[idx]
        
        hist = np.zeros(nb_bins, dtype=np.float32)

        for dx_zone in range(-range_zone, range_zone + 1):
            for dy_zone in range(-range_zone, range_zone + 1):
                x = x_kp + dx_zone
                y = x_kp + dy_zone

                if x < 0 or x > L.shape[0] - 1 or y < 0 or y > L.shape[1] - 1: 
                    continue

                dx = L[min(L.shape[0]-1, x+1)][y] - L[max(x-1, 0)][y]
                dy = L[x][min(L.shape[1]-1, y+1)] - L[x][max(y-1, 0)]
                m = np.sqrt(dx**2 + dy**2)
                theta = (np.arctan(dy/dx)+np.pi) * 180/np.pi
                
                # TODO: ajuster poids de m 
                #weight = kernel[oy+w, ox+w] * m
                weight = m 

                bin_number = int(np.floor(theta) // bin_size)
                hist[bin_number] += weight

        # TODO reste du code de l'article 

        # max_bin = np.argmax(hist)
        # new_kps.append([kp[0], kp[1], kp[2], fit_parabola(hist, max_bin, bin_width)])

        # max_val = np.max(hist)
        # for binno, val in enumerate(hist):
        #     if binno == max_bin: continue

        #     if .8 * max_val <= val:
        #         new_kps.append([kp[0], kp[1], kp[2], fit_parabola(hist, binno, bin_width)])

        # def fit_parabola(hist, binno, bin_width):
        #     centerval = binno*bin_width + bin_width/2.

        #     if binno == len(hist)-1: rightval = 360 + bin_width/2.
        #     else: rightval = (binno+1)*bin_width + bin_width/2.

        #     if binno == 0: leftval = -bin_width/2.
        #     else: leftval = (binno-1)*bin_width + bin_width/2.
            
        #     A = np.array([
        #         [centerval**2, centerval, 1],
        #         [rightval**2, rightval, 1],
        #         [leftval**2, leftval, 1]])
        #     b = np.array([
        #         hist[binno],
        #         hist[(binno+1)%len(hist)], 
        #         hist[(binno-1)%len(hist)]])

        #     x = LA.lstsq(A, b, rcond=None)[0]
        #     if x[0] == 0: x[0] = 1e-6
        #     return -x[1]/(2*x[0])



        # TODO est-ce qu'on compute toute la matrice des m et tetha avant?
        # mag_theta_matrix = np.zeros(L.shape)
        # for x in range(mag_theta_matrix.shape[0]):
        #     for x in range(mag_theta_matrix.shape[1]):
        #         dx = L[x+1][y] - L[x-1][y]
        #         dy = L[x][y+1] - L[x][y-1]
        #         m = np.sqrt(dx**2 + dy**2)
        #         theta = (np.arctan(dy/dx)+np.pi) * 180/np.pi
        #         mag_theta_matrix[x][y] = (m, theta)






        #keypoints_m_and_theta.append((x, y, sigma, m, theta))

    for keypoint in keypoints_m_and_theta:
        pass
        # get neighbours
        # 

def dogDerivative(stack_of_dog, candidate_keypoint):
    x = candidate_keypoint[0]
    y = candidate_keypoint[1]

    s = 1
    dx = (stack_of_dog[s][x+1][y] - stack_of_dog[s][x-1][y]) / 2.
    dy = (stack_of_dog[s][x][y+1] - stack_of_dog[s][x][y-1]) / 2.
    ds = (stack_of_dog[s+1][x][y] - stack_of_dog[s-1][x][y]) / 2.

    dxx = (stack_of_dog[s][x+1][y] - 2*stack_of_dog[s][x][y] + stack_of_dog[s][x-1][y]) 
    dyy = (stack_of_dog[s][x][y+1] - 2*stack_of_dog[s][x][y] + stack_of_dog[s][x][y-1]) 
    dss = (stack_of_dog[s+1][x][y] - 2*stack_of_dog[s][x][y] + stack_of_dog[s-1][x][y]) 

    dxy = ((stack_of_dog[s][x+1][y+1] - stack_of_dog[s][x-1][y+1]) - (stack_of_dog[s][x+1][y-1] - stack_of_dog[s][x-1][y-1])) /4.
    dxs = ((stack_of_dog[s+1][x+1][y] - stack_of_dog[s+1][x-1][y]) - (stack_of_dog[s-1][x+1][y] - stack_of_dog[s-1][x-1][y])) /4.
    dys = ((stack_of_dog[s+1][x][y+1] - stack_of_dog[s+1][x][y-1]) - (stack_of_dog[s-1][x][y+1] - stack_of_dog[s-1][x][y-1])) /4.

    d_dx = np.asarray([dx, dy, ds])
    dd_dxx = np.asarray([
        [dxx, dxy, dxs],
        [dxy, dyy, dys],
        [dxs, dys, dss]
    ])

    X = np.asarray(candidate_keypoint) # + (-np.linalg.inv(dd_dxx)).dot(d_dx)

    D_of_x = stack_of_dog[s][x][y] + 0.5 * ((d_dx).dot(X)) 

    # Ratio pour la courbature
    traceH = dxx + dyy
    detH = dxx*dyy - dxy**2

    ratio = traceH**2 / detH 

    return abs(D_of_x), detH, ratio

                
def isExtremum(previous, current, nextDog, x, y):
    value = current[x][y]
    allBigger = True
    allSmaller = True

    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if i == x and j == y:
                continue
            
            if previous[i][j] >= value:
                allBigger = False
            elif previous[i][j] <= value:
                allSmaller = False

            if current[i][j] >= value and not (i == x and j == y):
                allBigger = False
            elif current[i][j] <= value and not (i == x and j == y):
                allSmaller = False

            if nextDog[i][j] >= value:
                allBigger = False
            elif nextDog[i][j] <= value:
                allSmaller = False

            if not allBigger and not allSmaller:
                return False 

    return True

