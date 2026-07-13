# app/routes/auth_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from app.database import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        login_input = request.form['login']
        senha_input = request.form['senha']
        
        db = get_db()
        user = db.execute('SELECT * FROM user WHERE login = ?', (login_input,)).fetchone()
        
        if user and check_password_hash(user['senha'], senha_input):
            session['user_id'] = user['id']
            session['user_nome'] = user['nome']
            # Redireciona para a página de vendas após login bem-sucedido
            return redirect(url_for('vendas.vendas_page'))
        else:
            erro = 'Login ou senha incorretos!'
            
    return render_template('login.html', erro=erro)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))