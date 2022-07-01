from __future__ import print_function

import csv
import getopt
import json
import os
import sys
from datetime import datetime, timedelta
import time
import cv2
from deepface import DeepFace as df
from emonet.basic import emonet_analysis


# this function has been copied to {workspace}/bicyclewebsite/dataportal/generate_raw_results.py
#please update that file from now on, this is just for record keeping / testing
























def emotions(inputFile,outputFile):

    
    ms_delay = 1000 # Change this to increase or decrease the frame emotion sampling rate
    def creation_date(path_to_file):
        return os.path.getctime(path_to_file)


    def starting_time_from_title(file_name):
        print(f"double checking the passing through went smoothly: {file_name}\n")
        day = int(file_name[0:2])
        month = int(file_name[2:4])
        year = int(file_name[4:8])
        hours = int(file_name[8:10])
        minutes = int(file_name[10:12])
        seconds = int(file_name[12:14])
        print(f"day:{day} month: {month} year: {year}\n")
        combined = datetime(year,month,day,hours,minutes, seconds)

        return combined

   
    inputFilePath = inputFile
    outputFilePath = outputFile

    #comment block: command line input
    # try:
    #     opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    # except getopt.GetoptError:
    #     print('test.py -i <inputfile> -o <outputfile>')
    #     sys.exit(2)
    # for opt, arg in opts:
    #     if opt == '-h':
    #         print('emotion_detection_deepface.py -i <input_vid> -o <out_jpg_folder>')
    #         sys.exit()
    #     elif opt in ("-i", "--ifile"):
    #         inputFilePath = arg
    #     elif opt in ("-o", "--ofile"):
    #         outputFilePath = arg
    # print('Input file is "' + inputFilePath)
    # print('Output file is "' + outputFilePath)
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
        framesList.append(image)

        cv2.imwrite( outputFilePath + "/frame%d.jpg" % count, image)     # save frame as JPEG file
        count = count + 1
    
    #analyse frame
    
    emonet_results = emonet_analysis(outputFilePath)


    dominantEmotions =[]
    valence = []
    arousal = []
    
    for instance in emonet_results: #iterate through each frame and pick domininant emotions to add to a list 
        dominantEmotions.append(instance['emo_pred'])
        bob = instance['valence_pred'][0]
        bob = bob.item()
        valence_num = instance['valence_pred'][0]
        arousal_num = instance['arousal_pred'][0]
        valence.append(valence_num.item())
        arousal.append(arousal_num.item())

        #To Tyler: data structure of results are below
            #     result= {"filename":i, 
            # "expression_pred" : expression_pred, 
            # "valence_pred" : valence_pred, 
            # "arousal_pred" : arousal_pred,
            # "emo_pred" : emo_pred }

    # Tyler code addition
    # This section pulls the creation or modified date of the video files being analysed and converts it into readable format
    # It also adds a variable (currently 1000ms) of time to the time variable for each frame
    # Can use inputFilePath from earlier to save on redundant code

    start_time = starting_time_from_title(inputFileName)
    # This section is somewhat shelved for now as the creation and modified date is unreliable
    # creation = creation_date(file_name)
    # print(f"Entire date and time pulled: {datetime.fromtimestamp(creation).strftime('%d/%m/%y , %H-%M-%S')}\n")
    #initial_timestamp = datetime.fromtimestamp(start_time)#.strftime('%H:%M:%S')
    initial_timestamp = time.mktime(start_time.timetuple()) #converting to uint_32 to add time and then convert for the csv work
    initial_timestamp = datetime.fromtimestamp((initial_timestamp))
    additional_time = timedelta(seconds = ms_delay/1000) # adding 1 second with the division but keeping the variables consistent
    list_length = len(dominantEmotions)
    times = []
    i = 0
    # Creating a list of all the times that will be pushed into the csv file
    while i < list_length:
        times.append(initial_timestamp.strftime('%H:%M:%S'))
        i = i + 1
        initial_timestamp = initial_timestamp + additional_time
    with open(outputFilePath+'/dominant_emotions.txt', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(dominantEmotions)
        writer.writerow(arousal)
        writer.writerow(valence)
        writer.writerow(times)
    f.close()

    #emonet = {'emonet_results': emonet_results}
    #with open(outputFilePath+'/emotions.txt', 'w') as file:
    #   file.write(json.dumps(emonet)) # use `json.loads` to do the reverse
    #file.close()


emotions("/media/openface/datastorage/data/10022022121421.MP4","output/ana")
# emotions("/media/openface/datastorage/data/video/copy.mp4","pilottest")

