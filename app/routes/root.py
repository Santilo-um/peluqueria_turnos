from flask import Blueprint

root_bp = Blueprint('root', __name__)

@root_bp.route('/')
def index():
    return 'API Peluquería funcionando 🚀'