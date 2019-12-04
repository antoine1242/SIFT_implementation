import matplotlib.pyplot as plt
from afficher_img_avec_points_cles import add_keypoints
from afficher_img_avec_points_cles import afficher_img_avec_points_cles

def afficher_images_avec_point_cles_matched(img_color1, img_color2, keypoints_matched1, keypoints_matched2):
    fig, ax = plt.subplots(1, 2)

    ax[0].imshow(img_color1)
    ax[1].imshow(img_color2)

    for idx, kps_matched1 in enumerate(keypoints_matched1):
        color_tag = plt.cm.RdYlBu(idx/(len(keypoints_matched1) - 1))

        add_keypoints([kps_matched1], ax[0], color_tag, False)
        add_keypoints([keypoints_matched2[idx]], ax[1], color_tag, False)

    # Show the image
    plt.show()
