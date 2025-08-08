import json

ARQUIVO_SUGESTOES = 'apostas_sugeridas.json'
ARQUIVO_USUARIOS = 'apostas_usuarios.json'

def carregar_dados(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            # Garante que o retorno é sempre uma lista
            return dados if isinstance(dados, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_dados(caminho_arquivo, dados):
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

