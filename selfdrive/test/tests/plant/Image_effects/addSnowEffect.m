function Im_effect = addSnowEffect(Im, thickness)

if thickness > 0
    Im_effect = addFogEffect(Im, thickness);  % add hazzy effect
    snowEffect = uint8(zeros(size(Im,1), size(Im,2)));
    
    for i=1:thickness
        snow = uint8(zeros(size(Im,1), size(Im,2)));
        for j=1:250
            x = randi([1,size(snow,2)-2],1,1);
            y = randi([1,size(snow,1)-2],1,1);
            snow(y:y+1,x:x+1) = 255;
        end
        snowEffect = snowEffect + imgaussfilt(snow,0.5+(i/10));  % sigma 0.5~1.5
    end
    
    H = fspecial('motion',5,75);
    snowEffect = imfilter(snowEffect,H,'replicate');
    % figure;imshow(snowEffect)
    
    for i=1:3
        Im_effect(:,:,i) = Im_effect(:,:,i) + snowEffect;
    end
else
    Im_effect = Im;
end
