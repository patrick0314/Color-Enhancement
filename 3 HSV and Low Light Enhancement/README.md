# Color-Image-Enhancement
* Set your github to dark theme before reading

## [Foreword - Low Light Enhancement](https://github.com/justaneater/Color-Image-Enhancement/blob/main/Low_light_enhancement.m)
The full code can be found in [MATLAB Documentation](https://www.mathworks.com/help/images/low-light-image-enhancement.html?s_tid=srchtitle_low%20light_1). The code used in this project are divided into three steps.

Step 1 - Invert the low-light image using the `Imcomplement()` function

Step 2 - Apply the haze removal algorithm to the inverted low-light image using the `imreducehaze()` function

Step 3 - Invert the haze-reduced image back to obtain the enhanced image

The difference of image after each steps are shown as below :

![圖片1](https://user-images.githubusercontent.com/96414401/208234865-13ecc44a-3085-45b0-bec3-6dee6c85e3b4.png)
![圖片2](https://user-images.githubusercontent.com/96414401/208234867-18a311aa-973b-474b-bab1-b4b191956aab.png)

## [My Method - HSV Enhancement](https://github.com/justaneater/Color-Image-Enhancement/blob/main/HSV_enhancement.m)
Step 1 - Normalize the `V`(Value) channel and apply gamma correction with `γ=0.5`

Step 2.1 - Normalize the `S`(Saturation) channel and apply gamma correction with `γ=0.5`

Step 2.2 - Set the threshold of `S/V`, and restore the S value to the value before normalization if the color block is below the threshold

![CIELab](https://user-images.githubusercontent.com/96414401/208271342-7568b5f5-4a2f-460c-a0aa-50b8d6cf86f6.png)
![untitled](https://user-images.githubusercontent.com/96414401/208271343-3c267a6b-d1e8-43e5-8172-2d23df3e8ba2.png)


Step 3 - Divide the `H`(Hue) Channel into 12 pieces, and apply linear normalization to each pieces

![螢幕擷取畫面 2022-12-10 084129](https://user-images.githubusercontent.com/96414401/208231431-d81b299b-9c94-4c08-b2b1-c4456d63ef25.png)

The difference of image after each steps are shown as below :

![圖片4](https://user-images.githubusercontent.com/96414401/208231151-883ef113-6a27-4930-a134-3cca27afe95c.png)
![圖片3](https://user-images.githubusercontent.com/96414401/208231691-e0a946b1-5aef-483b-86b2-aed91b4fd14b.png)

## Usage
* [model_analysis_CIELAB.m](https://github.com/justaneater/Color-Image-Enhancement/blob/main/model_analysis_CIELAB.m) shows the colormaps within the gamut corresponding to different L values in the CIELAB color space, the results can be found in [CIELAB_gamut](https://github.com/justaneater/Color-Image-Enhancement/tree/main/model_analysis/CIELAB_gamut); you can also find the colormaps without gamut-mapping in [CIELAB](https://github.com/justaneater/Color-Image-Enhancement/tree/main/model_analysis/CIELAB)

* [model_analysis_HSV.m](https://github.com/justaneater/Color-Image-Enhancement/blob/main/model_analysis_HSV.m) shows the full colormaps and their acceptable white areas respectively within the gamut corresponding to different V values in the HSV color space. The results can be found in [HSV](https://github.com/justaneater/Color-Image-Enhancement/tree/main/model_analysis/HSV) and [HSV_w](https://github.com/justaneater/Color-Image-Enhancement/tree/main/model_analysis/HSV_w)

* [Dim_BackLight.m](https://github.com/justaneater/Color-Image-Enhancement/blob/main/Dim_BackLight.m) converts images into dim backlight and saves the result to [Dim_Backlight](https://github.com/justaneater/Color-Image-Enhancement/tree/main/Image/Dim_Backlight)

* [HSV_enhancement.m](https://github.com/justaneater/Color-Image-Enhancement/blob/main/HSV_enhancement.m) implements color enhancement on images in [Image](https://github.com/justaneater/Color-Image-Enhancement/tree/main/Image) and saves the result to [Result](https://github.com/justaneater/Color-Image-Enhancement/tree/main/Result)

* [Low_light_enhancement.m](https://github.com/justaneater/Color-Image-Enhancement/blob/main/Low_light_enhancement.m) implements color enhancement on images in [Image](https://github.com/justaneater/Color-Image-Enhancement/tree/main/Image) with the method of [Xuan Dong(2011)](https://ieeexplore.ieee.org/document/6012107) and saves the result in [Xuan](https://github.com/justaneater/Color-Image-Enhancement/tree/main/Xuan)

## Results

The left parts are the original image and its dim backlight version. The middle parts are the implement of [HSV_enhancement.m](https://github.com/justaneater/Color-Image-Enhancement/blob/main/HSV_enhancement.m). The right parts are the implement of [Low_light_enhancement.m](https://github.com/justaneater/Color-Image-Enhancement/blob/main/Low_light_enhancement.m).

![圖片7](https://user-images.githubusercontent.com/96414401/208224141-904939f9-2fdc-49fe-b4cf-b0fceafe918e.png)
![圖片8](https://user-images.githubusercontent.com/96414401/208224145-bf7931da-fd1d-4d48-a403-41ed0ddff5eb.png)
![圖片9](https://user-images.githubusercontent.com/96414401/208229814-f3e19c86-906e-4c24-9057-a632843dffdb.png)
![圖片10](https://user-images.githubusercontent.com/96414401/208224148-c0c5bc42-368e-4507-8af1-0536f1538759.png)



