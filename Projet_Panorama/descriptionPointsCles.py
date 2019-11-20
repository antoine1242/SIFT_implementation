import numpy as np
from detectionPointsCles import gaussian_filter

def descriptionPointsCles(keypoints, gaussian_filtered_images, gaussian_filtered_images_sigmas):
    keypoints_descriptor = []
    
    
    for keypoint in keypoints:
        x_kp = keypoint[0]
        y_kp = keypoint[1]
        sigma = keypoint[2]
        # TODO : v/rifier 
        circular_gaussian_window = gaussian_filter(16 / 6) # multiplies sigma by 3



        idx = gaussian_filtered_images_sigmas.index(sigma)
        L = gaussian_filtered_images[idx]

        range_zone = 8
        
        gradients_matrix = np.zeros((range_zone*2, range_zone*2))
       
        keypoint_descriptor = []

        for dx_zone in range(-range_zone, range_zone):
            for dy_zone in range(-range_zone, range_zone):
                x = x_kp + dx_zone
                y = y_kp + dy_zone

                if x < 0 or x > L.shape[0] - 1 or y < 0 or y > L.shape[1] - 1: 
                    continue

                dx = L[min(L.shape[0]-1, x+1)][y] - L[max(x-1, 0)][y]
                dy = L[x][min(L.shape[1]-1, y+1)] - L[x][max(y-1, 0)]
                m = np.sqrt(dx**2 + dy**2)
                theta = (np.arctan2(dy, dx)) * 180/np.pi
                
                gradients_matrix[dx_zone + range_zone][dy_zone + range_zone] = (m, theta)

        nb_bins = 8
        for i in range(0, 16, 4):
            for j in range(0, 16, 4):
                hist = np.zeros(nb_bins, dtype=np.float32)
                for k in range(i, i + 4):
                    for m in range(j, j + 4):
                        mag = gradients_matrix[k][m]
                        theta = gradients_matrix[k][m]
                
                        weight = circular_gaussian_window[dx_zone + range_zone][dy_zone + range_zone] * mag
                        bin_number = int(np.floor(theta) // (360 // nb_bins))
                        hist[bin_number] += weight
                        # TODO revoir si c<est cela qu<il faut append, ajouter normalisation etc.
                        keypoint_descriptor.extend(hist)


    
                
  


        # circular_gaussian_window = gaussian_filter(1.5 * sigma)
        idx = gaussian_filtered_images_sigmas.index(sigma)
        L = gaussian_filtered_images[idx]
        
     


  