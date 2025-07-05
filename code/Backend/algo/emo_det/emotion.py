from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline
from .speech_to_text import *

def emotion(file_path):

    tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
    model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")
    emotion = pipeline('sentiment-analysis', 
                        model='arpanghoshal/EmoRoBERTa')

    txt = speech_to_text(file_path=file_path)
    emotion_labels = emotion(txt)

    return emotion_labels

## Usage
# if __name__ == "__main__":
#     emo = emotion(<path/to/audio/file>)