from turtle import textinput
from numpy import append
import requests
import time

from requests.auth import HTTPBasicAuth
import requests
import os, csv

import scipy as sp

from bicyclewebsite.dataportal.generate_results import individual_words



#update key file (DO NOT STORE IN PROJECT FOLDER)
#sonixkeyfile = "/home/tommy/Documents/sonixKey.txt"
sonixkeyfile= "/home/openface/Documents/sonixkey.txt"
inputFilePath='/home/openface/Documents/data/ben1.mp3'
outputFilePath = "output/sonix1"

def sonix_transcribe(sonixkeyfile, inputFilePath,outputFilePath):


    api_url = "https://api.sonix.ai/v1/media"

    try:
        with open(sonixkeyfile) as f:
            sonixkey = f.read().splitlines()
        # headers = {'Accept': 'application/json'}
        headers = {'Authorization': sonixkey[0]}
    except:
        print("no sonix key! please check key location")


    files = {
        'file': open(inputFilePath, 'rb'),
        'language': (None, 'en'),
        'name': (None, 'sonixtest')
    }

    response = requests.post('https://api.sonix.ai/v1/media', headers=headers, files=files)

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


    
sonix_transcribe(sonixkeyfile, inputFilePath,outputFilePath)
