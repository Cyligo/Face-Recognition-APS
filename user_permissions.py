import csv
import os

def cadastro_usuario():
    arquivo_csv = 'usuarios.csv'
    cabecalho = ['nome', 'nivel']
    arquivo_existe = os.path.isfile(arquivo_csv)

    try:
        with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)

            if not arquivo_existe:
                escritor.writerow(cabecalho)
                print(f"Arquivo '{arquivo_csv}' criado com cabeçalho.")

            while True:
                print("\n--- Novo Registro ---")

                nome = input("Digite o nome da pessoa (ou 's' para sair): ")
                nome.replace(" ", "_")

                if nome.lower() == 's' or nome == "":
                    break

                while True:
                    nivel = input(f"Digite o nível para '{nome}' (1, 2 ou 3): ")
                    if nivel in ['1', '2', '3']:
                        break
                    else:
                        print("Erro: Nível inválido. Por favor, digite 1, 2 ou 3.")

                escritor.writerow([nome, nivel])
                print(f"✅ Usuário '{nome}' (Nível {nivel}) salvo com sucesso!")

        print("\nRegistro concluído.")

    except PermissionError:
        print(f"\n[ERRO] Permissão negada. Você fechou o arquivo '{arquivo_csv}' no Excel?")
    except Exception as e:
        print(f"\n[ERRO] Ocorreu um problema: {e}")