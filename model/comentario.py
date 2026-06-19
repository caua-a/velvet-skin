from database.conexao import conectar

def puxar_comentario(id):
    conexao, cursor = conectar()
    cursor.execute('SELECT * FROM comentarios where id_produto = %s', (id,))
    itens = cursor.fetchall()
    conexao.close()
    return itens

def inserir_comentario(nota ,nomeUsuario ,comentario):
    conexao, cursor = conectar()
    cursor.execute('INSERT INTO comentarios (usuario, comentario, nota) values(%s, %s, %s)', (nomeUsuario, comentario, nota))
    conexao.commit()
    conexao.close()
