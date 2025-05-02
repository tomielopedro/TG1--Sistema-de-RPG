class HandlePersonagens:
    def __init__(self, arquivo, classes, habilidades):
        self.arquivo = arquivo
        self.classes = classes
        self.habilidades = habilidades

    def ler_arquivo(self):
        with open(self.arquivo, 'r') as entrada:
            entrada = entrada.readlines()
            entrada = [x.strip() for x in entrada if x.strip() != '']
            return entrada

    def ler_personagens(self):
        entrada = self.ler_arquivo()
        personagens = []
        for i in range(len(entrada)):
            habilidades = []

            if entrada[i].startswith('###'):
                nome = entrada[i].replace('###', '').strip()
                i += 1
                if entrada[i].startswith('- **Classe**:'):
                    try:
                        classe = entrada[i].replace('- **Classe**:', '').strip()
                        classe = self.classes.get(classe)
                        i += 1
                    except KeyError:
                        continue
                    if entrada[i].startswith('- **Habilidades**:'):
                        i += 1
                        while entrada[i].startswith('-') and len(habilidades) < classe.limite_habilidades:

                            try:
                                habilidade = entrada[i].replace('-', '').strip()
                                habilidade = self.habilidades.get(habilidade)
                                habilidades.append(habilidade)
                                if i == len(entrada) - 1:
                                    break
                                i += 1
                            except KeyError:
                                continue
                        personagem = {
                            'nome': nome,
                            'classe': classe,
                            'habilidade': habilidades
                        }
                        personagens.append(personagem)
        return personagens



