#!/usr/bin/env python3


import sounddevice #Unused library but the program throws errors if not imported


import speech_recognition as sr


r = sr.Recognizer()
mic = sr.Microphone()


#Transcribe what you say into a string
def tell_your_name():

    with mic as source:
        r.adjust_for_ambient_noise(source, duration = 2)

        print("What's your name?")

        audio = r.listen(source)

        new_name = r.recognize_google(audio)

        print("Saving new name")

    return new_name
