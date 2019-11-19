def detectionPointsCles(dog, sigma, seuil_contraste=0.03, r_courbure_principale, resolution_octave):
    candidate_keypoint = []
    print(len(sigma))
    for i in range(1, len(dog)-1):
        previous = dog[i-1]
        current = dog[i]
        nextDog = dog[i+1]

        for x in range(1, len(previous)-1):
            for y in range(1, len(previous[0])-1):
                if isExtremum(previous, current, nextDog, x,y):
                    candidate_keypoint.append((x,y,sigma[i]))

    extremaDetectes = len(candidate_keypoint) 
    


    #for aTuple in candidate_keypoint:
    #    print(aTuple)

def dogDerivative(previous, current, nextDog, x, y, sigma):
    xDerivative = (current[x+1][y] - current[x-1][y]) / 2
    yDerivative = (current[x][y+1] - current[x][y-1]) / 2
    # C tu ça
    sigmaDerivative = (nextDog[x][y] - previous[x][y]) / 2

    derivative = [xDerivative, yDerivative, sigmaDerivative]
    

                
def isExtremum(previous, current, nextDog, x, y):
    value = current[x][y]
    allBigger = True
    allSmaller = True

    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if i == x and j == y:
                continue
            
            if previous[i][j] >= value:
                allBigger = False
            elif previous[i][j] <= value:
                allSmaller = False

            if current[i][j] >= value and not (i == x and j == y):
                allBigger = False
            elif current[i][j] <= value and not (i == x and j == y):
                allSmaller = False

            if nextDog[i][j] >= value:
                allBigger = False
            elif nextDog[i][j] <= value:
                allSmaller = False

            if not allBigger and not allSmaller:
                return False 

    return True
