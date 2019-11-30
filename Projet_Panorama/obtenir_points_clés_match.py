def obtenir_points_clés_match(k_lowest, keypoints1, keypoints2):
    keypoints_matched1 = []
    keypoints_matched2 = []

    for k in range(len(k_lowest)):
        idx_image1 = k_lowest[k][1]
        idx_image2 = k_lowest[k][2]
        
        keypoints_matched1.append((keypoints1[idx_image1][0], keypoints1[idx_image1][1]))
        keypoints_matched2.append((keypoints2[idx_image2][0], keypoints2[idx_image2][1]))

    # Réjection des points clés matched de même coordonnée
    coordinates_set = set()
    kept_indexes = []
    for i in range(len(keypoints_matched1)):    
        point = (keypoints_matched1[i][0], keypoints_matched1[i][1])    
        if point not in coordinates_set:
            kept_indexes.append(i)
            coordinates_set.add(point)

    keypoints_no_duplicates1 = []
    keypoints_no_duplicates2 = []

    for i in range(len(kept_indexes)):
        keypoints_no_duplicates1.append(keypoints_matched1[kept_indexes[i]])
        keypoints_no_duplicates2.append(keypoints_matched2[kept_indexes[i]])

    return keypoints_matched1, keypoints_matched2