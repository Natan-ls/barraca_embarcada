from flask import Flask, request, redirect, url_for, session
from app.config import Config
from app.database import close_connection, init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Registra o fechamento do banco quando a requisição acaba
    app.teardown_appcontext(close_connection)
    
    # Inicializa o banco de dados
    init_db(app)

    # --- REGISTRO DOS BLUEPRINTS ---
    from app.routes.auth_routes import auth_bp
    from app.routes.painel_routes import painel_bp
    from app.routes.vendas_routes import vendas_bp
    from app.routes.status_routes import status_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(painel_bp)
    app.register_blueprint(vendas_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(admin_bp)

    # --- INTERCEPTADOR GERAL ---
    @app.before_request
    def verificar_autenticacao():
        rotas_livres = ['auth.login', 'painel.painel', 'painel.api_painel', 'static']
        if request.endpoint not in rotas_livres and 'user_id' not in session:
            # Observação: ao usar blueprints, o endpoint ganha o prefixo do blueprint (ex: auth.login)
            if request.endpoint and not request.endpoint.startswith('static'):
                return redirect(url_for('auth.login'))

    return app