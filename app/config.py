import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave_secreta_ifnmg_embarcados'
    DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'barraca.db')