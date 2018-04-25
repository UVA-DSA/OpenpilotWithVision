clc; clear; close all;

effect = 'occlusion';  % rain/fog/snow/occlusion
imdir = 'sample_images/';

for i=10:10%20
    imfile = [imdir 'f' num2str(i-1,'%05.f') '.png'];
    Im = imread(imfile);
    Im = imcrop(Im,[75,75,449,299]);
%     Im_effect = Im;
    figure;imshow(Im)

    if strcmp(effect,'rain')
        thickness = 10;   % 0~10
        angle = 15;
        effect_dir = 'sample_rain_streaks/';
        Im_effect = addRainEffect(Im, effect_dir, thickness, angle);
    elseif strcmp(effect,'fog')
        thickness = 10;   % 0~10
        Im_effect = addFogEffect(Im, thickness);
    elseif strcmp(effect,'snow')
        thickness = 10;   % 0~10
        Im_effect = addSnowEffect(Im, thickness);
    elseif strcmp(effect,'occlusion')
        spots = 10; % number of blobs created by mud/snow
        Im_effect = addOccEffect(Im, spots);
    else
        Im_effect = imadjust(Im,[0,1],[0,0.5]);
    end
    
    
    figure;imshow(Im_effect)
    imwrite(Im_effect, ['Added_' effect '.png']);
end

