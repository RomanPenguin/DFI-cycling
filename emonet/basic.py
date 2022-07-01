from ast import Expression
from fileinput import filename
from lzma import PRESET_DEFAULT
from click import progressbar
import numpy as np
from pathlib import Path
import argparse

import torch
from torch import nn
from torch.utils.data import DataLoader
from torch.utils.data.sampler import WeightedRandomSampler
from torchvision import transforms 
from deepface import DeepFace
from natsort import natsorted

from emonet.emonet.models import EmoNet
import matplotlib.pyplot as plt
import csv, os, array


def emonet_analysis(inputImage):

    torch.backends.cudnn.benchmark =  True

    #Parse arguments
    

    # Parameters of the experiments
    n_expression = 8
    expressions_list = {0: 'neutral', 1:'happy', 2:'sad', 3:'surprise', 4:'fear', 5:'disgust', 6:'anger', 7:'contempt', 8:'none'}

    batch_size = 32
    n_workers = 2
    device = 'cpu'
    image_size = 256
    predictions = []

    # Create the data loaders
    transform_image = transforms.Compose([transforms.ToTensor()])
    # Loading the model 
    state_dict_path = Path(__file__).parent.joinpath('pretrained', f'emonet_{n_expression}.pth')

    print(f'Loading the model from {state_dict_path}.')
    state_dict = torch.load(str(state_dict_path), map_location=device)
    state_dict = {k.replace('module.',''):v for k,v in state_dict.items()}
    net = EmoNet(n_expression=n_expression).to(device)
    net.load_state_dict(state_dict, strict=False)
    net.eval()


    transform_image = transforms.Compose([transforms.ToTensor(),transforms.Resize([int(256),int(256)])])
    transform_image_og = transforms.Compose([transforms.ToTensor()])

    # plt.imshow(image1)
    backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']

    allpics = []
    imagefolder = inputImage
    for file in os.listdir(imagefolder):
        if file.endswith(".jpg"):
            allpics.append(file)

    allpics = natsorted(allpics)

    progress = 0
    totalcount = len(allpics)
    for i in allpics:
        progress += 1
        print(progress+"/"+totalcount)

        image1 = DeepFace.detectFace(imagefolder+"/"+i, target_size = (256, 256), detector_backend = backends[0], enforce_detection = False )
        # plt.imshow(image1)
        
        # plt.imshow(  image1.permute(1, 2, 0) )


        image1 = np.ascontiguousarray(image1)

        test_image1 = transform_image_og(image1)
        # plt.imshow(  test_image2.permute(1, 2, 0) )

        # test_image = [test_image1,test_image2]

        test_image1 = test_image1.unsqueeze(0)

        images1 = test_image1.to(device)
        with torch.no_grad():
            out1 = net(images1)


        # print(out1)

        expression_pred = out1['expression']
        emo_pred = out1['expression'].numpy()[0]
        emo_pred = np.where(emo_pred == np.amax(emo_pred))[0]
        emo_pred = expressions_list[emo_pred[0]]
        valence_pred = out1['valence']
        arousal_pred = out1['arousal'] 

        result= {"filename":i, 
            "expression_pred" : expression_pred, 
            "valence_pred" : valence_pred, 
            "arousal_pred" : arousal_pred,
            "emo_pred" : emo_pred }
        predictions.append(result)

    
    return predictions


