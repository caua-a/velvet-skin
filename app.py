from flask import Flask, render_template, redirect, request, jsonify


app = Flask(__name__)

app.secret_key = "senha123"

@app.route('/')
def pagina_inicial():
    return render_template('login.html')


@app.route('/questionario')
def pagina_questionario():
    return render_template('questionario.html')






app.run(host='0.0.0.0', port=8080, debug=True)

