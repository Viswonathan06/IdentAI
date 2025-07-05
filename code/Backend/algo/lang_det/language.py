from langdetect import detect
from .speech_to_text import *
from .mapping import *

def language(file_path):

    txt = speech_to_text(file_path=file_path)
    lang_map = mapping()

    lang = detect(txt)
    
    return lang_map[lang]