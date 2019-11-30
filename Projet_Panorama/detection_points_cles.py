import numpy as np
import matplotlib.pyplot as plt
from gaussian_filter import gaussian_filter
# TODO: resolution_octave ajuster position keypoint dans l'image selon la résolution de l'image à l'octave donnée.

def detection_points_cles(dog, sigma, seuil_contraste, r_courbure_principale, resolution_octave, gaussian_filtered_images, gaussian_filtered_images_sigmas):
    print("Detection des points cles")
    
    # Initialisation des constantes
    NB_BINS = 10
    BIN_SIZE = 360 // NB_BINS

    # Initialisation des compteurs
    cnt_candidates_curr = 0
    cnt_candidates_octave = []
    cnt_removed_contrast = 0
    cnt_removed_edge = 0

    ##### 1. Trouver points clés #####

    keypoints = []

    # Parcourir les différences de gaussiennes (DoG) exceptés la première et la dernière
    # afin de pouvoir trouver les points clés candidats extremums des DoG centrales.
    for i in range(1, len(dog)-1):
        previous = dog[i-1]
        current = dog[i]
        next_ = dog[i+1]
        candidate_keypoints = []

        # Sélection des points clés candidats
        for x in range(1, len(previous)-1):
            for y in range(1, len(previous[0])-1):
                if is_extremum(previous, current, next_, x, y):
                    candidate_keypoints.append((x,y,sigma[i]))
                    cnt_candidates_curr += 1
        
        # Élimination de certains point clés candidats
        for candidate_keypoint in candidate_keypoints:
            stack_of_dog = np.asarray([previous, current, next_])

            # Obtenir informations nécessaires à partir des Différences de Gaussiennes
            D_of_x, detH, ratio = dog_derivative(stack_of_dog, candidate_keypoint) 

            # Élimination des points-clés de faible contraste avec D(x)
            if D_of_x < seuil_contraste:
                cnt_removed_contrast += 1

            # Élimination des points situés sur les arêtes 
            elif detH < 0 or ratio > (r_courbure_principale + 1)**2 / r_courbure_principale:
                cnt_removed_edge += 1

            # Si le point clé candidat respecte l'ensemble des restrictions on l'ajoute aux points clés 
            else:
                keypoints.append(candidate_keypoint)

        cnt_candidates_octave.append(cnt_candidates_curr)
        cnt_candidates_curr = 0

    cnt_candidates = sum(cnt_candidates_octave)

    print("Extremas détectés: ", cnt_candidates)
    print("Points faible contraste éliminés: ", cnt_removed_contrast)
    print("Points d'arêtes éliminés: ", cnt_removed_edge)


    # TODO: Important REVOIR: Je ne pense pas qu'il faut faire cela
    # check_val = set()
    # keypoints_filtered = []
    # for x, y, s in keypoints:
    #     if (x, y) not in check_val:
    #         keypoints_filtered.append((x, y, s))

    keypoints_filtered = keypoints


    ##### 2. Trouver orientation des points clés #####

    keypoints_m_and_theta = []
    for keypoint in keypoints_filtered:
        x_kp = keypoint[0]
        y_kp = keypoint[1]
        sigma = keypoint[2]
        circular_gaussian_window = gaussian_filter(1.5 * sigma)

        # On pause une zone autour du point clé qui dépend du sigma de celui-ci
        range_zone = int(2*np.ceil(sigma) + 1)

        # Obtenir l'image filtrée L pour un sigma donné 
        idx = gaussian_filtered_images_sigmas.index(sigma)
        L = gaussian_filtered_images[idx]
        
        # Initialisation d'un histogramme avec NB_BINS bins
        hist = np.zeros(NB_BINS, dtype=np.float32)

        for dx_zone in range(-range_zone, range_zone + 1):
            for dy_zone in range(-range_zone, range_zone + 1):
                x = x_kp + dx_zone
                y = y_kp + dy_zone

                # Ne pas considérer point lorsqu'à l'extérieur de l'image
                if x < 0 or x > L.shape[0] - 1 or y < 0 or y > L.shape[1] - 1: 
                    continue

                # Évaluer dérivées dx et dy à partir de l'image L et de la position du point clé
                dx = L[min(L.shape[0]-1, x+1)][y] - L[max(x-1, 0)][y]
                dy = L[x][min(L.shape[1]-1, y+1)] - L[x][max(y-1, 0)]
                
                # Évaluer magnitude et orientation du gradiant du point clé
                m = np.sqrt(dx**2 + dy**2)
                theta = (np.arctan2(dy, dx)) * 180/np.pi
                
                # Obtenir poids pondéré de la magnitude tu point clé à partir d'une fenêtre gaussienne
                weight = circular_gaussian_window[dx_zone + range_zone][dy_zone + range_zone] * m

                # Obtenir le bin correspondant à l'orientation theta 
                bin_number = int(np.floor(theta) // BIN_SIZE)

                # Ajouter poids au bin correspondant dans l'histogramme
                hist[bin_number] += weight

        # Trouver à quel orientation fait partie le point clé
        max_bin = np.argmax(hist)

        # Trouver angle exacte theta par interpolation avec la fonction find_angle() et ajouter le point clé à keypoints_m_and_theta
        keypoints_m_and_theta.append((keypoint[0], keypoint[1], keypoint[2], find_angle(hist, max_bin, BIN_SIZE)))

        max_val = np.max(hist)
        for bin_index, m in enumerate(hist):
            if bin_index == max_bin: 
                continue

            if m >= .8 * max_val:
                keypoints_m_and_theta.append((keypoint[0], keypoint[1], keypoint[2], find_angle(hist, bin_index, BIN_SIZE)))

    return np.array(keypoints_m_and_theta)


# Permet de trouver angle theta par interpolation d'histogramme
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

    return -b / (2 * a)



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


# Permet de détecter si le point à la position x, y dans l'image est un extremum.
def is_extremum(previous, current, next_, x, y):
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

            if next_[i][j] >= value:
                allBigger = False
            elif next_[i][j] <= value:
                allSmaller = False

            if not allBigger and not allSmaller:
                return False 

    return True

