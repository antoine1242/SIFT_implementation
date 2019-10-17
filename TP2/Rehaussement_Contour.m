function [imageRehaussee] = Rehaussement_Contour(image, k)
    masqueGaussien = 1/16 * [1 2 1; 2 4 2; 1 2 1];
    Ig = Convolution(image, masqueGaussien);
    
    masqueLaplacien = [-1 -1 -1; -1 8 -1; -1 -1 -1];
    laplacien = Convolution(Ig, masqueLaplacien);
    %imshow(laplacien);
    
    imageRehaussee = Ig + k * laplacien;
    
    % Mettre les valeurs négatives à 0
    imageRehaussee(imageRehaussee < 0) = 0;
    
    imageRehaussee = uint8(imageRehaussee);
end