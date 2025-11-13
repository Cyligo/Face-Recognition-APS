import numpy as np
import cv2
import os
import csv

def distancia_euclidiana(v1, v2):
    return np.sqrt(((v1-v2)**2).sum())

def knn(treino, teste, k=5):
    distancias = []

    for i in range(treino.shape[0]):
        # Vetor de características (ix) e rótulo (iy)
        ix = treino[i, :-1]
        iy = treino[i, -1]
        d = distancia_euclidiana(teste, ix)
        distancias.append([d, iy])

    # Ordena e obtém os k vizinhos mais próximos
    dk = sorted(distancias, key=lambda x: x[0])[:k]
    rotulos = np.array(dk)[:, -1]

    # Encontra o rótulo com a maior frequência
    saida = np.unique(rotulos, return_counts=True)
    indice_max = np.argmax(saida[1])
    return saida[0][indice_max]

captura = cv2.VideoCapture(0)
detector_face = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

caminho_dataset = "./face_dataset/"

dados_face = []  # Vetores de características
rotulos_face = []  # Rótulos (ID da pessoa)
id_classe = 0      # ID único para cada pessoa
nomes = {}         # Mapeamento de IDs para nomes


# Preparação do Dataset
for arquivo_dados in os.listdir(caminho_dataset):
    if arquivo_dados.endswith('.npy'):
        nomes[id_classe] = arquivo_dados[:-4]
        dados_item = np.load(caminho_dataset + arquivo_dados)
        dados_face.append(dados_item)

        alvo = id_classe * np.ones((dados_item.shape[0],))
        id_classe += 1
        rotulos_face.append(alvo)

# Concatena todos os dados de face e rótulos
dataset_completo = np.concatenate(dados_face, axis=0)
vetor_rotulos = np.concatenate(rotulos_face, axis=0).reshape((-1, 1))

# Cria o conjunto de treinamento
conjunto_treino = np.concatenate((dataset_completo, vetor_rotulos), axis=1)

# Carrega permissões do arquivo CSV
permissoes = {}
try:
    with open('usuarios.csv', mode='r', encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            nome = linha['nome']
            nivel = int(linha['nivel'])
            permissoes[nome] = nivel

    print("✅ Permissões carregadas com sucesso:")
    print(permissoes)

except FileNotFoundError:
    print("🚨 ERRO: Arquivo 'usuarios.csv' não encontrado!")
    print("         Execute o script de registro ou crie o arquivo manualmente.")
except Exception as e:
    print(f"🚨 ERRO ao ler o arquivo CSV: {e}")


fonte = cv2.FONT_HERSHEY_SIMPLEX

while True:
    sucesso, quadro = captura.read()
    if not sucesso:
        continue

    gray = cv2.cvtColor(quadro, cv2.COLOR_BGR2GRAY)

    faces = detector_face.detectMultiScale(gray, 1.3, 5)

    for face in faces:
        x, y, l, a = face

        # Recorta a Região de Interesse (ROI) da face
        margem = 5
        secao_face = quadro[y-margem:y+a+margem, x-margem:x+l+margem]
        secao_face_redim = cv2.resize(secao_face, (100, 100))

        # Classifica a face usando KNN
        resultado = knn(conjunto_treino, secao_face_redim.flatten())

        # Identifica o nome da pessoa
        nome_predito = nomes[int(resultado)]

        # Busca o nível de permissão no dicionário
        nivel_permissao = permissoes.get(nome_predito, 0) # Retorna 0 se não encontrar

        if nivel_permissao == 1:
            texto_status = "Nivel 1: Acesso Basico"
            cor = (0, 255, 255) # Amarelo
        elif nivel_permissao == 2:
            texto_status = "Nivel 2: Acesso Intermediario"
            cor = (255, 165, 0) # Laranja
        elif nivel_permissao == 3:
            texto_status = "Nivel 3: Acesso Maximo"
            cor = (0, 255, 0)   # Verde
        else:
            texto_status = "ACESSO NEGADO"
            cor = (0, 0, 255)   # Vermelho

        # Desenha as informações na tela
        cv2.putText(quadro, nome_predito, (x, y-10), fonte, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(quadro, texto_status, (x, y+a+20), fonte, 0.7, cor, 2, cv2.LINE_AA)
        cv2.rectangle(quadro, (x, y), (x+l, y+a), cor, 2)

    cv2.imshow("Faces", quadro)

    # Sai ao pressionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

captura.release()
cv2.destroyAllWindows()