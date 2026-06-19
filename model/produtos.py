from database.conexao import conectar

def recuperar_produtos(categoria = None):
    conexao, cursor = conectar()
    if categoria:
        cursor.execute('SELECT * from produtos where categoria = %s', (categoria,))
    else:
        cursor.execute('SELECT * from produtos')
        
    dados = cursor.fetchall()
    conexao.close()
    return dados


def detalhe_produto(id):
    conexao, cursor = conectar()
    
    cursor.execute("SELECT id_produto, produto, descricao, preco, categoria,imagem FROM produtos WHERE id_produto = %s", (id,))
    
    produto_encontrado = cursor.fetchone()
    
    conexao.close()
    return produto_encontrado
