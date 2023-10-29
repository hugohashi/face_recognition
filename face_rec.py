#!/usr/bin/env python3

import face_recognition
import cv2
import os
import glob
import numpy as np

def IOU(det1, det2):
    x1_1, y1_1, x2_1, y2_1 = det1.left, det1.top, det1.right, det1.bottom
    x1_2, y1_2, x2_2, y2_2 = det2.left, det2.top, det2.right, det2.bottom

    area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
    area2 = (x2_2 - x1_2) * (y2_2 - y1_2)

    x1 = max(x1_1, x1_2)
    y1 = max(y1_1, y1_2)
    x2 = min(x2_1, x2_2)
    y2 = min(y2_1, y2_2)

    if x1 < x2 and y1 < y2:
        area_i = (x2 - x1) * (y2 - y1)
        
        area_u= area1 + area2  - area_i

        iou = area_i / area_u

        return iou
    else:
        return 0.0

class FaceRec:

    def __init__(self):

        self.known_face_encodings = []
        self.known_face_names = []


    def load_images(self, path):

        """
        Load encoding images from path
        """

        # Load Images
        images_path = glob.glob(os.path.join(path, "*.*"))

        # Store images and names
        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get the filename only from the initial file path.
            basename = os.path.basename(img_path)
            (filename, _) = os.path.splitext(basename)

            # Encode the images
            img_encoding = face_recognition.face_encodings(rgb_img)[0]

            # Store file name and file encoding
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)


    def detect_known_faces(self, frame):

        # Find all the faces and face encodings in the current frame of video
        # Convert the video frame from BGR (which OpenCV uses) to RGB (which face_recognition uses)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_names = []

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
            
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

            face_names.append(name)

        return face_locations, face_names


class Detection():

    def __init__(self, left, right, top, bottom, det_id, stamp):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        #coordenadas x, y do centro do retangulo da deteção 
        self.cx = int((self.right + self.left) / 2)
        self.cy = int((self.top + self.bottom) / 2)
        self.det_id = det_id 
        self.stamp = stamp

    #desenhar retangulo
    def draw(self, image, color):
        start_point = (self.left, self.top)
        end_point = (self.right, self.bottom)
        cv2.rectangle(image, start_point, end_point, color, 2) # desenha retangulo
        cv2.putText(image, str(self.det_id), (self.left, self.top-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    #definir ponto médio debaixo do quadrado
    def point(self):
        return (self.left + int((self.right - self.left)/2), self.bottom)


class Track:

    #definir classe
    def __init__(self, id, detection, color):
        self.id = id
        self.detections = [detection]
        self.color = color
        self.active = True

    #desenhar
    def draw(self, image):
        #desenhar retangulo do frame em q estamos!
        self.detections[-1].draw(image, self.color)

        #desenhar rasto
        for det_1, det_2 in zip(self.detections[0:-1], self.detections[1:]):
            start_pt = det_1.point()
            end_pt = det_2.point()
            cv2.line(image, start_pt, end_pt, self.color, 2)

    #update
    def update(self, detection):
        self.detections.append(detection)
