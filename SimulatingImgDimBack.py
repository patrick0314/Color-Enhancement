import os

import cv2
import numpy as np


def DeviceCharacteristicModeling(M, R, gr, gg, gb):
    res = np.matmul(M, np.array([R[2]**gr, R[1]**gg, R[0]**gb]))
    return res
    
if __name__ == '__main__':
    imgDir = 'results_tmm/natural image results'
    outDir = 'results_tmm/results'
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
        img = cv2.imread(os.path.join(imgDir, file))
        imgDim = np.ones(img.shape, dtype=np.uint8)

        m, n, o = img.shape
        for i in range(m):
            for j in range(n):
                # Change to XYZ with Low-backlight Display Model
                bgr = img[i, j, :].astype(np.float16) / 255
                xyz = DeviceCharacteristicModeling(Ml, bgr, gamma_rl, gamma_gl, gamma_bl)
                # Chnage to RGB with Full-backlight Dispaly Model
                xyzinv = np.matmul(np.linalg.inv(Mf), xyz)
                bgr[0] = xyzinv[2] ** (1 / gamma_bl)
                bgr[1] = xyzinv[1] ** (1 / gamma_bl)
                bgr[2] = xyzinv[0] ** (1 / gamma_bl)

                imgDim[i, j, :] = (bgr * 255).astype(np.uint8)

        # Show Results
        '''
        cv2.imshow('Comparison', cv2.vconcat([img, imgDim]))
        cv2.waitKey(0)
        '''

        # Save Results
        outPath = os.path.join(outDir, file)
        cv2.imwrite(outPath, cv2.vconcat([img, imgDim]))