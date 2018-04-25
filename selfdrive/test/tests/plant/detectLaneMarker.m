% clc; clear;
% close all;
% effect='';
% thickness = 0;
% im_ind = 3;
% lat_mov = 0;
function [lLane, rLane] = detectLaneMarker()
csvwrite('procImages.txt',0);
ppool = gcp('nocreate');
if isempty(ppool)
    parpool;
end
csvwrite('parpool.txt',1);
% tic

rng('shuffle'); % to generate different random number sequence each time matlab restarts

addpath(genpath('HOG_implementation'));
addpath(genpath('Image_effects'));

net = load('pattNet.mat');
pattNet = net.pattNet;
load('meter_per_pixel');  % polynomial mapping of horizontal pixels to meters w.r.t row



%scene = 'cordova1';
%laneWidth = 3.7;   % standard lane width (m) in US interstate

vision_dir = '/home/uva-dsa/Development/openpilot_git_repo/OpenPilot_latest/Vision_Images/';
all_effects = ['na';'ra';'fo';'sn';'oc';'cn';'br';'ba';'bg';'bm'];

roi_dim = [90, 235, 490, 120];%X= 90->540, Y= 235->355 %[90, 200, 490, 155]; % X= 50->570, Y= 200->355
% rval = roi_dim(2):roi_dim(2)+roi_dim(4);
rval = 200:355;
target_row = round(mean(rval));
target_col = zeros(1,2);

res = [32, 32];
imResolution = [32, 32];
blockSize = [8, 8];
binSize = 9;

t_ind = 1;
procIm = 0;
while(1)
  procIm = importdata('procImages.txt');
  if isnumeric(procIm)
    if procIm==1
      break;
    end
  end
end
for l_ind=1:1000
    if l_ind <= 615
      ind = l_ind;
    else
      ind = l_ind-615;
    end
    opPilotInfo = importdata('latMov.txt');
    if ~isnumeric(opPilotInfo) || length(opPilotInfo)<3
        continue;
    end
    effect = all_effects(opPilotInfo(1)+1,:);
    thickness = opPilotInfo(2);
    
    if strcmp(effect,'ra')
        im_dir = [vision_dir 'faulty_images/rain/' num2str(thickness(t_ind)) '/'];
    elseif strcmp(effect,'fo')
        im_dir = [vision_dir 'faulty_images/fog/' num2str(thickness(t_ind)) '/'];
    elseif strcmp(effect,'sn')
        im_dir = [vision_dir 'faulty_images/snow/' num2str(thickness(t_ind)) '/'];
    elseif strcmp(effect,'oc')
        im_dir = [vision_dir 'faulty_images/occlusion/' num2str(thickness(t_ind)) '/'];
    elseif strcmp(effect,'cn')
        im_dir = [vision_dir 'faulty_images/contrast/' num2str(thickness(t_ind)) '/'];
    elseif strcmp(effect,'br')
        im_dir = [vision_dir 'faulty_images/brightness/' num2str(thickness(t_ind)) '/'];
    elseif strcmp(effect,'ba')
        im_dir = [vision_dir 'faulty_images/blur_avg/' num2str(thickness(t_ind)) '/'];
    elseif strcmp(effect,'bg')
        im_dir = [vision_dir 'faulty_images/blur_gauss/' num2str(thickness(t_ind)) '/'];
    elseif strcmp(effect,'bm')
        im_dir = [vision_dir 'faulty_images/blur_median/' num2str(thickness(t_ind)) '/'];
    else
        im_dir = [vision_dir 'augmented_images/'];
    end
    Im = imread([im_dir 'f' num2str(ind-1, '%05.f') '.png']);
    
    lat_mov = opPilotInfo(3);
    if lat_mov > 1.0
      lat_mov = 1.0;
    elseif lat_mov < -1.0
      lat_mov = -1.0;
    end
    
    valMP = polyval(meter_per_pixel, round(size(Im,1)/2));   % gives val = meter/pixel for the row pathPoint(1)
    shVal = -1*round(lat_mov/valMP);
    
    Im_effect = imtranslate(Im,[double(shVal), 0]);
    
    % Inject image effects mentioned by 'effect' variable
%     if strcmp(effect,'ra')
%         angle = 15;
%         effect_dir = 'sample_rain_streaks/';
%         Im_effect = addRainEffect(Im, effect_dir, thickness(t_ind), angle);
%     elseif strcmp(effect,'fo')
%         Im_effect = addFogEffect(Im, thickness(t_ind));
%     elseif strcmp(effect,'sn')
%         Im_effect = addSnowEffect(Im, thickness(t_ind));
%     elseif strcmp(effect,'oc')
%         Im_effect = addOccEffect(Im, thickness(t_ind));
%     else
%         Im_effect = Im;
%     end

    Im_effect_gray = rgb2gray(Im_effect);
    r_array = roi_dim(2):res(1)/2:roi_dim(2)+roi_dim(4);
    c_array = roi_dim(1):res(2)/2:roi_dim(1)+roi_dim(3);
    test_feature=[];
    sblock_rec=[];
    parfor r=1:length(r_array)
        for c=1:length(c_array)
            if r_array(r)+res(1)-1> roi_dim(2)+roi_dim(4)
                continue;
            else
                r_step_size = res(1)-1;
            end
            if c_array(c)+res(2)-1> roi_dim(1)+roi_dim(3)
                continue;
            else
                c_step_size = res(2)-1;
            end
            if c_step_size < res(1)-1 || r_step_size < res(2)-1
                continue;
            end
            samp_block = imcrop(Im_effect_gray, [c_array(c), r_array(r), c_step_size, r_step_size]);
            test_feature = [test_feature;HOG_implementation(samp_block, imResolution, blockSize, binSize)];
            sblock_rec = [sblock_rec;[c_array(c), r_array(r), c_step_size, r_step_size]];
        end
    end
    Y=pattNet(test_feature');
    [~,label] = max(Y);
    e_ind=[];
    sblock_rec_c = sblock_rec(:,1);
    sblock_rec_r = sblock_rec(:,2);
    parfor f_ind=1:size(test_feature,1)
        if label(f_ind)==1
            samp_block = imcrop(Im_effect_gray, sblock_rec(f_ind,:));
            edge_block = edge(samp_block,'sobel','horizontal'); % horizontal derivative; vertical edges
            if sum(sum(edge_block)) >= 25
                index = [];
                [index(:,1), index(:,2)] = find(edge_block);
                index = index + [sblock_rec_r(f_ind) sblock_rec_c(f_ind)];
                e_ind = [e_ind ; index];
            end
        end
    end
    
    index = e_ind;
    if isempty(index)
        continue;
    end
    LNmid = [1, 640];
    LNind = [0, 0];
    [class,~] = dbscan(index,5,[]);
    if ~isempty(find(class,1))
        index((class==-1),:)=[];
        class((class==-1)) = [];
        num_cluster = length(unique(class));
        for k=1:num_cluster
            Cind = find(class==k);
            if length(Cind)>=30
                m = mean(index(Cind,2));
                if m < 320 && m >LNmid(1)
                    LNmid(1) = m;
                    LNind(1) = k;
                elseif m > 320 && m <LNmid(2)
                    LNmid(2) = m;
                    LNind(2) = k;
                end
            end
        end
        for k=1:2
            Cind = find(class==LNind(k));
            coeff = polyfit(index(Cind,1),index(Cind,2),1);
            %cval(k,:) = polyval(coeff, rval);
            target_col(k) = polyval(coeff, target_row);
            
        end
    end
    
    % represent the lane positions in meters
    pathPoint = [target_row, round(size(Im_effect,2)/2)];
    lPoint = [pathPoint(1), target_col(1)+3];
    rPoint = [pathPoint(1), target_col(2)-3];
    val = polyval(meter_per_pixel, pathPoint(1));   % gives val = meter/pixel for the row pathPoint(1)
    lLane = val*(lPoint(2)-pathPoint(2));
    rLane = val*(rPoint(2)-pathPoint(2));
    
    
    % figure;
    % imshow(Im);hold on;
    % plot(cval(1,:),rval,'r','LineWidth',5);hold on;
    % plot(cval(2,:),rval,'b','LineWidth',5);hold off;
    %     saveas(f_ind, ['Images/final_results/' scene '/f' num2str(ind-1, '%05.f') '.png']);
    %     csvwrite('laneData.dat',[lDist' rDist'],0,0);
    
    csvwrite('laneData.dat',[lLane rLane],0,0);
end
% toc
delete(gcp('nocreate'))
% end
