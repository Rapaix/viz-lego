import cv2 as cv
import numpy as np
import json

log = []
arr = np.array([])
color_log = []


redColor = (0, 0, 255)
yellowColor = (0, 255, 255)
greenColor = (0, 255, 0)
cyanColor = (255, 255, 0)
blueColor = (255, 0, 0)
purpleColor = (130, 0, 75)
magentaColor = (255, 0, 255)

# Testar HSV_FULL

magenta_lower = np.array([0, 100, 0], np.uint8)
magenta_upper = np.array([15, 255, 255], np.uint8)

yellow_lower = np.array([20, 60, 100], np.uint8)
yellow_upper = np.array([35, 255, 255], np.uint8)

green_lower = np.array([40, 100, 0], np.uint8)
green_upper = np.array([90, 255, 255], np.uint8)

cyan_lower = np.array([75, 100, 0], np.uint8)
cyan_upper = np.array([95, 255, 255], np.uint8)

blue_lower = np.array([84, 100, 0], np.uint8)
blue_upper = np.array([125, 255, 255], np.uint8)

purple_lower = np.array([126, 100, 0], np.uint8)
purple_upper = np.array([165, 255, 255], np.uint8)

red_lower = np.array([169, 100, 0], np.uint8)
red_upper = np.array([180, 255, 255], np.uint8)




# funcao para boundingBox de cor

cap = cv.VideoCapture("videos/videoLego1.webm")

def boundingColor(maskColor, color, cor):

    edge = cv.Canny(maskColor,100, 200)

    #cv.imshow("edge", edge)
    (cnts, hierarchy) = cv.findContours(maskColor, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:10]

    for c in cnts:
        area = cv.contourArea(c)

        if area > 300:

            x, y, w, h = cv.boundingRect(c)
            rect = cv.minAreaRect(c)
            box = cv.boxPoints(rect)
            box = np.int0(box)

            log.append({"x_Axis":x, "y_Axis":y,"width":w, "Height":h, "color":cor})
            #jason = json.dumps("x_Axis":x, "y_Axis":y,"width":w, "Height":h, "color":cor)
            color_log.append(color)
            cv.rectangle(copy, (x, y), (x + w, y + h), (color), 2)
            cv.drawContours(blank, [box], 0, (color), 2)



#funcao de desenho de todas as cores
def draw(image):

        (cnts, _) = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            area = cv.contourArea(c)
            if area > 300:
                x, y, w, h = cv.boundingRect(c)
                # usar no  ambiente de interação(pegar um Roi e ) faz o draw nele para retorna um roi para verfical

                rect = cv.rectangle(copy, (x, y), (x + w, y + h), (255, 255, 255), 1)

        return x, y, w, h



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
    roi_image = hsv[0:300, 0:100]

    (y, x, _) = hsv.shape

    cv.imshow("roi", roi_image)

    blank = np.zeros(hsv.shape)

    # range of colors
    #Analisar estrutura
    red = cv.inRange(hsv, red_lower, red_upper)
    yellow = cv.inRange(hsv, yellow_lower, yellow_upper)
    green = cv.inRange(hsv, green_lower, green_upper)
    cyan = cv.inRange(hsv, cyan_lower, cyan_upper)
    blue = cv.inRange(hsv, blue_lower, blue_upper)
    purple = cv.inRange(hsv, purple_lower, purple_upper)
    magenta = cv.inRange(hsv, magenta_lower, magenta_upper)

    sumRed = red + magenta


    # soma de todas as ranges para uma imagem
    maskTotal = red + yellow + green + cyan + blue + purple + magenta
    teste = maskTotal[0:300, 0:100]
    x, y, w, h = draw(teste)

    colors = cv.bitwise_and(copy, copy, mask=maskTotal)

    roi = hsv[y:y + h, x:x + w]

    cv.imshow("roi", roi)
    #draw(arr)
    
    comom = np.bincount(np.ravel(roi[:, :, 0])).argmax()

    print(comom)

    if comom >= 0 and comom <= 15:
        boundingColor(red, redColor,"red")
    elif comom >= 20 and comom <= 35:
        boundingColor(yellow, yellowColor, "yellow")
    elif comom >= 36 and comom <= 90:
        boundingColor(green, greenColor, "green")
    elif comom >= 75 and comom <= 95:
        boundingColor(cyan, cyanColor, "cyan")
    elif comom >= 84 and comom <= 130:
        boundingColor(blue, blueColor, "blue")
    elif comom >= 126 and comom <= 165:
        boundingColor(purple, purpleColor, "purple")
    elif comom >= 169 and comom <= 180:
        boundingColor(magenta, magentaColor, "magenta")

    k = cv.waitKey(25)
    if k == 27:
        break


    cv.imshow("img", blank)
    cv.imshow("frame", copy)
    cv.imshow("roi", roi)


#print(json.dumps(log, indent=4))
#print(len(log))
cap.release()

cv.destroyAllWindows()
""""
transformar as cores em um dicionario para pegar os nomes das cores
To-do 
-> fazer slice na imagem quando for desenhar
-> verificar script das mãos para usar

"""
