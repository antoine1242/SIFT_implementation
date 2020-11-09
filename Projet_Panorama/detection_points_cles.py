import numpy as np
import matplotlib.pyplot as plt
from gaussian_filter import gaussian_filter
from scipy.ndimage.filters import convolve
# TODO: resolution_octave ajuster position keypoint dans l'image selon la résolution de l'image à l'octave donnée.

def detection_points_cles(dog, sigma, seuil_contraste, r_courbure_principale, resolution_octave, gaussian_filtered_images, gaussian_filtered_images_sigmas):
    print("Detection des points cles - Octave " + str(resolution_octave + 1))
    
    # Initialisation des constantes
    NB_BINS = 10
    BIN_SIZE = 360 // NB_BINS

    # Initialisation des compteurs
    cnt_removed_extrema = 0
    cnt_removed_edge = 0
    cnt_removed_constrast = 0

    ##### 1. Trouver points clés #####

    keypoints = []

    gx_kernel = np.array([[0., 1., 0.],
                          [0., 0., 0.],
                          [0., -1., 0.],])

    gy_kernel = np.array([[0., 0., 0.],
                          [1., 0., -1.],
                          [0., 0., 0.],])

    #  dxx = (current[s][x+1][y] - 2*current[s][x][y] + current[s][x-1][y]) 
    gxx_kernel = np.array([[0., 1., 0.],
                           [0., -2., 0.],
                           [0., 1., 0.],])

    gyy_kernel = np.array([[0., 0., 0.],
                           [1., -2., 1.],
                           [0., 0., 0.],])

    # ((current[s][x+1][y+1] - current[s][x-1][y+1]) - (current[s][x+1][y-1] - current[s][x-1][y-1])) /4.
    gxy_kernel = np.array([[1., 0., -1.],
                           [0., 0., 0.],
                           [-1., 0., 1.],])


    # Parcourir les différences de gaussiennes (DoG) exceptés la première et la dernière
    # afin de pouvoir trouver les points clés candidats extremums des DoG centrales.
    for i in range(1, len(dog)-1):
        previous = dog[i-1]
        current = dog[i]
        next_ = dog[i+1]
        candidate_keypoints = []
       
        dx_matrix = 0.5 * convolve(current, gx_kernel)
        dy_matrix = 0.5 * convolve(current, gy_kernel)

        dxx_matrix = convolve(current, gxx_kernel)
        dyy_matrix = convolve(current, gyy_kernel)
        dxy_matrix = 0.25 * convolve(current, gxy_kernel)

        sigma_val = sigma[i]

        # Obtenir points-clés ca
        candidate_keypoints = []

        for x in range(len(current)):
            for y in range(len(current[0])):
                candidate_keypoint = (x, y, sigma_val)

                # Calculs pour D_of_x
                dx = dx_matrix[x][y]
                dy = dy_matrix[x][y]
                ds = 0.5 * (next_[x][y] - previous[x][y])

                d_dx = np.array([dx, dy, ds])   
                
                X = np.array(candidate_keypoint)

                D_of_x = current[x][y] + 0.5 * (d_dx.dot(X))

                # Si D_of_x plus grand que seuil de contraste on considère le point
                if abs(D_of_x) >= seuil_contraste:                     
                    # Calculs pour detH & ratio
                    dxx = dxx_matrix[x][y]
                    dyy = dyy_matrix[x][y]
                    dxy = dxy_matrix[x][y]

                    traceH = dxx + dyy
                    detH = dxx*dyy - dxy**2
                    ratio = traceH**2 / detH 
                    
                    # Si point n'est pas situé sur arête on l'ajoute aux points clés candidats
                    if detH >= 0 and ratio <= (r_courbure_principale + 1)**2 / r_courbure_principale:
                        candidate_keypoints.append(candidate_keypoint)
                    else:
                        cnt_removed_edge += 1
                else:
                    cnt_removed_constrast += 1

        cnt_removed_extrema = 0

        for candidate_keypoint in candidate_keypoints:
            x = candidate_keypoint[0]
            y = candidate_keypoint[1]

            # Si coordonnée est à l'extérieur de l'image ou sur le contour on ne la considère pas
            if x <= 0 or x >= current.shape[0] - 1 or y <= 0 or y >= current.shape[1] - 1: 
                continue

            if is_extremum(previous, current, next_, x, y):                
                keypoints.append(candidate_keypoint)
            else: 
                cnt_removed_extrema += 1

    print("Total de points faible contraste elimines: ", cnt_removed_constrast)
    print("Total de points d'arêtes elimines: ", cnt_removed_edge)
    print("Total de points non extremas elimines: ", cnt_removed_extrema)
    print("Total de points-cles trouves: ", len(keypoints))

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
                dx = 0.5 * (L[min(L.shape[0]-1, x+1)][y] - L[max(x-1, 0)][y])
                dy = 0.5 * (L[x][min(L.shape[1]-1, y+1)] - L[x][max(y-1, 0)])
                
                # Évaluer magnitude et orientation du gradiant du point clé
                m = np.sqrt(dx**2 + dy**2)
                theta = (np.arctan2(dy, dx)) * 180/np.pi
                
                # Obtenir poids pondéré de la magnitude tu point clé à partir d'une fenêtre gaussienne
                x_pos_in_window = dx_zone + range_zone
                y_pos_in_window = dy_zone + range_zone
                x_pos_in_gaussian_window = int((len(circular_gaussian_window) * x_pos_in_window) // (2*range_zone + 1))
                y_pos_in_gaussian_window = int((len(circular_gaussian_window) * y_pos_in_window) // (2*range_zone + 1))
                weight = circular_gaussian_window[x_pos_in_gaussian_window][y_pos_in_gaussian_window] * m

                # Obtenir le bin correspondant à l'orientation theta 
                bin_number = int(np.floor(theta) // BIN_SIZE)

                # Ajouter poids au bin correspondant dans l'histogramme
                hist[bin_number] += weight

        # Trouver à quel orientation fait partie le point clé
        max_bin = np.argmax(hist)

        # Trouver angle exact theta par interpolation avec la fonction find_angle() et ajouter le point clé à keypoints_m_and_theta
        keypoints_m_and_theta.append((keypoint[0], keypoint[1], keypoint[2], find_angle(hist, max_bin, BIN_SIZE)))

        max_val = np.max(hist)
        for bin_index, m in enumerate(hist):
            if bin_index == max_bin: 
                continue

            if m >= .8 * max_val:
                keypoints_m_and_theta.append((keypoint[0], keypoint[1], keypoint[2], find_angle(hist, bin_index, BIN_SIZE)))

    print("Total de points cles apres l'ajout de l'angle:", len(keypoints_m_and_theta))

    # Ajuster les coordonnées du point sur l'image d'origine selon la résolution de l'octave
    adjusted_keypoints = []
    for keypoint in keypoints_m_and_theta:
        adjusted_keypoints.append((keypoint[0]*(2**resolution_octave), keypoint[1]*(2**resolution_octave), keypoint[2], keypoint[3]))

    return np.array(adjusted_keypoints)


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

    return allBigger or allSmaller
