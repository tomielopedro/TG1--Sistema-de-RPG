from RPG import *
from utils import *

if __name__ == '__main__':
    classes = {
        'Mago': Mago(),
        'Guerreiro': Guerreiro(),
        'Ladino': Ladino()
    }

    habilidades_permitidas = {
        'BolaDeFogo': BolaDeFogo(),
        'Cura': Cura(),
        'Tiro de Arco': TiroDeArco()
    }

    handle_personagens = HandlePersonagens('data/entrada.txt', classes, habilidades_permitidas)
    print(handle_personagens.ler_personagens())