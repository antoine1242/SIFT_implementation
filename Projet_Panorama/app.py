import pandas as pd
import numpy as np
from difference_de_gaussiennes import difference_de_gaussiennes
from detectionPointsCles import detectionPointsCles, isExtremum
import cv2

def run():
    print("Project Pano is running!")
    
    img = cv2.imread("./images/lena_claire.jpg", cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    """
    print(type(img))
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """
    dogs, sigmas, gaussian_filtered_images, gaussian_filtered_images_sigmas = difference_de_gaussiennes(img, 3, 2)

    print("DETECTION DE POINTS CLES")
    #detectionPointsCles(dogs[0], sigmas[0], 0, 0, 0)

    """
    previous = np.array([[9, 9, 9], [9, 9, 9], [9, 9, 9]])
    current = np.array([[9, 9, 9], [9, 8, 9], [9, 9, 9]])
    suivant = np.array([[9, 9, 9], [9, 9, 9], [9, 9, 9]])

    print(isExtremum(previous, current, suivant, 1, 1))
    """
run()
