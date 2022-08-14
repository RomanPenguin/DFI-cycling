from turtle import textinput
from numpy import append
import requests


from requests.auth import HTTPBasicAuth
import requests
import os, csv

import scipy as sp

from bicyclewebsite.dataportal.generate_results import individual_words



#update key file (DO NOT STORE IN PROJECT FOLDER)
sonixkeyfile = "/home/tommy/Documents/sonixKey.txt"


# curl -XPOST https://api.sonix.ai/v1/media -H "Authorization: Bearer <API Key>"  \
#   -F file=@my_audio.mp3 \
#   -F language=en \
#   -F name='Podcast Episode 45' \
#   -F keywords='Sonix, Bergamasco, Kairos, Chewbacca' \
#   -F custom_data='{"internal_id": "123412", "customer_email": "joey@sonix.ai"}' 


api_url = "https://api.sonix.ai/v1/media"
media_id = "QnVba9MQ"
# /v1/media/<media id>/transcript 
download_url = api_url+"/"+media_id+"/transcript.json"
with open(sonixkeyfile) as f:
    sonixkey = f.read().splitlines()
# headers = {'Accept': 'application/json'}
headers = {'Authorization': sonixkey[0]}

files = {
    'file': open('/home/openface/Music/sonixtest.mp3', 'rb'),
    'language': (None, 'en'),
    'name': (None, 'sonixtest')
}

response = requests.post('https://api.sonix.ai/v1/media', headers=headers, files=files)



fileslist = requests.get(api_url+"?page=0", headers=headers)

req = requests.get(download_url, headers=headers)

results = req.json()
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

        



   
outputFilePath = "output/sonix1"
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


 
