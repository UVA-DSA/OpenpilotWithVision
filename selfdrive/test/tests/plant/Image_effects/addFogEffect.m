function Im_effect = addFogEffect(Im, thickness)

if thickness > 0
    Im_effect = uint8(zeros(size(Im,1), size(Im,2),3));
    hazyEffect = uint8(zeros(size(Im,1), size(Im,2)));
    
    haze_level = 15000*thickness;
    % hazyEffect = randi([0,255],size(Im,1), size(Im,2));    % sigma * rand(size(Im,1), size(Im,2));
    haze = randi([0,255], 1, haze_level);
    for i=1:haze_level
        x = randi([1,size(Im_effect,2)],1,1);
        y = randi([1,size(Im_effect,1)],1,1);
        hazyEffect(y,x) = haze(i);
    end
    
    hazyEffect = imgaussfilt(hazyEffect,7.0);  % sigma 5 ~7
    % figure;imshow(hazyEffect)
    
    % Im = imgaussfilt(Im,0.1);  % sigma 0.5~1.5
    gain = 0.9 - (0.05 * thickness);
    Im = imadjust(Im,[0,1],[0,gain]);  % gain 0.4 ~0.9
    
    for i=1:3
        Im_effect(:,:,i) = Im(:,:,i) + hazyEffect;
    end
else
    Im_effect = Im;
end
