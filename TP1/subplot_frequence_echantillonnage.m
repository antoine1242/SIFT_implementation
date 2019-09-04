function [] = subplot_frequence_echantillonnage(position, frequence, Y)
%SUBPLOT_FREQUENCE_ECHANTILLONNAGE Summary of this function goes here
%   Detailed explanation goes here
    subplot(6,1,position);
    t = linspace(0, 1, frequence);
    plot(t, Y(t));
    ylim([-20, 20]);
    title(strcat({'T en fonction de t pour une fréquence d''échantillonnage de '}, int2str(frequence), {' Hz'}));
    xlabel('t');
    ylabel('Y');
    legend('Y');
end

