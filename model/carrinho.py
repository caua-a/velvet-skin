from database.conexao import conectar

def recuperar_itens_carrinho():
    conexao, cursor = conectar()
    
    query = """
        SELECT 
            c.id_produto, 
            c.quantidade, 
            p.produto, 
            p.preco, 
            p.imagem 
        FROM carrinho c
        JOIN produtos p ON c.id_produto = p.id_produto
    """
    cursor.execute(query)
    itens = cursor.fetchall()  # Aqui ele já puxa uma lista de dicionários
    conexao.close()
    
    lista_formatada = []
    
    # Em vez de 'row', iteramos direto pegando cada 'item' do banco
    for item in itens:
        lista_formatada.append({
            "id_produto": item.get("id_produto"),
            "quantidade": int(item.get("quantidade", 1)),
            "produto": str(item.get("produto", "")),
            "preco": float(item.get("preco", 0.0)),
            "imagem": str(item.get("imagem", ""))
        })
        
    return lista_formatada

def salvar_item_carrinho(id_produto, quantidade):
    conexao, cursor = conectar()
    
    cursor.execute("SELECT quantidade FROM carrinho WHERE id_produto = %s", (id_produto,))
    item = cursor.fetchone()
    
    if item:
        # Atualiza o carrinho com a quantidade exata selecionada na página de produto
        cursor.execute("UPDATE carrinho SET quantidade = %s WHERE id_produto = %s", (quantidade, id_produto))
    else:
        cursor.execute("INSERT INTO carrinho (id_produto, quantidade) VALUES (%s, %s)", (id_produto, quantidade))
        
    conexao.commit()
    conexao.close()
    return True

def deletar_item_carrinho(id_produto):
    conexao, cursor = conectar()
    
    # Deleta o produto específico do carrinho
    cursor.execute("DELETE FROM carrinho WHERE id_produto = %s", (id_produto,))
    
    conexao.commit()
    conexao.close()
    return True