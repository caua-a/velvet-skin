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
    coment_quant = len(comentarios)
    produto = detalhe_produto(id)
    return render_template('produto.html', produto=produto, comentarios = comentarios, coment_quant = coment_quant)





@app.route('/produto/comentario/inserir/<int:id>', methods=["POST"])
def inserir_coment(id):
    # 1. Pega o dicionário da sessão
    dados_usuario = session.get('usuario_logado') 
    if not dados_usuario:
        return redirect('/login') 

    usuario_logado = dados_usuario['usuario']
    nota = request.form.get('stars')
    comentario = request.form.get('comment')
    inserir_comentario(nota, usuario_logado, comentario, id)
    return redirect(request.referrer or '/')


@app.route('/catalogo')
def catalogoo():
    dados = recuperar_produtos()
    return render_template('pagina_catalogo.html', dados =dados)


@app.route('/catalogonoturno')
def catalogo():
    dados = recuperar_produtos()
    return render_template('pagina_catalogoNoturno.html', dados =dados)
@app.route('/catalogodiurno')
def catalogod():
    dados = recuperar_produtos()
    return render_template('pagina_catalogoDiurno.html', dados =dados)




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
        contents=[imagem, """Você é um especialista em dermatologia e consultor de skincare personalizado. O seu objetivo é analisar as necessidades do cliente e recomendar os melhores produtos do nosso catálogo.

Aqui está o catálogo de produtos disponíveis (no formato: Nome, Descrição, Preço, Tipo de Uso, Caminho da Imagem):

[
  ('Máscara de Argila Noturna (Night Clay Mask)', 'Purificação noturna profunda com argila rica em minerais, lavanda e camomila. Revitaliza e refina a pele.', 89.90, 'noturno', '/static/img/argila noturn.jpg'),
  ('Kit Pele Oleosa green upgrade', 'Produto de teste para validação de layout do catálogo.', 29.90, 'diurno', '/static/img/img_teste1.png'),
  ('Protetor Solar Facial & Corporal FPS 50+', 'Proteção de amplo espectro UVA/UVB, resistente à água. Ação anti-manchas com Niacinamida e Óleo de Amêndoas. Toque seco.', 85.00, 'diurno', '/static/img/protetor solar.png'),
  ('Sérum Facial Normal', 'Sérum de manutenção diária para hidratação leve e controle de textura.', 95.00, 'diurno', '/static/img/seru normal.jpg'),
  ('Sérum Hidratante Facial (Hydrating Facial Serum)', 'Sérum diário com AHA (Alfa-hidroxiácidos) e Ácido Hialurónico. Promove revitalização e efeito Glow radiante.', 119.90, 'diurno', '/static/img/serum facial branco.png'),
  ('Sérum Noturno Renovador (Night Serum)', 'Tratamento intensivo de reparação noturna (Night Recovery & Repair). Estimula a renovação celular para acordar com uma pele iluminada.', 134.90, 'noturno', '/static/img/serum retinol noturno.png'),
  ('Duo Creme Marrom e Sérum Diurno', 'Tratamento combinado de alta performance para o período do dia.', 159.90, 'diurno', '/static/img/serum e um creme marrom diurno.png'),
  ('Creme Noturno Restaurador de Ceramidas (Night Restoring Cream)', 'Deep Night Hydration • Ceramides & Peptides • Restores and Nourishes the Skin Barrier. Hidratação profunda para restauração da barreira cutânea.', 94.90, 'noturno', '/static/img/creme_restoring.png'),
  ('Sérum Noturno de Peptídeos e Colágeno (Night Peptide Serum)', 'Targeted Night Repair • Peptides & Collagen Complex • Firms and Improves Skin Elasticity. Atua diretamente na firmeza e linhas de expressão.', 124.00, 'noturno', '/static/img/serum_night.png'),
  ('Bálsamo Facial de Reparação Intensiva (Deep Repair Facial Balm)', 'Intense Night Nourishment • High Concentration • Repairs and Rejuvenates Damaged Skin. Nutrição noturna concentrada e reparação celular.', 139.90, 'noturno', '/static/img/balm.png')
]

DIRETRIZES DE RECOMENDAÇÃO:
1. Ignore o "Kit Pele Oleosa green upgrade", pois ele é apenas um produto de teste.
2. Separe as recomendações entre a rotina "Diurna" e "Noturna", respeitando a coluna 'Tipo de Uso'.
3. Justifique a escolha de cada produto com base nas queixas do cliente.

FORMATO DA RESPOSTA:
Sua resposta deve ser simpática, profissional e organizada da seguinte forma:
- Saudação e breve análise do caso.
- **Rotina Diurna**: Nome do produto, Preço e o motivo da escolha.
- **Rotina Noturna**: Nome do produto, Preço e o motivo da escolha.
- Valor total do investimento.

PERFIL DO CLIENTE ATUAL:
"Tenho a pele um pouco manchada pelo sol, sinto que ela está perdendo a firmeza e preciso de uma rotina da noite que realmente hidrate e renove minha pele enquanto durmo, pois acordo com a pele muito seca.""""]
    )
    
    # 4. Mostra o texto que a IA respondeu direto na tela
    return render_template('resultado.html', resultado=resposta.text)


@app.route('/logout')
def logout():
    session.clear() 
    
    return redirect('/')



# --- ROTAS DA API DO CARRINHO (JSON) ---

@app.route("/api/get/carrinho", methods=["GET"])
def get_carrinho():
    dados_usuario = session.get('usuario_logado')
    if not dados_usuario:
        return redirect('/login') 

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
        
        # Recebe do front se deve somar ou não (padrão é False se não enviado)
        somar = dados.get("somar", False) 
        
        # Passa o parâmetro 'somar' para a model atualizada
        salvar_item_carrinho(id_produto, quantidade, somar=somar)
        
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
