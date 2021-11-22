from __future__ import print_function
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
import tkinter

s3 = boto3.client('s3')
#matplotlib.use('TkAgg')

def main(argv):

    #define input file and output file
    inputFilePath = ''
    outputFilePath = 'transcript.csv'
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <input_audio_file> -o <out_csv_putfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputFilePath = arg
        elif opt in ("-o", "--ofile"):
            outputFilePath = arg
    print('Input file is "' + inputFilePath)
    print('Output file is "' + outputFilePath)
    inputFileName = os.path.basename(inputFilePath)

    filename, file_extension = os.path.splitext(inputFilePath)
    audio_format=str(file_extension)
    accepted_format = ["mp3","mp4","wav","flac","ogg","amr","webm"]
    if audio_format[1:] in accepted_format:
        print("audio format accepted")
    else:
        print("audio format not supported please convert to mp3'|'mp4'|'wav'|'flac'|'ogg'|'amr'|'webm'")
        sys.exit()

        


    input_audio_bucket = "input-audio-dfi"
    output_transcription_bucket="transcribe-output-dfi"
    create_bucket(input_audio_bucket)
    create_bucket(output_transcription_bucket)
    with open(inputFilePath, "rb") as f:
        s3.upload_file(inputFilePath, input_audio_bucket,inputFileName)



    #start transcription
    transcribe = boto3.client('transcribe')
    job_name = inputFileName
    job_uri = "s3://"+input_audio_bucket+"/"+inputFileName
    try:
        transcribe.delete_transcription_job(
                    TranscriptionJobName=job_name
                )
        timer_begin=time.perf_counter()
    except:
        print("no existing job name clash")            
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat=audio_format[1:],           # MediaFormat='mp3'|'mp4'|'wav'|'flac'|'ogg'|'amr'|'webm',
        LanguageCode='en-AU',
        OutputBucketName=output_transcription_bucket
    )

    #waiting for async response
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)
    print(status)

    #save transcription as json
    timer_end = time.perf_counter()
    print("total time taken in seconds is "+str(timer_end-timer_begin))
    result_url=status["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]

    #get the results from s3 bucket
    entire_transcript_1, sentences_and_times_1, confidences_1, scores_1=get_transcript_text_and_timestamps(output_transcription_bucket,job_name+".json")
    show_conf_hist(scores_1)
    show_conf_hist(scores_1)

    show_low_conf(scores_1)

    s3_clientobj = s3.get_object(Bucket=output_transcription_bucket, Key=job_name+".json")
    s3_clientdata = s3_clientobj["Body"].read().decode("utf-8")

    data_json = json.loads(s3_clientdata)
    individual_word_analysis=data_json["results"]["items"]
    paragraphed_result=data_json["results"]["transcripts"][0]["transcript"]

    # csv header
    fieldnames = ['start_time', 'end_time', 'alternatives', 'type']
    #print(data_json)
    with open(outputFilePath+".csv", 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(individual_word_analysis)

    with open(outputFilePath+".txt","w") as f:
        f.write(paragraphed_result)

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
                end_time = items[i-1]["end_time"] if i-1 >= 0 else items[0]["end_time"]
                sentences_and_times.append(
                    {"start_time": temp_start_time,
                     "end_time": end_time,
                     "sentence": temp_sentence.strip(),
                     "min_confidence": temp_min_confidence
                    }
                )
                # reset the temp sentence and relevant variables
                newSentence = True
                temp_sentence = ""
                temp_min_confidence = 1.0
                
        i = i + 1
        
    sentences_and_times.append(
                    {"start_time": temp_start_time,
                     "end_time": confidences[-1]["end_time"],
                     "sentence": temp_sentence.strip(),
                     "min_confidence": temp_min_confidence
                    }
                )
    return entire_transcript, sentences_and_times, confidences, scores

def show_conf_hist(all_scores):
    plt.style.use('ggplot')

    #flat_scores_list = [j for sub in all_scores for j in sub] 
    flat_scores_list = all_scores

    plt.xlim([min(flat_scores_list)-0.1, max(flat_scores_list)+0.1])
    plt.hist(flat_scores_list, bins=20, alpha=0.5)
    plt.title('Distribution of confidence scores')
    plt.xlabel('Confidence score')
    plt.ylabel('Frequency')

    plt.show()

def show_low_conf(all_scores):
    THRESHOLD = 0.4
    #flat_scores_list = [j for sub in all_scores for j in sub] 
    flat_scores_list = all_scores
    # Filter scores that are less than THRESHOLD
    all_bad_scores = [i for i in flat_scores_list if i < THRESHOLD]
    print(f"There are {len(all_bad_scores)} words that have confidence score less than {THRESHOLD}")
    plt.xlim([min(all_bad_scores)-0.1, max(all_bad_scores)+0.1])
    plt.hist(all_bad_scores, bins=20, alpha=0.5)
    plt.title(f'Distribution of confidence scores less than {THRESHOLD}')
    plt.xlabel('Confidence score')
    plt.ylabel('Frequency')

    plt.show()

if __name__ == "__main__":
   main(sys.argv[1:])

            