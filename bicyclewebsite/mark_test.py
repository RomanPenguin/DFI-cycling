from dataportal.emonet.basic import emonet_analysis
import csv, os


input = "/home/openface/Documents/data/frames/"
outputFilePath = "/home/openface/Documents/data/mark_output"

try:
    os.mkdir(outputFilePath)
except:
    print("output directory is not empty")


predictions = emonet_analysis(input)
print(predictions)
dominantEmotions =["dominant emotions"]
valence = ["valence"]
arousal = ["arousal"]
filename = ["filename"]


for instance in predictions: #iterate through each frame and pick domininant emotions to add to a list 
    dominantEmotions.append(instance['emo_pred'])
    bob = instance['valence_pred'][0]
    bob = bob.item()
    valence_num = instance['valence_pred'][0]
    arousal_num = instance['arousal_pred'][0]
    filename_item = instance['filename']
    valence.append(valence_num.item())
    arousal.append(arousal_num.item())
    filename.append(filename_item)

rows = zip(filename,valence,arousal,dominantEmotions)
with open(outputFilePath+'/dominant_emotions.txt', 'w') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
    
f.close()