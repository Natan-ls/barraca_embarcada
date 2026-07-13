import sqlite3
from flask import g, current_app
from werkzeug.security import generate_password_hash

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(current_app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT UNIQUE NOT NULL,
                login TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                nome TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS item (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                descricao TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedido (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                senha INTEGER NOT NULL,
                preco_total REAL NOT NULL,
                status TEXT NOT NULL,
                nome_cliente TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS itens_pedido (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fkItem INTEGER NOT NULL,
                fkpedido INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                FOREIGN KEY (fkItem) REFERENCES item (id),
                FOREIGN KEY (fkpedido) REFERENCES pedido (id)
            )
        ''')
        
        cursor.execute('SELECT * FROM user WHERE login = ?', ('admin',))
        if not cursor.fetchone():
            senha_hash = generate_password_hash('admin123')
            cursor.execute('INSERT INTO user (user, login, senha, nome) VALUES (?, ?, ?, ?)',
                           ('admin', 'admin', senha_hash, 'Administrador do Sistema'))
        
        cursor.execute('SELECT * FROM item')
        if not cursor.fetchone():
            itens_iniciais = [
                ('Cachorro Quente', 10.00, 'Pão, salsicha, batata palha e molho especial'),
                ('Refrigerante Lata', 6.00, 'Coca-Cola ou Guaraná 350ml'),
                ('Espetinho de Carne', 12.00, 'Carne bovina selecionada com farofa'),
                ('Água Mineral', 4.00, 'Garrafa 500ml sem gás')
            ]
            cursor.executemany('INSERT INTO item (nome, preco, descricao) VALUES (?, ?, ?)', itens_iniciais)

        db.commit()