
# SPRINT 6 - SISTEMA BANCÁRIO COM POO

from abc import ABC, abstractmethod


# Classe abstrata
class Conta(ABC):

    def __init__(self, titular, saldo=0):
        self.titular = titular
        self.saldo = saldo

    # Encapsulamento do titular
    @property
    def titular(self):
        return self._titular

    @titular.setter
    def titular(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Titular inválido.")

        self._titular = valor

    # Encapsulamento do saldo
    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("Saldo inválido.")

        self._saldo = valor

    # Método de depósito
    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("Depósito inválido.")

        self.saldo += valor

    # Método de saque
    def sacar(self, valor):
        if valor <= 0:
            raise ValueError("Saque inválido.")

        if valor > self.saldo:
            raise ValueError("Saldo insuficiente.")

        self.saldo -= valor

    # Método abstrato
    @abstractmethod
    def calcular_rendimento(self):
        pass

    # Métodos especiais
    def __str__(self):
        return (
            f"Titular: {self.titular} | "
            f"Tipo: {self.__class__.__name__} | "
            f"Saldo: R$ {self.saldo:.2f}"
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"({self.titular!r}, {self.saldo!r})"
        )

    def __eq__(self, outro):
        if not isinstance(outro, Conta):
            return NotImplemented

        return (
            type(self) is type(outro)
            and self.titular == outro.titular
            and self.saldo == outro.saldo
        )


# Classe filha: Conta Corrente
class ContaCorrente(Conta):

    def __init__(self, titular, saldo=0, taxa=10):
        super().__init__(titular, saldo)
        self.taxa = taxa

    @property
    def taxa(self):
        return self._taxa

    @taxa.setter
    def taxa(self, valor):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("Taxa inválida.")

        self._taxa = valor

    # Polimorfismo
    def calcular_rendimento(self):
        return -self.taxa


# Classe filha: Conta Poupança
class ContaPoupanca(Conta):

    def __init__(self, titular, saldo=0, juros=0.005):
        super().__init__(titular, saldo)
        self.juros = juros

    @property
    def juros(self):
        return self._juros

    @juros.setter
    def juros(self, valor):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("Juros inválidos.")

        self._juros = valor

    # Polimorfismo
    def calcular_rendimento(self):
        return self.saldo * self.juros


# Classe Banco: composição
class Banco:

    def __init__(self, nome):
        self.nome = nome
        self.contas = []

    def adicionar_conta(self, conta):
        if not isinstance(conta, Conta):
            raise TypeError("Objeto não é uma conta.")

        self.contas.append(conta)

    def listar_contas(self):
        for conta in self.contas:
            print(conta)

    def calcular_total(self):
        return sum(conta.saldo for conta in self.contas)

    # Métodos especiais
    def __len__(self):
        return len(self.contas)

    def __str__(self):
        return (
            f"Banco {self.nome} | "
            f"Quantidade de contas: {len(self)}"
        )

    def __repr__(self):
        return f"Banco({self.nome!r})"


# Demonstração do sistema
def main():

    banco = Banco("Python Bank")

    # Criação de 10 instâncias
    contas = [
        ContaCorrente("Ana", 1000),
        ContaPoupanca("Bruno", 2000),
        ContaCorrente("Carlos", 1500),
        ContaPoupanca("Daniela", 3000),
        ContaCorrente("Eduardo", 800),
        ContaPoupanca("Fernanda", 2500),
        ContaCorrente("Gabriel", 1200),
        ContaPoupanca("Helena", 4000),
        ContaCorrente("Igor", 900),
        ContaPoupanca("Julia", 3500)
    ]

    for conta in contas:
        banco.adicionar_conta(conta)

    print("========== CONTAS CADASTRADAS ==========")
    banco.listar_contas()

    # Polimorfismo
    print("\n========== POLIMORFISMO ==========")

    for conta in banco.contas:
        print(
            f"{conta.titular} | "
            f"Rendimento: R$ "
            f"{conta.calcular_rendimento():.2f}"
        )

    # Depósito
    print("\n========== DEPÓSITO ==========")

    contas[0].depositar(500)
    print(contas[0])

    # Saque
    print("\n========== SAQUE ==========")

    contas[1].sacar(200)
    print(contas[1])

    # Métodos especiais
    print("\n========== MÉTODOS ESPECIAIS ==========")

    print(str(contas[0]))
    print(repr(contas[1]))
    print(f"Contas iguais: {contas[0] == contas[1]}")
    print(f"Quantidade de contas: {len(banco)}")

    # Teste de exceções
    print("\n========== TRATAMENTO DE EXCEÇÕES ==========")

    try:
        contas[0].sacar(999999)

    except ValueError as erro:
        print(f"Erro capturado: {erro}")

    try:
        contas[1].saldo = -100

    except ValueError as erro:
        print(f"Erro capturado: {erro}")

    try:
        contas[2].depositar(-50)

    except ValueError as erro:
        print(f"Erro capturado: {erro}")

    # Teste de titular inválido
    try:
        contas[3].titular = ""

    except ValueError as erro:
        print(f"Erro capturado: {erro}")

    # Relatório final
    print("\n========== RELATÓRIO FINAL ==========")

    print(banco)

    print(
        f"Saldo total do banco: "
        f"R$ {banco.calcular_total():.2f}"
    )


if __name__ == "__main__":
    main()

