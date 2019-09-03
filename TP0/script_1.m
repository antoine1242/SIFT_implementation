%% Nettoyage du workspace
clear all;
close all;
clc;
%% Exercice I
% Initialisation des variables
load lab0_data.mat;
mozzarella = mozzarella';
mozzarella(2) = 9.7;
annee = 2000:2009;

hold on;

yyaxis left;
plot(annee, mozzarella);
ylim([9, 11.1]);
xlabel('annee'); 
ylabel('mozzarella');

yyaxis right;
scatter(annee, doctorats);
ylim([400, 800]);
title('doctorats in function of annee');

% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% %
%%  Exercice II: G�n�rer et tracer des signaux
close all;
clear all;


s0 = @(x) sin(x);
s1 = @(x) sin(3 * x) / 3;
s2 = @(x) sin(5 * x) / 5;
s3 = @(x) s0(x) + s1(x) + s2(x);

x = linspace(0, 4*pi, 500);

hold on;

plot(x, s0(x), '--')
plot(x, s1(x), '--')
plot(x, s2(x), '--')
plot(x, s3(x), 'LineWidth', 2);

title('Multiple signals in function of x');
xlabel('Interval between 0 and 4pi');
ylabel('Sinusoidal Signals');
legend('s0', 's1', 's2');
grid on;

s4 = @(x) 0
for k=1:2:2001
    s4 = @(x) sin(k*x) / k + s4(x)
end

plot(x, s4(x))

%%  Exercice III: Images, Fonctions et Histogrammes
clear all; close all; clc;

% Lecture et affichage de l'image
image = imread('chat.png');
%imshow(image);

valeurMin = min(image(:));
valeurMax = max(image(:));

disp('-- Image de chat --');
disp(['min: ', num2str(valeurMin)]);
disp(['max: ', num2str(valeurMax)]);

% Affichage des dimensions de l'image (peut �tre fait simplement en console)
dimensions = size(image);
disp(['dimensions: ', num2str(dimensions)]);

%%
% Affichage du canal bleu
imshow(image(:,:,3));

%%
% Affichage de tous les canaux en couleurs
figure('pos', [10,10,900,300]);
subplot(1,3,1);
imshow(extraireCanal(image, 1));
title('Canal Rouge');

subplot(1,3,2);
imshow(extraireCanal(image, 2));
title('Canal Vert');

subplot(1,3,3);
imshow(extraireCanal(image, 3));
title('Canal Bleu');

%%
% Calcul et affichage de l'histogramme bleu (peut �tre fait en console)
figure();
histogramme_bleu = imhist(image(:,:,3));
bar(0:255, histogramme_bleu);
title('Histogramme du canal bleu');
ylabel('Fr�quence');
xlabel('Intensit� de couleur');

%%
% Affichage de tous les canaux en couleurs et de leurs histogrammes
figure('Name', 'Histogrammes', 'pos', [10,10,900,600])

subplot(2,3,1)
tracerHistogramme(image, 1);
subplot(2,3,4)
imshow(extraireCanal(image, 1));
title('Canal rouge');

subplot(2,3,2)
tracerHistogramme(image, 2);
subplot(2,3,5)
imshow(extraireCanal(image, 2));
title('Canal vert');

subplot(2,3,3)
tracerHistogramme(image, 3);
subplot(2,3,6)
imshow(extraireCanal(image, 3));
title('Canal bleu');


%%  Exercice IV: Images binaires, calcul matriciel, convolution et jeu de la vie
close all; clear all; clc;
load lab0_data.mat;

% Affichage de la carte
imagesc(carte);
colorbar;
title('Carte d''initialisation du jeu de la vie');

% L'�quation matricielle en fonction de E et N peut s'�crire:
% (N == 3) + (E .* N == 4)

%%
% D�finition de N en utilisant une convolution
N = @(map) conv2(map, ones(3,3), 'same');

% V�rification de N sur carteG
subplot(1,2,1);
imagesc(carteG);
title('carteG');

subplot(1,2,2);
imagesc(N(carteG));
colorbar;
title('N(carteG)');

%%
% LE JEU DE LA VIE
E = carte;

fenetreJeu = figure('Name', 'Jeu de la vie');

while( ishghandle(fenetreJeu) )
    imagesc(E);
    E = (N(E) == 3) + (E.*N(E) == 4);
    pause(0.01);
end

