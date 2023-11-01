#!/usr/bin/env python3


#Import libraries
import cv2
import copy
import random
import math
from threading import Thread
import speech_recognition as sr

from face_rec import FaceRec, Track, Detection, IOU
from pc_talk_to_us import say
from tell_your_name_to_pc import tell_your_name
from show_db import show_database


def main():
    global speech_triggered

    # Start Camera
    video = cv2.VideoCapture(0)

    # Initialize FaceRec class
    face_recog = FaceRec()

    #Load/Encode Images
    face_recog.load_images("./images")

    tracks = []

    frame_number = 0

    speech_triggered = False

    def do_something():

        global speech_triggered

        # Detect/Locate Faces and get Names of every face from the file name
        face_locations, face_names = face_recog.detect_known_faces(frame)

        #create a new list of detections for each frame
        detections = []

        for face_loc, name in zip(face_locations, face_names):
            #detection coordinates
            y1, x2, y2, x1 = face_loc 
            detection = Detection(x1, x2, y1, y2, name, frame_stamp) 
            detections.append(detection)

        for detection in detections:

            #if person is unknown, ask 'what's your name', save the name and face image
            if detection.det_id == "Unknown":

                #If Speech was triggered before set back to false to make sure it will trigger again
                speech_triggered = False

                #checks if the new detection corresponds to an old track through the distance between the center of rectangles and common area between rectangles
                if len(tracks) > 0:
                    for track in tracks:
                        distance = math.sqrt((detection.cx - track.detections[-1].cx)**2 + (detection.cy - track.detections[-1].cy)**2)
                        iou = IOU(detection, track.detections[-1])
                        print('distance: '+str(distance)+' iou:'+str(iou))
                        if iou > 0.5 or distance < 100:
                            detection.det_id = track.id
                            speech_triggered = True
                            break # leaves the loop and doesn't associate this detection to another track/person 

                if not speech_triggered:

                    start_point = (detection.left, detection.top)
                    end_point = (detection.right, detection.bottom)
                    cv2.rectangle(image_gui, start_point, end_point, (0, 0, 255), 2) # draw rectangle
                    cv2.imshow('Face recognition', image_gui)
                    cv2.waitKey(10)

                    # Start speech thread / Ask the unknown person what's their name
                    text = "What's Your name?"

                    speech_thread = Thread(target=say, args=(text,))
                    speech_thread.start()

                    # Set speech_triggered back to true so it doesn't ask again until another unknown person comes into frame
                    speech_triggered = True

                    # Save new person
                    try:
                        new_name = tell_your_name()
                    except sr.UnknownValueError:
                        new_name = input("Please type your name: ")


                    face = frame[detection.top-10:detection.bottom+10, detection.left-10:detection.right+10]


                    try:
                        cv2.imwrite(f'./images/{new_name}.jpg', face)  # Smile and take a pic      
                    except cv2.error:
                        cv2.imwrite(f'./images/{new_name}.jpg', frame)  # Smile and take a pic      

                    face_recog.load_images("./images")  # Reload images after adding a new one                    
                    face_names.append(new_name)  # Add the new name to the list of known names

                    #If Speech was triggered before set back to false to make sure it will trigger again to greet the new person
                    speech_triggered = False

                    ### Greet new person
                    text = f"Hello, {new_name}"

                    # # Start speech thread
                    speech_thread = Thread(target=say, args=(text,))
                    speech_thread.start()

                    # Set the flag
                    speech_triggered = True

            #If person is known say Hello
            if detection.det_id != "Unknown" and speech_triggered == False:
                text = f"Hello, {detection.det_id}"

                # # Start speech thread
                speech_thread = Thread(target=say, args=(text,))
                speech_thread.start()

                # Set the flag
                speech_triggered = True

        idx_remove = []

        for idx, detection in enumerate(detections):
            for track in tracks:
                if detection.det_id == track.id: 
                    #it's the same person, therefore update coordinates
                    track.update(detection)
                    track.active = True
                    idx_remove.append(idx) #saves the detection's index to remove afterwards
                    break

        # remove from the detection list those related to a track 
        idx_remove.reverse()
        for idx in idx_remove:
            del detections[idx]

        #creation of a new track for the remaining detections 
        for detection in detections:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            track = Track(detection.det_id, detection, color)
            tracks.append(track)

        #see if the track is active
        for track in tracks:
            time_since_last_detection = frame_stamp - track.detections[-1].stamp
            if time_since_last_detection > 3: 
                track.active = False
                track.detections = track.detections[-2:]

        #draw rectangles around the face and a tracking line 
        y = 0
        for track in tracks:
            if track.id != "Unknown" and track.active == True:
                track.draw(image_gui)
            #if track is inactive shows a message
            elif track.id != "Unknown" and track.active == False:
                cv2.putText(image_gui, track.id + ' was previously detected', (30,30+y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, track.color, 2)
                y += 20


    while True:

        _, frame = video.read()

        frame = cv2.flip(frame, 1)

        image_gui = copy.deepcopy(frame)

        frame_stamp = round(float(video.get(cv2.CAP_PROP_POS_MSEC))/1000, 2) 

        #for the first frame, shows the windows where is going to detect faces
        if frame_number == 0:
            cv2.imshow("Face recognition", image_gui)
            cv2.waitKey(100)
            frame_number += 1
        
        do_something()

        #Show windows with person to detect
        cv2.imshow("Face recognition", image_gui)

        #show data base when click d key
        if cv2.waitKey(1) & 0xFF == ord('d'):
                show_database('./images')

        #Break out of the while loop
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break



    # Release video and destroy all windows
    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()