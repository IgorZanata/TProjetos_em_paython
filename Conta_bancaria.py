from abc import ABC, abstractmethod

class Conta(ABC):
    def __init__(self,titular,saldo):
        self.titular = titular
        self.__saldo = saldo

    def get_saldo(self):
        return self.__saldo
    
    def set_saldo(self,valor):
        self.__saldo = valor

    def exibir(self):
        print(f"Titular:{self.titular}")
        print(f"Saldo R$", self.get_saldo())

    def sacar(self,valor):

        if valor > 0 and valor <= self.__saldo:
            self.__saldo -= valor
            print("Saque REALIZADO")
        
        else:
            print("Saldo insuficiente")

    def depositar(self,valor):

        if valor > 0:
            self.__saldo += valor
            print("Deposito REALIZADO")

        else:
            print("Valor invalido")

    @abstractmethod
    def taxa(self):
        pass

class Conta_cc(Conta):
    def __init__(self,titular,saldo,juros):
        super().__init__(titular,saldo)
        self.juros = juros
        self.taxa()
       

    def taxa(self):
        self.set_saldo(self.get_saldo() - self.juros)

class Conta_pp(Conta):
    def __init__(self,titular,saldo,juros):
        super().__init__(titular,saldo)
        self.juros = juros
        self.taxa()
    
   
    def taxa(self):
        self.set_saldo(self.get_saldo() + self.juros)



lista = []


    

def menu():

    try:    
        return int(input("1 - Adicionar\n" \
                         "2 - Remover\n"
                         "3 - Sacar\n" 
                         "4 - Depositar\n" \
                         "5 - Salvar\n" \
                         "0 - Sair\n" \
                         "--->>>"))
   
    except ValueError:
        print("Somente Numeros")
        return None

def remover(valor):

    for pessoa in lista:
        if pessoa.titular == valor:
            lista.remove(pessoa)
            print("Removido")
            return

    print("Não encontrado")

def salvar():

    with open("Documentos/GitHub/TProjetos_em_paython/Extrato_Bancario.txt", "w", encoding = "utf-8") as arquivo:

        for conta in lista:
            linha = f"Nome:{conta.titular} | Saldo R$ {conta.get_saldo()}\n"
            arquivo.write(linha)

def adicionar_cc():
    
    try:
        titular = input("Nome:").strip().upper()
        saldo = float(input("Saldo R$"))
        juros = float(input("Juros R$"))

        p1 = Conta_cc(titular, saldo, juros)

        lista.append(p1)
        print("Cadastro realizado com sucesso Conta Corrente")

    except ValueError:
        print("Somente numeros no saldo e juros")

def adicionar_cp():
    
    try:
        titular = input("Nome:").strip().upper()
        saldo = float(input("Saldo R$"))
        juros = float(input("Juros R$"))

        p2 = Conta_pp(titular, saldo, juros)

        lista.append(p2)
        print("Cadastro realizado Conta Poupança")

    except ValueError:
        print("Somente numeros no saldo e juros")

def busca(valor):

    for nome in lista:
        if nome.titular == valor:
            return nome
    
    
    return None



while True:

    print("==============================")
    opcao = menu()

    if opcao == None:
        continue

    if opcao == 0:
        print("Encerrando")
        break
    
    if opcao == 1:

        try:

            opcao = int(input("Cadastrar\nConta Poupança (1) | Conta corrente (2)\n--->>>"))

        except ValueError:
            print("Somente numeros ")

        if opcao == 1:
            adicionar_cp()
        
        elif opcao == 2:
            adicionar_cc()
        
        else:
            print("Somente as opções 1 e 2")
    
    elif opcao == 2:

        nome = input("Digite o nome para remover\n--->>>").strip().upper()
        remover(nome)
    
    elif opcao == 3:

        nome = input("Digite o nome para sacar\n--->>>").strip().upper()
        pessoa = busca(nome)

        if pessoa:

            try:
                valor = float(input("Digite o valor para saque R$"))
                pessoa.sacar(valor)

            except ValueError:
                print("Somente numeros")
        
        else:
            print("Nome não encontrado")



    elif opcao == 4:

        nome = input("Digite o nome para deposito\n--->>>").strip().upper()
        pessoa = busca(nome)

        if pessoa:
          
            try:
                valor = float(input("Digite o valor para deposito\n R$"))
                pessoa.depositar(valor)
        
            except ValueError:
                print("Somente numeros")
        
     
    
    elif opcao == 5:
        salvar()
        print("Salvo com sucesso")

