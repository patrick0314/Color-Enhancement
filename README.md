# Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement

## Version 1

According to ["Exploiting Perceptual Anchoring for Color Image Enhancement"](https://ieeexplore.ieee.org/document/7337421), we follow the step in the paper and implement it.

## Version 2

Use tone and color correction with the function `log((a-1)*img+1]) / log(a)` where `a` is a constant to modify the image.

We can see that this method exactly enhances the image with dim backlight. However, in the bright part of image, color become too bright and not the same color from our perspective.

## Version 3

Use SLIC to segment the image into few groups. This is because we think that #version 2 could not get the good performance due to its constant parameter. Therefore, we modify the parameter `a` into adaptation.

From below figure, We can see that when `a` gets larger, the curve become more bending. We wants that the bright parts of image don't change too much and the dark parts of image change much more. We use mean color of SLIC segmentation as sample and throw it to the method of #version 1 to get lightness `J` and chroma `C`. Set `a = 10000 / np.sqrt(J*C)`. Under this circumstance, we can see that the performance become better due the adaptation of this method.

## Requirement

```
numpy==1.23.5
opencv-python==4.6.0.66
```

## Usage

* [ColorPatchEnhanced.py](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/blob/main/ColorPatchEnhanced.py) implement color enhancement on input data folder - [color patch](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/tree/main/images/color%20patch) and save the results in the folder - [color patch results](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/tree/main/images/color%20patch%20results)

* [NaturalImgEnhanced.py](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/blob/main/NaturalImgEnhanced.py) implement color enhancement on input data folder - [natural image](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/tree/main/images/natural%20image) and save the results in the folder - [natural image results](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/tree/main/images/natural%20image%20results)

* [SimulatingImgDimBack.py](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/blob/main/SimulatingImgDimBack.py) can show the comparison between original img & the img with dim backlight and save the results in the folder - [results](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/tree/main/images/results)

## Results

The left-most row are the original image and its dim backlight version. The second are is the proposed results of ["Exploiting Perceptual Anchoring for Color Image Enhancement"](https://ieeexplore.ieee.org/document/7337421). The third row are our implement of ["Exploiting Perceptual Anchoring for Color Image Enhancement"](https://ieeexplore.ieee.org/document/7337421). And the last row are the implement of tone and color correction.

![01](https://user-images.githubusercontent.com/47914151/208063921-132bb8cf-c977-474a-8d41-77d00bba61a9.png)

![06](https://user-images.githubusercontent.com/47914151/208063937-7d7ffd08-2584-49dd-8887-0c0a7bca3f23.png)

![09](https://user-images.githubusercontent.com/47914151/208063955-dbae087f-404b-49e3-887f-4a08da1aa816.png)
