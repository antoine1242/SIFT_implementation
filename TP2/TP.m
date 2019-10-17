
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
horizontales = imread("Barres_Horizontales.png");
obliques = imread("Barres_Obliques.png");
imshow(verticales);
imshow(horizontales);
imshow(obliques);

%% 3.2.

% TODO revoir normaliser les valeurs?
% maillot_norm = maillot./max(max(max(maillot)));


fft2_verticales = fft2(verticales);
module_verticales = abs(fft2_verticales);
% size_verticales = size(verticales);
% module_verticales = module_verticales /
% size_verticales(1)*size_verticales(2);
shift_verticales = fftshift(module_verticales);
imshow(1 + log2(shift_verticales), []);


fft2_horizontales = fft2(horizontales);
module_horizontales = abs(fft2_verticales);
% size_horizontales = size(horizontales);
% module_horizontales = module_horizontales /
% size_horizontales(1)*size_horizontales(2);
shift_horizontales = fftshift(module_horizontales);
imshow(1 + log2(shift_horizontales), []);


fft2_obliques = fft2(obliques);
module_obliques = abs(fft2_obliques);
% size_obliques = size(obliques);
% module_obliques = module_obliques / size_obliques(1)*size_obliques(2);
shift_obliques = fftshift(module_obliques);
imshow(1 + log2(shift_obliques), []);


%% 3.3.

% TODO 
% 70 degré dans quel sens?
% 
verticales = imread("Barres_Verticales.png");
verticales_rotation70 = imrotate(verticales, 70, 'bilinear', 'crop');
imshow(verticales_rotation70)


fft2_verticales = fft2(verticales_rotation70);
module_verticales = abs(fft2_verticales);
% size_verticales = size(verticales);
% module_verticales = module_verticales /
% size_verticales(1)*size_verticales(2);
shift_verticales = fftshift(module_verticales);
imshow(1 + log2(shift_verticales), []);


%% 3.4.

% TODO revoir: pas certain des fft2 par rapport à la normalisation
% http://www.cs.toronto.edu/~jepson/csc320/notes/linearFilters2.pdf



%% Exercice 4: Filtrage spectral
close all;
clear all;
clc;

%% 4.1.
maillot = imread("maillot.png");
imshow(maillot);

fft2_maillot = fft2(maillot);
module_maillot = abs(fft2_maillot);
% size_maillot = size(maillot);
% module_maillot = module_maillot / % size_maillot(1)*size_maillot(2);
shift_maillot = fftshift(module_maillot);
imshow(1 + log2(shift_maillot), []);

%% 4.2.

% Manche côté gauche: diagonale pente positive??? pas suuposé être
% l'inverse?
% Manche côté droit: diagonale pente négative??? pas supposé être
% l'inverse?
% Collet: ?
% Pochette: Ligne horizontale??? pas supposé être verticale?
% Corps (ligne verticales): Ligne verticale??? pas supposé être
% horizontale?

%% TODO Question : Ne devrait pas redonner la même image?
maillot = imread("maillot.png");
H_times_F = fftshift(fft2(maillot));
maillot_img_with_filter = ifft2(ifftshift(H_times_F));
imshow(maillot_img_with_filter, []);


%% 4.3.
% Devons-nous utiliser TF^-1 pour afficher image ou imfilter(fft2_maillot,
% double(maillot))?

maillot = imread("maillot.png");
H = fspecial('gaussian', size(maillot), 60);
F = fftshift(fft2(double(maillot)));
low_pass_filtered_maillot = real(ifft2(ifftshift(H.*F)));
imshow(low_pass_filtered_maillot, []);


%% V2 4.4 
maillot = imread("maillot.png");
H = fspecial('gaussian', size(maillot), 300);
F = fftshift(fft2(double(maillot)));
low_pass_filtered_maillot = real(ifft2(ifftshift(H.*F)));

high_pass_filtered_maillot = double(maillot) - low_pass_filtered_maillot;
imshow(high_pass_filtered_maillot, []);

%% V1 4.4.

maillot = imread("maillot.png");
H = fspecial('gaussian', size(maillot), 300);
F = fftshift(fft2(double(maillot)));
low_pass_filtered_maillot = real(ifft2(ifftshift(H.*F)));

high_pass_filtered_maillot = double(maillot) - low_pass_filtered_maillot;
imshow(high_pass_filtered_maillot, []);

maillot = imread("maillot.png");
 
%% V2 4.4

maillot = imread("maillot.png");
gaussian_filter = fspecial('gaussian', size(H), 3)
I_filtered = maillot - imfilter( maillot, gaussian_filter); 
imshow(I_filtered, [])

%% V3 4.4 


% Transformée de Fourier centré de l'image
F = fftshift(fft2(maillot))
% Init filter
H = fspecial('gaussian', size(F), 3)
% Apply filter
% filtered_spectrum = filter2(gaussian_filter, img_spectrum) % same as H_times_F = H .* gaussian_filter;? 

% V1
%h1 = (1/9).*[1,1,1;1,1,1;1,1,1];
%filtered_spectrum = filter2(h1,img_spectrum);
filtered_spectrum = H .* F;
%filtered_spectrum = uint8(round(filtered_spectrum))
% Back to time domain
maillot_img_with_low_filter = ifft2(ifftshift(filtered_spectrum));
E = maillot_img_with_low_filter;
maillot_img_with_high_filter = double(maillot) - E;
imshow(maillot_img_with_high_filter, []);



%% 4.5.

%% 4.6.

%% 4.7.

%% 4.8.

%% 4.9.