from database.conexao import conectar

def recuperar_itens_carrinho():
    conexao, cursor = conectar()
    try:
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
        itens = cursor.fetchall()
        
        lista_formatada = []
        for item in itens:
            lista_formatada.append({
                "id_produto": item.get("id_produto"),
                "quantidade": int(item.get("quantidade", 1)),
                "produto": str(item.get("produto", "")),
                "preco": float(item.get("preco", 0.0)),
                "imagem": str(item.get("imagem", ""))
            })
            
        return lista_formatada
    finally:
        conexao.close()

def salvar_item_carrinho(id_produto, quantidade, somar=False):
    conexao, cursor = conectar()
    try:
        cursor.execute("SELECT quantidade FROM carrinho WHERE id_produto = %s", (id_produto,))
        item = cursor.fetchone()
        
        if item:
            if somar:
                # Se veio da página do produto, soma com o que já tem lá
                cursor.execute(
                    "UPDATE carrinho SET quantidade = quantidade + %s WHERE id_produto = %s", 
                    (quantidade, id_produto)
                )
            else:
                # Se veio do carrinho lateral (+/-), define o valor exato
                cursor.execute(
                    "UPDATE carrinho SET quantidade = %s WHERE id_produto = %s", 
                    (quantidade, id_produto)
                )
        else:
            cursor.execute("INSERT INTO carrinho (id_produto, quantidade) VALUES (%s, %s)", (id_produto, quantidade))
            
        conexao.commit()
        return True
    except Exception as e:
        conexao.rollback() # Cancela a operação se der erro
        print(f"Erro ao salvar item no carrinho: {e}")
        return False
    finally:
        conexao.close() # Garante que fecha MESMO se der erro

def deletar_item_carrinho(id_produto):
    conexao, cursor = conectar()
    try:
        cursor.execute("DELETE FROM carrinho WHERE id_produto = %s", (id_produto,))
        conexao.commit()
        return True
    except Exception as e:
        conexao.rollback()
        print(f"Erro ao deletar item do carrinho: {e}")
        return False
    finally:
        conexao.close()