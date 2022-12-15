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

    for file in allFiles:
        startTime = time.time()
        if 'original' not in file: continue

        imgPath = os.path.join(imgDir, file)
        img = cv2.imread(imgPath)
        img = img.astype(np.float16) / 255
        imgEnhanced = img.copy()

        JC = 0.2
        a = 4
        imgEnhanced[:, :, 0] = (1-JC) * np.log((a-1)*imgEnhanced[:, :, 0]+1) / np.log(a) + JC * img[:, :, 0]
        imgEnhanced[:, :, 1] = (1-JC) * np.log((a-1)*imgEnhanced[:, :, 1]+1) / np.log(a) + JC * img[:, :, 1]
        imgEnhanced[:, :, 2] = (1-JC) * np.log((a-1)*imgEnhanced[:, :, 2]+1) / np.log(a) + JC * img[:, :, 2]

        imgEnhanced *= 255
        imgEnhanced = imgEnhanced.astype(np.uint8)

        cv2.imshow('test', imgEnhanced)
        cv2.waitKey(0)

        cv2.imwrite(os.path.join(outDir, file[:2]+'_v3'+file[-4:]), imgEnhanced)
        endTime = time.time()
        print('cost:', endTime-startTime, 'sec')