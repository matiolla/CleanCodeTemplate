from src.controllers.sistema import Sistema

def main():
    '''Exibe o menu principal para o usuário'''
    sistema = Sistema()
    while True:
        print("\n#### Sistema mercado ####")
        print("[1] - Gerenciar produtos (adicionar / lista)")
        print("[2] - Abrir caixa e iniciar atendimento")
        print("[3] - Fechar sistema")
        opc = input("Escolha uma opção: ")

        if opc == "1":
            sistema.menu_gerenciar_produtos()
        elif opc == "2":
            sistema.abrir_caixa_e_atender()
        elif opc == "3":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida! Escolha uma das opções: 1, 2 ou 3")

if __name__ == "__main__":
    main()
