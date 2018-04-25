
function Im_effect = addRainEffect(Im, effect_dir, thickness, angle)

if thickness > 0
    Im_effect = uint8(zeros(size(Im,1)*2, size(Im,2)*2, 3));
    
    for j=1:10
        effect_file = [effect_dir 'cv0_osc' num2str(j-1) '.png'];
        effect_im = im2uint8(imresize(imread(effect_file),[32,1]));
        effect_im = imadjust(effect_im,[0,1],[0,0.1+(j/100)]);  % gain 0.1 ~0.2
        [r,c] = size(effect_im);
        
        for k=1:(thickness*100)  %% number of rain streaks to be added
            x = randi([1,size(Im_effect,2)-c],1,1);
            y = randi([1,size(Im_effect,1)-r],1,1);
            x_end = x+c-1;
            y_end = y+r-1;
            Im_effect(y:y_end, x:x_end,1) = Im_effect(y:y_end, x:x_end,1)+effect_im(:);
            Im_effect(y:y_end, x:x_end,2) = Im_effect(y:y_end, x:x_end,2)+effect_im(:);
            Im_effect(y:y_end, x:x_end,3) = Im_effect(y:y_end, x:x_end,3)+effect_im(:);
        end
    end
    
    sigma = 0.5 + (thickness/10);  % sigma 0.5~1.5
    Im = imgaussfilt(Im,sigma);
    
    gain = 0.75 - (thickness/100);  % gain 0.65~0.75
    Im = imadjust(Im,[0,1],[0,gain]);
    
    Im_effect = imrotate(Im_effect,angle,'bilinear','crop');
    % figure;imshow(Im_effect)
    
    Im_effect = imcrop(Im_effect, [264,264,size(Im,2)-1, size(Im,1)-1]);
    
    H = fspecial('motion',2,45);
    Im_effect = imfilter(Im_effect,H,'replicate');
    Im_effect = Im + Im_effect;
    
    % Im_effect = imadjust(Im_effect,[0,1],[0,0.7]);
else
    Im_effect = Im;
end
