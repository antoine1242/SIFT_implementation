function [imageEgalisee] = Egalisation_Histogramme(image)
    histogramme = zeros(1,256);
    [rows, cols] = size(image);
    
    for row = 1:rows
        for col = 1:cols
            index = image(row, col) + 1;
            disp(index);
            histogramme(index) = histogramme(index) + 1;
        end
    end
    %bar(histogramme);
    histogramme_cumulatif = zeros(1,256);
    somme = 0;
    
    for i = 1:256
       somme = somme + histogramme(i);
       histogramme_cumulatif(i) = somme;
    end
    
    imageEgalisee = zeros(rows, cols);
    pixels = rows * cols;
    
    for row = 1:rows
        for col = 1:cols
            index = image(row, col) + 1;
            value = histogramme_cumulatif(index);
            odds = value/pixels;
            newValue = round(255 * odds);
            imageEgalisee(row, col) = newValue;
        end
    end
    
    imageEgalisee = uint8(imageEgalisee);
    %{
    histogramme = zeros(1,256);
    
    for row = 1:rows
        for col = 1:cols
            index = imageEgalisee(row, col) + 1;
            disp(index);
            histogramme(index) = histogramme(index) + 1;
        end
    end
    bar(histogramme);
    %}
    
end