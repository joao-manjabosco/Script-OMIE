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