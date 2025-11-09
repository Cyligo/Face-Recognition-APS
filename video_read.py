import cv2

captura = cv2.VideoCapture(0)

while True:
    ret, frame = captura.read()
    
    if not ret:
        continue
    
    cv2.imshow("video frame",frame)
  
    tecla_pressionada = cv2.waitKey(1) & 0xFF
    
    if tecla_pressionada == ord('q'):
        break
    
captura.release()
cv2.destroyAllWindows()
