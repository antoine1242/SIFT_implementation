
%% Exercice 1: Rehaussement d'images
close all;
clear all;
clc;

%% 1.1.
theArtist = imread("theArtist.png");

type Egalisation_Histogramme.m;

theArtistEgalisee = Egalisation_Histogramme(theArtist);
imshow(theArtistEgalisee);

%% 1.2.
type Convolution.m;

%% 1.3.
masqueGuassien = 1/90 * [1 2 1 2 1; 2 4 8 4 2; 1 8 18 8 1; 2 4 8 4 2; 1 2 1 2 1];

theArtistConvolue = Convolution(theArtist, masqueGuassien);
imshow(theArtistConvolue);

%% 1.4.

%% 1.5.

%% Exercice 2: Compteur de monnaie
close all;
clear all;
clc;

%% 2.1.

%% 2.2.

%% 2.3.

%% 2.4.

%% Exercice 3: Transformée de Fourier 2D
close all;
clear all;
clc;

%% 3.1.

%% 3.2.

%% 3.3.

%% 3.4.

%% Exercice 4: Filtrage spectral
close all;
clear all;
clc;

%% 4.1.

%% 4.2.

%% 4.3.

%% 4.4.

%% 4.5.

%% 4.6.

%% 4.7.

%% 4.8.

%% 4.9.