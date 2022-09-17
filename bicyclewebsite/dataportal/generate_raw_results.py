from __future__ import print_function
import csv
import os

import time
import json
from dataclasses import dataclass, field
from zipfile import ZipFile 

from turtle import textinput
from numpy import append
import requests
import time

from requests.auth import HTTPBasicAuth
import requests
import os, csv

import scipy as sp





import time
import boto3
import json
from urllib.request import urlopen
import csv
import json
import sys, getopt
import logging
from botocore.exceptions import ClientError
import os
from matplotlib import pyplot as plt
import matplotlib

import sys
from datetime import datetime, timedelta
import cv2
from deepface import DeepFace as df
from dataportal.emonet.basic import emonet_analysis

s3 = boto3.client('s3')


#to switch back to AWS, use generate_raw_results_aws.py instead


def raw_analysis(inputFile, outputFile, sonixKeyFile) -> None:
    #inputFile['rawAudioFile','rawVideoFile','sessionID']
    #outputFile['path_to_output_folder']


    """Main function here"""
    if inputFile['rawVideoFile'] != '':
        emotions(inputFile['rawVideoFile'],outputFile)
    if inputFile['rawAudioFile'] != '':
        transcribe(inputFile['rawAudioFile'],outputFile,sonixKeyFile)

    def zip_write(zip, filename):
        zip.write(filename, os.path.basename(filename))

    z = ZipFile(outputFile+'/'+inputFile['sessionID']+'raw.zip', 'w')
    try:
        zip_write(z, outputFile+'/dominant_emotions.txt')
    except:
        print("no emotions results")
    try:
        zip_write(z, outputFile+'/words.csv')
        zip_write(z, outputFile+'/sentences.csv')
    except:
        print("no transcription results")
    z.close()


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






def transcribe(inputFilePath,outputFilePath,sonixkeyfile):


    api_url = "https://api.sonix.ai/v1/media"

    try:
        with open(sonixkeyfile) as f:
            sonixkey = f.read().splitlines()
        # headers = {'Accept': 'application/json'}
        headers = {'Authorization': sonixkey[0]}
    except:
        print("no sonix key! please check key location")


    filename = os.path.basename(inputFilePath)
    files = {
        'file': open(inputFilePath, 'rb'),
        'language': (None, 'en'),
        'name': (None, filename)
    }

    response = requests.post('https://api.sonix.ai/v1/media', headers=headers, files=files, timeout = 180)

    uploadInfo = response.json()

    # while True:
    #     headers = {
    #     'Authorization': sonixkey[0],
    #     }

    #     response = requests.get('https://api.sonix.ai/v1/media/'+uploadInfo["id"], headers=headers)
    #     if response.json()["status_code"]=="200":
    #         break
    #     else:
    #         time.sleep(5)

    media_id = response.json()["id"]
    # /v1/media/<media id>/transcript 
    download_url = api_url+"/"+media_id+"/transcript.json"
    headers = {'Authorization': sonixkey[0]}

    while True:

        req = requests.get(download_url, headers=headers)
        req = req.json()
        try:
            if req["code"]==409:
                time.sleep(5)
        except:
            break

    results = req
    results = results['transcript']

    wordlist = []
    starttimelist = []
    stoptimelist = []
    individual_words = {}
    specific_word={}
    count = 0

    for item in results:
        for word in item["words"]:
            specific_word["text"]=word["text"]
            wordlist.append(word['text'])
            specific_word["start time"]=word["start_time"]
            starttimelist.append(word['start_time'])
            specific_word["end_time"]=word["end_time"]
            stoptimelist.append(word['end_time'])
            individual_words[count]=specific_word.copy()
            count +=1
            specific_word.clear()

    sentences = []
    # start and end times are elapsed in seconds
    #format = start_time, end_time, sentence
    new_sentence = True

    for counter, words in enumerate(individual_words):
        numberKey = individual_words[counter]
        word = numberKey['text']
        if new_sentence:
            sentence_temp = ''
            times_and_sentence = []
            
            if ('.' in word):
                times_and_sentence.append(numberKey['start time'])
                times_and_sentence.append(numberKey['end_time'])
                times_and_sentence.append(word)
                sentences.append(times_and_sentence)
                new_sentence = True
            else:
                times_and_sentence.append(numberKey['start time'])
                sentence_temp += word
                new_sentence = False
        else:
            if ('.' in word):
                times_and_sentence.append(numberKey['end_time'])
                sentence_temp += word
                times_and_sentence.append(sentence_temp)
                sentences.append(times_and_sentence)
                new_sentence = True
            else:
                sentence_temp += word
                new_sentence = False

            



    
    # csv header
    fieldnames = ['start_time', 'end_time', 'alternatives', 'type']
    #print(data_json)
    headerIndividualWords = ['start_time','end_time','word']
    if os.path.isdir(outputFilePath) != True:
        os.mkdir(outputFilePath)
    with open(outputFilePath + "/words.csv", 'w', encoding='UTF8', newline='') as f:
        #writer = csv.DictWriter(f, fieldnames=fieldnames)
        #writer.writeheader()
        writer = csv.writer(f)
        writer.writerow(headerIndividualWords)
        i = len(individual_words)
        y = 0
        while y < i:
            rowToWrite = []
            numberKey = individual_words[y]
            rowToWrite.append(numberKey['start time'])
            rowToWrite.append(numberKey['end_time'])
            textWrite = numberKey['text']
            textWrite = textWrite.replace('"', '')
            textWrite = textWrite.replace(',', '')
            textWrite = textWrite.replace('.', '')
            textWrite = textWrite.strip()
            rowToWrite.append(textWrite)
            writer.writerow(rowToWrite)
            y = y + 1

    f.close()

    headerSentences = ['start_time','end_time','sentence']

    with open(outputFilePath + "/sentences.csv", 'w', encoding='UTF8', newline='') as g:
        #writer = csv.DictWriter(f, fieldnames=fieldnames)
        #writer.writeheader()
        writer = csv.writer(g)
        writer.writerow(headerSentences)

        for individualSentences in sentences:
            writer.writerow(individualSentences)

    g.close()







if __name__ == "__main__":
   raw_analysis()
