import os, sys

import soundfile as sf
import numpy as np

# suppress tensorflow messages
# include this if convenient
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
import numpy as np
import tensorflow as tf
import tensorflow_io as tfio
from scipy.signal import resample

import train_speech_id_model

def getAudioEmbeddings(file, target_rate, model):
    # Load audio data and sample rate using soundfile library
    audio_data, sample_rate = sf.read(file)
    print(f'Processing {file} with sample rate of {sample_rate}')
    
    # Keep only the first channel if it's a stereo audio
    if len(audio_data.shape) > 1:
        audio_data = audio_data[:, 0]
    
    # If sample rate doesn't match target_rate, resample the audio data
    if sample_rate != target_rate:
        print(f'Sampling rate is not {target_rate}. Resampling...')
        num_samples = int(len(audio_data) * target_rate / sample_rate)
        audio_data = resample(audio_data, num_samples)
    
    # Prepare audio data as a batch of size 1 and feed into pre-trained model
    cur_emb = model.predict(np.expand_dims(audio_data, axis=0))[0]
    return cur_emb

def checkHistoricalData(checkFile, savedDir = "savedAudioRecordings", target_rate = 48000, threshold = 0.83 ):
    
    home_path = os.path.join(os.getcwd(), 'algo/speech_det')
    pathToSaved = os.path.join(home_path, savedDir)
    audio_embeddings = []
    results = []
    audio_files = [x for x in os.listdir(pathToSaved) if x.endswith('wav')]
    print(f'Comparing current file with saved files: {audio_files}')
    if os.path.isfile(home_path+'/speech-id-model-110/saved_model.pb'):
        model = tf.keras.models.load_model(home_path+'/speech-id-model-110')
    else:
        model = train_speech_id_model.BaseSpeechEmbeddingModel()
        model.load_weights(home_path+'/speech-id-model-110/cp-0110.ckpt')
        model.save(home_path+'/speech-id-model-110')
    

    for file in audio_files:
        audio_embeddings.append(getAudioEmbeddings(os.path.join(pathToSaved,file), target_rate, model))
    
    inputEmbedding = getAudioEmbeddings(checkFile, target_rate, model)

    for p in range(len(audio_files)):
        f1 = audio_files[p]
        distance = np.linalg.norm(
            audio_embeddings[p] - inputEmbedding
        )
        if distance < threshold:
            conclusion = 'Same'
        else:
            conclusion = 'Different'
        print(f'{f1} and {checkFile}: {conclusion} {distance}')
        result_dict = {
            'audio_file': f1,
            'comparison_file': checkFile,
            'conclusion': conclusion,
            'distance': distance
        }
        results.append(result_dict)
    
    return results
    
if __name__ == "__main__":

    # execute only if run as a script
    checkHistoricalData("./savedAudioRecordings/", "./sample_1b.mp3")
