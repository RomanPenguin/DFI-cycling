from deepface import DeepFace as df

obj = df.analyze(img_path = "img4.jpg", actions = ['age', 'gender', 'race', 'emotion'])