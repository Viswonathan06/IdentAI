from .algo import VoiceCheck
from flask import Flask, Blueprint, jsonify, request
import time
import librosa
from io import BytesIO
import asyncio
from . import langDetectionService, AudioLogin, PasswordLogin
import json
import os


backendApp_bp = Blueprint("backendService",__name__)

async def langSentimentAPICall(audio_bytes):
    res = {}
    try:
        response = await langDetectionService.get_lang_and_sentiment(audio_bytes)
        dict_response = json.loads(response)
        res["lang"] = { key: value for key, value in dict_response["results"]["channels"][0].items() if key!="alternatives" }
        res["sentiments"] = dict_response["results"]["sentiments"]["average"]
    except Exception as e:
        res["error"] = e
    return res

async def api_call(file_path, audio_bytes):
    # isVoiceValid = await VoiceCheck.checkIfVoice(file_path)
    # if not isVoiceValid:
    #     return {"error": "No Speech Detected"}

    # calls = [langSentimentAPICall(audio_bytes)]
    #API call for language detection and Sentiment Detection
    #Model call for AI Voice or not
    #Model call for Emotion Analysis

    # await asyncio.gather(*calls)


    return {}

def getResponse(file_path, audio_bytes):
    try:
        return asyncio.run(api_call(file_path, audio_bytes))
    except Exception as err:
        return {"error": err}

def get_mfcc(audio_bytes):
    audio_data, sr = librosa.load(BytesIO(audio_bytes), sr=None)
    return librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13).tolist()


@backendApp_bp.route('/upload', methods=['POST'])
def uploadAudio():
    beginTime = time.time()

    if 'file' not in request.files:
        endTime = time.time()
        return jsonify( {
            "response": {
                'error': "No file part"
            },
            "responseTime": endTime-beginTime,
        } ), 401
    
    file = request.files['file']
    if file.filename == '':
        endTime = time.time()
        return jsonify( {
            "response": {
                'error': "No selected file"
            },
            "responseTime": endTime-beginTime
        } ), 401

    allowed_extensions = {'wav', 'mp3'}
    if file.filename.split('.')[-1].lower() not in allowed_extensions:
        endTime = time.time()
        return jsonify( {
            "response": {
                'error': 'Invalid file format'
            },
            "responseTime": endTime-beginTime,
        } ), 401

    file_size_kb = len(file.read())/1024
    if file_size_kb>5120:
        endTime = time.time()
        return jsonify( {
            "response": {
                "error": "File Size too big (Greater than 5 mb)"
            },
            "responseTime": endTime-beginTime
        }), 401

    
    audio_bytes = file.read()
    timestamp = str(int(time.time()))
    file_path = "D:\\wf Global Hackathon\\delphinium\\code\\Backend\\audio_uploads\\"+timestamp + "_" + file.filename

    file.save(file_path)
    
    response = getResponse(file_path, audio_bytes)
    print(response)

    #delete the file
    os.remove(file_path)

    endTime = time.time()

    return jsonify({
        "response": response,
        "responseTime": endTime - beginTime
    }), 200
    
@backendApp_bp.route('/login_with_password', methods=['POST'])
def login_with_password():
    username = request.form.get('userId')
    password = request.form.get('password')
    return jsonify(PasswordLogin.passwordLogin(username, password))

@backendApp_bp.route('/login_with_audio', methods=['POST'])
def login_with_audio():
    return jsonify(AudioLogin.audioLogin(request.form))