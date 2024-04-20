from deepface import DeepFace
import cv2

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
print("Выберите режим работы:)")
print("Введите 0 для работы с веб-камерой")
print("Введите любого другого символа будет означать работу с видео в формате .mp4")
x = input()
if x == "0":
    cap = cv2.VideoCapture(0)
else:
    print("Введи имя файла, который хотите открытьс указанием формата .mp4")
    cap = cv2.VideoCapture(input())
if not cap.isOpened():
    raise IOError("Техническая ошибка")
    
ton = [0 for i in range(6)]

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = faceCascade.detectMultiScale(gray, scaleFactor=1.01, minNeighbors=100, minSize=(135, 135))
  
    for x,y,w,h in face:
        image = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        try :
            result = DeepFace.analyze(frame, actions = ['emotion'])
            #fear, neutral, sad, surprise, angry, happy
            cv2.putText(frame, result[0]['dominant_emotion'], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            #к сожалению, putText только для латинских символов и цифр
            if result[0]['dominant_emotion'] == "neutral":
                print("спокойствие")
            elif result[0]['dominant_emotion'] == "sad":
                print("грусть")
            elif result[0]['dominant_emotion'] == "fear":
                print("страх")
            elif result[0]['dominant_emotion'] == "surprise":
                print("удивление")
            elif result[0]['dominant_emotion'] == "angry":
                print("злость")
            elif result[0]['dominant_emotion'] == "happy":
                print("радость")
        except:
            pass
            
    cv2.imshow('', frame)
    if cv2.waitKey(1) & 0xFF == ord('1'):
        break
      
max_ton = max(ton)
idx = ton.index(max_ton)
if idx == 0:
    print("Вердикт: спокойный тон")
elif idx == 1:
    print("Вердикт: минорный тон")
elif idx == 2:
     print("Вердикт: возбуждённый испуганный тон")
elif idx == 3:
     print("Вердикт: возбуждённый шокированный тон")
elif idx == 4:
     print("Вердикт: возбуждённый агрессивный тон")
else:
     print("Вердикт: возбуждённый радостный тон")

cap.release()
cv2.destroyAllWindows() 
