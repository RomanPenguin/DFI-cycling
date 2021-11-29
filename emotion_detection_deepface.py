from __future__ import print_function
from deepface import DeepFace as df
import argparse
import time
import json
from urllib.request import urlopen
import sys, getopt
import os
import cv2
import csv
from datetime import datetime
from datetime import timedelta
ms_delay = 1000 # Change this to increase or decrease the frame emotion sampling rate
def creation_date(path_to_file):
    return os.path.getmtime(path_to_file)

def main(argv):
    inputFilePath = ''
    outputFilePath = 'output/emotions_analysis'
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('emotion_detection_deepface.py -i <input_vid> -o <out_jpg_folder>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputFilePath = arg
        elif opt in ("-o", "--ofile"):
            outputFilePath = arg
    print('Input file is "' + inputFilePath)
    print('Output file is "' + outputFilePath)
    inputFileName = os.path.basename(inputFilePath)

    count = 0
    vidcap = cv2.VideoCapture(inputFilePath)
    success,image = vidcap.read()
    success = True

    framesList=[]
    while True:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*ms_delay))    # added this line
        success,image = vidcap.read()
        if success ==False:
            break 
        print ('Read a new frame: ', success)
        framesList.append(image)

        cv2.imwrite( outputFilePath + "\\frame%d.jpg" % count, image)     # save frame as JPEG file
        count = count + 1
    
    obj = df.analyze(img_path = framesList, actions = ['emotion'],enforce_detection= False)
    print(obj)

    dominantEmotions =[]
    secondaryEmotions =[]
    
    for instance in obj: #iterate through each frame and pick domininant emotions to add to a list 
        dominantEmotions.append(obj[instance]['dominant_emotion'])
    # Tyler code addition
    # This section pulls the creation or modified date of the video files being analysed and converts it into readable format
    # It also adds a variable (currently 1000ms) of time to the time variable for each frame
    creation = creation_date(r"face_video.wmv")
    initial_timestamp = datetime.fromtimestamp(creation)#.strftime('%H:%M:%S')
    additional_time = timedelta(seconds = ms_delay/1000) # adding 1 second with the division but keeping the variables consistent
    list_length = len(dominantEmotions)
    times = []
    i = 0
    # Creating a list of all the times that will be pushed into the csv file
    while i < list_length:
        times.append(initial_timestamp.strftime('%H:%M:%S'))
        i = i + 1
        initial_timestamp = initial_timestamp + additional_time
    with open(outputFilePath+'_dominant_emotions.txt', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(dominantEmotions)
        writer.writerow(times)
    f.close()

    obj = {'obj': obj}
    with open(outputFilePath+'_emotions.txt', 'w') as file:
        file.write(json.dumps(obj)) # use `json.loads` to do the reverse
    file.close()


if __name__ == "__main__":
   main(sys.argv[1:])



# Save some time and copy and paste this into Terminal
# python3 emotion_detection_deepface.py -i face_video.wmv -o output/face_video_frames