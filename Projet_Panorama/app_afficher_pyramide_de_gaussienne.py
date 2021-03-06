import cv2
import matplotlib.pyplot as plt
from difference_de_gaussiennes import difference_de_gaussiennes

def run():
    print("Projet Pano is running Afficher pyramide de gaussienne.")
    
    img = cv2.imread("./images/lena.png", cv2.IMREAD_COLOR).astype("float32")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    dogs, sigmas, gaussian_filtered_images, gaussian_filtered_images_sigmas = difference_de_gaussiennes(img, s=3, nb_octave=3)

    octave = 2

    fig = plt.figure(figsize=(12,8))
    for i in range(1, 6+1):
        axi = fig.add_subplot(2, 3, i)
        axi.title.set_text(str(gaussian_filtered_images_sigmas[octave][i-1]))
        plt.imshow(gaussian_filtered_images[octave][i-1], cmap=plt.cm.gray)
    plt.savefig("./images_rapport/lena_pyramide_de_gaussiennes_octave_" + str(octave + 1) + ".png")
    plt.show()

    fig = plt.figure(figsize=(12,8))
    for i in range(1, 6):
        fig.add_subplot(2, 3, i)
        plt.imshow(dogs[octave][i-1], cmap=plt.cm.gray)
    plt.savefig("./images_rapport/lena_difference_de_gaussiennes_octave_" + str(octave + 1) + ".png")
    plt.show()


run()
