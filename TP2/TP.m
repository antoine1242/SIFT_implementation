
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
type Rehaussement_Contour.m

theArtist = imread("theArtist.png");
theArtistRehaussee = Rehaussement_Contour(theArtist, 1/12);
imshow(theArtistRehaussee);

%% 1.5.

% Les contours de l'image rehauss�e sont ressortis. Cela est d� au fait que
% le filtre Laplacien conserve les contours, soient les transitions de
% couleur de pixels. En additionnant les contours, ou dans notre cas une
% fraction de ceux-ci, on fait ressortir les contours de l'image originale.

% Un filtre m�dian adaptatif pourrait �tre utilis� pour enlever le bruit.

%% Exercice 2: Compteur de monnaie
close all;
clear all;
clc;

%% 2.1.

%% 2.2.

%% 2.3.

%% 2.4.

%% Exercice 3: Transform�e de Fourier 2D
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