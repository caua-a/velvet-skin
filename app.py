from flask import Flask, render_template, redirect, request, jsonify
from google import genai
from PIL import Image
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.secret_key = "senha123"

client = genai.Client()
@app.route('/teste')
def pagina_inicial():
    return render_template('produtos.html')

@app.route('/')
def pagina_inicial():
    return render_template('pagina_inicial.html')

@app.route('/')
def pagina_inicial():
    return render_template('pagina_cadastro.html')

@app.route('/')
def pagina_inicial():
    return render_template('pagina_login.html')




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
        contents=[imagem, "Diga de forma curta se esta pele parece seca ou oleosa."]
    )
    
    # 4. Mostra o texto que a IA respondeu direto na tela
    return resposta.text


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
        "imagem": "img/creme hidratante bebe.png" # Ajustado para bater com sua pasta
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


@app.route("/api/get/carrinho", methods=["GET"])
def get_carrinho():
    # Retorna os produtos no formato JSON que o seu JavaScript espera
    return jsonify(CARRINHO_SIMULADO)


@app.route("/api/post/item_carrinho", methods=["POST"])
def post_item_carrinho():
    dados = request.get_json()
    id_produto = dados.get("id_produto")
    quantidade = dados.get("quantidade")
    
    # Lógica simples: Procura se o item já existe para atualizar a quantidade
    for item in CARRINHO_SIMULADO:
        if item["id_produto"] == id_produto:
            item["quantidade"] = quantidade
            return jsonify({"status": "sucesso", "mensagem": "Quantidade atualizada"}), 200
            
    return jsonify({"status": "sucesso", "mensagem": "Item adicionado"}), 200


@app.route("/api/delete/item_carrinho", methods=["DELETE"])
def delete_item_carrinho():
    dados = request.get_json()
    id_produto = dados.get("id_produto")
    
    # Remove o item da nossa lista simulada
    global CARRINHO_SIMULADO
    CARRINHO_SIMULADO = [item for item in CARRINHO_SIMULADO if item["id_produto"] != id_produto]
    
    return jsonify({"status": "sucesso", "mensagem": "Item removido"}), 200




app.run(host='0.0.0.0', port=8080, debug=True)

