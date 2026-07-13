# app/routes/status_routes.py
from flask import Blueprint, render_template, redirect, url_for
from app.database import get_db

# Criação do Blueprint de Status
status_bp = Blueprint('status', __name__)

@status_bp.route('/status')
def status_page():
    db = get_db()
    
    # Pega pedidos que ainda não foram entregues ao cliente
    pedidos = db.execute('''
        SELECT * FROM pedido 
        WHERE status IN ('Criado', 'em_preparacao', 'finalizado') 
        ORDER BY id ASC
    ''').fetchall()
    
    # Mapear os itens de cada pedido para os atendentes visualizarem na cozinha
    pedidos_com_itens = []
    for p in pedidos:
        itens = db.execute('''
            SELECT item.nome, itens_pedido.quantidade 
            FROM itens_pedido 
            JOIN item ON item.id = itens_pedido.fkItem 
            WHERE itens_pedido.fkpedido = ?
        ''', (p['id'],)).fetchall()
        
        p_dict = dict(p)
        p_dict['itens'] = [dict(i) for i in itens]
        pedidos_com_itens.append(p_dict)
        
    return render_template('status.html', pedidos=pedidos_com_itens)

@status_bp.route('/mudar_status/<int:pedido_id>/<novo_status>')
def mudar_status(pedido_id, novo_status):
    # Lista de status permitidos (segurança para evitar status inválidos)
    status_permitidos = ['Criado', 'em_preparacao', 'finalizado', 'entregue']
    
    if novo_status in status_permitidos:
        db = get_db()
        db.execute('UPDATE pedido SET status = ? WHERE id = ?', (novo_status, pedido_id))
        db.commit()
        
    # Redirecina de volta para a função status_page dentro do blueprint status
    return redirect(url_for('status.status_page'))