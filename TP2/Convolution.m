function [imageConvoluee] = Convolution(image, masque)
    masque = rot90(masque, 2);
    sizeMasque = size(masque);
    
    moitieMasque = floor(sizeMasque(1)/2);
    sommeMasque = sum(masque,'all');
    
    image = padarray(image, [floor(sizeMasque(1)/2), floor(sizeMasque(2)/2)], 0, 'both');
    
    [rows, cols] = size(image);
    imageConvoluee = zeros(rows, cols);
    
    for row=1+floor(sizeMasque(1)/2):rows-floor(sizeMasque(1)/2)
        for col=1+floor(sizeMasque(2)/2):cols-floor(sizeMasque(2)/2)
            sousMatrice = image(row-moitieMasque:row+moitieMasque, col-moitieMasque:col+moitieMasque);
            [rowsSM, colsSM] = size(sousMatrice);
            somme = 0;
            
            for i=1:rowsSM
                for j=1:colsSM
                    somme = somme + (masque(i,j) * sousMatrice(i,j));
                end
            end
            
            imageConvoluee(row, col) = round(somme/sommeMasque);
        end
    end
    
    imageConvoluee = imageConvoluee(floor(sizeMasque(1)/2)+1:rows-floor(sizeMasque(1)/2),floor(sizeMasque(1)/2)+1:cols-floor(sizeMasque(1)/2)); 
    imageConvoluee = uint8(imageConvoluee);
end