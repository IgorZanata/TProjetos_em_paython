
class Pessoa():
    def __init__(self,nome, numero):
        self.nome = nome
        self.numero = numero


    def exibir(self):
        print(f"Nome:{self.nome}")
        print(f"Numero:{self.numero}")

    
    def alterar_nome(self,valor):
        self.nome = valor

        
    def alterar_numero(self,valor):
        self.numero = valor

agenda = []


def menu():

    try:
        return int(input("1 - Adicionar\n" \
                        "2 - Alterar\n" \
                        "3 - Exibir Todos os contatos\n" \
                        "4 - Procurar Contato\n" \
                        "5 - Remover Contato\n" \
                        "6 - Salvar\n" \
                        "0 - Sair\n" \
                        "--->>>"))
    except ValueError:
        print("Somente Numeros")
        return None
    
def adicionar():


    try:
        nome = input("Nome:").strip().upper()
        numero = int(input("Numero:"))
        p1 = Pessoa(nome, numero)
        agenda.append(p1)
        print("Cadastro Realizado")
    
    except ValueError:
        print("Somente Numeros")
            
def deletar(valor):

    for pessoa in agenda:
        if pessoa.nome == valor:
            agenda.remove(pessoa)
            print("Removido")
            return
    
    
    print("Não encontrado")

def salvar():

    with open("/home/igor/Documentos/GitHub/Python_em_pratica/Lista_Contatos.txt", "w", encoding = "utf-8") as arquivo:

        for i in agenda:
            linha = f"Nome: {i.nome}, Tel: (16){i.numero}\n"
            arquivo.write(linha)

def menu2():
     
    try:

        valor = int(input("1 Alterar Nome\n" \
                            "2 Alterar numero\n" \
                            "--->>>"))
    except ValueError:
        print("Somente numeros")
    return valor




while True:

    opcao = menu()

    if opcao == None:
        continue

    if opcao == 0:
        print("Encerrando !!")
        break
    
    if opcao == 1:
        adicionar()

    elif opcao == 2:

        opcao = menu2()

        if opcao == 1:

            valor = input("Digite o nome para alterar:").strip().upper()

            for pessoa in agenda:
                if pessoa.nome == valor:
                    try:
                        novo_nome = input("Digite o nome atualizado:"). strip().upper()
                        pessoa.alterar_nome(novo_nome)
                        print("Nome alterado com sucesso")
                        break

                    except ValueError:
                        print("Somente numeros")
            else:
                print("Nome não encontrado")


        elif opcao == 2:

            valor = input("Digite o nome para alterar:").strip().upper()

            for pessoa in agenda:
                if pessoa.nome == valor:
                    try:
                        novo_numero= int(input("Digite o numero atualizado:"))
                        pessoa.alterar_numero(novo_numero)
                        print("NUmero alterado comsucesso")
                        break
                    
                    except ValueError:
                        print("Somente numeros")
                
            else:
                print("Nome não encontrado")
       
    elif opcao == 3:
        
        for i in agenda:
            i.exibir()
            print("==============")

    elif opcao == 4:

        nome = input("Digite o nome para encontrar").strip().upper()

        for i in agenda:
            if i.nome == nome:
                i.exibir()
                break
        else:
            print("Nome não encontrado")

    elif opcao == 5:

        nome = input("Digite o nome para deletar:").strip().upper()

        for i in agenda:
            if i.nome == nome:
                deletar(nome)
                break
        
        else:
            print("Nome não encontrado")

    elif opcao == 6:
        salvar()
        print("Salvado")

        