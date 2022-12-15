import os
import sys
import time

import cv2
import numpy as np

from ciecam import CIECAM02

if __name__ == '__main__':
    np.seterr(invalid='ignore')

    ## Load Input Image
    imgDir = 'results_tmm/natural image'
    outDir = 'results_tmm/natural image results'
    allFiles = os.listdir(imgDir)
    
    ## The Estimated Display Parameters
    # the full-backlight display (subscript f)
    gamma_rf, gamma_gf, gamma_bf = 2.4767, 2.4286, 2.3792
    Mf = np.array([[95.57, 64.67, 33.01], [49.49, 137.29, 14.76], [0.44, 27.21, 169.83]])

    # the low-backlight display (subscript l)
    gamma_rl, gamma_gl, gamma_bl = 2.2212, 2.1044, 2.1835
    Ml = np.array([[4.61, 3.35, 1.78], [2.48, 7.16, 0.79], [0.28, 1.93, 8.93]])

    for file in allFiles:
        startTime = time.time()
        if 'original' not in file: continue
        print('=== start', file, 'image ===')

        imgPath = os.path.join(imgDir, file)
        img = cv2.imread(imgPath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgEnhanced = np.ones(img.shape)
        JCs = np.ones(img.shape[:2])

        visited = {}
        m, n, o = img.shape
        img2 = np.pad(img, ((25, 25), (25, 25), (0, 0)), 'edge')
        for i in range(25, m+25):
            for j in range(25, n+25):
                ## Device Characteristic Modeling
                rgb = img2[i, j, :].astype(np.float16) / 255
                if tuple(rgb) in visited:
                    imgEnhanced[i-25, j-25, :] = visited[tuple(rgb)][::-1]
                    continue

                xyz = np.matmul(Mf, np.array([rgb[0]**gamma_rf, rgb[1]**gamma_gf, rgb[2]**gamma_bf]))
                white = np.matmul(Mf, np.array([1.0**gamma_rf, 1.0**gamma_gf, 1.0**gamma_bf]))

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
                JCs[i-25, j-25] = model.lightness * model.chroma
                
                ## Inversion of the Appearance Model
                LMSc = model.lmsc
                # Step 8 Invert the chromatic adaptation transform to compute LMS
                M_CAT = np.array([[0.7328, 0.4296, -0.1624], [-0.7036, 1.6975, 0.0061], [0.0030, 0.0136, 0.9834]])
                white = np.matmul(Ml, np.array([1.0**gamma_rl, 1.0**gamma_gl, 1.0**gamma_bl]))
                LMSw = np.matmul(M_CAT, white)
                LMS = LMSc / (100*D/LMSw + 1 - D)
                # Step 8 Invert the chromatic adaptation transform to compute XYZ
                M_CATinv = np.linalg.inv(M_CAT)
                xyze = np.matmul(M_CATinv, LMS)

                ## Post Gamut Mapping
                # Step 1 Convert the XYZ values to RGB values
                RGBe = np.matmul(np.linalg.inv(Ml), xyze)
                RGB2 = np.array([RGBe[0]**(1/gamma_rl), RGBe[1]**(1/gamma_gl), RGBe[2]**(1/gamma_bl)])
                RGB2 = np.nan_to_num(RGB2, nan=0.0)
                # Step 2 Clipping the RGB values with a hard threshold
                RGBc = np.clip(RGB2, 0, 1)

                ## Color Enhancement Image
                imgEnhanced[i-25, j-25, :] = RGBc[::-1]

                ## Save Dynamic Programming
                visited[tuple(rgb)] = RGBc

        JCs = JCs / np.max(JCs)
        JC = np.mean(JCs)
        a = 4
        imgEnhanced[:, :, 0] = (1-JC) * np.log((a-1)*imgEnhanced[:, :, 0]+1) / np.log(a) + JC * img[:, :, 2].astype(np.float16) / 255
        imgEnhanced[:, :, 1] = (1-JC) * np.log((a-1)*imgEnhanced[:, :, 1]+1) / np.log(a) + JC * img[:, :, 1].astype(np.float16) / 255
        imgEnhanced[:, :, 2] = (1-JC) * np.log((a-1)*imgEnhanced[:, :, 2]+1) / np.log(a) + JC * img[:, :, 0].astype(np.float16) / 255

        ## Show Results
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        imgEnhanced = (imgEnhanced * 255).astype(np.uint8)

        ## Save Results
        cv2.imwrite(os.path.join(outDir, file[:2]+'_v2'+file[-4:]), imgEnhanced)
        endTime = time.time()
        print('cost: ', endTime-startTime)