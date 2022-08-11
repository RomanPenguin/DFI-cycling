from numpy import append
import requests


from requests.auth import HTTPBasicAuth
import requests
import os, csv

import scipy as sp

from bicyclewebsite.dataportal.generate_results import individual_words



#update key file (DO NOT STORE IN PROJECT FOLDER)
sonixkeyfile = "/home/openface/Documents/sonixkey.txt"


# curl -XPOST https://api.sonix.ai/v1/media -H "Authorization: Bearer <API Key>"  \
#   -F file=@my_audio.mp3 \
#   -F language=en \
#   -F name='Podcast Episode 45' \
#   -F keywords='Sonix, Bergamasco, Kairos, Chewbacca' \
#   -F custom_data='{"internal_id": "123412", "customer_email": "joey@sonix.ai"}' 


api_url = "https://api.sonix.ai/v1/media"

media_id = "2VdmWL5Q"
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

   
outputFilePath = "output/sonix1"
# csv header
fieldnames = ['start_time', 'end_time', 'alternatives', 'type']
# print(data_json)
if os.path.isdir(outputFilePath) != True:
    os.mkdir(outputFilePath)
with open(outputFilePath + "/words.csv", 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(individual_words)

print(req)    
 
