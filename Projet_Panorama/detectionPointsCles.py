import numpy as np
import matplotlib.pyplot as plt

# TODO: resolution_octave ajuster position keypoint dans l,image selon la résolution de l'image à l'octave donnée.

def detectionPointsCles(dog, sigma, seuil_contraste, r_courbure_principale, resolution_octave, gaussian_filtered_images, gaussian_filtered_images_sigmas):
    print("Detection des points cles")

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
        y_kp = keypoint[1]
        sigma = keypoint[2]
        circular_gaussian_window = gaussian_filter(1.5 * sigma)

        range_zone = int(2*np.ceil(sigma) + 1)

        # TODO: Comment trouver le bon L
        # TODO: Comment trouver le nombre de pixels a observer autour

        idx = gaussian_filtered_images_sigmas.index(sigma)
        L = gaussian_filtered_images[idx]
        
        hist = np.zeros(nb_bins, dtype=np.float32)

        for dx_zone in range(-range_zone, range_zone + 1):
            for dy_zone in range(-range_zone, range_zone + 1):
                x = x_kp + dx_zone
                y = y_kp + dy_zone

                # Quoi faire pour les dérivées sur les côtés?
                if x < 0 or x > L.shape[0] - 1 or y < 0 or y > L.shape[1] - 1: 
                    continue

                dx = L[min(L.shape[0]-1, x+1)][y] - L[max(x-1, 0)][y]
                dy = L[x][min(L.shape[1]-1, y+1)] - L[x][max(y-1, 0)]
                m = np.sqrt(dx**2 + dy**2)
                #theta = (np.arctan(dy/dx)+np.pi) * 180/np.pi
                theta = (np.arctan2(dy, dx)) * 180/np.pi
                
                weight = circular_gaussian_window[dx_zone + range_zone][dy_zone + range_zone] * m

                bin_number = int(np.floor(theta) // bin_size)
                hist[bin_number] += weight

        max_bin = np.argmax(hist)
        keypoints_m_and_theta.append((keypoint[0], keypoint[1], keypoint[2], find_angle(hist, max_bin, bin_size)))

        max_val = np.max(hist)
        for bin_index, m in enumerate(hist):
            if bin_index == max_bin: 
                continue

            if m >= .8 * max_val:
                keypoints_m_and_theta.append((keypoint[0], keypoint[1], keypoint[2], find_angle(hist, bin_index, bin_size)))

    return np.array(keypoints_m_and_theta)



def find_angle(hist, max_bin, bin_size):
    bin_number = len(hist)

    center_x = max_bin * bin_size + bin_size / 2
    rigth_x = center_x + bin_size
    left_x = center_x - bin_size

    center_y = hist[max_bin]
    rigth_y = hist[(max_bin+1) % bin_number]
    left_y = hist[(max_bin+1) % bin_number]

    x_coordinates = np.array([[center_x**2, center_x, 1],
                             [left_x**2, left_x, 1],
                             [rigth_x**2, rigth_x, 1]])
    y_coordinates = np.array([center_y, left_y, rigth_y])

    result = np.linalg.lstsq(x_coordinates, y_coordinates, rcond=None)[0]
    a = result[0]
    b = result[1]

    if a == 0: 
        a = 1e-6
    #print(-b/(2*a))

    return -b/(2*a)





        #   est-ce qu'on compute toute la matrice des m et tetha avant?
        # mag_theta_matrix = np.zeros(L.shape)
        # for x in range(mag_theta_matrix.shape[0]):
        #     for x in range(mag_theta_matrix.shape[1]):
        #         dx = L[x+1][y] - L[x-1][y]
        #         dy = L[x][y+1] - L[x][y-1]
        #         m = np.sqrt(dx**2 + dy**2)
        #         theta = (np.arctan(dy/dx)+np.pi) * 180/np.pi
        #         mag_theta_matrix[x][y] = (m, theta)



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

# https://stackoverflow.com/questions/29731726/how-to-calculate-a-gaussian-kernel-matrix-efficiently-in-numpy
def gaussian_filter(sigma):
    length = 2 * np.ceil(3*sigma) + 1

    ax = np.linspace(-(length - 1) / 2, (length - 1) / 2, length)
    xx, yy = np.meshgrid(ax, ax)

    kernel = np.exp(-0.5 * (np.square(xx) + np.square(yy)) / np.square(sigma))

    return kernel / np.sum(kernel)
