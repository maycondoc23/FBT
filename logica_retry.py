def perguntar_resposta():
    resposta_correta = 1 + 1
    tentativas = 3

    for tentativa in range(1, tentativas + 1):
        resposta_usuario = input(f"Tentativa {tentativa}: Qual é o valor de 1 + 1? ")
        try:
            resposta_usuario = int(resposta_usuario)
            if resposta_usuario == resposta_correta:
                print("Resposta correta!")
                break
            else:
                print("Resposta incorreta.")
        except:
            print("Por favor, insira um número inteiro.")

    else:
        print(f"Todas as {tentativas} tentativas falharam. A resposta correta era {resposta_correta}.")

# Testando a função de pergunta
perguntar_resposta()
