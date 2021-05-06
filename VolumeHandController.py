import cv2
import time
import math
import numpy as np
import HandTrackingModule as Tracker

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

pTime = 0
cTime = 0
detector = Tracker.handDetector(detectionCon = 0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# volume.GetMute()
# volume.GetMasterVolumeLevel()

VolRange = volume.GetVolumeRange()
minVol = VolRange[0]
maxVol = VolRange[1]
vol = 0
Bar = 400
Percenatage = 0

cap = cv2.VideoCapture(0)

while True :
    success, img = cap.read()

    img = detector.findHands(img)
    PosList = detector.findPosition(img, draw = False)
    if len(PosList) != 0 :
        #print(PosList[4], PosList[8])

        x1, y1 = PosList[4][1], PosList[4][2]
        x2, y2 = PosList[8][1], PosList[8][2]
        cx, cy = (x1 + x2) //2, (y1 + y2) //2

        cv2.circle(img, (x1,y1), 10, (255,255,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (255,255,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,255,255),3)
        cv2.circle(img, (cx,cy), 10, (255,255,255), cv2.FILLED)

        length = math.hypot(x2 - x2, y1 - y2)
        print(length)

        # Hand range 10 - 350
        # Volume range 0 - 64

        vol = np.interp(length, [10,350], [minVol, maxVol])
        Bar = np.interp(length, [10,350], [400,150])
        Percenatage = np.interp(length, [10,350], [10,100])

        #print(int(length), vol)

        volume.SetMasterVolumeLevel(vol, None)
        cv2.rectangle(img, (50,150), (85,400), (255,0,0), 3)
        cv2.rectangle(img, (50,int(Bar)), (85,400), (255,0,0), cv2.FILLED)
        cv2.putText(img, f'{int(Percenatage)} %', (40,450), cv2.FONT_HERSHEY_DUPLEX, 2, (0,255,0), 2)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_DUPLEX, 2, (255,0,0), 2)

    cv2.imshow("Camera", img)
    cv2.waitKey(1)