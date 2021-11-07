from __future__ import print_function
from deepface import DeepFace as df
import argparse
import time
import json
from urllib.request import urlopen
import sys, getopt
import os
import cv2


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
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))    # added this line 
        success,image = vidcap.read()
        if success ==False :
            break 
        print ('Read a new frame: ', success)
        framesList.append(image)

        cv2.imwrite( outputFilePath + "\\frame%d.jpg" % count, image)     # save frame as JPEG file
        count = count + 1
    
    obj = df.analyze(img_path = framesList, actions = ['emotion'],enforce_detection= False)
    print(obj)

    obj = {'obj': obj}

    with open(outputFilePath+'_emotions.txt', 'w') as file:
        file.write(json.dumps(obj)) # use `json.loads` to do the reverse
    file.close()


if __name__ == "__main__":
   main(sys.argv[1:])



