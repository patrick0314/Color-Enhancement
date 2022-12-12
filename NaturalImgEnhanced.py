import os

import cv2
import numpy as np

from ciecam import CIECAM02


if __name__ == '__main__':
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
        if 'original' not in file: continue
        print('=== start', file, 'image ===')

        imgPath = os.path.join(imgDir, file)
        img = cv2.imread(imgPath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgEnhanced = np.ones(img.shape)

        visited = {}
        m, n, o = img.shape
        for i in range(m):
            for j in range(n):
                ## Device Characteristic Modeling
                rgb = img[i, j, :].astype(np.float16) / 255
                if tuple(rgb) in visited:
                    JC = 0.2
                    imgEnhanced[i, j, 0] = (1 - JC) * visited[tuple(rgb)][2] + JC * rgb[2]
                    imgEnhanced[i, j, 1] = (1 - JC) * visited[tuple(rgb)][1] + JC * rgb[1]
                    imgEnhanced[i, j, 2] = (1 - JC) * visited[tuple(rgb)][0] + JC * rgb[0]
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
                
                ''''
                print(model.hue_angle) # Hue h
                print(model.lightness) # Lightness J
                print(model.brightness) # Brightness Q
                print(model.chroma) # Chroma C
                print(model.colorfulness) # Colorfulness M
                print(model.saturation) # Saturation s
                '''
                
                ## Inversion of the Appearance Model
                '''
                # Step 1 Calculate t from C and J
                t = (model.chroma / np.sqrt(model.lightness/100) / (1.64-0.29**model.n)**0.73)**(10/9)
                # Step 2 Calculate et from h
                et = model.et # Eccentricity factor
                # Step 3 Calculate A from Aw and J
                A = model.A
                # Step 4 Calculate a and b from t, et, h and A
                a, b = model.a, model.b
                # Step 5 Calculate La, Ma and Sa from A, a, and b
                nbb = model.nbb
                tmp1 = 20 * ((A/nbb) + 0.305) # 40L + 20M + S
                tmp2 = 11 * a # 11L - 12M + S
                tmp3 = 9 * b # L + M - 2S
                tmp4 = tmp1 - tmp2 # 29L + 32M
                tmp5 = (2*tmp2 + tmp3) / 23 # L - M
                La = (tmp4 + 32*tmp5) / 61
                Ma = -(tmp5 - La)
                Sa = -(tmp3 - La - Ma) / 2
                delta = np.min([La, Ma, Sa])
                # Step 6 Use the inverse nonlinearity to compute LMS2
                Fl = model.f_l
                L2 = 100 * ((27.13 * (La-0.1)) / (400-La+0.1))**(100/42) / Fl
                M2 = 100 * ((27.13 * (Ma-0.1)) / (400-Ma+0.1))**(100/42) / Fl
                S2 = 100 * ((27.13 * (Sa-0.1)) / (400-Sa+0.1))**(100/42) / Fl
                # Step 7 Convert to Lc, Mc and Sc via linear transform
                M_CAT = np.array([[0.7328, 0.4296, -0.1624], [-0.7036, 1.6975, 0.0061], [0.0030, 0.0136, 0.9834]])
                M_Hinv = np.linalg.inv(np.array([[0.38971, 0.68898, -0.07868], [-0.22981, 1.18340, 0.04641], [0, 0, 1]]))
                LMSc = np.matmul(M_CAT, np.matmul(M_Hinv, np.array([L2, M2, S2])))
                '''
                LMSc = model.lmsc
                # Step 8 Invert the chromatic adaptation transform to compute LMS
                M_CAT = np.array([[0.7328, 0.4296, -0.1624], [-0.7036, 1.6975, 0.0061], [0.0030, 0.0136, 0.9834]])
                white = np.matmul(Ml, np.array([1.0**gamma_rl, 1.0**gamma_gl, 1.0**gamma_bl]))
                LMSw = np.matmul(M_CAT, white)
                L = LMSc[0] / (100*D/LMSw[0] + 1 - D)
                M = LMSc[1] / (100*D/LMSw[1] + 1 - D)
                S = LMSc[2] / (100*D/LMSw[2] + 1 - D)
                # Step 8 Invert the chromatic adaptation transform to compute XYZ
                M_CATinv = np.linalg.inv(M_CAT)
                xyze = np.matmul(M_CATinv, np.array([L, M, S]))

                ## Post Gamut Mapping
                # Step 1 Convert the XYZ values to RGB values
                RGBe = np.matmul(np.linalg.inv(Ml), xyze)
                RGB2 = np.array([RGBe[0]**(1/gamma_rl), RGBe[1]**(1/gamma_gl), RGBe[2]**(1/gamma_bl)])
                RGB2 = np.nan_to_num(RGB2, nan=0.0)
                # Step 2 Clipping the RGB values with a hard threshold
                RGBc = np.clip(RGB2, 0, 1)
                RGBc = np.log((10-1)*RGBc+1) / np.log(10)

                ## Color Enhancement Image
                JC = 0.2
                imgEnhanced[i, j, 0] = (1 - JC) * RGBc[2] + JC * rgb[2]
                imgEnhanced[i, j, 1] = (1 - JC) * RGBc[1] + JC * rgb[1]
                imgEnhanced[i, j, 2] = (1 - JC) * RGBc[0] + JC * rgb[0]

                ## Save Dynamic Programming
                visited[tuple(rgb)] = RGBc
                
        ## Show Results
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        imgEnhanced = (imgEnhanced * 255).astype(np.uint8)
        '''
        #cv2.imshow('Results', cv2.hconcat([img, imgEnhanced]))
        #cv2.waitKey(0)
        '''

        ## Save Results
        cv2.imwrite(os.path.join(outDir, file), cv2.hconcat([img, imgEnhanced]))