function [] = tracerHistogramme( image, canal )
%TRACEHISTOGRAMME Trace l'histogramme d'un canal d'une image

    % Calcul de l'histogramme
    histogramme = imhist(image(:, :, canal));
    histogramme = histogramme / sum(histogramme);

    % Choix de la couleur et du nom
    if(canal == 1)
        nom = 'rouge';
        couleur = 'r';
    elseif(canal == 2)
        nom = 'vert';
        couleur = 'g';
    else
        nom = 'bleu';
        couleur = 'b';
    end

    % Tracer de l'histogramme dans la bonne couleur
    bar(0:255, histogramme, couleur);
    xlim([0,255]);
    ylim([0,1]);
    xlabel('Intensité de couleur');
    ylabel('Fréquence');
    title(['Histogramme du canal ', nom]);
    
end

