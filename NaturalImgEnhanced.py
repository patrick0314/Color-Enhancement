import os
import sys
import time

import cv2
import numpy as np

from ciecam import CIECAM02, P, opponent_colour_dimensions_inverse

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
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgEnhanced = np.ones(img.shape)
        
        visited = {}
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                ## Device Characteristic Modeling
                sample = img[i, j, :].astype(np.float16) / 255
                if tuple(sample) in visited:
                    imgEnhanced[i, j, :] = visited[tuple(sample)][::-1]
                    continue

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

                ## Inversion of the Appearance Model
                white = np.matmul(Ml, np.array([1.0, 1.0, 1.0]))
                model = CIECAM02(xyz[0], xyz[1], xyz[2], white[0], white[1], white[2], Y_b, L_a, c, N_c, F)
                # Step 1 Calculate t from C and J
                n = Y_b / white[1]
                t = (C / (np.sqrt(J/100) * (1.64-0.29**n)**(0.73)))**(1/0.9)
                # Step 2 Calculate et from h
                et = (1 / 4) * (np.cos(2 + h * np.pi / 180) + 3.8)
                # Step 3 Calculate A from Aw and J
                z = 1.48 + np.sqrt(n)
                Aw = model.aw
                A = (J / 100)**(1/(c*z)) * Aw
                # Step 4 Calculate a and b from t, h and A
                nbb = 0.725 * (1/n)**(0.2)
                pn = P(N_c, nbb, et, t, A, nbb)
                ab = opponent_colour_dimensions_inverse(pn, h)
                # Step 5 Calculate La, Ma and Sa from A, a and b
                tmp1 = 20 * ((A / nbb) + 0.305) # 40La + 20Ma + Sa
                tmp2 = 11 * ab[0] # 11La - 12Ma + Sa
                tmp3 = 9 * ab[1] # La + Ma - 2Sa
                tmp4 = tmp1 - tmp2 # 29La + 32Ma
                tmp5 = (2*tmp2 + tmp3) / 23 # La - Ma
                tmp6 = tmp4 + 32 * tmp5 # 61La
                La = tmp6 / 61
                Ma = -(tmp5 - La)
                Sa = -(tmp3 - La - Ma) / 2
                LMSa = np.array([La, Ma, Sa])
                # Step 6 Use the inverse nonlinearity to compute L2, M2 and S2
                k = 1 / (5*L_a+1)
                Fl = 0.2 * k**4 * (5*L_a) + 0.1 * (1-k**4)**2 * (5*L_a)**(1/3)
                LMS2 = ((27.13*(LMSa-0.1)) / (400-LMSa+0.1))**(100/42) * 100 / Fl
                # Step 7 Convert to Lc, Mc and Sc vis linear transformer
                M_CAT02 = np.array([[0.7328, 0.4296, -0.1624], [-0.7036, 1.6975, 0.0061], [0.0030, 0.0136, 0.9834]])
                M_HPE = np.array([[0.38971, 0.68898, -0.07868], [-0.22981, 1.18340, 0.04641], [0, 0, 1]])
                M_HPE_inv = np.linalg.inv(M_HPE)
                LMSc = np.matmul(M_CAT02, np.matmul(M_HPE_inv, LMS2))
                # Step 8 Invert the chromatic adaptation transform to compute LMS
                LMSw = np.matmul(M_CAT02, white)
                LMS = LMSc / (100*D/LMSw + 1 - D)
                # Step 8 Invert the chromatic adaptation transform to compute XYZ
                M_CATinv = np.linalg.inv(M_CAT02)
                xyze = np.matmul(M_CATinv, LMS)

                ## Post Gamut Mapping
                # Step 1 Convert the XYZ values to RGB values
                RGBe = np.matmul(np.linalg.inv(Ml), xyze)
                RGB2 = np.array([RGBe[0]**(1/gamma_rl), RGBe[1]**(1/gamma_gl), RGBe[2]**(1/gamma_bl)])
                RGB2 = np.nan_to_num(RGB2, nan=0.0)
                # Step 2 Clipping the RGB values with a hard threshold
                RGBc = np.clip(RGB2, 0, 1)

                ## Color Enhancement Image
                imgEnhanced[i, j, :] = RGBc[::-1]

                ## Save Dynamic Programming
                visited[tuple(sample)] = RGBc

        JC = J * C / 10000
        imgEnhanced[:, :, 0] = (1-JC) * imgEnhanced[:, :, 0] + JC * img[:, :, 2].astype(np.float16) / 255
        imgEnhanced[:, :, 1] = (1-JC) * imgEnhanced[:, :, 1] + JC * img[:, :, 1].astype(np.float16) / 255
        imgEnhanced[:, :, 2] = (1-JC) * imgEnhanced[:, :, 2] + JC * img[:, :, 0].astype(np.float16) / 255

        ## Show Results
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        imgEnhanced = (imgEnhanced * 255).astype(np.uint8)
        
        ## Save Results
        cv2.imwrite(os.path.join(outDir, file[:2]+'_v1'+file[-4:]), imgEnhanced)
        endTime = time.time()
        print('cost:', endTime-startTime, 'sec')