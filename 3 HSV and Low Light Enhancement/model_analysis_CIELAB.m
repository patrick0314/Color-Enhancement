
clc,clear,close all
[a,b]=meshgrid(-100:100,100:-1:-100);
for L=1:101
    lab=cat(3,(L-1)*ones(201,201),a,b);
    rgb=lab2rgb(lab);
    R=rgb(:,:,1); G=rgb(:,:,2); B=rgb(:,:,3);
    mask=R>1|R<0|G>1|G<0|B>1|B<0;
    R(mask)=0; G(mask)=0; B(mask)=0;
    rgb=cat(3,R,G,B);
    imshow(rgb,'Border','tight')
    Lab{L}=rgb;
end
figure,montage(Lab,'Indices',2:101,'Size',[10 10],...
               'BorderSize',1,'BackgroundColor','w')
