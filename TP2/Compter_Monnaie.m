function [total] = Compter_Monnaie(image)
    nbStructures = 0;

    esBouchon= strel('disk', 200, 4);
    imageBouchon = imerode(image, esBouchon);
    bouchons = bwconncomp(imageBouchon);
    nbBouchons = bouchons.NumObjects - nbStructures;
    nbStructures = nbStructures + nbBouchons;
    
    es2Dollar = strel('disk', 140, 4);
    image2Dollars = imerode(image, es2Dollar);
    dollars = bwconncomp(image2Dollars);
    nb2Dollars = dollars.NumObjects - nbStructures;
    nbStructures = nbStructures + nb2Dollars;
    
    es25Cents = strel('disk', 120, 4);
    image25Cents = imerode(image, es25Cents);
    vingCincCents = bwconncomp(image25Cents);
    nb25Cents = vingCincCents.NumObjects - nbStructures;
    nbStructures = nbStructures + nb25Cents;
    
    es5Cents = strel('disk', 110, 4);
    image5Cents = imerode(image, es5Cents);
    cincCents = bwconncomp(image5Cents);
    nb5Cents = cincCents.NumObjects - nbStructures;
    nbStructures = nbStructures + nb5Cents;
    
    es10Cents = strel('disk', 90, 4);
    image10Cents = imerode(image, es10Cents);
    dixCents = bwconncomp(image10Cents);
    nb10Cents = dixCents.NumObjects - nbStructures;
    nbStructures = nbStructures + nb10Cents;
    
    total = 2 * nb2Dollars + 0.25 * nb25Cents + 0.10 * nb10Cents + 0.05 * nb5Cents;
end