class Produto:
    def __init__(self, codigo: int, nome: str, preco: float, estoque: int = 10):
        self._codigo = int(codigo)
        self._nome = nome
        self._preco = float(preco)
        self._estoque = int(estoque)

    @property
    def codigo(self) ->int:
        return self._codigo
    @property
    def nome(self) ->str:
        return self._nome
    @property
    def preco(self) ->float:
        return self._preco
    @property
    def estoque(self) -> int:
        return self._estoque

    # Método público para gerenciar o estoque
    def reduzir_estoque(self, quantidade: int):
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva.")
        if quantidade > self._estoque:
            raise ValueError(f"Estoque insuficiente! Disponível: {self._estoque}")
        self._estoque -= quantidade

    def aumentar_estoque(self, quantidade: int):
        '''Aumentar o estoque (usando para devoluções/remoção do carrinho)'''
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva.")
        self._estoque += quantidade

    def atualizar_estoque(self, nova_quantidade: int):
        '''Define o estoque para um valor específico 
        (útil no menu de administração)'''
        nova_quantidade = int(nova_quantidade)
        if nova_quantidade < 0:
            raise ValueError("Estoque não pode ser negativo")
        self._estoque = nova_quantidade

    def __str__(self) -> str:
        '''Retorna uma representação amigável do objeto'''
        return f"[{self._codigo}] {self._nome} - R$ {self._preco:.2f} (Estoque: {self._estoque})"

    def to_dict(self) -> dict:
        '''Converte o objeto Produto para um dicionário, útil para 
        utilização no JSON'''
        return {
            "codigo": self._codigo,
            "nome": self._nome,
            "preco": self._preco,
            "estoque": self._estoque
        }
    
    @staticmethod
    def from_dict(d: dict):
        '''Cria um objeto Produto a partir de um dicionário'''
        return Produto(d["codigo"], d["nome"], d["preco"], d.get("estoque", 0))
                   
        