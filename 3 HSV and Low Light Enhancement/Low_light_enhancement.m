
clc,clear,close all
Idata=imageDatastore('Image','IncludeSubfolders',true,'FileExtensions',{'.png'});
II=readall(Idata);
IName=dir('Image\**\*.png'); Iname={IName.name};
mkdir('Test'), cd Test
for i=1:numel(Iname)
    [M,N]=size(II{i},[1 2]);
    AInv=imcomplement(II{i});
    BInv=imreducehaze(AInv,'ContrastEnhancement','none');
    B=imcomplement(BInv);
    imwrite(B,[Iname{i}(1:2),'_E.png'])
end
close, disp('Successful.')
