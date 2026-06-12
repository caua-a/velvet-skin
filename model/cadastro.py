from database.conexao import conectar

def cadastrar_usuario(usuario, password, email, telefone, endereco):
    conexao, cursor = conectar()
    cursor.execute('SELECT * FROM usuario;')
    num_users = cursor.fetchall()
    try:
        cursor.execute('INSERT INTO usuario(usuario, senha, email, telefone, endereco_principal) VALUES(%s, %s, %s, %s, %s)', (usuario, password, email, telefone, endereco))
        conexao.commit()
        conexao.close()
        return True
    except:
        return False