# app/routes/vendas_routes.py
from flask import Blueprint, render_template, request, jsonify
from app.database import get_db

# Criação do Blueprint de Vendas
vendas_bp = Blueprint('vendas', __name__)

@vendas_bp.route('/vendas', methods=['GET', 'POST'])
def vendas_page():
    db = get_db()
    
    if request.method == 'POST':
        data = request.get_json()
        nome_cliente = data.get('nome_cliente', 'Cliente').strip()
        if not nome_cliente:
            nome_cliente = 'Cliente'
            
        itens = data.get('itens', []) # Lista de {id: int, qtd: int, preco: float}
        
        if not itens:
            return jsonify({'erro': 'Nenhum item selecionado'}), 400
            
        preco_total = sum(item['qtd'] * item['preco'] for item in itens)
        
        # Gerar número da senha (1 a 999 contínuo)
        ultima_senha = db.execute('SELECT MAX(senha) as max_s FROM pedido').fetchone()['max_s']
        nova_senha = 1 if not ultima_senha or ultima_senha >= 999 else ultima_senha + 1
        
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO pedido (senha, preco_total, status, nome_cliente)
            VALUES (?, ?, 'Criado', ?)
        ''', (nova_senha, preco_total, nome_cliente))
        pedido_id = cursor.lastrowid
        
        for item in itens:
            cursor.execute('''
                INSERT INTO itens_pedido (fkItem, fkpedido, quantidade)
                VALUES (?, ?, ?)
            ''', (item['id'], pedido_id, item['qtd']))
            
        db.commit()
        return jsonify({
            'sucesso': True, 
            'senha': nova_senha, 
            'total': preco_total, 
            'cliente': nome_cliente
        })

    # Se for GET, busca os itens do cardápio e renderiza a tela
    itens_db = db.execute('SELECT * FROM item ORDER BY nome ASC').fetchall()
    return render_template('vendas.html', itens=itens_db)