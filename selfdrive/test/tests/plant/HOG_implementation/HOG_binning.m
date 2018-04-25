function blockFeat = HOG_binning(magBlock, angBlock, blocksize, binsize)
halfBlockSize = blocksize./2;
blockFeat = [];
for r=1: halfBlockSize(2): blocksize(2)
    for c=1: halfBlockSize(1) : blocksize(1)
        subMagBlock = magBlock(r:r+halfBlockSize(2)-1, c:c+halfBlockSize(1)-1);
        subAngBlock = angBlock(r:r+halfBlockSize(2)-1, c:c+halfBlockSize(1)-1);
        blockHist = zeros(1,binsize);
        for p=1:halfBlockSize(2)
            for q=1:halfBlockSize(1)                   
                alpha= subAngBlock(p,q);
                % Binning Process
                if alpha>10 && alpha<=30
                    blockHist(1)=blockHist(1)+ subMagBlock(p,q)*(30-alpha)/20;
                    blockHist(2)=blockHist(2)+ subMagBlock(p,q)*(alpha-10)/20;
                elseif alpha>30 && alpha<=50
                    blockHist(2)=blockHist(2)+ subMagBlock(p,q)*(50-alpha)/20;                 
                    blockHist(3)=blockHist(3)+ subMagBlock(p,q)*(alpha-30)/20;
                elseif alpha>50 && alpha<=70
                    blockHist(3)=blockHist(3)+ subMagBlock(p,q)*(70-alpha)/20;
                    blockHist(4)=blockHist(4)+ subMagBlock(p,q)*(alpha-50)/20;
                elseif alpha>70 && alpha<=90
                    blockHist(4)=blockHist(4)+ subMagBlock(p,q)*(90-alpha)/20;
                    blockHist(5)=blockHist(5)+ subMagBlock(p,q)*(alpha-70)/20;
                elseif alpha>90 && alpha<=110
                    blockHist(5)=blockHist(5)+ subMagBlock(p,q)*(110-alpha)/20;
                    blockHist(6)=blockHist(6)+ subMagBlock(p,q)*(alpha-90)/20;
                elseif alpha>110 && alpha<=130
                    blockHist(6)=blockHist(6)+ subMagBlock(p,q)*(130-alpha)/20;
                    blockHist(7)=blockHist(7)+ subMagBlock(p,q)*(alpha-110)/20;
                elseif alpha>130 && alpha<=150
                    blockHist(7)=blockHist(7)+ subMagBlock(p,q)*(150-alpha)/20;
                    blockHist(8)=blockHist(8)+ subMagBlock(p,q)*(alpha-130)/20;
                elseif alpha>150 && alpha<=170
                    blockHist(8)=blockHist(8)+ subMagBlock(p,q)*(170-alpha)/20;
                    blockHist(9)=blockHist(9)+ subMagBlock(p,q)*(alpha-150)/20;
                elseif alpha>=0 && alpha<=10
                    blockHist(1)=blockHist(1)+ subMagBlock(p,q)*(alpha+10)/20;
                    blockHist(9)=blockHist(9)+ subMagBlock(p,q)*(10-alpha)/20;
                elseif alpha>170 && alpha<=180
                    blockHist(9)=blockHist(9)+ subMagBlock(p,q)*(190-alpha)/20;
                    blockHist(1)=blockHist(1)+ subMagBlock(p,q)*(alpha-170)/20;
                end
            end
        end 
        blockFeat = [blockFeat blockHist];
    end
end
if norm(blockFeat)
    blockFeat = blockFeat/norm(blockFeat);
end
end