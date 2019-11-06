import pandas as pd
from difference_de_gaussiennes import differenceDeGaussiennes
import cv2

def run():
    print("Project Pano is running!")
    img = cv2.imread("./images/lena_claire.jpg", cv2.IMREAD_COLOR)
    print(type(img))
    cv2.imshow('image',img)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()


    
run()