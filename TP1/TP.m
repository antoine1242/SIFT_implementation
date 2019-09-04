%%
% Exercice 1: Signaux simples
close all;
clear all;
clc;

% 1.

s = @(t) sin(pi*t) ./ (pi*t);

t = linspace(-4, 4, 1000);

plot(t, s(t));
title('Sinus cardinal en fonction de t');
xlabel('t');
ylabel('Sinus cardinal');
legend('Sinus cardinal');

% Le signal s est connu sous le nom de sinus cardinal.

% 2. 
close all;
clear all;
clc;

s1 = @(t) sin(t);
s2 = @(t) sin(3*t) / 3;
s3 = @(t) sin(5*t) / 5;

t = linspace(-2, 2, 500);

hold on;
plot(t, s1(t))
plot(t, s2(t))
plot(t, s3(t))

title('Superposition des signaux s1 s2 et s3 en fonction de t');
xlabel('t');
ylabel('Signaux s1 s2 et s3');
legend('s1', 's2', 's3');

% 3. 
close all;
clear all;
clc;

s1 = @(t) sin(t);
s2 = @(t) sin(3*t) / 3;
s3 = @(t) sin(5*t) / 5;
somme = @(t) s1(t) + s2(t) + s3(t);

t = linspace(-2, 2, 500);

hold on;
plot(t, s1(t), '--')
plot(t, s2(t), '--')
plot(t, s3(t), '--')
plot(t, somme(t), 'LineWidth', 2)

title('Superposition des signaux s1 s2 s3 et la somme de ces signaux en fonction de t');
xlabel('t');
ylabel('Signaux s1 s2 s3 et s4');
legend('s1', 's2', 's3', 'somme');

% 4.
close all;
clear all;
clc;

t = linspace(-2, 2, 500);
s50 = zeros(1, length(t));
for i=0:500
   k = 2*i + 1;
   h = sin(k*t) / k;
   s50 = (s50 + h);
end
s50 = 0.5 + (2/pi)* s50;

figure('Name', 'Approximation de la fonction échelon');
plot(t, s50);
title('Approximation de la fonction échelon');
xlabel('x');
ylabel('s');

%%
% Exercice 2: Échantillonnage
close all;
clear all;
clc;

% 1.
% Le signal Y(t) peut être décomposé en trois signaux: 
Y_1 = @(t) 2*sin(165*pi*t);
Y_2 = @(t) 13*cos(6*pi*t);
Y_3 = @(t) -3*cos(80*pi*t); 

% À l'aide de s(t) = A * sin(w*t + phi) et f = w / 2pi on peut trouver
% trois fréquences dans le signal Y(t):

% Y_1 -> 82.5 Hz
% Y_2 -> 3 Hz
% Y_3 -> 40 Hz

% 2. 
Y = @(t) Y_1(t) + Y_2(t) + Y_3(t);

figure('pos', [10,10,600,900]);

type subplot_frequence_echantillonnage.m;

subplot_frequence_echantillonnage(1, 20, Y);
subplot_frequence_echantillonnage(2, 75, Y);
subplot_frequence_echantillonnage(3, 100, Y);
subplot_frequence_echantillonnage(4, 160, Y);
subplot_frequence_echantillonnage(5, 180, Y);
subplot_frequence_echantillonnage(6, 330, Y);

% 3. 
% Plus la fréquence d'échantillonnage est élevée, plus l'échantillon épouse
% le réel signal.

% 4. 
% Le théorème de Nyquist-Shannon stipule que la fréquence d'échantillonnage
% doit être au moins égale au double de la fréquence maximale du signal
% analogique.
% Ici la fréquence max du signal Y est: 
% f_max = max(82.5, 3, 40) = 82.5 Hz
% Donc les fréquences 180 Hz et 330 Hz respectent la condition >= 2* 82.5
% Hz.
% Un compromis doit être fait entre la performance (rapadité d'analyse du 
% signal et espace de stockage) et la précision du signal reconstitué. 


%% Exercice 3: Analyse spectrale
close all;
clear all;
clc;

% 1. 
Fe = 250;
Y_1 = @(t) 7*sin(2*pi*10*t);
Y_2 = @(t) 4*sin(2*pi*25*t + pi/3);
Y_3 = @(t) 3*cos(2*pi*50*t);

t = linspace(0, 1, Fe);
hold on;
plot(t, Y_1(t));
plot(t, Y_2(t));
plot(t, Y_3(t));
title('Signaux sinusoïdaux en fonction de t');
xlabel('t');
ylabel('Signaux sinusoïdaux');
legend('Y_1', 'Y_2', 'Y_3');

% 2. 

% Période déterminée graphiquement:
% T_1_graph = 0,17671 - 0,076305 = 0,100405
% T_2_graph = 0,10442 - 0,064257 = 0,040163
% T_3_graph = 0,068273 - 0,048193 = 0,02008

% Période déterminée théoriquement:
% À l'aide de f = w/2pi  et T = 1/f nous obtenons T = 2pi / w
% T_1_théo = 2pi / (2pi*10) = 0,1
% T_2_théo = 2pi / (2pi*25) = 0,04
% T_3_théo = 2pi / (2pi*50) = 0,02

% Comparaison Période déterminée graphiquement vs Période déterminée
% théoriquement:
% T_1_théo_vs_graph = |0,1 - 0,100405| / 0,1 = 0.405% erreur
% T_2_théo_vs_graph = |0,04 - 0,040163| / 0,04 = 0.4075% erreur
% T_3_théo_vs_graph = |0,02 - 0,02008| / 0,02 = 0.4% erreur

% 3.
clf;

Z = @(t) Y_1(t) + Y_2(t) + Y_3(t);
plot(t, Z(t));
title('Somme des signaux Y1, Y2 et Y3 en fonction de t');
xlabel('t');
ylabel('Somme des signaux Y1, Y2 et Y3');
legend('Z');

% À l'aide de f = 1 / T où T est : 
% T = 0,026908 - 0,068273 = 0,200807
% La fréquence de Z(t) semble être de 1 / 0,200807 = 4,98 Hz

clf;
Y_1_fft = fft(Y_1(t));
bar(0:249, 2*abs(Y_1_fft)/length(Y_1_fft));
xlim([0 124])
title('Spectre de fréquence de Y1');
ylabel('Intensité');
xlabel('Fréquence');

clf;
Y_2_fft = fft(Y_2(t));
bar(0:249, 2*abs(Y_2_fft)/length(Y_2_fft));
xlim([0 124])
title('Spectre de fréquence de Y2');
ylabel('Intensité');
xlabel('Fréquence');

clf;
Y_3_fft = fft(Y_3(t));
bar(0:249, 2*abs(Y_3_fft)/length(Y_3_fft));
xlim([0 124])
title('Spectre de fréquence de Y3');
ylabel('Intensité');
xlabel('Fréquence');


clf;
Z_fft = fft(Z(t));
bar(0:249, 2*abs(Z_fft)/length(Z_fft));
xlim([0 124])
title('Spectre de fréquence de Z');
ylabel('Intensité');
xlabel('Fréquence');
