import datetime

class Caixa:
    '''Gerencia as operações de caixa, incluindo o registro de vendas 
    acumuladas e a geração de um relatório de fechamento do dia'''
    def __init__(self):
        self._total_dia = 0.0
        self._itens_vendidos = 0

    def registrar_vendas(self, total_compra: float, itens_vendidos: int):
        '''Registra uma venda, somendo os valores e itens ao total do dia'''
        self._total_dia += total_compra
        self._itens_vendidos += itens_vendidos

    def fechamento(self):
        '''Gera e exibe o relatório de fechamento do caixa, tanto no console 
        quanto em um arquivo de texto'''
        print("#### Fechamento do caixa ####")
        print(f"Total arrecadado no dia R$ {self._total_dia:.2f}")
        print(f"Total de itens vendidos: {self._itens_vendidos}")
        print("#"*30)

        agora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"relatório_{agora}.txt"

        with open (filename, "w", encoding="utf-8") as f:
            f.write("#### Fechamento do caixa ####\n")
            f.write(f"Total arrecadado no dia R$ {self._total_dia:.2f}\n")
            f.write(f"Total de itens vendidos: {self._itens_vendidos}\n")
            f.write("#################################\n")
        print(f"Relatório salvo em: {filename}")    

        