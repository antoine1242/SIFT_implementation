function [] = subplot_frequence_echantillonnage(position, frequence, Y)
% Cette fonction ajoute un subplot à la figure regroupant les six 
% représentations de Y(t) avec différentes fréquences d'échantillonage  
    subplot(6,1,position);
    t = linspace(0, 1, frequence);
    plot(t, Y(t));
    ylim([-20, 20]);
    title(strcat({'Y en fonction de t pour une fréquence d''échantillonnage de '}, int2str(frequence), {' Hz'}));
    xlabel('t');
    ylabel('Y(t)');
end

