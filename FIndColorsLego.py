import cv2 as cv
import numpy as np

log = []
arr = []


def main():
    redColor = (0, 0, 255)
    yellowColor = (0, 255, 255)
    greenColor = (0, 255, 0)
    cyanColor = (255, 255, 0)
    blueColor = (255, 0, 0)
    purpleColor = (128, 0, 128)
    magentaColor = (255, 0, 255)

    # funcao para boundingBox

    def boundingColor(maskColor, color, cor):

        (cnts, hierarchy) = cv.findContours(maskColor, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            area = cv.contourArea(c)
            if area > 300:
                x, y, w, h = cv.boundingRect(c)
                M = cv.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                log.append({"x_Axis": x, "y_Axis": y, "width": w, "Height": h, "color": color})
                cv.rectangle(blank, (x, y), (x + w, y + h), (color), -1)
                cv.rectangle(copy, (x, y), (x + w, y + h), (color), 2)
                cv.circle(copy, (cX, cY), 1, (color), -1)

    def draw(vetor_de_imagens):
        #for d in dict:
            #flag = dict[d]
            #if flag == True:
                #print("->", flag)
                for i in vetor_de_imagens:
                    (cnts, _) = cv.findContours(i, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                    for c in cnts:
                        area = cv.contourArea(c)
                        if area > 300:
                            x, y, w, h = cv.boundingRect(c)
                            cv.rectangle(copy, (x, y), (x+w, y+h), (255, 255, 255), 0)

    def ajusteGamma(image, gamma=0.5):
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")

        return cv.LUT(image, table)

    # Aquisição da imagem
    img = cv.imread('images/lego_revis1.jpg')
    copy = cv.resize(img.copy(), (300, 300))
    copy = cv.flip(copy, -1)
    copy = ajusteGamma(copy,1.5)
    hsv = cv.cvtColor(copy, cv.COLOR_BGR2HSV)

    # canvas de desenho para as mascaras ser desenahadas
    blank = np.zeros(hsv.shape)

    red_lower = np.array([0, 100, 0], np.uint8)
    red_upper = np.array([15, 255, 255], np.uint8)

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

    magenta_lower = np.array([169, 100, 100], np.uint8)
    magenta_upper = np.array([189, 255, 255], np.uint8)

    # range of colors

    red = cv.inRange(hsv, red_lower, red_upper)
    arr.append(red)
    yellow = cv.inRange(hsv, yellow_lower, yellow_upper)
    arr.append(yellow)
    green = cv.inRange(hsv, green_lower, green_upper)
    arr.append(green)
    cyan = cv.inRange(hsv, cyan_lower, cyan_upper)
    arr.append(cyan)
    blue = cv.inRange(hsv, blue_lower, blue_upper)
    arr.append(blue)
    purple = cv.inRange(hsv, purple_lower, purple_upper)
    arr.append(purple)
    magenta = cv.inRange(hsv, magenta_lower, magenta_upper)
    arr.append(magenta)
    sumRed = red + magenta

    # soma de todas as ranges para uma imagem
    maskTotal = red + yellow + green + cyan + blue + purple + magenta
    colors = cv.bitwise_and(copy, copy, mask=maskTotal)


    print("Escolhar o highlight\n 1- amarelo\t 2- vermelho\n 3- verde\t"
          " 4- cyan\n 5- roxo\t 6- azul\n 7- magenta\t 8 - todas as cores\n 0- Sair")

    draw(arr)

    while(1):
        k = cv.waitKey(33)
        if k == 49: #tecla 1
            boundingColor(yellow, yellowColor, "amarelo")

        elif k == 50:#tecla 2
            boundingColor(red, redColor, "vermelho")
        elif k == 51:   #tecla 3
            boundingColor(green, greenColor, "verde")
        elif k == 52:   #tecla 4
            boundingColor(cyan, cyanColor, "ciano")
        elif k == 53:   #tecla 5
            boundingColor(purple, purpleColor, "roxo")
        elif k == 54:   #tecla 6
            boundingColor(blue, blueColor, "azul")
        elif k == 55:  #tecla 7
            boundingColor(magenta, magentaColor, "magenta")
        elif k == 48:   #tecla 0
            draw(arr)
        elif k == 27:
            break


        frame = copy.copy()
        cv.imshow("blank", blank)
        cv.imshow("frame", frame)
        #cv.imwrite("blank.jpg", blank)
        #cv.imshow("verde", maskTotal)





        #for c,v in enumerate(dict):
        #   if v:
        #       dict[c]["color"]

    print(log)


    cv.waitKey(0)
    cv.destroyAllWindows()

#transformar as cores em um dicionario para pegar os nomes das cores
if __name__ == '__main__':
    main()