import azure.cognitiveservices.speech as speechsdk
speech_key, service_region = "459345ddae5d4707b46fc143fca6bbf8", "centralindia"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
def checkIfVoice(file_path):
    try:
        audio_config = speechsdk.audio.AudioConfig(filename=file_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        result = speech_recognizer.recognize_once()
        print("Speech recognition done")
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return True
        else:
            return False
    except Exception as e:
        try:
            audio_config = speechsdk.audio.AudioConfig(filename=file_path)
            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
            result = speech_recognizer.recognize_once()
            print("Speech recognition done")
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return True
            else:
                return False
        except Exception as e:
            print(e)
        print(e)
        return False
    
