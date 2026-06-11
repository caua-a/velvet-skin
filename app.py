from flask import Flask, render_template, redirect, request, jsonify
from google import genai
from PIL import Image
app = Flask(__name__)
app.secret_key = "senha123"
client = genai.Client(api_key='AQ.Ab8RN6KeRi89mCM7NUJSPd_bLDVTAmInnY1jtfQnXil5WsP7IA')
@app.route('/teste')
def pagina_inicial():
    return render_template('layout.html')

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







app.run(host='0.0.0.0', port=8080, debug=True)

