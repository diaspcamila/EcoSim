import random
import copy

largura, altura = 1000, 1000
passo = 20 #tamanho do passo
energia_padrao = 300 #quantidade arbitrária para usar em alguns momentos, o suficiente para o ser viver por um bom tempo
energia_reproducao = 500 #quantidade de energia necessária para o ser se reproduzir

class SerVivo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energia = energia_padrao

    def mover(self, plantas, animais): #TODO fazer a borda impassável
        movimentos = ['N', 'S', 'E', 'W'] #direões possíveis de andar

        seres = plantas+animais
        vizinhos = []
        for ser in seres: #faz uma lista de vizinhos
            if self != ser:
                if (abs(self.x - ser.x) <=passo) and (abs(self.y - ser.y) <=passo):
                    vizinhos.append(ser)

        direcao = random.choice(movimentos)
        tentativas = 0
        while True: #tenta a direção aleatória, se não der certo
            tentativas += 1
            if tentativas > 4:
                if self in plantas:
                    plantas.remove(self)
                if self in animais:
                    animais.remove(self)
                break

            match direcao: #escolhe uma direção aleatória, se não funcionar, tenta outra 3 vezes
                case 'N':
                    for vizinho in vizinhos:
                        if self.y - vizinho.y >= 0 or self.y < passo*2: #se a direção é impossível, tente de novo
                            direcao = 'S'
                            continue
                    self.y += passo
                case 'S':
                    for vizinho in vizinhos:
                        if self.y - vizinho.y <= 0 or self.y > altura-passo*2:
                            direcao = 'E'
                            continue
                    self.y += -passo
                case 'E':
                    for vizinho in vizinhos:
                        if self.x - vizinho.x <= 0 or self.x > largura-passo*2:
                            direcao = 'W'
                            continue
                    self.x += -passo
                case 'W':
                    for vizinho in vizinhos:
                        if self.x - vizinho.x >= 0 or self.x < passo*2:
                            direcao = 'N'
                            continue
                    self.x += passo
            break

    def gastarEnergia(self, plantas, animais):
        if self.energia > energia_reproducao: #se reproduzir se tiver energia o suficiente
            self.energia = energia_padrao
            filho = copy.deepcopy(self)
            for i in range(15):
                filho.mover(plantas, animais) #botar o filho levemente longe
            return filho
        elif self.energia > 0: #gastar energia para se manter vivo
            self.energia -= 6 #custo energético por turno para se manter vivo
            return 0
        else: #morrer
            return -1

class Planta(SerVivo):
    def fotossintese(self, plantas):
        vizinhos = 0
        for planta in plantas:
            if (abs(self.x - planta.x) <=passo*2) and (abs(self.y - planta.y) <=passo*2):
                vizinhos += 1
        if vizinhos < 4:
            self.energia += 20

class Animal(SerVivo):
    def predar(self, plantas, animais):
        return

class Mosquito(Animal):
    def predar(self, plantas, animais):
        if self.energia < 270: #verificar se está com fome
            for planta in plantas:
                if (abs(self.x - planta.x) <=passo) and (abs(self.y - planta.y) <=passo): #verificar se tem planta perto
                    plantas.remove(planta) #mata a planta
                    self.energia += 300 #ganha energia
                    break


