#                                                                                                               #
# Prototype 1: Facial Recognition Feature for the application AttendNow.                                        #   
# Created by Gavin Middleton                                                                                    #
#                                                                                                               #
# All the packages needed to be downloaded for the facial recognition software, this includes face_recognition  #
# opencv-python, cmake, and dlib for python version 3.9.                                                        #
#                                                                                                               #
# cmd >> "pip install cmake" >> "pip install face_recognition" >>                                               #
#                                                                                                               #
#   - (dlib needs python 3.7-3.9;                                                                               #
#       https://github.com/z-mahmud22/Dlib_Windows_Python3.x/blob/main/dlib-19.22.99-cp39-cp39-win_amd64.whl    #
#       [download the file for 3.9 in the directory])                                                           #
#                                                                                                               #
# >> "pip install opencv-python"                                                                                #
#                                                                                                               #


import face_recognition
import cv2 as cam
import numpy
import csv
import os
from datetime import datetime


#                                                                                                               #
# User input will be implemented at a later date when we have a full webpage to add to this                     #
# the webpage is where the user will be asked to input a photo, and name of the student/employee                #
# this data will then be appended to the pictures subfile (photo), and the known_faces_names list               #
#                                                                                                               #


faceScanner = cam.VideoCapture(0)

# Call/load the photos in the file location (This is the list of students)
# *NAME*_image = face_recognition.load_image_file("*FILE PATH*")
# *NAME*_encoding = face_recognition.face_encoding(*NAME*_image)[0]

gavin_middleton_image = face_recognition.load_image_file("Pictures\Gavin Middleton.jpg")
gavin_middleton_encoding = face_recognition.face_encodings(gavin_middleton_image)[0]

# Create a list for the encoded pictures
known_face_encoding = [
    # *NAME*_encoding,
    # ...
    
    gavin_middleton_encoding
]

# Create a list for the known names for the pictures
known_faces_names = [
    # "*NAME*",
    # ...
    
    "Gavin Middleton"
]

# copy of the known faces
students = known_faces_names.copy()


# variables declared that are for the faces coming from the webcam

# - Face coordinates from the webcam
face_coords = []

# - Raw data
face_encoding = []

# - Name of the face, if present in the camera
face_names = []
trueVar = True

# - Show the current date in the excel spread sheet for when the student/employee clocks into work/class
timeNow = datetime.now()
currentDate = timeNow.strftime("%Y-%m-%d")

# - Parameters are as follows; file name ('2024-6-3.csv'), opening with write+ method, and newline has no value
attendanceList = open(currentDate + '.csv',  'w+', newline = '')

# - Class instance for writing data in the csv file
lnwriter = csv.writer(attendanceList)


while True:
    _,frame = faceScanner.read()
    small_frame = cam.resize(frame, (0, 0), fx = 0.25, fy = 0.25)
    rgb_small_frame = small_frame [:, :, :: - 1]
    if trueVar:
        
        # This will detect if there is a face in the frame or not
        face_coords = face_recognition.face_locations(rgb_small_frame)
        
        # Stores the face data of the face in the frame
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_coords)
        face_names = []
        
        for face_encoding in face_encodings:
            
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
            
            # numpy.argmin to get the best match from the data given in the webcam, and the database of pictures
            best_match_index = numpy.argmin(face_distance)
            
            # Then if the match exists the name will be connected with the face scan
            if matches[best_match_index]:
                
                name = known_faces_names[best_match_index]
                
            # Now we can enter the name in the csv file
            # if the appended name is in the known_faces_names list then we can write the name, and
            # time of attendance to the csv file
            
            face_names.append(name)
            if name in known_faces_names:
                
                if name in students:
                    
                    # The name is removed to prevent repetition
                    students.remove(name)
                    print(students)
                    currentTime = timeNow.strftime("%H-%M-%S")
                    lnwriter.writerow([name, currentTime])
    
    # Loop exit conditions
    cam.imshow("attendance system", frame)
    # Executed when 'q' is pressed
    if cam.waitKey(1) & 0xFF == ord('q'):
        break
    
faceScanner.release()
cam.destroyAllWindows()
attendanceList.close()