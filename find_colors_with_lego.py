import cv2 as cv
import numpy as np
import json
from operator import itemgetter

log = []
color_log = []

#RGB das cores

redColor = (0, 0, 255)
yellowColor = (0, 255, 255)
orangeColor = (0, 165, 255)
greenColor = (0, 255, 0)
cyanColor = (255, 255, 0)
blueColor = (255, 0, 0)
purpleColor = (130, 0, 75)
magentaColor = (255, 0, 255)

# limite de cores no HSV

magenta_lower = np.array([0, 100, 0], np.uint8)
magenta_upper = np.array([10, 255, 255], np.uint8)

orange_lower = np.array([10,100,0], np.uint8)
orange_upper = np.array([20,255,255], np.uint8)

yellow_lower = np.array([20, 60, 100], np.uint8)
yellow_upper = np.array([35, 255, 255], np.uint8)

green_lower = np.array([32, 100, 0], np.uint8)
green_upper = np.array([90, 255, 255], np.uint8)

cyan_lower = np.array([90, 100, 0], np.uint8)
cyan_upper = np.array([95, 255, 255], np.uint8)

blue_lower = np.array([95, 100, 0], np.uint8)
blue_upper = np.array([125, 255, 255], np.uint8)

purple_lower = np.array([126, 100, 0], np.uint8)
purple_upper = np.array([165, 255, 255], np.uint8)

red_lower = np.array([169, 100, 0], np.uint8)
red_upper = np.array([180, 255, 255], np.uint8)


cap = cv.VideoCapture(1)

#funcao que encontra a peça de lego e dar destaque
def boundingColor(maskColor, color, cor, id):


    (cnts, hierarchy) = cv.findContours(maskColor, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:10]

    for c in cnts:
        area = cv.contourArea(c)
        if area > 300:

            x, y, w, h = cv.boundingRect(c)
            rect = cv.minAreaRect(c)
            box = cv.boxPoints(rect)
            box = np.int0(box)
            M = cv.moments(c)
            cX = int(M["m10"] / M["m00"])
            if cX >=100:
                if (id in color_log):
                    pass
                else:
                    log.append({"Height": h, "color": cor, "center": cX})

            cv.rectangle(copy, (x, y), (x + w, y + h), (color), 2)
            cv.drawContours(blank, [box], 0, (color), 2)
    color_log.append(id)


#funcao que encontra contorno da peça e retorna as coordenadas do contorno
def draw(image):

        (cnts, _) = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            area = cv.contourArea(c)
            epsilon = 0.1*cv.arcLength(c,True)
            approx = cv.approxPolyDP(c, epsilon, True)
            if len(approx) == 4:
                if area > 300:

                    x, y, w, h = cv.boundingRect(c)
                    # usar no  ambiente de interação(pegar um Roi e ) faz o draw nele para retorna um roi para verficar

                    img_roi = hsv[y:y + h, x:x + w]
                    cv.imshow("roi", img_roi)
                    #retorna o valor mais recorrente da camada H
                    commom = np.bincount(np.ravel(img_roi[:, :, 0])).argmax()
                    print("commo",commom)
                    cv.rectangle(copy, (x, y), (x + w, y + h), (255, 255, 255), 1)

                    return commom


# funcao que ajusta o gamma da cena
def ajusteGamma(image, gamma=0.5):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    return cv.LUT(image, table)



while (cap.isOpened()):
    ret, frame = cap.read()
    frame = cv.flip(frame, -1)
    copy = cv.resize(frame.copy(), (300, 300))

    blur = cv.GaussianBlur(copy, (11, 11), 0)
    blur = ajusteGamma(blur, 1.5)
    hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
    roi_image = hsv[29:76, 145:217]

    (y, x, _) = hsv.shape

    #Gera as mascaras de cada cor
    red = cv.inRange(hsv, red_lower, red_upper)
    orange = cv.inRange(hsv, orange_lower, orange_upper)
    yellow = cv.inRange(hsv, yellow_lower, yellow_upper)
    green = cv.inRange(hsv, green_lower, green_upper)
    cyan = cv.inRange(hsv, cyan_lower, cyan_upper)
    blue = cv.inRange(hsv, blue_lower, blue_upper)
    purple = cv.inRange(hsv, purple_lower, purple_upper)
    magenta = cv.inRange(hsv, magenta_lower, magenta_upper)
    # juntei as duas mascaras de cor vermelha
    sumRed = red + magenta

    # soma de todas as ranges para uma imagem
    maskTotal = red + yellow + green + cyan + blue + purple + magenta + orange
    teste = maskTotal[0:300, 0:100]
    cv.line(copy, (100,0), (100,300), (0,100,255), 1)

    comom = draw(teste)

    #colors = cv.bitwise_and(copy, copy, mask=maskTotal)

    #comom = np.bincount(np.ravel(roi[:, :, 0])).argmax()

    #comom = np.random.randint(180) # Testa se reconhece as cores


    if comom == None: # Para não quebrar a execução se não tiver nada
        pass
    elif comom >= 0 and comom <= 10:
        boundingColor(sumRed, redColor,"red",1)
    elif comom >= 10 and comom <= 20:
        boundingColor(orange, orangeColor, "orange",2)
    elif comom >= 20 and comom <= 35:
        boundingColor(yellow, yellowColor, "yellow",3)
    elif comom >= 36 and comom <= 90:
        boundingColor(green, greenColor, "green",4)
    elif comom >= 75 and comom <= 95:
        boundingColor(cyan, cyanColor, "cyan",5)
    elif comom >= 84 and comom <= 130:
        boundingColor(blue, blueColor, "blue",6)
    elif comom >= 126 and comom <= 165:
        boundingColor(purple, purpleColor, "purple",7)

    new_log = sorted(log, key=itemgetter('center'))
    print(json.dumps(new_log, indent=4))
    print("*"*5)

    k = cv.waitKey(25)
    if k == 27:
        break



    cv.imshow("copy", copy)


print("tamanho", len(log))

cap.release()

cv.destroyAllWindows()

