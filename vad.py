# import voxseg
# from tensorflow.keras import models

# # feature extraction
# data = extract_feats.prep_data('data/sample_35s.mp3') # prepares audio from Kaldi-style data directory
# feats = extract_feats.extract(data) # extracts log-mel filterbank spectrogram features
# normalized_feats = extract_feats.normalize(norm_feats) # normalizes the features

# #model execution
# model = models.load_model('path/to/model.h5') # loads a pretrained VAD model
# predicted_labels = run_cnnlstm.predict_labels(model, normalized_feats) # runs the VAD model on features
# utils.save(predicted_labels, 'path/for/output/labels.h5') # saves predicted labels to .h5 file