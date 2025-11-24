from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.dashboard_service import get_dashboard_data, update_usuario, update_publicacion, update_rueda, eliminar_usuario_completamente
from config.firebase_config import get_db
from google.cloud import firestore

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    # Verificar si el usuario está autenticado como admin
    if 'user' not in session:
        flash('Acceso denegado. Debes iniciar sesión para acceder al dashboard.', 'error')
        return redirect(url_for('auth.login'))  # Redirigir al login
    
    if session.get('user_role') != 'admin':
        flash('Acceso denegado. No tienes permisos de administrador.', 'error')
        return redirect(url_for('main.inicio'))  # Redirigir a la página principal
    
    # Usar el servicio para obtener datos
    dashboard_data = get_dashboard_data()
    
    if not dashboard_data:
        flash('Error al cargar los datos del dashboard', 'error')
        return render_template('dashboardadmin.html')
    
    return render_template(
        'dashboardadmin.html',
        usuarios=dashboard_data["usuarios"],
        publicaciones=dashboard_data["publicaciones"],
        comentarios=dashboard_data["comentarios"],
        ruedas=dashboard_data["ruedas"],
        total_usuarios=dashboard_data["total_usuarios"],
        total_publicaciones=dashboard_data["total_publicaciones"],
        total_comentarios=dashboard_data["total_comentarios"],
        total_productos=dashboard_data["total_productos"],
        total_ruedas=dashboard_data["total_ruedas"]
    )
    
    #####Usar el servicio para obtener datos
    dashboard_data = get_dashboard_data()
    
    if not dashboard_data:
        flash('Error al cargar los datos del dashboard', 'error')
        return render_template('dashboardadmin.html')
    
    return render_template(
        'dashboardadmin.html',
        usuarios=dashboard_data["usuarios"],
        publicaciones=dashboard_data["publicaciones"],
        comentarios=dashboard_data["comentarios"],
        ruedas=dashboard_data["ruedas"],
        total_usuarios=dashboard_data["total_usuarios"],
        total_publicaciones=dashboard_data["total_publicaciones"],
        total_comentarios=dashboard_data["total_comentarios"],
        total_productos=dashboard_data["total_productos"],
        total_ruedas=dashboard_data["total_ruedas"]
    )

# --- RUTAS DE EDICIÓN Y ELIMINACIÓN ---

@dashboard_bp.route('/editar_usuario_dashboard/<user_id>', methods=['POST'])
def editar_usuario_dashboard(user_id):
    nombre = request.form.get('nombre', '').strip()
    correo = request.form.get('correo', '').strip()
    numero = request.form.get('numero', '').strip()
    emprendimiento = request.form.get('emprendimiento', '').strip()
    
    if not nombre or not correo:
        flash('Nombre y correo son obligatorios', 'error')
        return redirect(url_for('dashboard.dashboard'))

    update_data = {
        'nombre': nombre,
        'correo': correo,
        'numero': numero,
        'emprendimiento': emprendimiento
    }

    if update_usuario(user_id, update_data):
        flash('✅ Usuario actualizado correctamente', 'success')
    else:
        flash('❌ Error al actualizar el usuario', 'error')
    
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/eliminar_usuario_dashboard/<user_id>', methods=['POST'])
def eliminar_usuario_dashboard(user_id):
    try:
        print(f"🗑️ SOLICITUD DE ELIMINACIÓN COMPLETA para usuario: {user_id}")
        
        if eliminar_usuario_completamente(user_id):
            flash('✅ Usuario y todo su contenido eliminado completamente', 'success')
        else:
            flash('❌ Error al eliminar el usuario completamente', 'error')
        
    except Exception as e:
        flash(f'❌ Error crítico al eliminar el usuario: {str(e)}', 'error')
        print(f"💥 Error eliminando usuario {user_id}: {e}")
    
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/editar_publicacion_dashboard/<pub_id>', methods=['POST'])
def editar_publicacion_dashboard(pub_id):
    descripcion = request.form.get('descripcion', '').strip()
    url_Imagen = request.form.get('url_Imagen', '').strip()

    if not descripcion or not url_Imagen:
        flash('Descripción y URL de imagen son obligatorios', 'error')
        return redirect(url_for('dashboard.dashboard'))

    update_data = {
        'descripcion': descripcion,
        'url_Imagen': url_Imagen
    }

    if update_publicacion(pub_id, update_data):
        flash('✅ Publicación actualizada correctamente', 'success')
    else:
        flash('❌ Error al actualizar la publicación', 'error')
    
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/eliminar_publicacion_dashboard/<pub_id>', methods=['POST'])
def eliminar_publicacion_dashboard(pub_id):
    db_firestore = get_db()
    if not db_firestore:
        flash('Error de conexión con Firebase', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    try:
        print(f"🗑️ Eliminando publicación {pub_id}")
        db_firestore.collection('Publicacion').document(pub_id).delete()
        flash('✅ Publicación eliminada correctamente', 'success')
        
    except Exception as e:
        flash(f'❌ Error al eliminar la publicación: {str(e)}', 'error')
        print(f"❌ Error eliminando publicación {pub_id}: {e}")
    
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/editar_rueda_dashboard/<rueda_id>', methods=['POST'])
def editar_rueda_dashboard(rueda_id):
    # Obtener todos los campos reales del formulario
    tema = request.form.get('tema', '').strip()
    descripcion = request.form.get('descripcion', '').strip()
    fecha = request.form.get('fecha', '')
    hora = request.form.get('hora', '')
    link = request.form.get('link', '').strip()
    estado = request.form.get('estado', 'activa')
    
    # Validar campos obligatorios
    if not tema or not descripcion or not fecha or not hora:
        flash('Tema, descripción, fecha y hora son obligatorios', 'error')
        return redirect(url_for('dashboard.dashboard'))

    update_data = {
        'tema': tema,
        'descripcion': descripcion,
        'fecha': fecha,
        'hora': hora,
        'link': link,
        'estado': estado
    }

    if update_rueda(rueda_id, update_data):
        flash('✅ Rueda de negocio actualizada correctamente', 'success')
    else:
        flash('❌ Error al actualizar la rueda de negocio', 'error')
    
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/eliminar_rueda_dashboard/<rueda_id>', methods=['POST'])
def eliminar_rueda_dashboard(rueda_id):
    db_firestore = get_db()
    if not db_firestore:
        flash('Error de conexión con Firebase', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    try:
        print(f"🗑️ Eliminando rueda {rueda_id}")
        db_firestore.collection('RuedaNegocio').document(rueda_id).delete()
        flash('✅ Rueda de negocio eliminada correctamente', 'success')
        
    except Exception as e:
        flash(f'❌ Error al eliminar la rueda de negocio: {str(e)}', 'error')
        print(f"❌ Error eliminando rueda {rueda_id}: {e}")
    
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/eliminar_comentario_dashboard/<comentario_id>', methods=['POST'])
def eliminar_comentario_dashboard(comentario_id):
    db_firestore = get_db()
    if not db_firestore:
        flash('Error de conexión con Firebase', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    try:
        print(f"🗑️ Eliminando comentario {comentario_id}")
        db_firestore.collection('Comentarios').document(comentario_id).delete()
        flash('✅ Comentario eliminado correctamente', 'success')
        
    except Exception as e:
        flash(f'❌ Error al eliminar el comentario: {str(e)}', 'error')
        print(f"❌ Error eliminando comentario {comentario_id}: {e}")
    
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/logout')
def logout():
    """Cierra sesión y redirige adecuadamente"""
    # Guardar información de la sesión antes de limpiar (opcional)
    user_email = session.get('user', {}).get('email', 'Usuario')
    
    # Limpiar toda la sesión
    session.clear()
    
    # Mostrar mensaje de confirmación
    flash(f'Sesión cerrada correctamente. ¡Hasta pronto, {user_email}!', 'success')
    
    # Redirigir al inicio principal O al login
    try:
        # Intenta redirigir al inicio principal si existe
        return redirect(url_for('main.inicio'))
    except:
        # Si no existe 'main.inicio', redirige al login
        return redirect(url_for('auth.login'))