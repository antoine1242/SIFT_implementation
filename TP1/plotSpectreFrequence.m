function [] = plotSpectreFrequence(nomFichier)

[Data,Fe] = audioread(nomFichier);

% Calcul taille des donn�es audio recueillies
L = length(Data);
% Obtenir vecteur repr�sentant la plage de fr�quences du fichier audio
f = Fe*(0:(L/2))/L;
% Obtenir fft du signal audio
audio_fft = fft(Data);
% Seulement prendre les valeur positives + normaliser les donn�es
all_data = abs(audio_fft/L);
% S�lectionner seulement la moiti� des 
firt_half = all_data(1:L/2+1);
% Doubler amplitude des signaux de la premi�re moiti� puisque les signaux
% de la seconde moiti� ont �t� group� au signaux de la premi�re partie.
firt_half(2:end-1) = 2*firt_half(2:end-1);

plot(f,firt_half) 
title(strcat({'TDF du signal '}, nomFichier));
xlabel('Fr�quence')
ylabel('Intensit�')
end

