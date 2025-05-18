import os

# Caminho base do projeto (dois níveis acima de utils/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def caminho_img(*partes):
    """
    Retorna o caminho absoluto para uma imagem dentro de 'assets/images'.
    Exemplo: caminho_img("mapas", "vilarejo.png")
    """
    return os.path.join(BASE_DIR, "assets", "images", *partes)

def caminho_dado(*partes):
    """
    Retorna o caminho absoluto para um arquivo de dados dentro de 'data'.
    Exemplo: caminho_dado("historico_batalhas.csv")
    """
    return os.path.join(BASE_DIR, "data", *partes)

def caminho_statico(*partes):
    """
    Caminhos genéricos para arquivos estáticos adicionais.
    """
    return os.path.join(BASE_DIR, *partes)
