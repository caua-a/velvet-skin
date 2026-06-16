from database.conexao import conectar


def recuperar(usuario):
    conexao, cursor = conectar()
    cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (usuario,))
    user = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    return user

def recuperar_users(usuario, password):
    conexao, cursor = conectar()
    cursor.execute('SELECT usuario, senha FROM usuarios WHERE usuario = %s AND senha = %s', (usuario, password))
    user = cursor.fetchone()
    if user:
        return user
    else:
        return []


def cadastrar_usuario(usuario, password, email, telefone, endereco):
    conexao, cursor = conectar()
    try:
        cursor.execute('INSERT INTO usuarios(usuario, senha, email, telefone, endereco_principal) VALUES(%s, %s, %s, %s, %s)', (usuario, password, email, telefone, endereco))
        conexao.commit()
        conexao.close()
        return True
    except:
        return False