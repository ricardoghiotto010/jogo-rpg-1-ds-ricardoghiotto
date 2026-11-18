import random
import time

class Entidade:
    def __init__(self, nome, vida, ataque, defesa):
        self.nome = nome
        self.vida = vida
        self.vida_max = vida
        self.ataque = ataque
        self.defesa = defesa

    def esta_vivo(self):
        return self.vida > 0

    def receber_dano(self, dano):
        self.vida = max(0, self.vida - dano)

class Jogador(Entidade):
    def __init__(self, nome, classe):
        # Stats base
        vida = 100
        ataque = 10
        defesa = 5

        # Bônus por classe
        if classe == "Guerreiro":
            ataque += 5
            defesa += 3
        elif classe == "Mago":
            ataque += 8
            defesa -= 2
        elif classe == "Arqueiro":
            ataque += 4
            defesa += 2

        super().__init__(nome, vida, ataque, defesa)
        self.classe = classe
        self.nivel = 1
        self.xp = 0
        self.xp_proximo = 50
        self.ouro = 25
        self.inventario = {"Poção de Cura": 2}

    def mostrar_status(self):
        print("\nSTATUS DO PERSONAGEM")
        print(f"Nome: {self.nome}")
        print(f"Classe: {self.classe}")
        print(f"Nível: {self.nivel}")
        print(f"XP: {self.xp}/{self.xp_proximo}")
        print(f"Vida: {self.vida}/{self.vida_max}")
        print(f"Ataque: {self.ataque}")
        print(f"Defesa: {self.defesa}")
        print(f"Ouro: {self.ouro}")
        print("Inventário:")
        if self.inventario:
            for item, qtd in self.inventario.items():
                print(f"  - {item}: {qtd}")
        else:
            print("  (vazio)")

    def adicionar_item(self, item, quantidade=1):
        if item in self.inventario:
            self.inventario[item] += quantidade
        else:
            self.inventario[item] = quantidade

    def usar_pocao(self):
        if "Poção de Cura" in self.inventario and self.inventario["Poção de Cura"] > 0:
            cura = 35
            vida_antes = self.vida
            self.vida = min(self.vida_max, self.vida + cura)
            recuperado = self.vida - vida_antes

            self.inventario["Poção de Cura"] -= 1
            if self.inventario["Poção de Cura"] <= 0:
                del self.inventario["Poção de Cura"]

            print(f"Você usou uma Poção de Cura e recuperou {recuperado} de vida.")
            print(f"Vida atual: {self.vida}/{self.vida_max}")
            return True
        else:
            print("Você não possui Poção de Cura.")
            return False

    def ganhar_xp(self, quantidade):
        self.xp += quantidade
        print(f"Você ganhou {quantidade} de XP!")
        while self.xp >= self.xp_proximo:
            self.subir_nivel()

    def subir_nivel(self):
        self.nivel += 1
        self.xp -= self.xp_proximo
        self.xp_proximo = int(self.xp_proximo * 1.4)
        self.vida_max += 12
        self.vida = self.vida_max
        self.ataque += 3
        self.defesa += 2
        print("\nVocê subiu de nível!")
        print(f"Agora você é nível {self.nivel}.")
        print(f"Vida máxima: {self.vida_max} | Ataque: {self.ataque} | Defesa: {self.defesa}")

class Monstro(Entidade):
    def __init__(self, nome, vida, ataque, defesa, xp, ouro):
        super().__init__(nome, vida, ataque, defesa)
        self.xp = xp
        self.ouro = ouro

def ler_opcao(mensagem, opcoes_validas):
    """Função com tratamento de erro para ler opções do jogador"""
    while True:
        try:
            escolha = input(mensagem).strip()
            if escolha in opcoes_validas:
                return escolha
            else:
                print("Opção inválida. Tente novamente.")
        except Exception:
            print("Erro na entrada. Digite novamente.")

def criar_personagem():
    print("\nCRIAÇÃO DE PERSONAGEM")
   
    while True:
        nome = input("Digite o nome do seu herói: ").strip()
        if nome:
            break
        print("O nome não pode ficar em branco.")

    print("\nEscolha sua classe:")
    print("1 - Guerreiro (mais força e resistência)")
    print("2 - Mago (alto ataque, pouca defesa)")
    print("3 - Arqueiro (equilibrado)")

    escolha = ler_opcao("Digite 1, 2 ou 3: ", ["1", "2", "3"])

    if escolha == "1":
        classe = "Guerreiro"
    elif escolha == "2":
        classe = "Mago"
    else:
        classe = "Arqueiro"

    return Jogador(nome, classe)

def gerar_monstro(nivel_jogador):
    # Todos os monstros têm nome, vida, ataque e defesa
    lista_monstros = [
        ("Goblin Faminto", 28, 7, 2, 12, 6),
        ("Lobo Sombrio", 38, 10, 3, 18, 9),
        ("Orc Guerreiro", 55, 13, 5, 28, 15),
        ("Esqueleto Amaldiçoado", 42, 11, 4, 22, 11),
        ("Troll da Floresta", 85, 17, 7, 45, 25),
        ("Bruxa Louca", 50, 15, 3, 35, 20)
    ]

    if nivel_jogador <= 2:
        dados = random.choice(lista_monstros[:2])
    elif nivel_jogador <= 4:
        dados = random.choice(lista_monstros[1:4])
    else:
        dados = random.choice(lista_monstros[2:])

    return Monstro(*dados)

def combate(jogador, monstro):
    print(f"\nUm {monstro.nome} surgiu do meio das árvores!")
    print(f"Vida do monstro: {monstro.vida} | Ataque: {monstro.ataque} | Defesa: {monstro.defesa}")

    while jogador.esta_vivo() and monstro.esta_vivo():
        print(f"\nSEU TURNO (Vida: {jogador.vida}/{jogador.vida_max})")
        print("1 - Atacar")
        print("2 - Usar Poção de Cura")
        print("3 - Tentar Fugir")

        acao = ler_opcao("Escolha uma ação: ", ["1", "2", "3"])

        if acao == "1":
            dano = max(1, jogador.ataque - monstro.defesa + random.randint(1, 6))
            monstro.receber_dano(dano)
            print(f"Você atacou e causou {dano} de dano.")
            print(f"Vida restante do {monstro.nome}: {monstro.vida}")

        elif acao == "2":
            if not jogador.usar_pocao():
                continue  # Se não tinha poção, volta a pedir ação

        elif acao == "3":
            chance = random.random()
            if chance < 0.45:
                print("Você conseguiu fugir da batalha!")
                return False
            else:
                print("Você tentou fugir, mas o monstro te alcançou!")

        if not monstro.esta_vivo():
            break

        # Turno do monstro
        print(f"\nTURNO DO {monstro.nome.upper()}")
        dano_monstro = max(1, monstro.ataque - jogador.defesa + random.randint(0, 5))
        jogador.receber_dano(dano_monstro)
        print(f"O {monstro.nome} atacou e causou {dano_monstro} de dano.")
        print(f"Sua vida: {jogador.vida}/{jogador.vida_max}")

    if not jogador.esta_vivo():
        print("\nVocê foi derrotado...")
        print("A escuridão do MUNDO DOS DOENTES MENTAIS te consumiu.")
        return False

    print(f"\nVocê derrotou o {monstro.nome}!")
    jogador.ganhar_xp(monstro.xp)
    jogador.ouro += monstro.ouro
    print(f"Você recebeu {monstro.ouro} de ouro.")

    if random.random() < 0.35:
        jogador.adicionar_item("Poção de Cura")
        print("Você encontrou uma Poção de Cura no corpo do inimigo.")

    return True

def gerenciar_inventario(jogador):
    while True:
        print("\nINVENTÁRIO")
        if jogador.inventario:
            for item, qtd in jogador.inventario.items():
                print(f"- {item}: {qtd}")
        else:
            print("(vazio)")

        print("\n1 - Usar Poção de Cura")
        print("2 - Voltar ao menu")

        opcao = ler_opcao("Escolha: ", ["1", "2"])

        if opcao == "1":
            jogador.usar_pocao()
        else:
            break

def menu_principal(jogador):
    while True:
        print("\nMENU PRINCIPAL")
        print(f"SALDO: {jogador.ouro} de ouro")
        print(f"Vida: {jogador.vida}/{jogador.vida_max}")
        print("1 - Explorar a floresta")
        print("2 - Ver Status")
        print("3 - Descansar (custa 10 de ouro)")
        print("4 - Comprar Poção (15 de ouro)")
        print("5 - Ver / Usar Inventário")
        print("6 - Sair do jogo")

        opcao = ler_opcao("Escolha uma opção: ", ["1", "2", "3", "4", "5", "6"])

        if opcao == "1":
            print("\nVocê caminha pela floresta densa do MUNDO DOS DOENTES MENTAIS...")
            time.sleep(1.2)
            monstro = gerar_monstro(jogador.nivel)
            venceu = combate(jogador, monstro)
            if not venceu and not jogador.esta_vivo():
                print("Fim de jogo.")
                break

        elif opcao == "2":
            jogador.mostrar_status()

        elif opcao == "3":
            if jogador.ouro >= 10:
                jogador.ouro -= 10
                jogador.vida = jogador.vida_max
                print("Você encontrou um local seguro e recuperou toda a vida.")
            else:
                print("Você não tem ouro suficiente para descansar.")

        elif opcao == "4":
            if jogador.ouro >= 15:
                jogador.ouro -= 15
                jogador.adicionar_item("Poção de Cura")
                print("Você comprou uma Poção de Cura.")
            else:
                print("Você não tem ouro suficiente.")

        elif opcao == "5":
            gerenciar_inventario(jogador)

        elif opcao == "6":
            print(f"\nObrigado por jogar, {jogador.nome}.")
            print(f"Você chegou ao nível {jogador.nivel} no MUNDO DOS DOENTES MENTAIS.")
            break

def mostrar_historia():
    print("RPG - MUNDO DOS DOENTES MENTAIS")
    print()
    print("Há muito tempo, este lugar era um reino normal.")
    print("Até que uma maldição atingiu todos os seus habitantes.")
    print("Agora, criaturas loucas e perigosas vagam pela floresta.")
    print()
    print("Você é um aventureiro que decidiu explorar este território amaldiçoado.")
    print("Seu objetivo é sobreviver, ficar mais forte e descobrir o que realmente aconteceu aqui.")
    print()
    print("COMO JOGAR:")
    print("1 - Explorar: Procura por monstros para ganhar XP e ouro")
    print("2 - Ver Status: Mostra suas informações atuais")
    print("3 - Descansar: Recupera toda a vida (custa 10 de ouro)")
    print("4 - Comprar Poção: Compra Poção de Cura (custa 15 de ouro)")
    print("5 - Inventário: Usa itens que você possui")
    print("6 - Sair: Encerra o jogo")
    print()
    print("Durante as batalhas você sempre terá pelo menos 2 opções.")
    print()
    input("Pressione ENTER para começar sua jornada...")

def main():
    mostrar_historia()
   
    jogador = criar_personagem()
    print(f"\nSeja bem-vindo, {jogador.nome} o {jogador.classe}.")
    print("A floresta do MUNDO DOS DOENTES MENTAIS te espera...")
    time.sleep(1.5)
   
    menu_principal(jogador)

if __name__ == "__main__":
    main()
