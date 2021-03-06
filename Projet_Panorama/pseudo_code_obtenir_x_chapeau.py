
def obtenir_x_chapeau(stack_of_dog, candidate_keypoint)
    # stack_of_dog contient la différence de gaussienne 
    # précédente, courante et prochaine aux index 0, 1, 2 
    # respectivement.
    # stack_of_dog[0]: contient différence de gaussienne précédente
    # stack_of_dog[1]: contient différence de gaussienne courante
    # stack_of_dog[2]: contient différence de gaussienne prochaine

    x = candidate_keypoint[0]
    y = candidate_keypoint[1]

    s = 1
    dx = (stack_of_dog[s][x+1][y] - stack_of_dog[s][x-1][y]) / 2.
    dy = (stack_of_dog[s][x][y+1] - stack_of_dog[s][x][y-1]) / 2.
    ds = (stack_of_dog[s+1][x][y] - stack_of_dog[s-1][x][y]) / 2.

    dxx = (stack_of_dog[s][x+1][y] - 2*stack_of_dog[s][x][y] + stack_of_dog[s][x-1][y]) 
    dyy = (stack_of_dog[s][x][y+1] - 2*stack_of_dog[s][x][y] + stack_of_dog[s][x][y-1]) 
    dss = (stack_of_dog[s+1][x][y] - 2*stack_of_dog[s][x][y] + stack_of_dog[s-1][x][y]) 

    dxy = ((stack_of_dog[s][x+1][y+1] - stack_of_dog[s][x-1][y+1]) - (stack_of_dog[s][x+1][y-1] - stack_of_dog[s][x-1][y-1])) /4.
    dxs = ((stack_of_dog[s+1][x+1][y] - stack_of_dog[s+1][x-1][y]) - (stack_of_dog[s-1][x+1][y] - stack_of_dog[s-1][x-1][y])) /4.
    dys = ((stack_of_dog[s+1][x][y+1] - stack_of_dog[s+1][x][y-1]) - (stack_of_dog[s-1][x][y+1] - stack_of_dog[s-1][x][y-1])) /4.

    d_dx = np.asarray([dx, dy, ds])

    dd_dxx = np.asarray([
        [dxx, dxy, dxs],
        [dxy, dyy, dys],
        [dxs, dys, dss]
    ])

    x_chapeau = -np.linalg.inv(dd_dxx).dot(d_dx)

    return x_chapeau

