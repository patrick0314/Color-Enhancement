import os
import sys

import cv2
import numpy as np

if __name__ == '__main__':
    np.seterr(invalid='ignore')

    imgDir = 'images/natural image results'
    outDir = 'images/results'
    allFiles = os.listdir(imgDir)

    ## The Estimated Display Parameters
    # the full-backlight display (subscript f)
    gamma_rf, gamma_gf, gamma_bf = 2.4767, 2.4286, 2.3792
    Mf = np.array([[95.57, 64.67, 33.01], [49.49, 137.29, 14.76], [0.44, 27.21, 169.83]])

    # the low-backlight display (subscript l)
    gamma_rl, gamma_gl, gamma_bl = 2.2212, 2.1044, 2.1835
    Ml = np.array([[4.61, 3.35, 1.78], [2.48, 7.16, 0.79], [0.28, 1.93, 8.93]])

    fileDic = {}
    for file in allFiles:
        if 'SLIC' in file: continue
        if file[:2] not in fileDic: fileDic[file[:2]] = [file]
        else: fileDic[file[:2]].append(file)

    for files in fileDic.keys():
        print('=== start', files, 'image ===')
        first = True
        for file in fileDic[files]:
            img = cv2.imread(os.path.join(imgDir, file))
            imgDim = np.ones(img.shape, dtype=np.uint8)

            m, n, o = img.shape
            for i in range(m):
                for j in range(n):
                    # Change to XYZ with Low-backlight Display Model
                    bgr = img[i, j, :].astype(np.float16) / 255
                    xyz = np.matmul(Ml, np.array([bgr[2]**gamma_rl, bgr[1]**gamma_gl, bgr[0]**gamma_bl]))
                    # Chnage to RGB with Full-backlight Dispaly Model
                    xyzinv = np.matmul(np.linalg.inv(Mf), xyz)
                    bgr[0] = xyzinv[2] ** (1 / gamma_bf)
                    bgr[1] = xyzinv[1] ** (1 / gamma_gf)
                    bgr[2] = xyzinv[0] ** (1 / gamma_rf)

                    imgDim[i, j, :] = (bgr * 255).astype(np.uint8)
            
            res = cv2.vconcat([img, imgDim])
            res = np.pad(res, ((30, 0), (0, 0), (0, 0)), 'constant', constant_values=255)
            cv2.putText(res, file[3:-4], (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1, cv2.LINE_AA)
        
            if first: ress = res; first = False
            else: ress = cv2.hconcat([ress, res])

        # Save Results
        outPath = os.path.join(outDir, file[:2]+'v3'+file[-4:])
        cv2.imwrite(outPath, ress)
