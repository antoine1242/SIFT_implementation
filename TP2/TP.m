
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

theArtistConvolue = Convolution(theArtistEgalisee, masqueGuassien);
imshow(theArtistConvolue);

%% 1.4.
type Rehaussement_Contour.m

theArtistRehaussee = Rehaussement_Contour(theArtistConvolue, 1/15);
imshow(theArtistRehaussee);

%% 1.5.

% TODO: Revoir

% Les contours de l'image rehaussée sont ressortis. Cela est dû au fait que
% le filtre Laplacien conserve les contours, soient les transitions de
% couleur de pixels. En additionnant les contours, ou dans notre cas une
% fraction de ceux-ci, on fait ressortir les contours de l'image originale.

% Un filtre médian adaptatif pourrait être utilisé pour enlever le bruit.

%% Exercice 2: Compteur de monnaie
close all;
clear all;
clc;

%% 2.1.
pieces = imread("pieces.jpg");
pieces = rgb2gray(pieces);

imshow(pieces);

%% 2.2.
type Binariser.m

piecesBinarisee = Binariser(pieces, 250);
piecesBinarisee(piecesBinarisee==0) = 1 ;
piecesBinarisee(piecesBinarisee==255) = 0 ;
piecesBinarisee(piecesBinarisee==1) = 255 ;

imshow(piecesBinarisee);

%% 2.3.

elementStructurant = strel('disk', 10, 4);
piecesFermee = imclose(piecesBinarisee, elementStructurant);

imshow(piecesFermee);

%% 2.4.
type Compter_Monnaie.m
total = Compter_Monnaie(piecesFermee);

disp(total)


%% Exercice 3: Transformée de Fourier 2D
close all;
clear all;
clc;

%% 3.1.
verticales = imread("Barres_Verticales.png");
imshow(verticales);

%%
horizontales = imread("Barres_Horizontales.png");
imshow(horizontales);

%%
obliques = imread("Barres_Obliques.png");
imshow(obliques);

%% 3.2.

% TODO revoir normaliser les valeurs?

fft2_verticales = fft2(verticales);
module_verticales = abs(fft2_verticales);
module_verticales = module_verticales / length(module_verticales);
shift_verticales = fftshift(module_verticales);
imshow(1 + log10(shift_verticales), []);

%%
fft2_horizontales = fft2(horizontales);
module_horizontales = abs(fft2_horizontales);
module_horizontales = module_horizontales / length(module_horizontales);
shift_horizontales = fftshift(module_horizontales);
imshow(1 + log10(shift_horizontales), []);

%%
fft2_obliques = fft2(obliques);
module_obliques = abs(fft2_obliques);
module_obliques = module_obliques / length(module_obliques)
shift_obliques = fftshift(module_obliques);
imshow(1 + log10(shift_obliques), []);


%% 3.3.

verticales = imread("Barres_Verticales.png");
verticales_rotation70 = imrotate(verticales, 70, 'bilinear', 'crop');
imshow(verticales_rotation70)

%%
fft2_verticales = fft2(verticales_rotation70);
module_verticales = abs(fft2_verticales);
module_verticales = module_verticales / length(module_verticales);
shift_verticales = fftshift(module_verticales);
imshow(1 + log10(shift_verticales), []);


%% 3.4.

% TODO revoir: pas certain des fft2 par rapport à la normalisation
% http://www.cs.toronto.edu/~jepson/csc320/notes/linearFilters2.pdf

% Symétrie et translation

%% Exercice 4: Filtrage spectral
close all;
clear all;
clc;

%% 4.1.
maillot = imread("maillot.png");
fft2_maillot = fft2(maillot);
norm_maillot = fft2_maillot / length(fft2_maillot);
module_maillot = abs(norm_maillot);
shift_maillot = fftshift(module_maillot);
imshow(log10(1 + shift_maillot), []);

%%
maillot = imread("maillot_2.png");
maillot = rgb2gray(maillot);

fft2_maillot = fft2(maillot);
norm_maillot = fft2_maillot / length(fft2_maillot);
module_maillot = abs(norm_maillot);
shift_maillot = fftshift(module_maillot);
imshow(log10(1 + shift_maillot), []);

%% 4.2.

% Manche côté gauche (avec moins de lignes): diagonale pente négative principale
% Manche côté droit (avec beaucoup de lignes): diagonale pente positive principale
% Col: ?
% Pochette: Ligne centrale verticale
% Torse: ligne centrale horizontale


%% 4.3.
maillot = imread("maillot.png");
maillot = double(maillot)/255;

H = fspecial('gaussian', size(maillot), 60);
H = H./max(H(:));
F = fftshift(fft2(maillot));
low_pass_filtered_maillot = real(ifft2(ifftshift(H.*F)));
imshow(low_pass_filtered_maillot);

%% 4.4 
maillot = imread("maillot.png");
maillot = double(maillot)/255;

H = fspecial('gaussian', size(maillot), 60);
F = fftshift(fft2(maillot));
H = H./max(H(:));
low_pass_filtered_maillot = real(ifft2(ifftshift(H.*F)));

high_pass_filtered_maillot = maillot - low_pass_filtered_maillot;
imshow(high_pass_filtered_maillot);
 

%% 4.5.

maillot = imread("maillot.png");
maillot = double(maillot)/255;

H = imread("filter4_5.png");
H = rgb2gray(H);
H = double(H)/255;

F = fftshift(fft2(maillot));
low_pass_filtered_maillot = real(ifft2(ifftshift(H.*F)));

imshow(low_pass_filtered_maillot);

%% 4.6.

maillot = imread("maillot.png");
maillot = double(maillot)/255;

H = imread("filter4_6.png");
H = rgb2gray(H);
H = double(H)/255;

F = fftshift(fft2(maillot));
low_pass_filtered_maillot = real(ifft2(ifftshift(H.*F)));

high_pass_filtered_maillot = maillot - low_pass_filtered_maillot;
imshow(low_pass_filtered_maillot);

%% 4.7.

% Un filtre idéal est un filte passe-bas. Son masque spatial de convolution 
% contient des ondulations. Ces ondulations causent des cercles 
% d'artefacts. Le filtre Butterworth est aussi un filtre
% passe-bas, mais il diminue les ondulations ce qui permet de diminuer le
% nombre d'artefact.

%% 4.8.

% La fréquence 0 correspond à la fréquence moyenne du spectre. En enlevant
% cette valeur on se retrouve donc à la soustraire de toutes les autres
% fréquences. Cette soustraction correspond à une translation de l'ensemble
% du spectre de fréquences. Il est donc possible d'affirmer que l'image
% résultante sera plus sombre que l'image originale.


%% 4.9.

% Puisque les composantes du maillot apparaissent en ordre décroissant de
% fréquence (séquence de ligne blanche noire plus blanc) nous avons donc
% besoin d'un filtre passe haut qui devient de plus en plus petit (en
% diminuant la fréquence de coupure).
% On peut le voir comme un disque noir qui diminue.
% 