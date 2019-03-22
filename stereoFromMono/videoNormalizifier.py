
import cv2
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path

VIDEO_FOLDER = Path('C:/Users/Navarre/Desktop/videosForComputerVision/')
LEFT_VIDEO = VIDEO_FOLDER / 'left2.mpeg'
RIGHT_VIDEO = VIDEO_FOLDER / 'right2.mpeg'
num_disp = 16
block_size = 33

class videoNormalizifier:

    def __init__(self, leftVideo, rightVideo):
        print(leftVideo)
        capL = cv2.VideoCapture(str(leftVideo))
        capR = cv2.VideoCapture(str(rightVideo))
        countL = int(capL.get(cv2.CAP_PROP_FRAME_COUNT))
        countR = int(capR.get(cv2.CAP_PROP_FRAME_COUNT))
        total = min(countL,countR)

        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        out = cv2.VideoWriter('output.avi', fourcc, 29.97, (752, 480))

        stereo = cv2.StereoBM_create(numDisparities=num_disp, blockSize=block_size)

        elapsed = 0
        while(capL.isOpened()):

            # Capture frame-by-frame, use returned value to indicate file is done
            retL,frameL = capL.read()
            retR,frameR = capR.read()


            #operations to apply to each frame go here

            if retL == True and retR == True:

                elapsed += 1
                print("Frame {}/{}".format(elapsed, total) )

                grayL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)
                grayR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)

                grayL = cv2.normalize(grayL, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
                grayR = cv2.normalize(grayR, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

                disparity = stereo.compute(grayL, grayR)

                minimum = disparity.min()
                maximum = disparity.max()
                disparity = np.uint8(255 * (disparity - minimum) / (maximum - minimum))

                disparity = cv2.applyColorMap(disparity, cv2.COLORMAP_JET)
                out.write(disparity)

            else:
                break

        print('Finished Main Loop')
        capL.release()
        capR.release()
        out.release()
        cv2.destroyAllWindows()




if __name__ == '__main__':
    vn = videoNormalizifier(LEFT_VIDEO,RIGHT_VIDEO)