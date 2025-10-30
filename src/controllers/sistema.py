import os, json, datetime
from src.models.produto import Produto
from src.models.carrinho import Carrinho
from src.models.pagamento import Pagamento
from src.models.caixa import Caixa

class Sistema:
    def __init__(self):
        self._arquivo = "database/produto.json"
        self._proximo_codigo = 1
        self.produtos: list[Produto] = []
        self.caixa = Caixa()
        self._carregar_produtos()

    def _salvar_produtos(self):
        dados = [p.to_dict() for p in self.produtos]
        with open(self._arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

    def _carregar_produtos(self):
        if os.path.exists(self._arquivo):
            try:
                with open(self._arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                self.produtos = [Produto.from_dict(d) for d in dados]
                if self.produtos:
                    self._proximo_codigo = max(p.codigo for p in self.produtos) + 1
            except Exception as e:
                print(f"Erro ao ler {self._arquivo}: {e}")
                self.produtos = []
                self._proximo_codigo = 1
        else:
            self.produtos = []
            self._proximo_codigo = 1

    def menu_gerenciar_produtos(self):
        while True:
            print("\n#### Gerenciar produtos ####")
            print("[1] - Listar produtos")
            print("[2] - Adicionar produto")
            print("[3] - Ajustar estoque de um produto")
            print("[4] - Deletar produto")
            print("[0] - Voltar")
            opc = input("Escolha uma opção: ")

            if opc == "1":
                self.lista_produtos()
            elif opc == "2":
                self.adicionar_produto_interativo()
            elif opc == "3":
                self.ajustar_estoque_interativo()
            elif opc == "4":
                self.deletar_produto_interativo()
            elif opc == "0":
                break
            else:
                print("Opção inválida! Tente novamente.")

    def lista_produtos(self):
        if not self.produtos:
            print("Nenhum produto cadastrado.")
            return
        print("\n==== Produtos ====")
        for p in self.produtos:
            print(p)

    def adicionar_produto_interativo(self):
        try:
            nome = input("Nome do produto: ")
            preco = float(input("Preço unitário R$ "))
            estoque = int(input("Quantidade inicial do estoque: "))
            novo = Produto(self._proximo_codigo, nome, preco, estoque=estoque)
            self.produtos.append(novo)
            self._proximo_codigo += 1
            self._salvar_produtos()
        except ValueError:
            print("Entrada inválida. Use valores numéricos para preço e estoque.")

    def ajustar_estoque_interativo(self):
        try:
            codigo = int(input("Informe o código do produto: "))
            produto = next((p for p in self.produtos if p.codigo == codigo), None)
            if produto is None:
                print("Produto não encontrado.")
                return
            novo_estoque = int(input(f"Novo estoque para '{produto.nome}': "))
            produto.atualizar_estoque(novo_estoque)
            self._salvar_produtos()
            print(f"Estoque de '{produto.nome}' atualizado para {produto.estoque}.")
        except ValueError:
            print("Entrada inválida. Use números inteiros para código e estoque")

    def deletar_produto_interativo(self):
        try:
            codigo = int(input("Código do produto a deletar: "))
            produto = next((p for p in self.produtos if p.codigo == codigo), None)
            if produto is None:
                print("Produto não encontrado.")
                return
            confirma = input(f"Confirma remover '{produto.nome}'? (S/N): ").lower()
            if confirma == "s":
                self.produtos.remove(produto)
                self._salvar_produtos()
                print(f"Produto '{produto.nome}' removido do catálogo")
            else:
                print("Operação cancelada.")
        except ValueError:
            print("Entrada inválida.")

    def abrir_caixa_e_atender(self):
        print("### Caixa aberto ###")
        while True:
            print("\n[1] - Atender próximo cliente")
            print("[2] - Fechar caixa e gerar relatório diário")
            opc = input("Escolha uma opção: ")
            if opc == "1":
                self.processo_compra()
            elif opc == "2":
                print("Fechando caixa...")
                self.fechamento_dia()
                break
            else:
                print("Opção inválida! Digite 1 ou 2")

    def exibir_menu_produtos_venda(self):
        if not self.produtos:
            print("Não há produtos para vender. Cadastre produtos no menu de adm")
            return False
        print("\n#### Produtos disponíveis ####")
        for idx, produto in enumerate(self.produtos, start=1):
            print(f"[{idx}] {produto}")
        print("[0] - Remover item do carrinho")
        print("[9] - Finalizar compra")
        return True

    def escolher_produto(self, opcao: int):
        if 1 <= opcao <= len(self.produtos):
            return self.produtos[opcao - 1]
        return None

    def processo_compra(self):
        if not self.exibir_menu_produtos_venda():
            return
        carrinho = Carrinho()
        while True:
            try:
                opcao = int(input("Escolha a opção: "))
            except ValueError:
                print("Digite um número válido.")
                continue

            if opcao == 9:
                if carrinho.vazio():
                    print("O carrinho está vazio! Adicione itens antes de finalizar.")
                    continue
                else:
                    break
            elif opcao == 0:
                self.remover_do_carrinho(carrinho)
                continue
            produto = self.escolher_produto(opcao)
            if produto:
                try:
                    qtd = int(input(f"Quantos '{produto.nome}' deseja adicionar: "))
                    carrinho.adicionar(produto, qtd)
                    print(f"{qtd}x '{produto.nome}' adicionado ao carrinho")
                except ValueError as e:
                    print(e)
            else:
                print("Opção inválida! Selecione um número do menu.")

        self.finalizar_compra(carrinho)

    def remover_do_carrinho(self, carrinho: Carrinho):
        if carrinho.vazio():
            print("O carrinho está vazio, não há itens para remover.")
            return
        print("### Itens no carrinho ###")
        itens = list(carrinho.listar_itens())
        for idx, (produto, qtd) in enumerate(itens, start=1):
            print(f"[{idx}] {produto.nome} - {qtd} unidade(s)")

        try:
            opcao = int(input("Escolha o item que deseja remover: "))
            if 1 <= opcao <= len(itens):
                produto, _ = itens[opcao - 1]
                qtd_remover = int(input(f"Quantas unidade(s) de '{produto.nome}' deseja remover: "))
                if qtd_remover > 0:
                    carrinho.remover(produto, qtd_remover)
                    print(f"{qtd_remover}x '{produto.nome}' removido do carrinho.")
                else:
                    print("Quantidade inválida.")
            else:
                print("Opção inválida.")
        except ValueError:
            print("Digite um número válido.")

    def finalizar_compra(self, carrinho: Carrinho):
        total = carrinho.calcular_total()

        print("#### Forma de pagamento ####")
        print("[1] - Dinheiro ou PIX - 10% desconto")
        print("[2] - Cartão de débito - 5% desconto")
        print("[3] - Cartão de crédito 1x - mesmo valor")
        print("[4] - Cartão de crédito 2x - 5% acréscimo")
        print("[5] - Cartão de crédito 3x - 10% acréscimo")
        print("[6] - Cartão de crédito 4x - 15% acréscimo")

        while True:
            try:
                opcao = int(input("Escolha a forma de pagamento: "))
                pagamento = Pagamento(total)
                pagamento.calcular_pagamento(opcao)
                break
            except ValueError as e:
                print(e)
                print("Opção inválida! Tente novamente.")

        print("### Resumo da compra ###")
        for produto, qtd in carrinho.listar_itens():
            print(f"{qtd}x {produto.nome} - R$ {produto.preco * qtd:.2f}")

        print(f"Forma de pagamento: {pagamento.forma}")
        print(f"Total a pagar R$ {pagamento.valor_final:.2f}")

        self.caixa.registrar_vendas(pagamento.valor_final, carrinho.total_itens())

        agora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"public/assets/nota_{agora}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("#### Nota fiscal ####\n")
            f.write(f"Data/hora: {agora}\n\n")
            for produto, qtd in carrinho.listar_itens():
                f.write(f"{qtd}x {produto.nome} - R$ {produto.preco * qtd:.2f}\n")
            f.write(f"\nForma de pagamento: {pagamento.forma}\n")
            f.write(f"Total a pagar R$ {pagamento.valor_final:.2f}\n")
            f.write("###########################\n")
        print(f"Nota fiscal salva em: {filename}")
        self._salvar_produtos()

    def fechamento_dia(self):
        self.caixa.fechamento()
