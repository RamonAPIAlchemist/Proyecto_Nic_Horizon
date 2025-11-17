from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.dashboard_service import get_dashboard_data

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
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

# --- RUTAS DE EDICIÓN Y ELIMINACIÓN ---

@dashboard_bp.route('/editar_usuario_dashboard/<user_id>', methods=['POST'])
def editar_usuario_dashboard(user_id):
    from services.dashboard_service import update_usuario
    
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
    from config.firebase_config import get_db
    
    db_firestore = get_db()
    if not db_firestore:
        flash('Error de conexión con Firebase', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    try:
        print(f"🗑️ Eliminando usuario: {user_id}")
        db_firestore.collection('Usuario').document(user_id).delete()
        flash('✅ Usuario eliminado correctamente', 'success')
        
    except Exception as e:
        flash(f'❌ Error al eliminar el usuario: {str(e)}', 'error')
        print(f"❌ Error eliminando usuario {user_id}: {e}")
    
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/editar_publicacion_dashboard/<pub_id>', methods=['POST'])
def editar_publicacion_dashboard(pub_id):
    from services.dashboard_service import update_publicacion
    
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
    from config.firebase_config import get_db
    
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
    from services.dashboard_service import update_rueda
    
    nombre = request.form.get('nombre', '').strip()
    fecha = request.form.get('fecha', '')
    descripcion = request.form.get('descripcion', '').strip()
    estado = request.form.get('estado', 'activa')
    
    if not nombre or not fecha or not descripcion:
        flash('Nombre, fecha y descripción son obligatorios', 'error')
        return redirect(url_for('dashboard.dashboard'))

    update_data = {
        'nombre': nombre,
        'fecha': fecha,
        'descripcion': descripcion,
        'estado': estado
    }

    if update_rueda(rueda_id, update_data):
        flash('✅ Rueda de negocio actualizada correctamente', 'success')
    else:
        flash('❌ Error al actualizar la rueda de negocio', 'error')
    
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/eliminar_rueda_dashboard/<rueda_id>', methods=['POST'])
def eliminar_rueda_dashboard(rueda_id):
    from config.firebase_config import get_db
    
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
    from config.firebase_config import get_db
    
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
    from flask import session
    session.clear()
    return redirect(url_for('main.inicio'))