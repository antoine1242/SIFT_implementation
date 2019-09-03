function [ out ] = extraireCanal( input, canal)
%EXTRAIRECANAL extrait un canal d'une image
%   Retourne une image où tous les canaux, sauf celui spécifié sont nuls.
    
    % Création d'une matrice nulle similaire à input
    out = uint8(zeros(size(input)));
    
    % Copie du canal désiré de input dans out
    out(:, :, canal) = input(:, :, canal);
    
    % out sera automatiquement retourner par extraireCanal.
end