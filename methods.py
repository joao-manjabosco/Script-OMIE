def estrutura_categorias(categorias):
    # Criando colunas de níveis 1, 2 e 3 na base categorias
    categorias['caixa_n1'] = categorias['codigo'].astype(str).str.slice(stop=1).map({
        '0': '2. TRANSFERÊNCIAS',
        '1': '3. RECEITAS',
        '2': '4. DESPESAS'
    })
    categorias['caixa_n2'] = categorias['descricao'].where(categorias['codigo'].apply(len) == 4, None).ffill()
    categorias['caixa_n3'] = categorias['descricao'].where(categorias['codigo'].apply(len) > 4, 'null')

def estrutura_dre(dre):
    # Criando tabelas dimensão
    dre_n1 = dre[dre['nivelDRE'] == 1]
    dre_n2 = dre[dre['nivelDRE'] == 2]
    dre_n3 = dre[dre['nivelDRE'] == 3]

    # Criando colunas de níveis 1 2 e 3 na base dre
    dre.loc[dre['nivelDRE'] == 1, 'dre_n1'] = dre['descricaoDRE']
    dre.loc[dre['nivelDRE'] == 2, 'dre_n2'] = dre['descricaoDRE']
    dre.loc[dre['nivelDRE'] == 3, 'dre_n3'] = dre['descricaoDRE']
    # Preenchendo os campos vazios com valores NaNs
    dre['dre_n1'] = dre['dre_n1'].ffill()
    dre['dre_n2'] = dre['dre_n2'].ffill()

def saldo_inicial(contas):
    # Montando base com ajuste de saldo
    saldos = contas.copy().rename(columns={'saldo_data':'detalhes.dDtPagamento','saldo_inicial':'resumo.nValPago','nCodCC':'detalhes.nCodCC'})
    saldos = saldos[['detalhes.dDtPagamento','resumo.nValPago','detalhes.nCodCC']].assign(
        **{
            'detalhes.cCodCateg': '0.01.01',
            'detalhes.cGrupo': 'CONTA_CORRENTE_REC',
            'detalhes.cNatureza': 'R',
            'detalhes.cOrigem': '-',
            'detalhes.cStatus': 'RECEBIDO'
        }
    )