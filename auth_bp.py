from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from config.firebase_config import get_db
from google.cloud import firestore
import hashlib
import secrets

auth_bp = Blueprint('auth', __name__)

# Usuarios administradores predefinidos (en producción usar base de datos)
ADMIN_USERS = {
    'admin@nichorizon.com': {
        'password': 'admin123',  # Cambiar en producción
        'nombre': 'Administrador Principal',
        'role': 'admin'
    },
    'moderador@nichorizon.com': {
        'password': 'mod123',  # Cambiar en producción
        'nombre': 'Moderador',
        'role': 'moderator'
    }
}

def hash_password(password):
    """Hashea la contraseña para mayor seguridad"""
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        # Verificar credenciales
        if email in ADMIN_USERS:
            user_data = ADMIN_USERS[email]
            if password == user_data['password']:  # En producción comparar hash
                # Crear sesión
                session['user'] = {
                    'email': email,
                    'nombre': user_data['nombre'],
                    'role': user_data['role']
                }
                session['user_role'] = user_data['role']
                session.permanent = True
                
                flash(f'¡Bienvenido {user_data["nombre"]}!', 'success')
                return redirect(url_for('dashboard.dashboard'))
        
        flash('Credenciales incorrectas o usuario no autorizado', 'error')
    
    # Si ya está autenticado, redirigir al dashboard
    if 'user' in session and session.get('user_role') == 'admin':
        return redirect(url_for('dashboard.dashboard'))
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('auth.login'))