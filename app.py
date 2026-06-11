from flask import Flask, render_template, redirect, request, jsonify
from google import genai
from PIL import Image
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.secret_key = "senha123"

nfcmgh

client = genai.Client()
@app.route('/teste')
def pagina_inicial():
    return render_template('layout.html')

@app.route('/')
def index():
    return render_template('teste.html')

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







app.run(host='0.0.0.0', port=8080, debug=True)

