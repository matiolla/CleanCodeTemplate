from models.produto import Produto

class Carrinho:
    def __init__(self):
        self.__itens: dict[Produto, int] = {}

    def adicionar(self, produto: Produto, quantidade: int):
        '''Adiciona produto ao carrinho, validando estoque e reservando unidades'''
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")
        '''Chama o método da classe Produto para tentar reduzir o estoque.
        Se o estoque for insuficiente, a exceção é programada'''
        produto.reduzir_estoque(quantidade)

        '''Se a redução de estoque foi bem-sucedida, adiciona o produto 
        ao carrinho'''
        if produto in self.__itens:
            self.__itens[produto] += quantidade
        else:
            self.__itens[produto] = quantidade

    def remover(self, produto: Produto, quantidade: int):
        '''Remover unidades do carrinho e devolve essas unidades 
        ao estoque do produto'''
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError("Quantidade inválida.")
        if produto in self.__itens:
            qtd_no_carrinho = self.__itens[produto]
            if quantidade >= qtd_no_carrinho:
                # Devolve todas as unidades e remove o item do carrinho
                produto.aumentar_estoque(qtd_no_carrinho)
                del self.__itens[produto]
            else:
                # Devolve apenas a quantidade especificada
                self.__itens[produto] -= quantidade
                produto.aumentar_estoque(quantidade)

    def listar_itens(self):
        '''Método público para acessar os itens do carrinho de forma segura'''
        return self.__itens.items()
    
    def calcular_total(self) -> float:
        '''Calcula e retorna o valor total de todos os itens no carrinho'''
        return sum(produto.preco * qtd for produto, qtd in self.__itens.items())
    
    def total_itens(self) -> int:
        '''Retorna o número total de unidades no carrinho'''
        return sum(qtd for qtd in self.__itens.values())
    
    def vazio(self) -> bool:
        '''Verifica se o carrinho está vazio'''
        return len(self.__itens) == 0
                            