
from comparer_eig_vs_svd import comparer_eig_vs_svd

def run():
    print("Projet Pano is running - Comparer eig vs svd.")

    keypoints_matched1 = [(444.0, 766.0), (503.0, 749.0), (494.0, 619.0), (229.0, 638.0), (437.0, 760.0), (277.0, 810.0), (355.0, 818.0), (398.0, 924.0), (109.0, 988.0), (368.0, 908.0), (177.0, 749.0), (363.0, 624.0), (440.0, 645.0)]
    keypoints_matched2 = [(447.0, 164.0), (507.0, 147.0), (499.0, 15.0), (230.0, 32.0), (440.0, 157.0), (277.0, 207.0), (356.0, 216.0), (399.0, 323.0), (105.0, 386.0), (369.0, 307.0), (176.0, 144.0), (366.0, 19.0), (444.0, 41.0)]

    H_norm_svd_eig, H_flatten_eig, H_norm_svd_svd, H_flatten_svd = comparer_eig_vs_svd(keypoints_matched1, keypoints_matched2)

    print()
    print("H_flatten")
    print(H_norm_svd_eig)
    print(H_norm_svd_svd)

run()
