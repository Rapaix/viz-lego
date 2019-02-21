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


def drawlog(img, metric_mae, cont=None):
    max_x, max_y = int(img.shape[0]), int(img.shape[1])
    cv.putText(img, 'mae: ' + str(metric_mae), rec.top_position, rec.font, .5,
               rec.FONT_COLOR, rec.thickness, cv.LINE_AA)
    if cont:
        cv.putText(img, "frame: " + str(cont), (50,50), rec.font, .5, rec.FONT_COLOR, rec.thickness, cv.LINE_AA)

    return img

def extractcolor(base_frame, images):
    handcolors = []

    for i in range(len(images)):
        frame = cv.cvtColor(images[i], cv.COLOR_BGR2RGB)

        # isolating differences of hand on template
        diff = cv.convertScaleAbs(base_frame.astype(np.int16) - frame)
        non_zero_condition = diff < 50
        non_zero = 255 - (non_zero_condition.astype(np.int) * (255, 255, 255))
        mask = cv.convertScaleAbs(frame & non_zero)  # get hand on black background

        # clustering colors
        # TODO: declare kmeans estimator here or before the loop?
        kmeans_cluster = cluster.KMeans(n_clusters=2) # without black the clusters tend to organize on a red hue
        flat_frame = np.reshape(mask, (mask.shape[0] * mask.shape[1], mask.shape[2]))

        non_zero_flat_indexes = np.mean(flat_frame > [10, 10, 10], axis=1).astype(
            np.bool)  # eliminating black portion (speeds up a lot)
        flat_frame = flat_frame[non_zero_flat_indexes]
        kmeans_cluster.fit(flat_frame)
        cluster_centers = kmeans_cluster.cluster_centers_

        colors = np.asarray(cluster_centers, np.uint8)
        handcolors.append(colors[np.argmax(colors[:, 0])])  # add the redish color (color near the hand)
        if i % 5 == 0:
            print("processing: " + str(i) + "/" + str(len(images)), end="\r")

    handcolors = np.asarray(handcolors, dtype=np.float)
    return np.asarray(([np.mean(handcolors[:, i]) for i in range(3)]), dtype=np.uint8)  # average by channel


if __name__ == "__main__":
    args = parser_arg()
    DEBUG_FLAG = args.debug
    cap, _ = rec.getvideocap(args)

    cv.namedWindow("main")
    cv.moveWindow("main", 300, 30)  # Move it to (40,30)

    timewait=args.waitkey

    template_frame = rec.gettemplate()
    cont = 1
    video_buffer = []
    mae_buffer = []
    while cap.isOpened():

        ret, frame = cap.read()
        frame = cv.flip(frame, 1)

        mae = MAE(template_frame, frame)

        if mae > 60: # TODO: discuss or learn this valor
            print("saved frame", cont)
            mae_buffer.append(mae)
            video_buffer.append(frame)
            print("saved: " + str(len(video_buffer)))

        #print_pic = drawlog(frame.copy(), mae, cont)
        cv.imshow("main", drawlog(frame.copy(), mae, cont))

        k = cv.waitKey(timewait)
        # 27 -> Esc
        if k == 27 or k == ord('q') or cont == 500 or len(video_buffer) == 20:  # TODO: discuss this valor
            break
        # if cont == 320:
        #     cv.imwrite("print.jpg", print_pic)
        if cont % 100 == 0:
            print("frame:" + str(cont))
        cont += 1

    cap.release()
    cv.destroyAllWindows()

    # save results if necessary
    # if DEBUG_FLAG:
    #     pickle.dump({"mae": mae_buffer, "images": video_buffer}, open("handextraction.pkl", "+wb"))

    finalhandcolor = extractcolor(template_frame,video_buffer)
    #save for next script
    pickle.dump(finalhandcolor, open(rec.HAND_COLOR_NAME, "+wb"))
    print("saved hand color")


