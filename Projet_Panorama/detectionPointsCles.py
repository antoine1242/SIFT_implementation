import numpy as np

def detectionPointsCles(dog, sigma, seuil_contraste, r_courbure_principale, resolution_octave, gaussian_filtered_images, gaussian_filtered_images_sigmas):
    print("detectionPointsCles")
    cnt_candidates_curr = 0
    cnt_candidates_octave = []
    cnt_removed_contrast = 0
    cnt_removed_edge = 0
    keypoints = []

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
        x = keypoint[0]
        y = keypoint[1]
        sigma = keypoint[2]
        
        w = int(2*np.ceil(sigma) + 1)

        # s = np.clip(s, 0, octave.shape[2] - 1) ???
        # TODO: 
        #kernel = gaussian_filter(image_initiale_norm, sigma=sigma) 

        # TODO: Comment trouver le bon L
        # TODO: Comment trouver le nombre de pixels a observer autour
        idx = gaussian_filtered_images_sigmas.index(sigma)
        L = gaussian_filtered_images[idx]
        m = ((L[x+1][y] - L[x-1][y])**2 + (L[x][y+1] - L[x][y-1])**2)**(1/2)
        theta = np.arctan((L[x][y+1] - L[x][y-1])/(L[x+1][y] - L[x-1][y]))
        keypoints_m_and_theta.append((x, y, sigma, m, theta))

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

