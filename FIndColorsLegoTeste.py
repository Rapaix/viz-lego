import cv2 as cv
import numpy as np

log = {}
arr = []


def main():
    redColor = (0, 0, 255)
    yellowColor = (0, 255, 255)
    greenColor = (0, 255, 0)
    cyanColor = (255, 255, 0)
    blueColor = (255, 0, 0)
    purpleColor = (130, 0, 75)
    magentaColor = (255, 0, 255)

    # funcao para boundingBox de cor


    def boundingColor(maskColor, color):


        edge = cv.Canny(maskColor,100, 200)


        (cnts, hierarchy) = cv.findContours(maskColor, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:10]
        for c in cnts:
            area = cv.contourArea(c)
            #rect = cv.minAreaRect(c)
            #print(rect)
            #(xa, ya), (wa, ha), _ = rect
            peri = cv.arcLength(c, True)
            approx = cv.approxPolyDP(c, 0.05*peri, True)
            #corrigir

            if area > 300:

                x, y, w, h = cv.boundingRect(c)
                rect = cv.minAreaRect(c)
                box = cv.boxPoints(rect)
                box = np.int0(box)
                #print(xa,ya, wa,ha)
                print(x,w,w,h)
                M = cv.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                cv.rectangle(frame, (x, y), (x + w, y + h), (color), 1)
                cv.drawContours(frame, [box],0, (255,0,255),2)
                #cv.line(copy,(x,y), (x+w,y+h),(redColor), 2)
                #cv.circle(copy, (cX, cY), 1, (color), -1)


    #funcao de desenho de todas as cores
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
                    cv.rectangle(copy, (x, y), (x+w, y+h), (255, 255, 255), 1)

    # canvas de desenho para as mascaras ser desenhadas
    cap = cv.VideoCapture("videos/videoTeste6.webm")

    print("Escolhar o highlight\n 1- amarelo\t 2- vermelho\n 3- verde\t"
          " 4- cyan\n 5- roxo\t 6- azul\n 7- magenta\t 8 - todas as cores\n 0- Sair")


    while (cap.isOpened()):

        ret,frame = cap.read()
        frame = cv.flip(frame,-1)

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

        # Aquisição da imagem

        #img = cv.imread('images/lego.jpg')
        w, h, _ = frame.shape
        copy = cv.resize(frame.copy(), (w,h))
        blur = cv.GaussianBlur(copy, (5,5), 1.5)
        hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
        blank = np.zeros((hsv.shape[0], hsv.shape[1]), np.uint8)



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




        #draw(arr)


        k = cv.waitKey(33)
        if k == 49: #tecla 1
            boundingColor(yellow, yellowColor)
        elif k == 50:#tecla 2
            boundingColor(red, redColor)
        elif k == 51:   #tecla 3
            boundingColor(green, greenColor)
        elif k == 52:   #tecla 4
            boundingColor(cyan, cyanColor)
        elif k == 53:   #tecla 5
            boundingColor(purple, purpleColor)
        elif k == 54:   #tecla 6
            boundingColor(blue, blueColor)
        elif k == 55:  #tecla 7
            boundingColor(magenta, magentaColor)
        elif k == 48:   #tecla 0
            draw(arr)
        elif k == 27:
            break


        cv.imshow("img", maskTotal)
        frame = copy.copy()
        cv.imshow("frame", frame)


    cap.release()
    cv.destroyAllWindows()

#transformar as cores em um dicionario para pegar os nomes das cores
if __name__ == '__main__':
    main()


"""
To do:

melhorar o pre-processamento da imagem, deixar ela mais limpa
colocar em video



"""