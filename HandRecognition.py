import cv2 as cv
import numpy as np

cap =  cv.VideoCapture(0)


def makeHandMask(img):
    gray= cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5,5), 0)
    _, threshold = cv.threshold( blurred, 90,255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)

    return threshold

def findHand(img):
    _, cnts, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key=lambda x: cv.contourArea(x))
    hull = cv.convexHull(c)
    moments = cv.moments(c)
    if moments != 0:
        cx = int(moments['m10']/moments['m00'])
        cy = int(moments['m01']/moments['m00'])

    center = (cx,cy)
    cv.circle(frame,center,5,[0,0,255],2)
    cv.drawContours(frame,[c],0 ,(255,0,0),2)
    cv.drawContours(frame,[hull],0,(0,0,255),2)
    hull = cv.convexHull(c, returnPoints=False)
    defects  = cv.convexityDefects(c,hull)
    mind =0
    maxd =0
    i=0

    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(c[s][0])
        end = tuple(c[e][0])
        far = tuple(c[f][0])
        dist = cv.pointPolygonTest(c, center, True)
        cv.line(frame, start,end,[0,255,255],2)
        cv.circle(frame, far, 5, [255,255,0],-1)
        colors = hsv[center]
        upper = np.array([colors[0] + 10, colors[1] + 10, colors[2] + 40])
        lower = np.array([colors[0] - 10, colors[1] - 10, colors[2] - 40])
        print(lower, colors, upper)


while(cap.isOpened()):

    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    img = makeHandMask(frame)
    findHand(img)
    cv.imshow('img', img)
    cv.imshow('frama', frame)
    k = cv.waitKey(10)# Esc
    if k == 27:
        break

