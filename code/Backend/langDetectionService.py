from deepgram import DeepgramClient, PrerecordedOptions, FileSource
import asyncio

AUDIO_FILE = "D:\\Games\\test file.mp3"

DEEPGRAM_API_KEY = "b452528c0296073c99e6cf9ae2d5dabfd7b5e235"


async def get_lang_and_sentiment(audio_bytes):
    deepgram = DeepgramClient(DEEPGRAM_API_KEY)
    payload: FileSource = {
        "buffer": audio_bytes
    }

    options = PrerecordedOptions(
        model="nova",
        detect_language=True,
        sentiment=True
    )

    response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
    return response.to_json()
