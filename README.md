
# Project for Computer Vision Class


## Content Table

1. [Project Objectives](#objectives)

2. [Bibliotecas necessarias](#libraries)

3. [Funcionamento](#functioning)

4. [Como rodar o script](#run)


<a name="objectives"></a>
## 1. Project Objectives:

1 - The system should detect faces. 

2 - It should recognize the people from the group, working with a pre-loaded database. 

3 - There should be also a way to run the program without any information in the database.

4 - It needs a function to show the database in real-time.

5 - The system should greet the people on the database and ask about new people.


<a name="libraries"></a>
## 2. Requirements

opencv

copy

random

math

threading

pyttsx3

time

os

glob

face_recognition

numpy

speech_recognition

sounddevice


<a name="functioning"></a>
## 3. Functioning

The program turns on the camera and if it doesn't recognize the person on the frame it asks for their name;

When the person answers it records the name, takes a picture of the new person and saves it with the corresponding name;

If the system already knows the person that is in the frame, it greets them.


<a name="run"></a>
## 4. How to run the script

Clone the repository

 ```
git clone https://github.com/ritapm18/Trab1_G3
 ```

Go into the folder

 ```
cd path/to/folder
 ```

Run main script

 ```
python3 main.py
 ```
