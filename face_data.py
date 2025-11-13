import cv2
import numpy as np
import os
from user_permissions import cadastro_usuario

captura_video = cv2.VideoCapture(0)
detector_face = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

caminho_dataset = "./face_dataset/"
contador_pulos = 0
dados_face = []

cadastro_usuario()
nome_pessoa = input("Digite novamente seu nome: ")
if nome_pessoa == "":
    print("[ERRO] Campo vazio, tente novamente.")
    cadastro_usuario()
nome_arquivo = nome_pessoa.replace(" ", "_")


while True:
    sucesso, frame_atual = captura_video.read()

    gray_frame = cv2.cvtColor(frame_atual, cv2.COLOR_BGR2GRAY)

    if not sucesso:
        continue

    faces_detectadas = detector_face.detectMultiScale(gray_frame, 1.3, 5)
    if len(faces_detectadas) == 0:
        continue

    indice_face = 1

    faces_ordenadas = sorted(faces_detectadas, key = lambda item : item[2]*item[3] , reverse = True)

    contador_pulos += 1

    for face_principal in faces_ordenadas[:1]:
        x, y, largura, altura = face_principal

        margem = 5
        secao_face_bruta = frame_atual[y-margem:y+altura+margem, x-margem:x+largura+margem]
        secao_face_padronizada = cv2.resize(secao_face_bruta,(100,100))

        if contador_pulos % 10 == 0:
            dados_face.append(secao_face_padronizada)
            print (len(dados_face))


        cv2.imshow(str(indice_face), secao_face_padronizada)
        indice_face += 1

        cv2.rectangle(frame_atual,(x,y),(x+largura,y+altura),(0,255,0),2)

    cv2.imshow("Faces", frame_atual)

    tecla_pressionada = cv2.waitKey(1) & 0xFF
    if tecla_pressionada == ord('q'):
        break

dados_face = np.array(dados_face)
dados_face = dados_face.reshape((dados_face.shape[0], -1))
print (dados_face.shape)

caminho_completo_arquivo = os.path.join(caminho_dataset, nome_arquivo)

np.save(caminho_completo_arquivo, dados_face)
print ("Dataset salvo em: {}.npy".format(caminho_completo_arquivo))

captura_video.release()
cv2.destroyAllWindows()