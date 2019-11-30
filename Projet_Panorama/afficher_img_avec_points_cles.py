import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arrow
import math 

def afficher_img_avec_points_cles(img, keypoints, has_angle):
    # Create a figure. Equal aspect so circles look circular
    fig,ax = plt.subplots(1)
    ax.set_aspect('equal')

    # Show the image
    ax.imshow(img)#, cmap=plt.cm.gray)

    # Now, loop through coord arrays, and create a circle at each x,y pair
    for keypoint in keypoints:
        x = keypoint[0]
        y = keypoint[1]
        
        if has_angle: 
            r = 5 * keypoint[2]
        else: 
            r = 10
        
        circ = Circle((y,x), r, fill=False)
        ax.add_patch(circ)
        
        if has_angle:
            
            angle = math.radians(keypoint[3])
            dx = r * np.cos(angle)
            dy = r * np.sin(angle)
            line = Arrow(y, x, dx, dy, width=2.0)
            ax.add_patch(line)        

    # Show the image
    plt.show()