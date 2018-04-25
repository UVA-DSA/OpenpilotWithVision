function [feature] = HOG_implementation(I, resolution, blocksize, binsize)
%
% inputs: 'I' is the original RGB image 
% 'resolution' is the target image block size, such as 64x64. 
% 'blocksize' is variable but resolution must be divisible by blocksize such as for
% 64x64, blocksize can be 16x16 or 8x8 etc. This code is implemented for
% 'binsize' 9. So binsize must be 9 here.
%
%% change image resolution
% if size(I,3)>1
%     I = rgb2gray(I);
% end
if resolution(2)~= size(I,1) || resolution(1)~= size(I,2)
    I = imresize(I, resolution);
end
I = padarray(I, [1 1]); % one layer zero padding around the image
I = double(I);

%% Calculate gradient vecotors, magnitudes and angles
gradX = imfilter(I, [-1,0,1]);
gradY = imfilter(I, [1;0;-1]);
gradX = gradX(2:resolution(1)+1, 2:resolution(1)+1);
gradY = gradY(2:resolution(2)+1, 2:resolution(2)+1);
gradMagnitude = sqrt(gradX.^2 + gradY.^2);
gradAngle = atan2(gradY, gradX)*180/pi;
gradAngle(gradAngle<0) = gradAngle(gradAngle<0) + 180;

%% Calculate histogram for each block of 'blocksize' in bins of 'binsize'
feature = [];
blockHist = zeros(2, binsize*4); % first row for bin angle and second for histogram
binRange = 0:180/binsize:180;
for i=1:binsize
    blockHist(1,i:binsize:binsize*4) = (binRange(i)+binRange(i+1))/2;
end
for r=1:blocksize(2)/2:size(gradX,1)-(blocksize(2)/2)
    for c=1:blocksize(1)/2:size(gradX,2)-(blocksize(1)/2)
        gradMagBlock = gradMagnitude(r:r+blocksize(2)-1, c:c+blocksize(1)-1);
        gradAngBlock = gradAngle(r:r+blocksize(2)-1, c:c+blocksize(1)-1);
        blockHist(2,:) = HOG_binning(gradMagBlock, gradAngBlock, blocksize, binsize);
        feature = [feature blockHist(2,:)];
    end
end

end
