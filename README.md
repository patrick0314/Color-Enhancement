# Color Enhancement

We can divide our project into saveral parts: 

  1. **Exploiting Perceptual Anchoring for Color Image Enhancement :** In this part, we implement the method of the paper "Exploiting Perceptual Anchoring for Color Image Enhancement". The details can be seen in the [README](https://github.com/patrick0314/DIP-Final-Project/blob/main/1%20Exploiting%20Perceptual%20Anchoring%20for%20Color%20Image%20Enhancement/README.md)
  
  
  ```
  cd ./1 Exploiting Perceptual Anchoring for Color Image Enhancement/
  python ColorPatchEnhanced.py
  ```
  ```
  cd ./1 Exploiting Perceptual Anchoring for Color Image Enhancement/
  python NatrualImgEnhanced.py
  python SimulatingDimBack.py
  ```
  
  2. **Gamma Correction - CIELUV & HSV & YCrCb & RGB :** In this part, we use Gamma Correction to analysis the difference of different color space. The details can be seen in the [README](https://github.com/patrick0314/DIP-Final-Project/blob/main/2%20Gamma%20Correction/README.md)
  
  ```
  cd ./2 Gamma Correction/
  python gamma_test.py
  python SimulatingDimBack.py
  ```
  
  3. **HSV Enhancement + Low Light Enhancement :** After the analysis of different color space, we choose HSV as our target color space and then modify the image withj HSV color space. Besides, we find a method in 2011 and we think it has good performance. We compare our method with this old method. The details can be seen in the [README](https://github.com/patrick0314/DIP-Final-Project/blob/main/3%20HSV%20and%20Low%20Light%20Enhancement/README.md)
  
  ```
  cd ./3 HSV and Low Light Enhancement/
  run HSV_enhancement.m
  run Low_light_enhancement.m
  run Dim_BackLight.m
  ```
  
  4. **Color Correction + SLIC + CIECAM02 :** Last, we attempt another method - Tone and Color Correction. Based on our acknowledgement domain, we adopt SLIC + CIECAM02 to modify Tone and Color Correction and derive the results which we think better than original ones. The details can be seen in the [README](https://github.com/patrick0314/DIP-Final-Project/blob/main/4%20Tone%20And%20Color%20Correction/README.md)
  
  ```
  cd ./4 Tone And Color Correction/
  python ToneAndColorCorrection.py
  python SLIC.py
  python SimulatingImgDimBack.py
  ```
