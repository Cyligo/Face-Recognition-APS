import csv
import os

def verificar_usuario_existe(nome_usuario, arquivo_csv):
    if not os.path.isfile(arquivo_csv):
        return False

    try:
        with open(arquivo_csv, mode='r', newline='', encoding='utf-8') as f:
            leitor = csv.DictReader(f)
            for linha in leitor:
                if linha.get('nome') == nome_usuario:
                    return True
    except Exception as e:
        print(f"[ERRO] Ocorreu um problema ao ler o arquivo para verificação: {e}")
        return True

    return False

def cadastro_usuario():
    arquivo_csv = 'usuarios.csv'
    cabecalho = ['nome', 'nivel']
    arquivo_existe = os.path.isfile(arquivo_csv)

    if not arquivo_existe:
        try:
            with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as f:
                escritor = csv.writer(f)
                escritor.writerow(cabecalho)
                print(f"Arquivo '{arquivo_csv}' criado com cabeçalho.")
        except PermissionError:
            print(f"\n[ERRO] Permissão negada. Você fechou o arquivo '{arquivo_csv}' no Excel?")
            return
        except Exception as e:
            print(f"\n[ERRO] Ocorreu um problema ao criar o arquivo: {e}")
            return

    while True:
        print("\n--- Novo Registro ---")

        nome = input("Digite o nome da pessoa (ou 's' para sair): ")
        nome = nome.replace(" ", "_")

        if nome.lower() == 's' or nome == "":
            break

        if verificar_usuario_existe(nome, arquivo_csv):
            print(f"[ERRO: Usuário '{nome}' já existe no arquivo. Não foi salvo.")
            continue

        while True:
            nivel = input(f"Digite o nível para '{nome}' (1, 2 ou 3): ")
            if nivel in ['1', '2', '3']:
                break
            else:
                print("ERRO: Nível inválido. Por favor, digite 1, 2 ou 3.")

        try:
            with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as f:
                escritor = csv.writer(f)
                escritor.writerow([nome, nivel])
                print(f" Usuário '{nome}' (Nível {nivel}) salvo com sucesso!")
                break

        except PermissionError:
            print(f"\n[ERRO] Permissão negada. Você fechou o arquivo '{arquivo_csv}' no Excel?")
        except Exception as e:
            print(f"\n[ERRO] Ocorreu um problema ao salvar: {e}")

    print("\nRegistro concluído.")