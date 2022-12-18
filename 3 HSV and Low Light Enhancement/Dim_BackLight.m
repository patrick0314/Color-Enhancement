
clc,clear,close all
Idata=imageDatastore('Original','IncludeSubfolders',true,'FileExtensions',{'.png'});
II=readall(Idata);
IName=dir('Original\*.png'); Iname={IName.name};
mkdir('Dim_Backlight'), cd Dim_Backlight
for i=1:numel(Iname)
    RGB=im2double(II{i});
    R=RGB(:,:,1);G=RGB(:,:,2);B=RGB(:,:,3);
    Mf=[95.57 64.67 33.01;49.49 137.29 14.76;0.44 27.21 169.83];
    Ml=[4.61 3.35 1.78;2.48 7.16 0.79;0.28 1.93 8.93];
    r_rf=2.4767; r_gf=2.4286; r_bf=2.3792;
    r_rl=2.2212; r_gl=2.1044; r_bl=2.1835;
    X=Ml(1,1).*(R.^r_rl)+Ml(1,2).*(G.^r_gl)+Ml(1,3).*(B.^r_bl);
    Y=Ml(2,1).*(R.^r_rl)+Ml(2,2).*(G.^r_gl)+Ml(2,3).*(B.^r_bl);
    Z=Ml(3,1).*(R.^r_rl)+Ml(3,2).*(G.^r_gl)+Ml(3,3).*(B.^r_bl);
    mf=Mf^(-1);
    nR=(mf(1,1).*X+mf(1,2).*Y+mf(1,3).*Z).^(1/r_rf);
    nG=(mf(2,1).*X+mf(2,2).*Y+mf(2,3).*Z).^(1/r_gf);
    nB=(mf(3,1).*X+mf(3,2).*Y+mf(3,3).*Z).^(1/r_bf);
    nRGB=real(cat(3,nR,nG,nB));
%     imshow(nRGB,'Border','tight')
    imwrite(nRGB,[Iname{i}(1),'2.png'])
end
close, disp('Successful.')
