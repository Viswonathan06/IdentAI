import speech_recognition as sr

def speech_to_text(file_path):
    print(file_path)
    r = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        print("Converting Speech to Text . . .")
        print("Text: ",text)
        return text