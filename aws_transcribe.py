from __future__ import print_function
import time
import boto3
import json
from urllib.request import urlopen
import csv
import sys, getopt


def main(argv):

    #define input file and output file
    inputfile = ''
    outputfile = 'transcript.csv'
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
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print('Input file is "' + inputfile)
    print('Output file is "' + outputfile)


    #start transcription
    transcribe = boto3.client('transcribe')
    job_name = "nycbike35stest"
    job_uri = "s3://text-transcribe-test/sample_35s.flac"
    transcribe.delete_transcription_job(
                    TranscriptionJobName=job_name
                )
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='flac',
        LanguageCode='en-US'
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
    with open(outputfile, 'a+') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in data_json.items():
            writer.writerow([key, value])

if __name__ == "__main__":
   main(sys.argv[1:])

            