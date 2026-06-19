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
    return jsonify(CARRINHO_SIMULADO)


@app.route("/api/post/item_carrinho", methods=["POST"])
def post_item_carrinho():
    dados = request.get_json()
    id_produto = int(dados.get("id_produto"))
    quantidade = int(dados.get("quantidade"))
    
    # Verifica se o item já está no carrinho simulado para atualizar
    for item in CARRINHO_SIMULADO:
        if item["id_produto"] == id_produto:
            item["quantidade"] = quantidade
            return jsonify({"status": "sucesso", "mensagem": "Quantidade atualizada"}), 200
            
    # Se fosse um item novo (adicionar do zero), precisaríamos dar um .append() aqui
    return jsonify({"status": "sucesso", "mensagem": "Item processado"}), 200


@app.route("/api/delete/item_carrinho", methods=["DELETE"])
def delete_item_carrinho():
    dados = request.get_json()
    id_produto = int(dados.get("id_produto"))
    
    global CARRINHO_SIMULADO
    # Filtra mantendo apenas os itens que NÃO possuem o id_produto deletado
    CARRINHO_SIMULADO = [item for item in CARRINHO_SIMULADO if item["id_produto"] != id_produto]
    
    return jsonify({"status": "sucesso", "mensagem": "Item removido"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
