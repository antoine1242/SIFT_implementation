import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arrow
import math 

def afficher_img_avec_points_cles(img, keypoints_octaves, has_angle, name_file=""):
    fig,ax = plt.subplots(1)
    ax.set_aspect('equal')

    ax.imshow(img)  # cmap=plt.cm.gray pour affichage en gris

    for idx, keypoints in enumerate(keypoints_octaves):
        if len(keypoints_octaves) > 1:
            tag = idx/(len(keypoints_octaves) - 1)
        else:
            tag = idx
        color_tag = plt.cm.RdYlBu(tag)
        add_keypoints(keypoints, ax, color_tag, has_angle)

    if name_file != "":
        plt.savefig("./images_rapport/" + str(name_file) + ".png")
        
    plt.show()



def add_keypoints(keypoints, ax, color_tag, has_angle):
    R_INIT = 5
    for keypoint in keypoints:
        x = keypoint[0]
        y = keypoint[1]

        if has_angle: 
            r = R_INIT * keypoint[2]
        else: 
            r = R_INIT * 3
        
        circ = Circle((y,x), r, color=color_tag, fill=False)
        ax.add_patch(circ)
        
        if has_angle:            
            angle = math.radians(keypoint[3])
            dx = r * np.cos(angle)
            dy = r * np.sin(angle)
            line = Arrow(y, x, dx, dy, width=2.0)
            ax.add_patch(line)    

    return ax    