from __future__ import print_function
import csv
import os

import time
import json
from dataclasses import dataclass, field
from zipfile import ZipFile 



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





def raw_analysis(inputFile, outputFile) -> None:
    #inputFile['rawAudioFile','rawVideoFile','sessionID']
    #outputFile['path_to_output_folder']


    """Main function here"""
    if inputFile['rawVideoFile'] != '':
        emotions(inputFile['rawVideoFile'],outputFile)
    if inputFile['rawAudioFile'] != '':
        transcribe(inputFile['rawAudioFile'],outputFile)

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






def transcribe(inputFile, outputFile):
    # define input file and output file
    inputFilePath = inputFile
    outputFilePath = outputFile
    
    print('Input file is "' + inputFilePath)
    print('Output file is "' + outputFilePath)
    inputFileName = os.path.basename(inputFilePath)

    filename, file_extension = os.path.splitext(inputFilePath)
    audio_format = str(file_extension)
    accepted_format = ["mp3", "mp4", "wav", "flac", "ogg", "amr", "webm"]
    if audio_format[1:] in accepted_format:
        print("audio format accepted")
    else:
        print("audio format not supported please convert to mp3'|'mp4'|'wav'|'flac'|'ogg'|'amr'|'webm'")
        sys.exit()

    input_audio_bucket = "input-audio-dfi-web"
    output_transcription_bucket = "transcribe-output-dfi-web"
    create_bucket(input_audio_bucket)
    create_bucket(output_transcription_bucket)
    with open(inputFilePath, "rb") as f:
        s3.upload_file(inputFilePath, input_audio_bucket, inputFileName)

    # start transcription
    transcribe = boto3.client('transcribe')
    job_name = inputFileName
    job_uri = "s3://" + input_audio_bucket + "/" + inputFileName
    try:
        transcribe.delete_transcription_job(
            TranscriptionJobName=job_name
        )
        timer_begin = time.perf_counter()
        print('timer begin')
    except:
        print("no existing job name clash")
        timer_begin = time.perf_counter()
        print('timer begin')
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat=audio_format[1:],  # MediaFormat='mp3'|'mp4'|'wav'|'flac'|'ogg'|'amr'|'webm',
        LanguageCode='en-AU',
        OutputBucketName=output_transcription_bucket
    )

    # waiting for async response
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)
    print(status)

    # save transcription as json
    timer_end = time.perf_counter()
    print("total time taken in seconds is " + str(timer_end - timer_begin))
    result_url = status["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]

    # get the results from s3 bucket
    entire_transcript_1, sentences_and_times_1, confidences_1, scores_1 = get_transcript_text_and_timestamps(
        output_transcription_bucket, job_name + ".json")
    # show_conf_hist(scores_1)
    # show_conf_hist(scores_1)

    # show_low_conf(scores_1)

    s3_clientobj = s3.get_object(Bucket=output_transcription_bucket, Key=job_name + ".json")
    s3_clientdata = s3_clientobj["Body"].read().decode("utf-8")

    data_json = json.loads(s3_clientdata)
    individual_word_analysis = data_json["results"]["items"]
    paragraphed_result = data_json["results"]["transcripts"][0]["transcript"]

    # csv header
    fieldnames = ['start_time', 'end_time', 'alternatives', 'type']
    # print(data_json)
    if os.path.isdir(outputFilePath) != True:
        os.mkdir(outputFilePath)
    with open(outputFilePath + "/words.csv", 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(individual_word_analysis)

    # with open(outputFilePath+".txt","w") as f:
    #   f.write(paragraphed_result)

    # with open(outputFilePath + "_sentences.csv", 'w') as f:
    #    for items in sentences_and_times_1:
    #        print(items, file=f)

    with open(outputFilePath + "/sentences.csv", 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(sentences_and_times_1)
        # writer.writerows(sentences_and_times_1)


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region
    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).
    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def get_transcript_text_and_timestamps(bucket_name, file_name):
    """take json file from S3 bucket and returns a tuple of:
       entire transcript, list object of tuples of timestamp and individual sentences

    Args:
        bucket_name (str): name of s3 bucket
        file_name (str): name of file
    Returns:
        (
        entire_transcript: str,
        sentences_and_times: [ {start_time (sec) : float,
                                end_time (sec)   : float,
                                sentence         : str,
                                min_confidence   : float (minimum confidence score of that sentence)
                                } ],
        confidences:  [ {start_time (sec) : float,
                         end_time (sec)   : float,
                         content          : str, (single word/phrase)
                         confidence       : float (confidence score of the word/phrase)
                         } ],
        scores: list of confidence scores
        )
    """
    s3_clientobj = s3.get_object(Bucket=bucket_name, Key=file_name)
    s3_clientdata = s3_clientobj["Body"].read().decode("utf-8")

    original = json.loads(s3_clientdata)
    items = original["results"]["items"]
    entire_transcript = original["results"]["transcripts"]

    sentences_and_times = []
    temp_sentence = ""
    temp_start_time = 0
    temp_min_confidence = 1.0
    newSentence = True

    confidences = []
    scores = []
    temp = []

    i = 0
    for item in items:
        # always add the word
        if item["type"] == "punctuation":
            temp_sentence = (
                    temp_sentence.strip() + item["alternatives"][0]["content"] + " "
            )
        else:
            temp_sentence = temp_sentence + item["alternatives"][0]["content"] + " "
            temp_min_confidence = min(temp_min_confidence,
                                      float(item["alternatives"][0]["confidence"]))
            confidences.append({"start_time": float(item["start_time"]),
                                "end_time": float(item["end_time"]),
                                "content": item["alternatives"][0]["content"],
                                "confidence": float(item["alternatives"][0]["confidence"])
                                })
            scores.append(float(item["alternatives"][0]["confidence"]))

        # if this is a new sentence, and it starts with a word, save the time
        if newSentence == True:
            if item["type"] == "pronunciation":
                temp_start_time = float(item["start_time"])
            newSentence = False
        # else, keep going until you hit a punctuation
        else:
            if (
                    item["type"] == "punctuation"
                    and item["alternatives"][0]["content"] != ","
            ):
                # end time of sentence is end_time of previous word
                end_time = items[i - 1]["end_time"] if i - 1 >= 0 else items[0]["end_time"]

                temp = []
                temp.append(temp_start_time)
                temp.append(float(end_time))
                temp.append(temp_sentence.strip())
                temp.append(temp_min_confidence)

                sentences_and_times.append(temp)

                temp = []

                # sentences_and_times.append(temp_start_time)
                # sentences_and_times.append(end_time)
                # sentences_and_times.append(temp_sentence.strip())
                # sentences_and_times.append(temp_min_confidence)

                # sentences_and_times.append(
                #    {temp_start_time,
                #     end_time,
                #     temp_sentence.strip(),
                #    temp_min_confidence
                #    }
                # )
                # reset the temp sentence and relevant variables
                newSentence = True
                temp_sentence = ""
                temp_min_confidence = 1.0

        i = i + 1

    temp.append(temp_start_time)
    temp.append(confidences[-1]["end_time"])
    temp.append(temp_sentence.strip())
    temp.append(temp_min_confidence)

    sentences_and_times.append(temp)

    # sentences_and_times.append(temp_start_time)
    # sentences_and_times.append(confidences[-1]["end_time"])
    # sentences_and_times.append(temp_sentence.strip())
    # sentences_and_times.append(temp_min_confidence)
    # sentences_and_times.append(
    #     {"start_time": temp_start_time,
    #      "end_time": confidences[-1]["end_time"],
    #     "sentence": temp_sentence.strip(),
    #     "min_confidence": temp_min_confidence
    #     }
    # )
    return entire_transcript, sentences_and_times, confidences, scores


def show_conf_hist(all_scores):
    plt.style.use('ggplot')

    # flat_scores_list = [j for sub in all_scores for j in sub]
    flat_scores_list = all_scores

    plt.xlim([min(flat_scores_list) - 0.1, max(flat_scores_list) + 0.1])
    plt.hist(flat_scores_list, bins=20, alpha=0.5)
    plt.title('Distribution of confidence scores')
    plt.xlabel('Confidence score')
    plt.ylabel('Frequency')
    plt.show()


def show_low_conf(all_scores):
    THRESHOLD = 0.4
    # flat_scores_list = [j for sub in all_scores for j in sub]
    flat_scores_list = all_scores
    # Filter scores that are less than THRESHOLD
    all_bad_scores = [i for i in flat_scores_list if i < THRESHOLD]
    print(f"There are {len(all_bad_scores)} words that have confidence score less than {THRESHOLD}")
    plt.xlim([min(all_bad_scores) - 0.1, max(all_bad_scores) + 0.1])
    plt.hist(all_bad_scores, bins=20, alpha=0.5)
    plt.title(f'Distribution of confidence scores less than {THRESHOLD}')
    plt.xlabel('Confidence score')
    plt.ylabel('Frequency')
    plt.show()





if __name__ == "__main__":
   raw_analysis()
