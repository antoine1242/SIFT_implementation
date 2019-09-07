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
ylabel('s(t)');
legend('s (Sinus cardinal)');

% R�ponse question: Le signal s est connu sous le nom de sinus cardinal.

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
ylabel('Signaux s1(t) s2(t) et s3(t)');
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

title('Superposition des signaux s1 s2 s3 ainsi que la somme de ces signaux en fonction de t');
xlabel('t');
ylabel('Signaux s1 s2 s3 et leur somme');
legend('s1', 's2', 's3', 'somme');

% 4.
close all;
clear all;
clc;

% Calcul de la fonction S50(t)
t = linspace(-2, 2, 500);
S50 = zeros(1, length(t));
for i=0:500
   k = 2*i + 1;
   h = sin(k*t) / k;
   S50 = (S50 + h);
end
S50 = 0.5 + (2/pi)* S50;

figure('Name', 'Approximation de la fonction �chelon');
plot(t, S50);
title('Approximation de la fonction �chelon');
xlabel('t');
ylabel('S50(t)');

% R�ponse question: Le signal S50(t) semble approximer la fonction �chelon.

%%
% Exercice 2: �chantillonnage
close all;
clear all;
clc;

% 1.
% Le signal Y(t) peut �tre d�compos� en trois signaux: 
Y_1 = @(t) 2*sin(165*pi*t);
Y_2 = @(t) 13*cos(6*pi*t);
Y_3 = @(t) -3*cos(80*pi*t); 

% � l'aide de s(t) = A * sin(w*t + phi) et f = w / 2pi on peut trouver
% trois fr�quences dans le signal Y(t):

% Y_1 -> 165pi / 2pi = 82.5 Hz
% Y_2 -> 6pi / 2pi = 3 Hz
% Y_3 -> 80pi / 2pi = 40 Hz

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
% Plus la fr�quence d'�chantillonnage est �lev�e, plus l'�chantillon �pouse
% le r�el signal.

% 4. 
% Le th�or�me de Nyquist-Shannon stipule que la fr�quence d'�chantillonnage
% doit �tre au moins �gale au double de la fr�quence maximale du signal
% analogique.
% Ici la fr�quence maximale du signal Y(t) est: 
% f_max = max(82.5, 3, 40) = 82.5 Hz
% R�ponse question: Donc les fr�quences 180 Hz et 330 Hz respectent la condition >= 2*82.5
% Hz.

% R�ponse question: Un compromis doit �tre fait entre la pr�cision du signal 
% reconstitu� et la quantit� de donn�es recueillies.
% En effet, si la fr�quence d'�chantillonage est �lev�e il sera
% possible d'�chantilloner des fr�quences �lev�es. De plus, la latence du 
% signal sera diminu�e. Cependant, si la fr�quence d'�chantillonage est
% �lev�e une plus grande quantit� de donn�es devra �tre recueillie afin 
% de repr�senter ce signal.

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
title('Signaux Y_1, Y_2, et Y_3 en fonction de t');
xlabel('t');
ylabel('Signaux Y_1, Y_2, et Y_3');
legend('Y_1', 'Y_2', 'Y_3');

% 2. 

% R�ponse question: 

% P�riode d�termin�e graphiquement:
% T_1_graph = 0,17671 - 0,076305 = 0,100405
% T_2_graph = 0,10442 - 0,064257 = 0,040163
% T_3_graph = 0,068273 - 0,048193 = 0,02008

% P�riode d�termin�e th�oriquement:
% � l'aide de f = w/2pi  et T = 1/f nous obtenons T = 2pi / w
% T_1_th�o = 2pi / (2pi*10) = 0,1
% T_2_th�o = 2pi / (2pi*25) = 0,04
% T_3_th�o = 2pi / (2pi*50) = 0,02

% Comparaison P�riode d�termin�e graphiquement vs P�riode d�termin�e
% th�oriquement:
% T_1_th�o_vs_graph = |0,1 - 0,100405| / 0,1 = 0.405% erreur
% T_2_th�o_vs_graph = |0,04 - 0,040163| / 0,04 = 0.4075% erreur
% T_3_th�o_vs_graph = |0,02 - 0,02008| / 0,02 = 0.4% erreur

% 3.
clf;

Z = @(t) Y_1(t) + Y_2(t) + Y_3(t);
plot(t, Z(t));
title('Somme des signaux Y1, Y2 et Y3 en fonction de t');
xlabel('t');
ylabel('Somme des signaux Y1, Y2 et Y3');
legend('Z');

% TODO revoir:
% R�ponse question:
% � l'aide de f = 1 / T o� T est : 
% T = 0,026908 - 0,068273 = 0,200807
% La fr�quence de Z(t) semble �tre de 1 / 0,200807 = 4,98 Hz


% 4. 
clf;
Y_1_fft = fft(Y_1(t));
bar(0:249, 2*abs(Y_1_fft)/length(Y_1_fft));
xlim([0 124])
title('Spectre de fr�quence de Y1');
ylabel('Intensit�');
xlabel('Fr�quence');

clf;
Y_2_fft = fft(Y_2(t));
bar(0:249, 2*abs(Y_2_fft)/length(Y_2_fft));
xlim([0 124])
title('Spectre de fr�quence de Y2');
ylabel('Intensit�');
xlabel('Fr�quence');

clf;
Y_3_fft = fft(Y_3(t));
bar(0:249, 2*abs(Y_3_fft)/length(Y_3_fft));
xlim([0 124])
title('Spectre de fr�quence de Y3');
ylabel('Intensit�');
xlabel('Fr�quence');

% TODO: Revoir
% R�ponse question:
% Le spectre de fr�quence de chacun des signaux pr�sente l'intensit� du
% signal en fonction de la fr�quence. Il nous est possible de constater que
% chaque spectre de fr�quence a une fr�quence pro�minente. Cette fr�quence
% pro�minente correspond bel et bien � la fr�quence th�orique de chacun des
% signaux. De plus, l'intensit� du signal repr�sent� dans chacun des 
% spectres de fr�quence correspond aussi � l'intensit� th�orique de chacun
% des signaux.

% 5. 
clf;
Z_fft = fft(Z(t));
bar(0:249, 2*abs(Z_fft)/length(Z_fft));
xlim([0 124])
title('Spectre de fr�quence de Z');
ylabel('Intensit�');
xlabel('Fr�quence');

% TODO: Revoir
% R�ponse question:
% Ce spectre de fr�quence pr�sente l'intensit� du  signal en fonction de la 
% fr�quence. Il nous est possible de constater qu'il y a trois fr�quences 
% pro�minentes. Ces fr�quences ainsi que leur intensit� correspondent aux 
% signaux Y_1(t), Y_2(t), et Y_3(t) qui composent le signal Z(t) analys�.
