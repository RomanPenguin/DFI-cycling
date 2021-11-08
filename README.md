# Initial Set Up

This repo contains basic setup for Google Cloud speech to text and AWS Transcribe for Python.

To start, make sure to have Python 3 installed https://www.python.org/downloads/.

Highly recommended: create a virtual environment before continuing, see https://docs.python.org/3/library/venv.html.
this will help making sure packages are not in conflict with other projects.

# Google Speech to Text 
All Monash accounts have the ability to use Google Cloud services, including student and staff accounts.
You will need to enable Google additional services for your specific account https://www.monash.edu/esolutions/email-collaboration/google-apps. 
You might have to enter your credit card details before you can use Google Cloud. 
$300 USD free credit is provided for you to start.


Once you are signed into the console, you can start setting up following the steps listed here https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries.
You can use the code provided here in this repo and the sample audio files for testing.

# AWS Transcribe 
You have to register an AWS account, and you will require to put in your credit card details. 
There are free tiers to test out the services, 60 minutes free per month for 12 months. 
follow the guide here to set up https://docs.aws.amazon.com/transcribe/latest/dg/getting-started-python.html.
The AWS trancription code is defaulted to mp3 and therefore make sure all the audio files are converted before running the transription. 
Since this is an async operation, the audio files will be uploaded and stored temorarily in an s3 bucket and the results will be available in a few minutes for a short <1hr long audio clip. 

Following documentation assumes AWS is the implementation used and I recommend AWS over Google TTS for this use case. 

 # Voice Activity Detection
 You may choose to use Voice Activity Dectection (VAD) to reduce cost for cloud transcription. See https://github.com/NickWilkinson37/voxseg for more details about the implementation. This feature is currently not used and is under development. 

# Emotion Analysis 
Emotion analysis is carried out with the deepface framework. (https://github.com/serengil/deepface) It provides robust feature sets including age, gender, race and emotion. Only emotion is used to speed up the detection. Current implementation takes a video and pulls out one frame per second and provides a prediction on the emotion exhibited. This can run on most video format. 

# Examples
This repo has some example files to test the functionality of the code 
## AWS transcription
    aws_transcribe.py -i [input_file] -o [output_file]
this function takes two arguements, input file which is the audio recorded and an output file which the final result would be written to. 
example use transcribing an audio file called ben1.mp3 from data subfolder and save the results to output/transcript.txt: 

    aws_transcribe.py -i data/ben1.mp3 -o output/transcipt.txt

## Emotion Detection
    emotion_detection_deepface.py -i face_video.wmv -o output/face_video_frames 
this function takes two arguments, input video file and output files location. Similar to AWS transcription with one key difference: it will generate image files alongside the emotion prediction to allow for human verification of the face.
