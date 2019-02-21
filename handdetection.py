import pickle

import cv2 as cv
import numpy as np
import argparse
import recog_utils as rec
from metrics import MAE
from sklearn import cluster

DEBUG_FLAG = False

def parser_arg():
    parser = argparse.ArgumentParser(description='Hand Color detection for Lego Visualization')
    parser.add_argument('-v', dest='video_path', help='path to video file (empty for live feed)')
    parser.add_argument('-debug', default=False, dest='debug',
                        help='debug boolean flag, only for development, as slowdown everything and more')
    parser.add_argument('-w', dest='waitkey', default=1, help='frame by frame miliseconds passage')
    return parser.parse_args()


def getchandcolor():
    return pickle.load(open(rec.HAND_COLOR_NAME, "rb"))


def drawlogs(img, hashand=False, debug=None):
    cv.putText(img, "Reconhece lego(cena sem maos)? : " + str(not hashand),
               (50, 50), rec.font, .3, rec.FONT_COLOR, rec.thickness, cv.LINE_AA)
    return img


def scenehashand(img, c, t=None):
    cond1 = img < c + 10
    cond2 = img > c - 10
    a = (cond1 & cond2)
    cont = np.count_nonzero(a)
    return cont > t if t else cont
    # if t:
    #     return cont > t
    # else:return cont


if __name__ == "__main__":
    args = parser_arg()
    DEBUG_FLAG = args.debug
    cap, _ = rec.getvideocap(args)

    cv.namedWindow("main")
    cv.moveWindow("main", 300, 30)  # Move it to (40,30)

    timewait=args.waitkey

    template_frame = rec.gettemplate()
    handcolor = getchandcolor()
    cont = 1
    base_hand_val = scenehashand(template_frame, handcolor) * 5
    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv.flip(frame, 1)

        isHand= scenehashand(frame, handcolor, base_hand_val)
        cv.imshow("main", drawlogs(frame, isHand))

        k = cv.waitKey(timewait)
        # 27 -> Esc
        if k == 27 or k == ord('q'):
            break
        if cont % 100 == 0:
            print("frame:" + str(cont))
        cont += 1


    cap.release()
    cv.destroyAllWindows()