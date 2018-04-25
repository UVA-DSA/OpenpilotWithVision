function Im_effect = addOccEffect(Im, spots)

if spots > 0
    Im_effect = Im;
    Im_occ = uint8(255*ones(size(Im,1), size(Im,2)));
    Yind = 1:1:size(Im,1);
    for i=1:spots
        R = randi([5, 50],1,1);   % radius
        X = randi([10+R,size(Im_effect,2)-10-R],1,1);  %center
        Y = randi([(round(size(Im_effect,1)/2)),size(Im_effect,1)-R],1,1);  % center
        t = linspace(0, 2*pi,R*8);
        l = length(t);
        
        x = X + R*cos(t);
        y = Y + R*sin(t);
        x1 = round(x(1));
        y1 = round(y(1));
        Im_occ(y1,x1) = 0;
        
        for j=2:l
            xj = round(x(j));
            yj = y(j);
            if j<=l/2
                Im_occ(Yind <= yj & Yind >= y1,xj) = 0;
            else
                Im_occ(Yind >= yj & Yind <= y1,xj) = 0;
            end        
        end
    end
%     figure;imshow(Im_occ)
    Im_occ = imgaussfilt(Im_occ,7.0);
%     figure;imshow(Im_occ)
    
    [row,col] = find(Im_occ<150);
    for r = 1:size(row)
        Im_effect(row(r),col(r),:) = uint8(Im_occ(row(r),col(r),:));
    end
else
    Im_effect = Im;
end