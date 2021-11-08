from __future__ import print_function
import time
import boto3
import json
from urllib.request import urlopen
import csv
import sys, getopt
import logging
from botocore.exceptions import ClientError
import os

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

    
    s3 = boto3.client('s3')
    create_bucket("text-transcribe-test")
    with open(inputFilePath, "rb") as f:
        s3.upload_file(inputFilePath, "text-transcribe-test",inputFileName)



    #start transcription
    transcribe = boto3.client('transcribe')
    job_name = inputFileName
    job_uri = "s3://text-transcribe-test/"+inputFileName
    try:
        transcribe.delete_transcription_job(
                    TranscriptionJobName=job_name
                )
    except:
        print("no existing job name clash")            
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',           # MediaFormat='mp3'|'mp4'|'wav'|'flac'|'ogg'|'amr'|'webm',
        LanguageCode='en-AU'
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
    result_url=status["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    #print(result_url)
    response=urlopen(result_url)
    data_json = json.loads(response.read())
    #print(data_json)
    with open(outputFilePath, 'a+') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in data_json.items():
            writer.writerow([key, value])

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


if __name__ == "__main__":
   main(sys.argv[1:])

            