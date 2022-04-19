# Initial Set Up

This repo contains basic setup for data collection and analysis for DFI cycling project.

To start, make sure to have Python 3 installed https://www.python.org/downloads/.


# Website set up 
This project is based on Django framework for ease of use and development. There is a web interface for easy management of the participants and researchers and safekeeping of data. To set up the website to run on a local machine (this example will be for Ubuntu 20.04 LTS) use the following instructions. 

## initial steps
Make sure everything is up to date on the system:
    
    sudo apt update
    sudo apt upgrade
Install required packages 
    
    sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3
    sudo apt install python3.8-venv
Install Node Version Manager since Ubuntu included Node version is very old and not compatible 
    
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
restart the terminal or follow on screen instructions

## Installation
create a new folder 
    
    mkdir webserver
    cd webserver
clone the repo
    
    git clone https://github.com/RomanPenguin/DFI-cycling.git
create and activate a virtual environment for keeping python packages contained within this project 
    
    cd DFI-cycling
    python3 -m venv servervenv
    source servervenv/bin/activate

install from requirements.txt and ensure django version is 3.2

    pip install -r requirements.txt
    pip3 install django==3.2 
    pip install django-tailwind
    pip install django-cleanup

 
This command installs the latest Node LTS version. If there is any errors install 16.10    
    
    nvm install --lts
    
initialise tailwind 

    cd bicyclewebsite/
    python manage.py tailwind install

create database within the Django framework 

    python manage.py makemigrations
    python manage.py migrate
    python manage.py collectstatic
    
create admin user 

    python manage.py createsuperuser
follow the on screen steps to choose an username and password (press enter to skip email if you wish)

now try:

    python manage.py runserver 127.0.0.1:8000

open your web browser and navigate to 127.0.0.1:8000/awstranscription and you should see the log in page. Enter your login you created earlier to access the portal. 
To look at the data collected and modify items please go to 127.0.0.1:8000/admin and log in. This is not for participants to use. 


# brief explanation of the data analysis packages

This project relies on the following:

## AWS Transcribe 
You have to register an AWS account, and you will require to put in your credit card details. 
There are free tiers to test out the services, 60 minutes free per month for 12 months. 
follow the guide here to set up https://docs.aws.amazon.com/transcribe/latest/dg/getting-started-python.html.
The AWS trancription code is defaulted to mp3 and therefore make sure all the audio files are converted before running the transription. 
Since this is an async operation, the audio files will be uploaded and stored temorarily in an s3 bucket and the results will be available in a few minutes for a short <1hr long audio clip. 

Following documentation assumes AWS is the implementation used and I recommend AWS over Google TTS for this use case. 

## Audio pre-processing: best practices for improved results
- sampling rate 16KHz or better is preferred 
- losses codec such as FLAC or LINEAR16 is preferred 
- Do not apply noise cancelling or reduction before sending to Google 
- Use custom dictionaries for better results for commonly misheard words or proper nouns or phrases
- Do not use automatic gain control 
- avoid clipping 


## Emotion Analysis - deepface
Emotion analysis is carried out with the deepface framework. (https://github.com/serengil/deepface) It provides robust feature sets including age, gender, race and emotion. Only emotion is used to speed up the detection. Current implementation takes a video and pulls out one frame per second and provides a prediction on the emotion exhibited. This can run on most video format. 


## Emotion analysis - EmoNet
Emonet is used to provide valence and arousal values to complement the specific categories of emotions (such as angry or happy) and allows for more mathematical analysis of the data. GitHub link (https://github.com/face-analysis/emonet)

## AffectNet
Affectnet dataset is used to test the models. (http://mohammadmahoor.com/affectnet/)  

## Examples
This repo has some example files to test the functionality of the code 


# Past files
## Google Speech to Text 
All Monash accounts have the ability to use Google Cloud services, including student and staff accounts.
You will need to enable Google additional services for your specific account https://www.monash.edu/esolutions/email-collaboration/google-apps. 
You might have to enter your credit card details before you can use Google Cloud. 
$300 USD free credit is provided for you to start.


Once you are signed into the console, you can start setting up following the steps listed here https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries.
You can use the code provided here in this repo and the sample audio files for testing.


## Google Transcription
There are two options for Google ASR, one is for audio clips less than 1 minute in length, which can be directly sent to Google for transcription. Any clips longer than 1 minute will require the clip to be first uploaded to a storage bucket then start async compute for a result. 

Google transcription is not in use currently. 



 ## Voice Activity Detection
 You may choose to use Voice Activity Dectection (VAD) to reduce cost for cloud transcription. See https://github.com/NickWilkinson37/voxseg for more details about the implementation. This feature is currently not used and is not under development. 

 ## AWS transcription
    aws_transcribe.py -i [input_file] -o [output_file]
this function takes two arguements, input file which is the audio recorded and an output file which the final result would be written to. 
example use transcribing an audio file called ben1.mp3 from data subfolder and save the results to output/transcript.txt: 

    aws_transcribe.py -i data/ben1.mp3 -o output/transcipt.txt

## Emotion Detection
    emotion_detection_deepface.py -i face_video.wmv -o output/face_video_frames 
this function takes two arguments, input video file and output files location. Similar to AWS transcription with one key difference: it will generate image files alongside the emotion prediction to allow for human verification of the face.

