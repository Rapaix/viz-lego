import cv2 as cv
import numpy as np

log = {}

def main():
    redColor = (0, 0, 255)
    yellowColor = (0, 255, 255)
    greenColor = (0, 255, 0)
    cyanColor = (255, 255, 0)
    blueColor = (255, 0, 0)
    purpleColor = (130, 0, 75)
    magentaColor = (255, 0, 255)

    # funcao para boundingBox

    def boundingColor(img2, maskColor, color):
        (_, cnts, hierarchy) = cv.findContours(maskColor, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            area = cv.contourArea(c)
            if area > 300:
                x, y, w, h = cv.boundingRect(c)
                M = cv.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                print(color, "cY:", cY, "cX", cX)
                log[color] = cX

                teste = cv.rectangle(img2, (x, y), (x + w, y + h), (color), 2)
                cv.circle(img2, (cX, cY), 1, (color), -1)
                return cv.imshow("teste", teste)

    # Aquisição da imagem
    img = cv.imread('images/lego.jpg')
    copy = cv.resize(img.copy(), (300, 300))
    cv.imshow("img", copy)
    hsv = cv.cvtColor(copy, cv.COLOR_BGR2HSV)

    # canvas de desenho para as mascaras ser desenahadas
    blank = np.zeros((hsv.shape[0], hsv.shape[1]), np.uint8)

    red_lower = np.array([0, 100, 0], np.uint8)
    red_upper = np.array([15, 255, 255], np.uint8)

    yellow_lower = np.array([20, 60, 100], np.uint8)
    yellow_upper = np.array([35, 255, 255], np.uint8)

    green_lower = np.array([50, 100, 0], np.uint8)
    green_upper = np.array([80, 255, 255], np.uint8)

    cyan_lower = np.array([75, 100, 0], np.uint8)
    cyan_upper = np.array([95, 255, 255], np.uint8)

    blue_lower = np.array([84, 100, 0], np.uint8)
    blue_upper = np.array([125, 255, 255], np.uint8)

    purple_lower = np.array([126, 100, 0], np.uint8)
    purple_upper = np.array([165, 255, 255], np.uint8)

    magenta_lower = np.array([170, 100, 0], np.uint8)
    magenta_upper = np.array([180, 255, 255], np.uint8)

    # range of colors

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
    edge = cv.Canny(maskTotal, 10 ,200)
    colors = cv.bitwise_and(copy, copy, mask=maskTotal)

    cv.imshow(" maskara", blue)




    print("Escolhar o highlight\n 1- amarelo\n 2- vermelho\n 3- verde\n 4- cyan\n 5-roxo\n 6- azul\n 7- magenta\n 8 - todas as cores\n 0- Sair")

    #boundingColor(copy, red, redColor)
    #boundingColor(copy, yellow, yellowColor)
    #boundingColor(copy, green, greenColor)
    #boundingColor(copy, cyan, cyanColor)
    #boundingColor(copy, purple, purpleColor)
    #boundingColor(copy, blue, blueColor)
    #boundingColor(copy, magenta, magentaColor)

    while(1):
        k = cv.waitKey(33)
        if k == 49:
            boundingColor(copy.copy(), yellow, yellowColor)
        elif k == 50:
            boundingColor(copy.copy(), red, redColor)
        elif k == 51:
            boundingColor(copy.copy(), green, greenColor)
        elif k == 52:
            boundingColor(copy.copy(), cyan, cyanColor)
        elif k == 53:
            boundingColor(copy.copy(), purple, purpleColor)
        elif k == 54:
            boundingColor(copy.copy(), blue, blueColor)
        elif k == 55:
            boundingColor(copy.copy(), magenta, magentaColor)
        elif k == 27:
            break

        frame = copy.copy()
        #for c,v in enumerate(dict):
         #   if v:
         #       dict[c]["color"]


    print("log:", log)
    print(sorted(log.values()))

    cv.waitKey(0)
    cv.destroyAllWindows()

#transformar as cores em um dicionario para pegar os nomes das cores
if __name__ == '__main__':
    main()
