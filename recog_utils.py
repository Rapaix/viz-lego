import cv2 as cv, cv2
import numpy as np
import argparse

TEMPLATE_NAME = "template.jpg"
HAND_COLOR_NAME = "handmean.pkl"
font = cv2.FONT_HERSHEY_SIMPLEX
FONT_COLOR = (18, 255, 15) #(18, 127, 15)
thickness = 1
top_position = (20,20)

def parser_arg():
    parser = argparse.ArgumentParser(description='Hand Color extraction for detection')
    parser.add_argument('-v', dest='video_path',help='path to video file (empty for live feed)')
    parser.add_argument('-debug', default=False, dest='debug',
                        help='debug boolean flag, only for development, as it slows everything and more')
    return parser.parse_args()


def getvideocap(args):
    if args.video_path:
        return cv.VideoCapture(args.video_path), None
    else:
        return cv.VideoCapture(0), None  # TODO: check if is number or path for video interface


def savetemplate(frame):
    cv.imwrite(TEMPLATE_NAME, frame)


def gettemplate():
    return cv.imread(TEMPLATE_NAME, 1)


def drawControls(img, cont=None, state="stopped"):
    max_x, max_y = int(img.shape[0]), int(img.shape[1])
    ratio_x = max_x // 10
    ratio_y = max_y // 10
    cv2.putText(img, 'f - forward', (max_y - 3 * ratio_y, ratio_x * 2), font, .5, FONT_COLOR, thickness, cv2.LINE_AA)
    cv2.putText(img, 's - stop', (max_y - 3 * ratio_y, ratio_x * 3), font, .5, FONT_COLOR, thickness, cv2.LINE_AA)
    cv2.putText(img, 'c - capture template', (max_y - 3 * ratio_y, ratio_x * 4), font, .5, FONT_COLOR, thickness, cv2.LINE_AA)
    cv2.putText(img, 'Esc or q - exit', (max_y - 3 * ratio_y, ratio_x * 5), font, .5, FONT_COLOR, thickness, cv2.LINE_AA)
    if cont:
        cv2.putText(img, "state: " + state + " | frame: " + str(cont), top_position, font, .5, FONT_COLOR, thickness, cv2.LINE_AA)

    return img

def control(userchar, s=None, t=None):
    state = s
    timeskip = t
    if userchar == ord('s'):  # stop
        state, timeskip = "stopped",0
    elif userchar == ord('f'):  # forward
        state = "forward"
        timeskip = 10
    elif userchar == ord('c'):  # capture
        state = "captured"
        timeskip = 0
        savetemplate(frame)
    # 27 -> Esc
    elif userchar == 27 or userchar == ord('q'):  # exit
        return (None, None)
    return state, timeskip


if __name__ == "__main__":
    args = parser_arg()
    cap, _ = getvideocap(args)

    timeskip = 0
    cont = 1
    state = "stopped"
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv.flip(frame, 1)

        cv.imshow("Capture Template", drawControls(frame.copy(), cont, state))

        k = cv.waitKey(timeskip)
        state, timeskip = control(k,state,timeskip)
        while state == "stopped":
            k = cv.waitKey(timeskip)
            state, timeskip = control(k,state,timeskip)
        if state is None:
            break
        cont += 1
