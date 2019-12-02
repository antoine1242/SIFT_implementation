import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arrow
import math 

def afficher_img_avec_points_cles(img, keypoints_octaves, has_angle):


    # Create a figure. Equal aspect so circles look circular
    fig,ax = plt.subplots(1)
    ax.set_aspect('equal')

    # Show the image
    ax.imshow(img)#, cmap=plt.cm.gray)

    for idx, keypoints in enumerate(keypoints_octaves):
        # Now, loop through coord arrays, and create a circle at each x,y pair
        color_tag = plt.cm.RdYlBu(idx/(len(keypoints_octaves) - 1))
        add_keypoints(keypoints, ax, color_tag, has_angle)

    # Show the image
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