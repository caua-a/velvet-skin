from database.conexao import conectar

def puxar_comentario(id):
    conexao, cursor = conectar()
    cursor.execute('SELECT * FROM comentarios where id_produto = %s', (id,))
    itens = cursor.fetchall()
    conexao.close()
    return itens

def inserir_comentario(nota ,nomeUsuario ,comentario, id):
    conexao, cursor = conectar()
    cursor.execute('INSERT INTO comentarios (usuario, comentario, nota, id_produto) values(%s, %s, %s, %s)', (nomeUsuario, comentario, nota, id))
    conexao.commit()
    conexao.close()
