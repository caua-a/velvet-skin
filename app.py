from flask import Flask, render_template, redirect, request, jsonify, session
from google import genai
from PIL import Image
from dotenv import load_dotenv
from model.cadastro import cadastrar_usuario, recuperar_users, recuperar
from model.produtos import recuperar_produtos, detalhe_produto
from model.comentario import inserir_comentario, puxar_comentario   
from model.carrinho import recuperar_itens_carrinho, salvar_item_carrinho, deletar_item_carrinho

load_dotenv()
app = Flask(__name__)
app.secret_key = "senha123"

client = genai.Client(api_key='AQ.Ab8RN6L5F8DgyoMhOUcrHSg0NtmSpfIQwXNICXyFJMz0JzMWBw')


@app.route('/')
def pagina_inicial():
    dados = recuperar_produtos()
    return render_template('index.html', dados = dados)

@app.route('/cadastro')
def pagina_cadastro():
    return render_template('pagina_cadastro.html')

@app.route('/login')
def pagina_login():
    return render_template('pagina_login.html')


@app.route('/perfil_user')
def pagina_perfil():
    usuario_sessao = session.get('usuario_logado')
    
    if not usuario_sessao:
        return redirect('/login') 
        

    usuario_nome = usuario_sessao['usuario'] if isinstance(usuario_sessao, dict) else usuario_sessao

    usuario = recuperar(usuario_nome) 
    return render_template('perfil.html', usuario=usuario)


@app.route('/login/logar',methods = ['post'])
def logando():
    usuario = request.form.get('usuariologin')
    senha = request.form.get('senhalogin')
    user = recuperar_users(usuario, senha)
    if user:
        session['usuario_logado'] = user
        return redirect('/perfil_user')
    return redirect('/cadastro')


@app.route('/cadastro/cadastrar', methods=['POST', 'GET'])
def cadastrando():
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    endereco = request.form.get('endereco')
    senhapri = request.form.get('senha')
    senhaconf = request.form.get('confirmar-senha')
    if cadastrar_usuario(nome, senhapri, email, telefone, endereco) and senhapri == senhaconf:
        return redirect('/login')
    return redirect('/cadastro')

@app.route('/produto/<int:id>')
def detalhe_produtoo(id):
    comentarios = puxar_comentario(id)
    produto = detalhe_produto(id)
    return render_template('produto.html', produto=produto, comentarios = comentarios)




@app.route('/produto/comentario/inserir/<int:id>', methods =["POST"])
def inserir_coment(id):
    nome = request.form.get('name')
    nota = request.form.get('stars')
    comentario = request.form.get('comment')
    
    inserir_comentario(nota, nome, comentario, id)
    return redirect(request.referrer or '/')









@app.route('/obter-popup')
def obter_popup():
    # Envia o seu HTML do formulário quando o JS pedir
    return render_template('assistente.html')
@app.route('/analisar', methods=['POST'])
def analisar_foto():
    # 1. Pega a foto que veio do HTML
    foto_do_usuario = request.files['foto']
    
    # 2. Abre a imagem para a IA conseguir ver
    imagem = Image.open(foto_do_usuario.stream)
    
    # 3. Envia a foto e a pergunta para o Gemini
    resposta = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[imagem, """Analise a pele da pessoa na foto e responda em um texto curto e amigável.

Informe:
- O tipo de pele (oleosa, seca, mista ou normal).
- Uma breve explicação do motivo.
- Até 3 recomendações simples de cuidados.

Não faça diagnósticos médicos.
Não mencione doenças.
Responda em no máximo 5 linhas."""]
    )
    
    # 4. Mostra o texto que a IA respondeu direto na tela
    return render_template('resultado.html', resultado=resposta.text)


@app.route('/questionario')
def pagina_questionario():
    return render_template('questionario.html')


CARRINHO_SIMULADO = [
    {
        "id_carrinho": 1,
        "id_produto": 1,
        "produto": "Sérum de Ácido Hialurónico",
        "preco": 24.99,
        "quantidade": 1,
        "imagem": "img/creme hidratante bebe.png" 
    },
    {
        "id_carrinho": 2,
        "id_produto": 3,
        "produto": "Creme Hidratante Velvet Night",
        "preco": 29.90,
        "quantidade": 2,
        "imagem": "img/creme hidratante bebe.png"
    }
]

# --- ROTAS DA API DO CARRINHO (JSON) ---

@app.route("/api/get/carrinho", methods=["GET"])
def get_carrinho():
    try:
        # Busca os itens reais direto do MySQL
        itens_reais = recuperar_itens_carrinho()
        return jsonify(itens_reais), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


@app.route("/api/post/item_carrinho", methods=["POST"])
def post_item_carrinho():
    try:
        dados = request.get_json()
        id_produto = int(dados.get("id_produto"))
        quantidade = int(dados.get("quantidade"))
        
        # Salva ou atualiza no banco de dados MySQL
        salvar_item_carrinho(id_produto, quantidade)
        
        return jsonify({"status": "sucesso", "mensagem": "Item processado no banco de dados"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


@app.route("/api/delete/item_carrinho/<int:id_produto>", methods=["DELETE"])
def delete_item_carrinho(id_produto):
    try:
        # Executa a deleção no banco de dados
        deletar_item_carrinho(id_produto)
        return jsonify({"status": "sucesso", "mensagem": "Item removido com sucesso"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
