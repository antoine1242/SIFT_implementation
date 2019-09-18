function [] = subplot_frequence_echantillonnage(position, frequence, Y)
% Cette fonction ajoute un subplot � la figure regroupant les six 
% repr�sentations de Y(t) avec diff�rentes fr�quences d'�chantillonage  
    subplot(6,1,position);
    t = linspace(0, 1, frequence);
    plot(t, Y(t));
    ylim([-20, 20]);
    title(strcat({'Y en fonction de t pour une fr�quence d''�chantillonnage de '}, int2str(frequence), {' Hz'}));
    xlabel('t');
    ylabel('Y(t)');
end

