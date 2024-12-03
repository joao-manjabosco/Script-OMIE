from client import OmieAPI 

# Função para automatizar a criação de instâncias e chamada ao método busca_dados
def obter_dados_omie(tipos, empresa, app_key, app_secret):
    dados_coletados = {}
    
    # Itera sobre os tipos fornecidos
    for tipo in tipos:
        instancia = OmieAPI(empresa, app_key, app_secret)
        try:
            # Chama o método busca_dados e armazena no dicionário
            dados = instancia.busca_dados(tipo)
            dados_coletados[tipo] = dados
        except Exception as e:
            print(f"Erro ao buscar dados para {tipo}: {e}")
    
    return dados_coletados

# Lista de tipos que deseja buscar
tipos = ['movimentos_financeiros', 'clientes', 'departamentos', 'categorias', 'contas_correntes', 'dres']

# Chamada da função com suas credenciais
dados = obter_dados_omie(tipos, 'Kibarlana', '4558687441308', 'eaf281d58ee604401cfa047001bed805')

movimentos_financeiros, clientes, departamentos, categorias, contas_correntes, dres = dados

# Exibe os dados de categorias como exemplo
# display(dados['categorias'])
# display(movimentos_financeiros)

categorias = dados['categorias']
mf = dados['movimentos_financeiros']
clientes = dados['clientes']
departamentos = dados['departamentos']
categorias = dados['categorias']
contas_correntes = dados['contas_correntes']
dre = dados['dres']

categorias = categorias.rename(columns={'codigo':'detalhes.cCodCateg','descricao':'categ.descricao'})
dre = dre.rename(columns={'codigoDRE':'codigo_dre'})
clientes = clientes.rename(columns={'codigo_cliente_omie':'detalhes.nCodCliente'})
contas_correntes = contas_correntes.rename(columns={'nCodCC': 'detalhes.nCodCC', 'descricao': 'cc.descricao'})
mf = mf.merge(categorias, on='detalhes.cCodCateg', how='left')
mf = mf.merge(dre, on='codigo_dre', how='left')
mf = mf.merge(clientes, on='detalhes.nCodCliente', how='left')
mf = mf.merge(contas_correntes, on='detalhes.nCodCC', how='left')
