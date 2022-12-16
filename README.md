# Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement

## [Version 1](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/blob/main/NaturalImgEnhanced.py)

According to ["Exploiting Perceptual Anchoring for Color Image Enhancement"](https://ieeexplore.ieee.org/document/7337421), we follow the step in the paper and implement it.

## [Version 2](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/blob/main/ToneAndColorCorrection.py)

Use tone and color correction with the function `log((a-1)*img+1]) / log(a)` where `a` is a constant to modify the image.

We can see that this method exactly enhances the image with dim backlight. However, in the bright part of image, color become too bright and not the same color from our perspective.

## [Version 3](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/blob/main/SLIC.py)

Use SLIC to segment the image into few groups. This is because we think that #version 2 could not get the good performance due to its constant parameter. Therefore, we modify the parameter `a` into adaptation.

From below figure, We can see that when `a` gets larger, the curve become more bending. We wants that the bright parts of image don't change too much and the dark parts of image change much more. We use mean color of SLIC segmentation as sample and throw it to the method of #version 1 to get lightness `J` and chroma `C`. Set `a = 10000 / np.sqrt(J*C)`. Under this circumstance, we can see that the performance become better due the adaptation of this method.

![網頁擷取_16-12-2022_234912_www desmos com](https://user-images.githubusercontent.com/47914151/208136409-f86bb49d-f412-49d7-9028-c435c48893d2.jpeg)

## Requirement

```
numpy==1.23.5
opencv-python==4.6.0.66
```

## Usage

* [ColorPatchEnhanced.py](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/blob/main/ColorPatchEnhanced.py) implement color enhancement on input data folder - [color patch](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/tree/main/images/color%20patch) and save the results with name `v1` in the folder - [color patch results](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/tree/main/images/color%20patch%20results)

* [NaturalImgEnhanced.py](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/blob/main/NaturalImgEnhanced.py) implement **method 1** color enhancement on input data folder - [natural image](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/tree/main/images/natural%20image) and save the results with name `v1` in the folder - [natural image results](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/tree/main/images/natural%20image%20results)

* [ToneAndColorCorrection.py](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/blob/main/NaturalImgEnhanced.py) implement **method 2** color enhancement on input data folder - [natural image](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/tree/main/images/natural%20image) and save the results with name `v2` in the folder - [natural image results](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/tree/main/images/natural%20image%20results)

* [SLIC.py](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/blob/main/NaturalImgEnhanced.py) implement **method 3** color enhancement on input data folder - [natural image](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/tree/main/images/natural%20image) and save the results with name `v3` in the folder - [natural image results](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/tree/main/images/natural%20image%20results)

* [SimulatingImgDimBack.py](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/blob/main/SimulatingImgDimBack.py) can show the comparison between original img & the img with dim backlight and save the results in the folder - [results](https://github.com/patrick0314/Exploiting-Perceptual-Anchoring-for-Color-Image-Enhancement/tree/main/images/results)

## Results

The left-most row are the original image and its dim backlight version. The second are is the proposed results of ["Exploiting Perceptual Anchoring for Color Image Enhancement"](https://ieeexplore.ieee.org/document/7337421). The 3rd row are our implement of ["Exploiting Perceptual Anchoring for Color Image Enhancement"](https://ieeexplore.ieee.org/document/7337421). The 4th row are the implement of tone and color correction. And the last row are the implement of SLIC + tone and color correction + ["Exploiting Perceptual Anchoring for Color Image Enhancement"](https://ieeexplore.ieee.org/document/7337421)

![01](https://user-images.githubusercontent.com/47914151/208147535-d9b7dca3-068b-46c9-ba7b-2c08945c3317.png)

![06](https://user-images.githubusercontent.com/47914151/208147614-00b3ed54-1852-41b2-9dbf-363a331f09ed.png)

![11](https://user-images.githubusercontent.com/47914151/208148142-de2d1b67-b47f-49f4-9262-69b1d2a86c9d.png)

