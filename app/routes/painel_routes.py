# app/routes/painel_routes.py
from flask import Blueprint, render_template, jsonify
from app.database import get_db

painel_bp = Blueprint('painel', __name__)

@painel_bp.route('/')
@painel_bp.route('/painel')
def painel_page():
    return render_template('painel.html')

@painel_bp.route('/api/painel_dados')
def api_painel():
    db = get_db()
    
    # 1. Busca o último finalizado para exibir em destaque gigante
    ultimo_pronto = db.execute('''
        SELECT senha, nome_cliente FROM pedido 
        WHERE status = 'finalizado' ORDER BY id DESC LIMIT 1
    ''').fetchone()
    
    # 2. Busca os últimos 10 finalizados (excluindo o que já está no destaque)
    id_excluir = -1
    if ultimo_pronto:
        res = db.execute("SELECT id FROM pedido WHERE status = 'finalizado' ORDER BY id DESC LIMIT 1").fetchone()
        id_excluir = res['id'] if res else -1

    ultimos_10 = db.execute('''
        SELECT senha, nome_cliente FROM pedido 
        WHERE status = 'finalizado' AND id != ? ORDER BY id DESC LIMIT 10
    ''', (id_excluir,)).fetchall()
    
    # 3. Busca os pedidos que estão sendo preparados pela cozinha
    em_preparacao = db.execute('''
        SELECT senha, nome_cliente FROM pedido 
        WHERE status = 'em_preparacao' ORDER BY id ASC
    ''').fetchall()

    return jsonify({
        'ultimo_pronto': dict(ultimo_pronto) if ultimo_pronto else None,
        'ultimos_10': [dict(row) for row in ultimos_10],
        'em_preparacao': [dict(row) for row in em_preparacao]
    })