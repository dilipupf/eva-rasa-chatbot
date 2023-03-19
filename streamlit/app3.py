import streamlit as st
import requests
from streamlit_chat import message
import json
import uuid
from voice_to_text import STT
from voice_to_text import LANGUAGES
from text_to_voice import text_to_audio
from IPython.display import Audio
from playsound import playsound

# Generate unique key for widget
widget_key = str(uuid.uuid4())

# # Use key in widget creation
# st.streamlit_chat.streamlit_chat(key=widget_key)

URL = "http://localhost:5005/webhooks/rest/webhook"


def predict(text):

    data = {}
    data["message"] = text
    data["sender"] = "wp"

    response = requests.post(URL, json=data)
    # print response
    json_str = json.dumps(response.json(), indent=4)
    print(json_str)
    # print('resonpse json 1', response.json()[1])
    # print('resonpse json 2', response.json()[2])

  
    answer = eval(response.text)[0]["text"]
    if len(response.json()) > 1:
        button_response = response.json()[1]
        return [answer, button_response]
    else:
        return [answer, '']


def display_button_message(response):
    message = response['text']
    buttons = response['buttons']
    st.write(message)
    for button in buttons:
        st.button(button['title'])

if __name__ == '__main__':
    sttModule = STT(8000, 5, 'english')
    whisper_languages_list = []
    for key in LANGUAGES:
        whisper_languages_list.append(LANGUAGES[key])

    st.header('Eva Rasa Chatbot')

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    if "_get_last_key_pressed" not in st.session_state:
        st.session_state._get_last_key_pressed = None

    record_button = st.sidebar.button('Start speech recording')
    user_language = st.sidebar.selectbox('User language:', whisper_languages_list)
    recording_duration = st.sidebar.selectbox('Recording duration in seconds:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    user_input = st.text_input("Enter some text", key="my_text_input")

    if record_button:
        with st.spinner('Recording...'):
            sttModule.recordMicAudio_ToWavFile()
        with st.spinner('Translating and transcribing...'):
            user_input = sttModule.translateAndTranscribe_FromWavFile()
 
    if user_language:
        sttModule.setUserLanguage(user_language)

    if recording_duration:
        sttModule.setRecordingDuration(recording_duration)

    if user_input:
        ans, button_response = predict(user_input)
        print('ans', type(ans))
        
        if button_response:
            button_message = button_response['text']
            buttons = button_response['buttons']
            st.write(button_message)
            for index, button in enumerate(buttons):
                button_value = st.button(button['title'], key=button['payload'])
                user_input = button_value
                print('user input', user_input)
        else:
            st.write(ans)

        # Display bot response
        st.session_state.past.append(user_input)
        st.session_state.generated.append(ans)

        file_name_path = text_to_audio("en-GB-Neural2-A", str(ans))
        # Audio(filename = file_name_path, autoplay = True)

        # audio_file = open('response.mp3', 'rb')
        # audio_bytes = audio_file.read()

        playsound('response.mp3')



    print(st.session_state)
    
    for i in range(len(st.session_state['past'])):
        widget_key = str(uuid.uuid4())
        message(st.session_state['past'][i], is_user=True, key=widget_key)
        if len(st.session_state['generated']) > i:
            widget_key = str(uuid.uuid4())
            message(st.session_state['generated'][i], key = widget_key)