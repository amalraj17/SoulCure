from django.shortcuts import render,redirect
import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model
from django.contrib.auth.decorators import login_required


def inFrame(lst):
    if lst[28].visibility > 0.6 and lst[27].visibility > 0.6 and lst[15].visibility > 0.6 and lst[16].visibility > 0.6:
        return True
    return False




def inf(request):
    cap = cv2.VideoCapture(0)
    holistic = mp.solutions.pose
    holis = holistic.Pose()
    drawing = mp.solutions.drawing_utils
    model = load_model('models/model.h5')
    labels = np.load('models/labels.npy')
    while True:
        _, frm = cap.read()
        frm = cv2.flip(frm, 1)
        res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
        if res.pose_landmarks and inFrame(res.pose_landmarks.landmark):
            lst = []
            for i in res.pose_landmarks.landmark:
                lst.append(i.x - res.pose_landmarks.landmark[0].x)
                lst.append(i.y - res.pose_landmarks.landmark[0].y)
            X = np.array(lst)
            pred = model.predict(X.reshape(1, -1))[0]
            label = labels[np.argmax(pred)]
            if np.max(pred) < 0.9:
                label = "Asana is not Defined"
            cv2.putText(frm, label, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)
        else:
            cv2.putText(frm, "Make Sure Full body visible", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
        drawing.draw_landmarks(frm, res.pose_landmarks, holistic.POSE_CONNECTIONS)
        cv2.imshow("window", frm)
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            cap.release()
            break
    return redirect('yoga')
# Create your views here.
@login_required
def yoga_page(request):
    return render(request, 'yoga.html')
@login_required
def yoga_instructions(request):
    return render(request, 'yoga_instructions.html')