from flask import Flask
from config.firebase_config import init_firebase
from routes.main_routes import main_bp
from routes.dashboard_routes import dashboard_bp

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = 'tu_clave_secreta_aqui'

    # Inicializar Firebase
    init_firebase()

    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)

    return app

# Crear la instancia de app para Gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=8000)