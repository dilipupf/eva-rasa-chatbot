import os
import sys
import sounddevice as sd
from typing import Sequence
import google.cloud.texttospeech as tts
import IPython.display as ipd

# Add the current directory to the path so that the script can find the data folder
folder_path = sys.path.append(os.path.dirname(os.path.realpath(__file__)))
print('folder_path', folder_path)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'GTTS_ApiKey.json'

def unique_languages_from_voices(voices: Sequence[tts.Voice]):
    language_set = set()
    for voice in voices:
        for language_code in voice.language_codes:
            language_set.add(language_code)
    return language_set


def list_languages():
    client = tts.TextToSpeechClient()
    response = client.list_voices()
    languages = unique_languages_from_voices(response.voices)

    print(f" Languages: {len(languages)} ".center(60, "-"))
    for i, language in enumerate(sorted(languages)):
        print(f"{language:>10}", end="\n" if i % 5 == 4 else "")


def list_voices(language_code=None):
    client = tts.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)

    print(f" Voices: {len(voices)} ".center(60, "-"))
    for voice in voices:
        languages = ", ".join(voice.language_codes)
        name = voice.name
        gender = tts.SsmlVoiceGender(voice.ssml_gender).name
        rate = voice.natural_sample_rate_hertz
        print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")


def text_to_audio(voice_name: str, text: str):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.LINEAR16, pitch=-3, effects_profile_id=["telephony-class-application"])

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )

    filename = "response.mp3"

    with open(filename, "wb") as out:
        out.write(response.audio_content)
        # print(f'Generated speech saved to "{filename}"')
    file_name_path = '/Users/dilipharish/Software Projects/whisper/eva-rasa-chatbot/streamlit/response.mp3'

    return file_name_path

# available_lang = np.array(list_languages())

language_codes = {'af-ZA': 'Afrikaans',
                  'ar-XA': 'Arabic',
                  'bg-BG': 'Bulgarian',
                  'bn-IN': 'Bengali',
                  'ca-ES': 'Catalan',
                  'cmn-CN': 'Chinese (Mandarin, China)',
                  'cmn-TW': 'Chinese (Mandarin, Taiwan)',
                  'cs-CZ': 'Czech',
                  'da-DK': 'Danish',
                  'nl-BE': 'Dutch (Belgium)',
                  'nl-NL': 'Dutch (Netherlands)',
                  'en-AU': 'English (Australia)',
                  'en-IN': 'English (India)',
                  'en-GB': 'English (United Kingdom)',
                  'en-US': 'English (United States)',
                  'fil-PH': 'Filipino',
                  'fi-FI': 'Finnish',
                  'fr-CA': 'French (Canada)',
                  'fr-FR': 'French (France)',
                  'gl-ES': 'Galician',
                  'de-DE': 'German',
                  'el-GR': 'Greek',
                  'gu-IN': 'Gujarati',
                  'he-IL': 'Hebrew',
                  'hi-IN': 'Hindi',
                  'hu-HU': 'Hungarian',
                  'is-IS': 'Icelandic',
                  'id-ID': 'Indonesian',
                  'it-IT': 'Italian',
                  'ja-JP': 'Japanese',
                  'kn-IN': 'Kannada',
                  'ko-KR': 'Korean',
                  'lv-LV': 'Latvian',
                  'lt-LT': 'Lithuanian',
                  'ms-MY': 'Malay',
                  'ml-IN': 'Malayalam',
                  'mr-IN': 'Marathi',
                  'nb-NO': 'Norwegian (Bokmål)',
                  'pl-PL': 'Polish',
                  'pt-BR': 'Portuguese (Brazil)',
                  'pt-PT': 'Portuguese (Portugal)',
                  'pa-IN': 'Punjabi',
                  'ro-RO': 'Romanian',
                  'ru-RU': 'Russian',
                  'sr-RS': 'Serbian',
                  'sk-SK': 'Slovak',
                  'sl-SI': 'Slovenian',
                  'es-ES': 'Spanish (Spain)',
                  'es-US': 'Spanish (United States)',
                  'sv-SE': 'Swedish',
                  'ta-IN': "Tamil(India)",
                  'te-IN': "Telugu(India)",
                  'th-TH': "Thai(Thailand)",
                  'tr-TR': "Turkish(Turkey)",
                  'uk-UA': "Ukrainian(Ukraine)",
                  'vi-VN': "Vietnamese(Vietnam)",
                  'yue-HK': "Cantonese(Hong Kong)",
                  }