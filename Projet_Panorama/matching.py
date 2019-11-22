def match_neighbors(descriptors_image1, descriptors_image2):
    pass

def eucledian_distance(descriptor1, descriptor2):
    sum = 0.
    
    for i in range(2, 131):
        sum += (descriptor1[i] - descriptor2[i])**2

    return sum**(1/2)
