from .Classe import *
from .Personagem import *

class Arena:
    def init(self, lista_personagens):
        self.lista_personagens = list()
        
    def addPersonagens(self, *args):
        for personagem in args:
            if (isinstance(personagem, Personagem)):
                self.lista_personagens.add(personagem)
                
    def removePersonagem(self, personagem):
        self.lista_personagem = self.lista_personagens.remove(personagem)
    
    def __str__(self) -> str:
        for personagem in self.lista_personagem:
            print(f'Personagem: {personagem} \n')
    
if __name__ == "__main__":
    lista_habilidades = Cura, TiroDeArco
    p1 = Personagem("Carolina", Ladino, lista_habilidades)
    p2 = Personagem("Pedro", Mago, lista_habilidades )
    arena1 = Arena()
    arena1.addPersonagens(p1,p2)
    print(arena1)
    