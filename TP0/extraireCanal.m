function [ out ] = extraireCanal( input, canal)
%EXTRAIRECANAL extrait un canal d'une image
%   Retourne une image o� tous les canaux, sauf celui sp�cifi� sont nuls.
    
    % Cr�ation d'une matrice nulle similaire � input
    out = uint8(zeros(size(input)));
    
    % Copie du canal d�sir� de input dans out
    out(:, :, canal) = input(:, :, canal);
    
    % out sera automatiquement retourner par extraireCanal.
end