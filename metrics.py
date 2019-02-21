import numpy as np
import cv2 as cv
import glob
import shutil
import json


dst = 'D:/Documentos/Lego/repetidas'
src = "D:/Documentos/Lego/imagens/*.jpg"
data ={}

def MAE(imgA, imgB): # TODO: Verify image size and resize if different

    sum = np.sum(np.absolute(imgB.astype("float")-imgA.astype("float")))
    mean = sum/ float(imgA.shape[0] * imgA.shape[1])

    return abs(mean)

if __name__ == '__main__':
    tree = glob.glob(src)
    print(tree)

    for filename in tree:
        imgA = cv.imread(filename)
        imgA = cv.resize(imgA, (300, 300))
        for i,fl in enumerate(glob.glob(src)):
            imgB = cv.imread(fl)
            imgB = cv.resize(imgB, (300, 300))
            if filename != fl:
                mae = MAE(imgA, imgB)
                if (mae >= 0.0 and mae <=0.5):
                    shutil.move(fl, dst)
                    data.setdefault(filename, []).append(fl)
                    tree.remove(fl)



    log = json.dumps(data)
    print(log)
    with open('log.json', 'w') as outfile:
        json.dump(log, outfile)
