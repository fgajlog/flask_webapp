from flask import Flask, render_template, request, redirect, flash, session, url_for

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console=console

jogo1 = Jogo('Tetriz', 'puzzle', 'Atari')
jogo2 = Jogo('Pacman', 'action', 'PC')
lista_jogos = [jogo1, jogo2]

app = Flask(__name__)
app.secret_key = 'alura'

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('teste', 'test', '1234')
usuario2 = Usuario('python', 'py', 'py')

usuarios = { usuario1.nickname : usuario1,
             usuario2.nickname: usuario2 }

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos Flask', jogos=lista_jogos)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome,categoria, console)
    lista_jogos.append(jogo)
    #return render_template('lista.html', titulo='Jogos', jogos=lista_jogos)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    if proxima == None:
        proxima = '/'
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():

    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('usuario nao logado!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Deslogado!')
    return redirect(url_for('index'))




app.run(debug=True)


