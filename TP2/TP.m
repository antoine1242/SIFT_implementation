
%% Exercice 1: Rehaussement d'images
close all;
clear all;
clc;

%% 1.1.
% Image originale:
theArtist = imread("theArtist.png");
imshow(theArtist);

%%
% Fonction Egalisation_Histogramme.m:
type Egalisation_Histogramme.m;

%%
% Image avec �galisation:
theArtistEgalisee = Egalisation_Histogramme(theArtist);
imshow(theArtistEgalisee);

%% 1.2.
% Fonction Convolution.m:
type Convolution.m;

%% 1.3.
masqueGuassien = 1/90 * [1 2 1 2 1; 2 4 8 4 2; 1 8 18 8 1; 2 4 8 4 2; 1 2 1 2 1];

theArtistConvolue = Convolution(theArtistEgalisee, masqueGuassien);
imshow(theArtistConvolue);

%% 1.4.
%%
% Fonction Rehaussement_Contour.m:
type Rehaussement_Contour.m

%%
theArtistRehaussee = Rehaussement_Contour(theArtistConvolue, 1/15);
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
pieces = imread("pieces.jpg");
pieces = rgb2gray(pieces);

imshow(pieces);

%% 2.2.

%%
% Voici le d�tail de la fonction Binariser.m
type Binariser.m;

%%
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
%%
% Voici le d�tail de la fonction Compter_Monnaie.m
type Compter_Monnaie.m;

%%
total = Compter_Monnaie(piecesFermee);

%%
% Voici le total calcul� par la fonction Compter_Monnaie.m en $:
disp(total);


%% Exercice 3: Transform�e de Fourier 2D
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
% Voici le spectre de l'image: Barres_Verticales
fft2_verticales = fft2(verticales);
module_verticales = abs(fft2_verticales);
module_verticales = module_verticales / length(module_verticales);
shift_verticales = fftshift(module_verticales);
imshow(log10(1 + shift_verticales), []);

%%
% Voici le spectre de l'image: Barres_Horizontales
fft2_horizontales = fft2(horizontales);
module_horizontales = abs(fft2_horizontales);
module_horizontales = module_horizontales / length(module_horizontales);
shift_horizontales = fftshift(module_horizontales);
imshow(log10(1 + shift_horizontales), []);

%%
% Voici le spectre de l'image: Barres_Obliques
fft2_obliques = fft2(obliques);
module_obliques = abs(fft2_obliques);
module_obliques = module_obliques / length(module_obliques);
shift_obliques = fftshift(module_obliques);
imshow(log10(1 + shift_obliques), []);


%% 3.3.
verticales = imread("Barres_Verticales.png");
verticales_rotation70 = imrotate(verticales, 70, 'bilinear', 'crop');
imshow(verticales_rotation70)

%%
fft2_verticales = fft2(verticales_rotation70);
module_verticales = abs(fft2_verticales);
module_verticales = module_verticales / length(module_verticales);
shift_verticales = fftshift(module_verticales);
imshow(log10(1 + shift_verticales), []);


%% 3.4.

% TODO revoir: pas certain des fft2 par rapport � la normalisation
% http://www.cs.toronto.edu/~jepson/csc320/notes/linearFilters2.pdf
% https://www.eee.hku.hk/~work8501/WWW2008/ho4.pdf

% Il est possible d'inf�rer qu'une transform�e de Fourier 2D respecte les
% propri�t�es suivantes:
% 1. Sym�trie: La transform�e de Fourier est clairement sym�trique.
% 2. Rotation: Il est possible de voir qu'une rotation d'une image d'un
% angle x implique que sa transform�e de fourier subit une rotation d'un 
% angle x elle aussi.
% 3. Shift/Translation?
% transform�e de Fourier est �galement tourn�e d'un m�me angle.


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

%% 4.2.

% Voici notre r�ponse textuelle. Voir le sch�ma ci-dessous pour plus de
% d�tails.

% Manche c�t� gauche (avec moins de lignes): diagonale pente n�gative principale
% Manche c�t� droit (avec beaucoup de lignes): diagonale pente positive principale
% Col: Voir ci-dessous
% Pochette: Ligne centrale verticale
% Torse: ligne centrale horizontale

%%
spectre_identifie = imread("spectre_identifie.png");
imshow(spectre_identifie);

%%
% D�tail pour l'identification du spectre du col:

% Premi�rement, nous avons isol� le col:
col = imread("col.png");
col = rgb2gray(col);
imshow(col);

%%
% D�tail pour l'identification du spectre du col:

% Deuxi�mement, nous avons calcul son spectre:
fft2_col = fft2(col);
norm_col = fft2_col / length(fft2_col);
module_col = abs(norm_col);
shift_col = fftshift(module_col);
imshow(log10(1 + shift_col), []);

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
H = imread("filter4_5_7.png");
H = rgb2gray(H);
H = double(H)/255;

%%
% Voici le filtre id�al que avons cr�� et utilis� pour conserver uniquement 
% la texture des deux manches.
imshow(H);

%%
% Voici le r�sultat final:
F = fftshift(fft2(maillot));
low_pass_filtered_maillot = real(ifft2(ifftshift(H.*F)));
imshow(low_pass_filtered_maillot);

%% 4.6.

maillot = imread("maillot.png");
maillot = double(maillot)/255;
H = imread("filter4_6.png");
H = rgb2gray(H);
H = double(H)/255;

%%
% Voici le filtre id�al que avons cr�� et utilis� pour faire disparaitre 
% la texture du torse.
imshow(H);

%%
% Voici le r�sultat final:
F = fftshift(fft2(maillot));
low_pass_filtered_maillot = real(ifft2(ifftshift(H.*F)));
imshow(low_pass_filtered_maillot);

%% 4.7.

% Un filtre id�al est un filtre passe-bas. De plus,
% le masque spatial de convolution d'un filtre id�al   
% contient des ondulations. Lorsqu'on applique un filtre sur une image ces
% ondulations causent des cercles d'artefacts sur l'image finale.

% Le filtre Butterworth est aussi un filtre passe-bas. Par contre, 
% les ondulations qui peuvent se trouver dans son masque spatial de 
% convolution son grandement att�nu�es puisque la transistion entre le cercle
% central blanc et le noir l'entourant est beaucoup plus lisse que dans un  
% filtre id�al. Cela permet par le m�me fait de significativement diminuer
% le nombre d'artefacts dans l'image finale. Par contre, il est important de 
% noter que lorsque l'ordre du filtre Butterworth augmente celui-ci se   
% rapproche d'un filtre id�al et donc il y aura apparition d'art�facts.

%% 4.8.

% La fr�quence 0 correspond � la fr�quence moyenne du spectre. En enlevant
% cette valeur on se retrouve donc � la soustraire de toutes les autres
% fr�quences. Cette soustraction correspond � une translation de l'ensemble
% du spectre de fr�quences vers 0. Il est donc possible d'affirmer que l'image
% r�sultante sera plus "noire" que l'image originale ou �gale.


%% 4.9.

% Puisque les composantes du maillot apparaissent en ordre d�croissant de
% fr�quence (alternance entre lignes blanches et noires rapide) nous avons donc
% besoin d'un filtre passe haut qui laisse passer de plus en plus de basses
% fr�quences.
% Il est possible de produire ce comportement � l'aide d'un filtre id�al
% passe haut avec initialement une grande fr�quence de coupure  (donc un cercle noir 
% centr� avec un grand rayon). Ensuite, diminuer la fr�quence de coupure 
% petit � petit jusqu'� ce que celle-ci soit 0 et donc aucune fr�quence 
% ne sera coup�e ce qui permettra d'obtenir la couleur moyenne de l'image. 



