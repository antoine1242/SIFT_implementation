import pandas as pd
from difference_de_gaussiennes import difference_de_gaussiennes
import cv2





def run():
    print("Project Pano is running!")
    img = cv2.imread("./images/lena_claire.jpg", cv2.IMREAD_COLOR)
    print(type(img))
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    
run()