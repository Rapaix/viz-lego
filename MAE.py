import glob
import numpy as np
import cv2 as cv


def calculateMAE(imgA, imgB):

    mae = np.sum(np.absolute((imgB.astype("float")-imgA.astype("float"))))
    mae /= float(imgA.shape[0] * imgA.shape[1]*255)
    if mae < 0:
        return mae * -1
    else:
        return mae


img = cv.imread("images/img.jpg")
imgteste = cv.imread("images/imgteste.jpg")
img = cv.resize(img,(300, 300))
imgteste = cv.resize(imgteste, (300, 300))
cv.imshow("img", img)
cv.imshow("teste", imgteste)

print(calculateMAE(img, imgteste))

cv.waitKey(0)
cv.destroyAllWindows()

