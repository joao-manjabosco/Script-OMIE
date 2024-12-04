import os
from client import OmieAPI
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Recupera as variáveis do ambiente
acesso = {
    'TAG': {
        'lista_empresa': os.getenv('TAG_LISTA_EMPRESA').split(','),  # Converte de string para lista
        'lista_app_key': os.getenv('TAG_LISTA_APP_KEY').split(','),
        'lista_app_secret': os.getenv('TAG_LISTA_APP_SECRET').split(','),
    },
}

def obter_dados_omie(tipos, empresas, keys, secrets):
    import pandas as pd
    
    dados_coletados = {}
    
    # Itera sobre as empresas e credenciais
    for empresa, app_key, app_secret in zip(empresas, keys, secrets):
        for tipo in tipos:
            instancia = OmieAPI(empresa, app_key, app_secret)
            try:
                # Chama o método busca_dados e armazena no dicionário
                dados = instancia.busca_dados(tipo)
                
                # Adiciona o nome da empresa como coluna nos dados retornados
                if isinstance(dados, pd.DataFrame):  # Verifica se é DataFrame
                    dados['empresa'] = empresa
                elif isinstance(dados, list):  # Se for lista de dicionários
                    for item in dados:
                        item['empresa'] = empresa
                
                # Combina dados para cada tipo
                if tipo not in dados_coletados:
                    dados_coletados[tipo] = dados
                else:
                    if isinstance(dados, pd.DataFrame):  # Concatena DataFrame
                        dados_coletados[tipo] = pd.concat([dados_coletados[tipo], dados], ignore_index=True)
                    elif isinstance(dados, list):  # Combina listas
                        dados_coletados[tipo].extend(dados)
            except Exception as e:
                print(f"Erro ao buscar dados para {tipo} na empresa {empresa}: {e}")
    
    return dados_coletados

# Lista de tipos que deseja buscar
tipos = ['movimentos_financeiros', 'clientes', 'departamentos', 'categorias', 'contas_correntes', 'dres', 'bancos']

# Chamada da função com suas credenciais
dados = obter_dados_omie(tipos, acesso['TAG']['lista_empresa'], acesso['TAG']['lista_app_key'], acesso['TAG']['lista_app_secret'])

mf = dados['movimentos_financeiros']
clientes = dados['clientes']
departamentos = dados['departamentos']
categorias = dados['categorias']
contas_correntes = dados['contas_correntes']
dre = dados['dres']
bancos = dados['bancos']
