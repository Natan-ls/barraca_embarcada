# app/routes/admin_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash
from app.database import get_db
from app.utils import get_local_ip

# Criamos o Blueprint 'admin'
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_page():
    db = get_db()
    itens = db.execute('SELECT * FROM item ORDER BY nome ASC').fetchall()
    usuarios = db.execute('SELECT id, user, login, nome FROM user ORDER BY nome ASC').fetchall()
    
    ip_box = get_local_ip()
    url_acesso = f"http://{ip_box}:5000/login"
    
    return render_template('admin.html', itens=itens, usuarios=usuarios, url_acesso=url_acesso)

@admin_bp.route('/admin/item/salvar', methods=['POST'])
def salvar_item():
    db = get_db()
    id_item = request.form.get('id')
    nome = request.form['nome']
    preco = float(request.form['preco'])
    descricao = request.form.get('descricao', '')
    
    if id_item:
        db.execute('UPDATE item SET nome=?, preco=?, descricao=? WHERE id=?', (nome, preco, descricao, id_item))
    else:
        db.execute('INSERT INTO item (nome, preco, descricao) VALUES (?, ?, ?)', (nome, preco, descricao))
    db.commit()
    # Importante: para redirecionar para uma rota de um blueprint, usamos 'nome_do_blueprint.funcao'
    return redirect(url_for('admin.admin_page'))

@admin_bp.route('/admin/item/excluir/<int:id_item>')
def excluir_item(id_item):
    db = get_db()
    db.execute('DELETE FROM item WHERE id=?', (id_item,))
    db.commit()
    return redirect(url_for('admin.admin_page'))

@admin_bp.route('/admin/user/salvar', methods=['POST'])
def salvar_user():
    db = get_db()
    id_user = request.form.get('id')
    user = request.form['user']
    login_input = request.form['login']
    nome = request.form['nome']
    senha_input = request.form.get('senha')
    
    if id_user:
        if senha_input:
            senha_hash = generate_password_hash(senha_input)
            db.execute('UPDATE user SET user=?, login=?, nome=?, senha=? WHERE id=?', (user, login_input, nome, senha_hash, id_user))
        else:
            db.execute('UPDATE user SET user=?, login=?, nome=? WHERE id=?', (user, login_input, nome, id_user))
    else:
        if not senha_input:
            senha_input = '123456'
        senha_hash = generate_password_hash(senha_input)
        db.execute('INSERT INTO user (user, login, senha, nome) VALUES (?, ?, ?, ?)', (user, login_input, senha_hash, nome))
        
    db.commit()
    return redirect(url_for('admin.admin_page'))

@admin_bp.route('/admin/user/excluir/<int:id_user>')
def excluir_user(id_user):
    if id_user != session.get('user_id'):
        db = get_db()
        db.execute('DELETE FROM user WHERE id=?', (id_user,))
        db.commit()
    return redirect(url_for('admin.admin_page'))