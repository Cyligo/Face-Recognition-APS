import cv2
import numpy as np

captura = cv2.VideoCapture(0)
classificador_face = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

while True:
    sucesso, frame = captura.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if not sucesso:
        continue

    faces = classificador_face.detectMultiScale(gray_frame, 1.3, 5)
    if len(faces) == 0:
        continue

    for face in faces[:1]:
        x, y, l, a = face

        margem = 10
        selecao_face_margem = frame[y - margem:y + a + margem, x - margem:x + l + margem]
        selecao_face_redimensionada = cv2.resize(selecao_face_margem, (100, 100))

        cv2.imshow("Face", selecao_face_redimensionada)
        cv2.rectangle(frame, (x, y), (x + l, y + a), (0, 255, 0), 2)

    cv2.imshow("Faces", frame)

    tecla_pressionada = cv2.waitKey(1) & 0xFF
    if tecla_pressionada == ord('q'):
        break

captura.release()
cv2.destroyAllWindows()