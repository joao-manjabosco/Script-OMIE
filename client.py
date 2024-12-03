# Importando bibliotecas
import requests
import pandas as pd
import time

class OmieAPI:
    # Listas de APIS
    movimentos_financeiros = {
        'Endpoint': 'https://app.omie.com.br/api/v1/financas/mf/',
        'omie_call': 'ListarMovimentos',
        'params': {
            'nPagina': 'nPagina',
            'registros_por_pagina': 'nRegPorPagina',
        },   
        'body': 'movimentos',
        'total_paginas': 'nTotPaginas'
    }

    clientes = {
        'Endpoint': 'https://app.omie.com.br/api/v1/geral/clientes/',
        'omie_call': 'ListarClientes',
        'params': {
            'nPagina': 'pagina',
            'registros_por_pagina': 'registros_por_pagina',
        },
        'body': 'clientes_cadastro',
        'total_paginas': 'total_de_paginas'   
    }

    departamentos = {
        'Endpoint': 'https://app.omie.com.br/api/v1/geral/departamentos/',
        'omie_call': 'ListarDepartamentos',
        'params': {
            'nPagina': 'pagina',
            'registros_por_pagina': 'registros_por_pagina',
        },
        'body': 'departamentos',
        'total_paginas': 'total_de_paginas'     
    }

    categorias = {
        'Endpoint': 'https://app.omie.com.br/api/v1/geral/categorias/',
        'omie_call': 'ListarCategorias',
        'params': {
            'nPagina': 'pagina',
            'registros_por_pagina': 'registros_por_pagina',
        },
        'body': 'categoria_cadastro',
        'total_paginas': 'total_de_paginas'  
    }

    contas_correntes = {
        'Endpoint': 'https://app.omie.com.br/api/v1/geral/contacorrente/',
        'omie_call': 'ListarContasCorrentes',
        'params': {
            'nPagina': 'pagina',
            'registros_por_pagina': 'registros_por_pagina',
            "apenas_importado_api": "N"
        },
        'body': 'ListarContasCorrentes',
        'total_paginas': 'total_de_paginas'
    }

    dres = {
        'Endpoint': 'https://app.omie.com.br/api/v1/geral/dre/',
        'omie_call': 'ListarCadastroDRE',
        'params': {
            "apenasContasAtivas": "N"
        },
        'body': 'dreLista',
    }

    calls = { 'movimentos_financeiros': movimentos_financeiros, 'clientes': clientes, 'departamentos': departamentos, 'categorias': categorias, 'contas_correntes': contas_correntes, 'dres': dres }

    def __init__(self, empresa, app_key, app_secret):
        self.empresa = empresa
        self.app_key = app_key
        self.app_secret = app_secret
        self.nPagina=1

    def busca_dados(self, tipo):
        if tipo not in self.calls:
            return None
        
        # Definindo a URL da API e os cabeçalhos da requisição
        url = self.calls[tipo]['Endpoint']
        headers = {
            'Content-type': 'application/json',
        }

        # Inicializando o número da página
        nPagina = 1

        # Lista para armazenar os dados da API
        db = []

        while True:
            # Preparar os parâmetros de acordo com a API
            parametros = {}
            if 'nPagina' in self.calls[tipo]['params'] and 'registros_por_pagina' in self.calls[tipo]['params']:
                parametros[self.calls[tipo]['params']['nPagina']] = nPagina
                parametros[self.calls[tipo]['params']['registros_por_pagina']] = 500
            # Adicionar outros parâmetros fixos, se existirem
            parametros.update({k: v for k, v in self.calls[tipo]['params'].items() if k not in ['nPagina', 'registros_por_pagina']})

            data = {
                'call': self.calls[tipo]['omie_call'],
                'app_key': self.app_key,
                'app_secret': self.app_secret,
                'param': [parametros]
            }

            # Enviando a requisição POST para a API
            response = requests.post(url, json=data, headers=headers)
            # Verificar se houve erro na requisição
            if response.status_code != 200:
                raise Exception(f"Erro na API: {response.status_code} - {response.text}")
            
            # Extendendo a lista com os dados obtidos na página atual
            db.extend(response.json().get(self.calls[tipo]['body'], []))

            # Verificar se a API suporta paginação
            if 'total_paginas' in self.calls[tipo] and 'nPagina' in self.calls[tipo]['params']:
                # Verificando se há mais páginas para serem recuperadas
                if nPagina >= response.json().get(self.calls[tipo]['total_paginas'], 1):
                    break
                else:
                    nPagina += 1
            else:
                break

        # Convertendo os dados para um DataFrame pandas
        dados = pd.json_normalize(db)
        return dados
