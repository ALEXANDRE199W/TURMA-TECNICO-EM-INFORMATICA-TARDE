from flask import Flask, render_template, request
import psycopg2
import os

Aplicativo = Flask(__name__)

def conecta_db():
    conecta = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='12345')
    return conecta

@Aplicativo.route('/')
def homepage():
    return render_template('tela1.html')
#Alexandre
@Aplicativo.route("/cadastro", methods=['POST'])
def cadastro():
    if request.method =='POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        usuario = request.form['usuario']

        conexao = conecta_db()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO Clientes (nome, email, telefone, usuario) VALUES (%s, %s, %s, %s)", (nome, email, telefone, usuario))
        conexao.commit()
        cursor.close()
        conexao.close()

        return render_template('tela2.html')
@Aplicativo.route("/grid", methods=['GET', 'POST'])
def grid():
    if request.method == 'POST':
        relatorio = request.form['gerar_grid']
        conexao = conecta_db()
        cursor = conexao.cursor
        cursor.execute("SELECT * FROM clientes")
        resultado = cursor.fetchall()

        cursor.close()

        return render_template('grid.html', resultado=resultado)
    else:
        return render_template('grid.html', resultado=None)
#informação padrão do sistema web
if __name__ == "__main__":
    Aplicativo.run(debug=True, port=8085, host='127.0.0.1')


#filtro de pesquisa

@Aplicativo.route("/tela2", methods=['GET', 'POST'])
def filtro():
    if request.method == 'POST':
        filtro_pesquisa = request.form['filtro_input']
        conexao = conecta_db()
        cursor.execute("SELECT nome, email, telefone, usuario FROM clientes WHERE nome LIKE %s", ('%' + filtro_pesquisa + '%',))
        resultado = cursor.fetchall()

        cursor.close()

        return render_template('tela2.html', resultado=resultado)
    else:
        return render_template('filtro.html', resultado=None)
