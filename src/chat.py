from search import search_prompt

def main():
    while True:
        user_input = input("\nFaça sua pergunta:\nPERGUNTA: ")
        command = user_input.strip().lower()

        if command in ("sair", "encerrar"):
            print("RESPOSTA: Encerrando o chat. Até mais!")
            break

        resposta = search_prompt(user_input)

        print("\nRESPOSTA:", resposta)

if __name__ == "__main__":
    main()