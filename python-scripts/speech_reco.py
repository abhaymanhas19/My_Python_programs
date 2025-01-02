import speech_recognition as sr
import pyaudio as py


recognizer = sr.Recognizer()

def record_input_audio():
    with sr.Microphone() as microphone:
        print("Listening....")
        audio = recognizer.listen(microphone)
    text = recognizer.recognize_greoogle_cloud(audio_data=audio)
    print(text)
    return audio

# def play_audio(audio):
    
    

print(record_input_audio())