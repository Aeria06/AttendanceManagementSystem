# import os
# import pickle
# import numpy as np
# import cv2
# import face_recognition
# import cvzone
# import firebase_admin
# from firebase_admin import credentials, db
# from datetime import datetime

# # Initialize Firebase (Realtime DB only)
# cred = credentials.Certificate("serviceAccountsKey.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL': "https://attendancerecorder-2c65a-default-rtdb.firebaseio.com/"
# })

# # Open Webcam
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)

# # Load Background and Mode Images
# imgBackground = cv2.imread('Resources/background.png')
# folderModePath = 'Resources/Modes'
# imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in os.listdir(folderModePath)]

# # Load Encoded Data
# print("Loading Encode File ...")
# with open('EncodeFile.p', 'rb') as file:
#     encodeListKnown, studentIds = pickle.load(file)
# print("Encode File Loaded")

# # Initialize State
# modeType = 0
# counter = 0
# id = -1
# imgStudent = []

# while True:
#     success, img = cap.read()
#     if not success:
#         print("Failed to read webcam.")
#         continue

#     imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

#     faceCurFrame = face_recognition.face_locations(imgS)
#     encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

#     imgBackground[162:162 + 480, 55:55 + 640] = img
#     imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

#     if faceCurFrame:
#         for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
#             matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
#             faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
#             matchIndex = np.argmin(faceDis)

#             if matches[matchIndex]:
#                 y1, x2, y2, x1 = [v * 4 for v in faceLoc]
#                 bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
#                 imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
#                 id = studentIds[matchIndex]

#                 if counter == 0:
#                     cvzone.putTextRect(imgBackground, "Loading", (275, 400))
#                     cv2.imshow("Face Attendance", imgBackground)
#                     cv2.waitKey(1)
#                     counter = 1
#                     modeType = 1

#         if counter != 0:
#             if counter == 1:
#                 # Fetch student data
#                 studentInfo = db.reference(f'Students/{id}').get()
#                 print(studentInfo)

#                 if studentInfo is None:
#                     print(f"No student data found for ID: {id}")
#                     modeType = 0
#                     counter = 0
#                     continue  # Skip to next frame

#                 # Load image from local
#                 imagePath = f'Images/{id}.png'
#                 if os.path.exists(imagePath):
#                     imgStudent = cv2.imread(imagePath)
#                 else:
#                     imgStudent = np.zeros((216, 216, 3), dtype=np.uint8)

#                 # Check last attendance time safely
#                 last_attendance_time = studentInfo.get('last_attendance_time')
#                 if last_attendance_time is None:
#                     secondsElapsed = 99999  # Force attendance update
#                 else:
#                     datetimeObject = datetime.strptime(last_attendance_time, "%Y-%m-%d %H:%M:%S")
#                     secondsElapsed = (datetime.now() - datetimeObject).total_seconds()


#                 if secondsElapsed > 30:
#                     ref = db.reference(f'Students/{id}')
#                     studentInfo['total_attendance'] += 1
#                     ref.child('total_attendance').set(studentInfo['total_attendance'])
#                     ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#                 else:
#                     modeType = 3
#                     counter = 0
#                     imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

#             if modeType != 3:
#                 if 10 < counter < 20:
#                     modeType = 2

#                 imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

#                 if counter <= 10:
#                     cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
#                                 cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
#                     cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
#                     cv2.putText(imgBackground, str(id), (1006, 493),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
#                     cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
#                     cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
#                     cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

#                     (w, _), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
#                     offset = (414 - w) // 2
#                     cv2.putText(imgBackground, studentInfo['name'], (808 + offset, 445),
#                                 cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

#                     imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

#                 counter += 1

#                 if counter >= 20:
#                     counter = 0
#                     modeType = 0
#                     studentInfo = []
#                     imgStudent = []
#                     imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

#     else:
#         modeType = 0
#         counter = 0

#     cv2.imshow("Face Attendance", imgBackground)
#     cv2.waitKey(1)


import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
from datetime import datetime
from pymongo import MongoClient

# Initialize MongoDB client and select database/collection
client = MongoClient("mongodb://localhost:27017/")  # Change if needed
db = client['attendance_recorder']
students_collection = db['Students']

# Open Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Load Background and Mode Images
imgBackground = cv2.imread('Resources/background.png')
folderModePath = 'Resources/Modes'
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in os.listdir(folderModePath)]

# Load Encoded Data
print("Loading Encode File ...")
with open('EncodeFile.p', 'rb') as file:
    encodeListKnown, studentIds = pickle.load(file)
print("Encode File Loaded")

# Initialize State
modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()
    if not success:
        print("Failed to read webcam.")
        continue

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = [v * 4 for v in faceLoc]
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]

                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                # Fetch student data from MongoDB
                studentInfo = students_collection.find_one({"_id": id})
                

                if studentInfo is None:
                    print(f"No student data found for ID: {id}")
                    modeType = 0
                    counter = 0
                    continue  # Skip to next frame

                # Load image from local
                imagePath = f'Images/{id}.png'
                if os.path.exists(imagePath):
                    imgStudent = cv2.imread(imagePath)
                else:
                    imgStudent = np.zeros((216, 216, 3), dtype=np.uint8)

                # Check last attendance time safely
                last_attendance_time = studentInfo.get('last_attendance_time')
                if last_attendance_time is None:
                    secondsElapsed = 99999  # Force attendance update
                else:
                    datetimeObject = datetime.strptime(last_attendance_time, "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()

                if secondsElapsed > 30:
                    # Update attendance count and last attendance time in MongoDB
                    new_total = studentInfo['total_attendance'] + 1
                    students_collection.update_one(
                        {"_id": id},
                        {
                            "$set": {"last_attendance_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                            "$inc": {"total_attendance": 1}
                        }
                    )
                    # Fetch updated info to display
                    studentInfo['total_attendance'] = new_total
                    studentInfo['last_attendance_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:
                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, _), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, studentInfo['name'], (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    else:
        modeType = 0
        counter = 0

    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
