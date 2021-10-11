from __future__ import print_function
import time
import boto3
import json
from urllib.request import urlopen
import csv

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
print(result_url)
result_url="https://s3.us-east-1.amazonaws.com/aws-transcribe-us-east-1-prod/832870047395/nycbike35stest/e6e35391-15f3-4dce-9a33-a241bb3d7d2b/asrOutput.json?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEG0aCXVzLWVhc3QtMSJHMEUCIQDtlArhtcS7P9exQE68h1WJdTwp0yLir9K4a%2BzjzotDKgIgNoodWM0hx0NoAv6JeCYnkurqIzBPFLIIcd34c2fBXCUqgwQI5f%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARADGgwyNzY2NTY0MzMxNTMiDNfJs4xGL6IHvma5qSrXA0SUvl8Qv%2FIYSz8QkhB%2FFYyMLoai%2BsXpV3xPJUFDDC%2ByuATshhWYcR3L2zeMPTs7qCS247iIq1OxaEjJ%2BE%2BGgFlO3Kq5KCTNd26s3yImgU4sW7ce9VMHf0SSucfUd0iznCRMXE57pGMerCuCZp7T8yIjCiPlFomlxWS8k27kk%2F6KQGubAqDD8CDRgKxyUXSys8Elh6arIshv6zL2z3QfwjN6CkNdmTxOOWtk2%2FzPh73%2FhN7cWK26cYrlWOpn%2FNOAqLKllYqU4PWc7dG5XmNZAoBqZfIK%2BeqONFu1YwQ5gsLVWz6wV%2BumKx5qGYrpv34HkqTPlWAnM2t6TZSED8nhr40Zd5l27Zix8jR9Yk8FNWhpLnb9y9yPzOcz2gNLvvi0QANjICbssHiUVLWzgNvd5AU3LyAAx%2FO5zAs6oz%2FdWxxRCm29mhvCIywzyvOwXzVIx7PfHrudjev69QaUQECR0scPKYyxpwlpbE6gbZdhAVidFLl%2BbrxoIjbhxGDieGlJsPdSwVU3UkZNmX9xmm8vjV2TdBhDC9BzgnlMZp5p2VOAE80SaxeEr%2ByFhxQZ5O9NB34bQJZoz06ckGFMbrqPMnlwXGjgR8vMskT4miqJyDjwz2AmkToqSDDW946LBjqlAQbgLT1fjfJIGJt9VmasbzmnPQIJmIEaMsq8jLWikTcl%2BuQy4yvouEry7TTBn1vsfpjSfgWAhMu9F3g33JUTTR4OP%2FTSIrQGhwUw%2FD07LP51tl7%2FzeOtRIxTg1gPodXjetRe27ciPcYMrSbpk0gZ%2BuQDpC1N0wHMIc0v0AXzEp1UncVZW9QSzG7PLeUtfQpk7rk1rMIaOS49ObAA2z%2FjdXftPTJOZw%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20211011T051003Z&X-Amz-SignedHeaders=host&X-Amz-Expires=900&X-Amz-Credential=ASIAUA2QCFAAUQHPPJKX%2F20211011%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=0cadb518275b093e3d5683bd382384d9235739a991e0fb40d08882e9b4b0ac54"
response=urlopen(result_url)
data_json = json.loads(response.read())
print(data_json)
with open('transcript.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in data_json.items():
       writer.writerow([key, value])



            