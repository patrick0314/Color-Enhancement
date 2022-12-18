
clc,clear,close all
[a,b]=meshgrid(-1:0.01:1,1:-0.01:-1);
h=atan2(b,a)/(2*pi); h(h<0)=h(h<0)+1;
s=sqrt(a.^2+b.^2);
% gamut checking
for V=0:100
    hsv=cat(3,h,s,V*ones(201,201)/100);
    rgb=hsv2rgb(hsv);
    R=rgb(:,:,1); G=rgb(:,:,2); B=rgb(:,:,3);
    mask=R>1|R<0|G>1|G<0|B>1|B<0;
    R(mask)=0; G(mask)=0; B(mask)=0;
    RGB=cat(3,R,G,B);
    imshow(RGB,'Border','tight')
    HSV{V+1}=RGB;
end
montage(HSV,'Indices',2:101,'Size',[10 10],...
        'BorderSize',1,'BackgroundColor','w')
% grayspace threshold
for V=0:100
    hsv=cat(3,h,s,V*ones(201,201)/100);
    rgb=hsv2rgb(hsv);
    R=rgb(:,:,1); G=rgb(:,:,2); B=rgb(:,:,3);
    mask=R>1|R<0|G>1|G<0|B>1|B<0;
    R(mask)=0; G(mask)=0; B(mask)=0;
    mask=s<=sqrt(V)*0.01;
    R(~mask)=0; G(~mask)=0; B(~mask)=0;
    RGB=cat(3,R,G,B);
    imshow(RGB,'Border','tight')
    HSV{V+1}=RGB;
end
figure, montage(HSV,'Indices',2:101,'Size',[10 10],...
                'BorderSize',1,'BackgroundColor','w')
