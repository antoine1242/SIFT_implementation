function [] = plotSpectreFrequence(nomFichier)

[Data,Fe] = audioread(nomFichier);

% Calcul taille des données audio recueillies
L = length(Data);
% Obtenir vecteur représentant la plage de fréquences du fichier audio
f = Fe*(0:(L/2))/L;
% Obtenir fft du signal audio
audio_fft = fft(Data);
% Seulement prendre les valeur positives + normaliser les données
all_data = abs(audio_fft/L);
% Sélectionner seulement la moitié des 
firt_half = all_data(1:L/2+1);
% Doubler amplitude des signaux de la première moitié puisque les signaux
% de la seconde moitié ont été groupé au signaux de la première partie.
firt_half(2:end-1) = 2*firt_half(2:end-1);

plot(f,firt_half) 
title(strcat({'TDF du signal '}, nomFichier));
xlabel('Fréquence')
ylabel('Intensité')
end

