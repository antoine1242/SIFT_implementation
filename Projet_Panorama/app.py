from skimage.io import imread
from obtenir_panorama import obtenir_panorama

def run():
    print("Project Pano is running!")
    
    # Importer Images
    img_color1 = imread("./images/gauche.jpg")
    img_color2 = imread("./images/droite.jpg")

    # Obtenir panorama à partir des images
    panorama = obtenir_panorama(img_color1, img_color2)

run()
