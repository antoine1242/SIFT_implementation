function [imageBinarisee] = Binariser(image, seuil)
    [rows, cols] = size(image);
    imageBinarisee = zeros(rows, cols);
    
    for row = 1:rows
        for col = 1:cols
            if image(row, col) >= seuil
               imageBinarisee(row, col) = 255; 
            else
                imageBinarisee(row, col) = 0;
            end
        end
    end
end