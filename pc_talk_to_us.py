#!/usr/bin/env python3


import pyttsx3
import time


#Make the computer talk to us
def say(text):
    time.sleep(1)
    pyttsx3.speak(text)
