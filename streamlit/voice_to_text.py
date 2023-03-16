import ssl # disable ssl checking
import whisper
ssl._create_default_https_context = ssl._create_unverified_context


def main():
    print('Executing')

    model = whisper.load_model('base') # executed only 1st time this python script is run

    # result = model.transcribe('english-speech.wav', fp16 = False) 
    # result = whisper.transcribe(model = model, audio = 'hindi-speech.mp3', fp16 = False, task = 'translate', language = 'ur')
    result = whisper.transcribe(model = model, audio = 'italian-speech.flac', fp16 = False, task = 'translate', language = 'it')

    # list of languages andsupported for translation and identifiers https://github.com/openai/whisper/blob/main/whisper/tokenizer.py
    print(result['text'])

if __name__ == '__main__':
    main()