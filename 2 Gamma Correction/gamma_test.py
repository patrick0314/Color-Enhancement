import os
import numpy as np
import cv2 as cv
import math

if __name__ == '__main__':

    gamma = 0.6

    ## Load Input Image
    file = os.listdir('test_image/images')

    def gamma_HSV():
        # gamma correction in HSV
        for f in file:
            img = cv.imread(os.path.join('test_image/images', f))

            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            hue, sat, val = cv.split(hsv)

            '''# compute gamma = log(mid*255)/log(mean)
            mid = 0.4
            mean = np.mean(val)
            gamma = math.log(mid*255)/math.log(mean)
            print(gamma)'''

            # do gamma correction on V channel
            # val_gamma = np.power(val, gamma).clip(0,255).astype(np.uint8)
            max_v = np.max(val)
            val_gamma = (np.power(val/max_v, gamma)*max_v).astype(np.uint8)
            # combine HSV
            hsv_gamma = cv.merge([hue, sat, val_gamma])
            img_gamma = cv.cvtColor(hsv_gamma, cv.COLOR_HSV2BGR)
            outPath = os.path.join('test_image/results', f)
            cv.imwrite(outPath, cv.hconcat([img, img_gamma]))

    def gamma_CIELUV():
        # gamma correction in CIELUV
        for f in file:
            img = cv.imread(os.path.join('test_image/images', f))

            luv = cv.cvtColor(img, cv.COLOR_BGR2LUV)
            L, U, V = cv.split(luv)

            # do gamma correction on L channel
            # L_gamma = np.power(L, gamma).clip(0,255).astype(np.uint8)
            max_L = np.max(L)
            L_gamma = (np.power(L/max_L, gamma)*max_L).astype(np.uint8)

            # combine LUV
            luv_gamma = cv.merge([L_gamma, U, V])
            img_gamma = cv.cvtColor(luv_gamma, cv.COLOR_LUV2BGR)

            outPath = os.path.join('test_image/results', f)
            cv.imwrite(outPath, cv.hconcat([img, img_gamma]))

    def gamma_YCrCb():
        # gamma correction in YCrCb
        for f in file:

            img = cv.imread(os.path.join('test_image/images', f))
            ycrcb = cv.cvtColor(img, cv.COLOR_BGR2YCrCb)
            Y, Cr, Cb = cv.split(ycrcb)

            # do gamma correction on Y channel
            # Y_gamma = np.power(Y, gamma).clip(0,255).astype(np.uint8)
            max_Y = np.max(Y)
            Y_gamma = (np.power(Y/max_Y, gamma)*max_Y).astype(np.uint8)

            # combine YCrCb
            YCrCb_gamma = cv.merge([Y_gamma, Cr, Cb])
            img_gamma = cv.cvtColor(YCrCb_gamma, cv.COLOR_YCrCb2BGR)

            outPath = os.path.join('test_image/results', f)
            cv.imwrite(outPath, cv.hconcat([img, img_gamma]))

    def gamma_RGB():
        # gamma correction in RGB
        for f in file:

            img = cv.imread(os.path.join('test_image/images', f))
            rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

            # do gamma correction on Y channel
            # Y_gamma = np.power(Y, gamma).clip(0,255).astype(np.uint8)
            max_rgb = np.max(rgb)
            rgb_gamma = (np.power(rgb/max_rgb, gamma)*max_rgb).astype(np.uint8)

            img_gamma = cv.cvtColor(rgb_gamma, cv.COLOR_RGB2BGR)

            outPath = os.path.join('test_image/results', f)
            cv.imwrite(outPath, cv.hconcat([img, img_gamma]))

    # call function
    gamma_HSV()
    gamma_CIELUV()
    gamma_YCrCb()
    gamma_RGB()