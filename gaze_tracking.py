
import cv2, os
from GazeTracking.gaze_tracking import GazeTracking
import numpy as np

inputFilePath = "/media/openface/datastorage/data/video/myself.mp4"
outputFilePath = "output/gaze"
ms_delay=100
gaze = GazeTracking()


inputFileName = os.path.basename(inputFilePath)

count = 0
vidcap = cv2.VideoCapture(inputFilePath)
success,image = vidcap.read()
success = True

cap = cv2.VideoCapture(inputFilePath)


try:
    os.mkdir(outputFilePath)
except:
    print("output directory is not empty")



framesList=[]
while True:

    vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*ms_delay))    # added this line
    success,image = vidcap.read()
    if success ==False:
        break 
    print ('Read a new frame: ', success)

    gaze.refresh(image)

    frame = gaze.annotated_frame()
    text = ""

    # cv2.imshow("test", np.array(frame, dtype = np.uint8 ))



    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)
    if cv2.waitKey(1) == 27:
        break




    framesList.append(frame)
    cv2.imwrite( outputFilePath + "/frame%d.jpg" % count, frame)     # save frame as JPEG file
    count = count + 1
    