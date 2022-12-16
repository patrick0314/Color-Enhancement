import os
import sys
import time

import cv2
import numpy as np
from skimage.segmentation import mark_boundaries, slic

from ciecam import CIECAM02

if __name__ == '__main__':
    np.seterr(invalid='ignore')
    
    ## Load Input Image
    imgDir = 'images/natural image'
    outDir = 'images/natural image results'
    allFiles = os.listdir(imgDir)
    
    ## The Estimated Display Parameters
    # the full-backlight display (subscript f)
    gamma_rf, gamma_gf, gamma_bf = 2.4767, 2.4286, 2.3792
    Mf = np.array([[95.57, 64.67, 33.01], [49.49, 137.29, 14.76], [0.44, 27.21, 169.83]])

    # the low-backlight display (subscript l)
    gamma_rl, gamma_gl, gamma_bl = 2.2212, 2.1044, 2.1835
    Ml = np.array([[4.61, 3.35, 1.78], [2.48, 7.16, 0.79], [0.28, 1.93, 8.93]])

    for file in allFiles:
        print('=== start', file, 'image ===')
        startTime = time.time()

        imgPath = os.path.join(imgDir, file)
        img = cv2.imread(imgPath)
        img = img.astype(np.float64) / 255

        segments = slic(img, n_segments=5, sigma=5)
        imgEnhanced = np.zeros(img.shape, dtype=np.float64)
        for idx in range(1, np.max(segments)+1):
            sampleImg = np.ones(img.shape, dtype=np.float64)
            sampleImg[:, :, 0] = np.multiply(img[:, :, 0], (segments==idx))
            sampleImg[:, :, 1] = np.multiply(img[:, :, 1], (segments==idx))
            sampleImg[:, :, 2] = np.multiply(img[:, :, 2], (segments==idx))

            sample = np.ones(3)
            sample[0] = np.sum(sampleImg[:, :, 0]) / np.sum(segments==idx)
            sample[1] = np.sum(sampleImg[:, :, 1]) / np.sum(segments==idx)
            sample[2] = np.sum(sampleImg[:, :, 2]) / np.sum(segments==idx)

            xyz = np.matmul(Mf, np.array([sample[0]**gamma_rf, sample[1]**gamma_gf, sample[2]**gamma_bf]))
            white = np.matmul(Mf, np.array([1.0, 1.0, 1.0]))

            ## Color Reproduction
            # Step 1 determining parameters
            Y_b = 25 # Background relative luminance
            L_a = 60 # Adapting luminance
            c = 0.69 # [avg, dim, dark] = [0.69, 0.59, 0.525]
            N_c = 1.0 # [avg, dim, dark] = [1.0, 0.9, 0.8]
            F = 1.0 # [avg, dim, dark] = [1.0, 0.9, 0.8]
            D = F * (1 - (1/3.6)*np.exp(-(L_a+42)/92))

            # Step 2-5 use python library
            model = CIECAM02(xyz[0], xyz[1], xyz[2], white[0], white[1], white[2], Y_b, L_a, c, N_c, F)
            h = model.hue_angle
            J = model.lightness
            C = model.chroma

            a = np.sqrt(10000 / (J*C))
            imgEnhanced[:, :, 0] += 0.8 * np.log((a-1)*sampleImg[:, :, 0]+1) / np.log(a) + 0.2 * sampleImg[:, :, 0]
            imgEnhanced[:, :, 1] += 0.8 * np.log((a-1)*sampleImg[:, :, 1]+1) / np.log(a) + 0.2 * sampleImg[:, :, 1]
            imgEnhanced[:, :, 2] += 0.8 * np.log((a-1)*sampleImg[:, :, 2]+1) / np.log(a) + 0.2 * sampleImg[:, :, 2]

        imgEnhanced *= 255
        imgEnhanced = imgEnhanced.astype(np.uint8)

        cv2.imwrite(os.path.join(outDir, file[:2]+'_v3'+file[-4:]), imgEnhanced)
        endTime = time.time()
        print('cost:', endTime-startTime, 'sec')