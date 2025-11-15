from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import firebase_admin
from firebase_admin import credentials, firestore, storage


# Inicializamos la aplicación Flask
app = Flask(__name__, template_folder="templates")
app.secret_key = 'tu_clave_secreta_aqui'  # ¡IMPORTANTE! Agrega una clave secreta

# ----------------- CONFIGURACIÓN FIREBASE -----------------
try:
    # Ruta del archivo JSON de credenciales de Firebase
    firebase_key_path = os.path.join(os.path.dirname(__file__), 'pay-nic-firebase-adminsdk-fbsvc-4de59097dc.json')

    # Inicializar Firebase con el archivo JSON
    cred = credentials.Certificate(firebase_key_path)
    firebase_app = firebase_admin.initialize_app(cred, {
        'storageBucket': 'pay-nic.appspot.com'
    })
    print("✅ Firebase inicializado correctamente")

except Exception as e:
    print(f"❌ Error inicializando Firebase: {e}")
    firebase_app = None

# Inicializar clientes de Firebase
if firebase_app:
    db_firestore = firestore.client()
    bucket = storage.bucket()
else:
    db_firestore = None
    bucket = None

# Configuración para uploads de imágenes
UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB máximo

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ----------------- FUNCIONES FIREBASE -----------------

def upload_to_firebase_storage(file, destination_path):
    """Sube un archivo a Firebase Storage"""
    if not bucket:
        return None
    
    try:
        blob = bucket.blob(destination_path)
        blob.upload_from_file(file)
        blob.make_public()
        return blob.public_url
    except Exception as e:
        print(f"Error subiendo archivo a Firebase: {e}")
        return None

# ----------------- RUTAS PRINCIPALES -----------------

@app.route('/')
def inicio():
    return render_template("index.html")

@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/contactopost', methods=['GET', 'POST'])
def contactopost():
    user = {'nombre': '', 'email': '', 'mensaje': ''}
    if request.method == 'POST':
        user['nombre'] = request.form.get('nombre', '')
        user['email'] = request.form.get('email', '')
        user['mensaje'] = request.form.get('mensaje', '')
    return render_template("contactopost.html", usuario=user)

@app.route('/acercade')
def acercade():
    return render_template("acercade.html")

# ----------------- DASHBOARD ADMIN -----------------
@app.route('/dashboard')
def dashboard():
    if not db_firestore:
        flash('Error de conexión con Firebase', 'error')
        return render_template('dashboardadmin.html')
    
    try:
        # --- Usuarios ---
        usuarios_ref = db_firestore.collection('Usuario')
        usuarios_docs = usuarios_ref.stream()
        usuarios = []
        for doc in usuarios_docs:
            data = doc.to_dict()
            usuarios.append({
                'id': doc.id,
                'nombre': data.get('nombre'),
                'correo': data.get('correo'),
                'fotoPerfil': data.get('fotoPerfil'),
                'numero': data.get('numero'),
                'emprendimiento': data.get('emprendimiento'),
                'descripcionEmprendimiento': data.get('descripcionEmprendimiento'),
                'productosServicios': data.get('productosServicios'),
                'ubicacion': data.get('ubicacion')
            })

        total_usuarios = len(usuarios)

        # --- Publicaciones ---
        publicaciones_ref = db_firestore.collection('Publicacion')
        publicaciones_docs = publicaciones_ref.stream()
        publicaciones = []
        for doc in publicaciones_docs:
            data = doc.to_dict()
            publicaciones.append({
                'id': doc.id,
                'descripcion': data.get('descripcion'),
                'url_Imagen': data.get('url_Imagen'),
                'userName': data.get('userName'),
                'userEmprendimiento': data.get('userEmprendimiento'),
                'userId': data.get('userId'),
                'userPhotoUrl': data.get('userPhotoUrl'),
                'fechaCreacion': data.get('fechaCreacion'),
                'likes': data.get('likes', []),
                'comentarios': data.get('comentarios', 0)
            })

        total_publicaciones = len(publicaciones)

        # --- Comentarios ---
        comentarios_ref = db_firestore.collection('Comentarios')
        comentarios_docs = comentarios_ref.stream()
        comentarios = []
        for doc in comentarios_docs:
            data = doc.to_dict()
            comentarios.append({
                'id': doc.id,
                'texto': data.get('texto'),
                'userName': data.get('usuarioNombre'),
                'usuarioId': data.get('usuarioId'),
                'usuarioFotoUrl': data.get('usuarioFotoUrl'),
                'publicacionId': data.get('publicacionId'),
                'fechaComentario': data.get('fechaComentario'),
                'likes_Comentarios': data.get('likes_Comentarios', [])
            })

        total_comentarios = len(comentarios)

        # --- Ruedas de Negocio ---
        ruedas_ref = db_firestore.collection('RuedaNegocio')
        ruedas_docs = ruedas_ref.stream()
        ruedas = []
        for doc in ruedas_docs:
            data = doc.to_dict()
            ruedas.append({
                'id': doc.id,
                'nombre': data.get('nombre'),
                'fecha': data.get('fecha'),
                'descripcion': data.get('descripcion'),
                'participantes': data.get('participantes', []),
                'estado': data.get('estado', 'activa'),
                'creado_por': data.get('creado_por'),
                'fecha_creacion': data.get('fecha_creacion')
            })

        total_ruedas = len(ruedas)

        # --- Productos/Servicios ---
        total_productos = sum([len(u.get('productosServicios', [])) for u in usuarios])

        return render_template(
            'dashboardadmin.html',
            usuarios=usuarios,
            publicaciones=publicaciones,
            comentarios=comentarios,
            ruedas=ruedas,
            total_usuarios=total_usuarios,
            total_publicaciones=total_publicaciones,
            total_comentarios=total_comentarios,
            total_productos=total_productos,
            total_ruedas=total_ruedas
        )
    
    except Exception as e:
        print(f"Error cargando dashboard: {e}")
        flash('Error al cargar los datos del dashboard', 'error')
        return render_template('dashboardadmin.html')

# ----------------- FUNCIONES EDITAR DASHBOARD -----------------
@app.route('/editar_usuario_dashboard/<user_id>', methods=['POST'])
def editar_usuario_dashboard(user_id):
    if not db_firestore:
        flash('Error de conexión con Firebase', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        numero = request.form.get('numero', '').strip()
        emprendimiento = request.form.get('emprendimiento', '').strip()
        
        print(f"📝 Editando usuario {user_id}:")
        print(f"  Nombre: {nombre}")
        print(f"  Correo: {correo}")
        print(f"  Teléfono: {numero}")
        print(f"  Emprendimiento: {emprendimiento}")

        # Validar campos requeridos
        if not nombre or not correo:
            flash('Nombre y correo son obligatorios', 'error')
            return redirect(url_for('dashboard'))

        update_data = {
            'nombre': nombre,
            'correo': correo,
            'numero': numero,
            'emprendimiento': emprendimiento
        }

        db_firestore.collection('Usuario').document(user_id).update(update_data)
        flash('✅ Usuario actualizado correctamente', 'success')
        print(f"✅ Usuario {user_id} actualizado")
        
    except Exception as e:
        flash(f'❌ Error al actualizar el usuario: {str(e)}', 'error')
        print(f"❌ Error actualizando usuario {user_id}: {e}")
    
    return redirect(url_for('dashboard'))

@app.route('/editar_publicacion_dashboard/<pub_id>', methods=['POST'])
def editar_publicacion_dashboard(pub_id):
    if not db_firestore:
        flash('Error de conexión con Firebase', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        descripcion = request.form.get('descripcion', '').strip()
        url_Imagen = request.form.get('url_Imagen', '').strip()

        print(f"📝 Editando publicación {pub_id}:")
        print(f"  Descripción: {descripcion}")
        print(f"  URL Imagen: {url_Imagen}")

        # Validar campos requeridos
        if not descripcion or not url_Imagen:
            flash('Descripción y URL de imagen son obligatorios', 'error')
            return redirect(url_for('dashboard'))

        update_data = {
            'descripcion': descripcion,
            'url_Imagen': url_Imagen
        }

        db_firestore.collection('Publicacion').document(pub_id).update(update_data)
        flash('✅ Publicación actualizada correctamente', 'success')
        print(f"✅ Publicación {pub_id} actualizada")
        
    except Exception as e:
        flash(f'❌ Error al actualizar la publicación: {str(e)}', 'error')
        print(f"❌ Error actualizando publicación {pub_id}: {e}")
    
    return redirect(url_for('dashboard'))

@app.route('/editar_rueda_dashboard/<rueda_id>', methods=['POST'])
def editar_rueda_dashboard(rueda_id):
    if not db_firestore:
        flash('Error de conexión con Firebase', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        nombre = request.form.get('nombre', '').strip()
        fecha = request.form.get('fecha', '')
        descripcion = request.form.get('descripcion', '').strip()
        estado = request.form.get('estado', 'activa')
        
        print(f"🔄 Procesando edición de rueda {rueda_id}")
        print(f"📝 Datos recibidos:")
        print(f"  Nombre: {nombre}")
        print(f"  Fecha: {fecha}")
        print(f"  Descripción: {descripcion}")
        print(f"  Estado: {estado}")

        # Validar que los campos requeridos no estén vacíos
        if not nombre:
            flash('❌ El nombre es obligatorio', 'error')
            return redirect(url_for('dashboard'))
        if not fecha:
            flash('❌ La fecha es obligatoria', 'error')
            return redirect(url_for('dashboard'))
        if not descripcion:
            flash('❌ La descripción es obligatoria', 'error')
            return redirect(url_for('dashboard'))

        # Preparar datos para actualizar
        update_data = {
            'nombre': nombre,
            'fecha': fecha,
            'descripcion': descripcion,
            'estado': estado
        }

        print(f"📤 Actualizando rueda {rueda_id} con: {update_data}")

        # Verificar que el documento existe antes de actualizar
        rueda_ref = db_firestore.collection('RuedaNegocio').document(rueda_id)
        rueda_doc = rueda_ref.get()
        
        if not rueda_doc.exists:
            flash('❌ La rueda de negocio no existe', 'error')
            print(f"❌ Rueda {rueda_id} no encontrada en Firebase")
            return redirect(url_for('dashboard'))

        # Actualizar en Firebase
        rueda_ref.update(update_data)
        
        flash('✅ Rueda de negocio actualizada correctamente', 'success')
        print(f"✅ Rueda {rueda_id} actualizada exitosamente")
        
    except Exception as e:
        flash(f'❌ Error al actualizar la rueda de negocio: {str(e)}', 'error')
        print(f"❌ Error crítico actualizando rueda {rueda_id}: {e}")
    
    return redirect(url_for('dashboard'))

# ----------------- FUNCIONES ELIMINAR DASHBOARD -----------------
@app.route('/eliminar_usuario_dashboard/<user_id>', methods=['POST'])
def eliminar_usuario_dashboard(user_id):
    if not db_firestore:
        flash('Error de conexión con Firebase', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        print(f"🗑️ ELIMINACIÓN COMPLETA para usuario: {user_id}")
        
        # Obtener información del usuario antes de eliminarlo
        usuario_ref = db_firestore.collection('Usuario').document(user_id)
        usuario_doc = usuario_ref.get()
        
        if not usuario_doc.exists:
            flash('❌ El usuario no existe', 'error')
            print(f"❌ Usuario {user_id} no encontrado en Firebase")
            return redirect(url_for('dashboard'))
        
        usuario_data = usuario_doc.to_dict()
        usuario_nombre = usuario_data.get('nombre', 'Usuario sin nombre')
        
        print(f"🔍 Investigando estructura de datos para usuario: {usuario_nombre}")
        
        # INVESTIGAR ESTRUCTURA DE PUBLICACIONES
        print(f"📝 INVESTIGANDO PUBLICACIONES...")
        publicaciones_ref = db_firestore.collection('Publicacion')
        publicaciones_docs = publicaciones_ref.stream()
        
        publicaciones_del_usuario = []
        for doc in publicaciones_docs:
            data = doc.to_dict()
            # Verificar diferentes posibles campos de usuario
            if (data.get('userId') == user_id or 
                data.get('userID') == user_id or 
                data.get('usuarioId') == user_id or
                data.get('user_id') == user_id or
                data.get('userName') == usuario_nombre):
                publicaciones_del_usuario.append(doc.id)
                print(f"📄 Publicación del usuario encontrada: {doc.id} - {data}")
        
        print(f"🔍 Encontradas {len(publicaciones_del_usuario)} publicaciones del usuario")
        
        # 1. ELIMINAR PUBLICACIONES DEL USUARIO
        publicaciones_eliminadas = 0
        for publicacion_id in publicaciones_del_usuario:
            print(f"🗑️ Eliminando publicación {publicacion_id}")
            
            # 1.1 ELIMINAR COMENTARIOS DE ESTA PUBLICACIÓN
            comentarios_ref = db_firestore.collection('Comentarios')
            comentarios_query = comentarios_ref.where('publicacionId', '==', publicacion_id).stream()
            
            comentarios_publicacion_eliminados = 0
            for comentario_doc in comentarios_query:
                comentario_id = comentario_doc.id
                print(f"🗑️ Eliminando comentario {comentario_id} de la publicación {publicacion_id}")
                comentarios_ref.document(comentario_id).delete()
                comentarios_publicacion_eliminados += 1
            
            print(f"✅ Eliminados {comentarios_publicacion_eliminados} comentarios de la publicación {publicacion_id}")
            
            # 1.2 ELIMINAR LA PUBLICACIÓN
            publicaciones_ref.document(publicacion_id).delete()
            publicaciones_eliminadas += 1
        
        print(f"✅ Eliminadas {publicaciones_eliminadas} publicaciones del usuario")
        
        # 2. ELIMINAR COMENTARIOS DEL USUARIO (en publicaciones de otros usuarios)
        print(f"📝 Buscando comentarios del usuario {user_id}")
        comentarios_ref = db_firestore.collection('Comentarios')
        comentarios_query = comentarios_ref.where('usuarioId', '==', user_id).stream()
        
        comentarios_eliminados = 0
        for comentario_doc in comentarios_query:
            comentario_id = comentario_doc.id
            print(f"🗑️ Eliminando comentario {comentario_id}")
            comentarios_ref.document(comentario_id).delete()
            comentarios_eliminados += 1
        
        print(f"✅ Eliminados {comentarios_eliminados} comentarios del usuario")
        
        # 3. INVESTIGAR ESTRUCTURA DE RUEDAS DE NEGOCIO
        print(f"🔍 INVESTIGANDO RUEDAS DE NEGOCIO...")
        ruedas_ref = db_firestore.collection('RuedaNegocio')
        ruedas_docs = ruedas_ref.stream()
        
        ruedas_del_usuario = []
        for doc in ruedas_docs:
            data = doc.to_dict()
            print(f"🔍 Rueda {doc.id}: {data}")
            # Verificar diferentes campos donde podría estar el usuario
            if (data.get('creado_por') == user_id or
                data.get('creador') == user_id or
                data.get('userId') == user_id or
                data.get('usuarioId') == user_id or
                data.get('owner') == user_id):
                ruedas_del_usuario.append(doc.id)
                print(f"🎯 Rueda creada por el usuario encontrada: {doc.id}")
        
        print(f"🔍 Encontradas {len(ruedas_del_usuario)} ruedas creadas por el usuario")
        
        # ELIMINAR RUEDAS DE NEGOCIO CREADAS POR EL USUARIO
        ruedas_eliminadas = 0
        for rueda_id in ruedas_del_usuario:
            print(f"🗑️ Eliminando rueda de negocio {rueda_id}")
            ruedas_ref.document(rueda_id).delete()
            ruedas_eliminadas += 1
        
        print(f"✅ Eliminadas {ruedas_eliminadas} ruedas de negocio creadas por el usuario")
        
        # 4. ELIMINAR AL USUARIO DE LAS RUEDAS DE NEGOCIO COMO PARTICIPANTE
        print(f"📝 Buscando ruedas de negocio donde participe el usuario {user_id}")
        ruedas_participante_query = ruedas_ref.stream()
        
        ruedas_actualizadas = 0
        for rueda_doc in ruedas_participante_query:
            rueda_data = rueda_doc.to_dict()
            participantes = rueda_data.get('participantes', [])
            
            # Buscar si el usuario está en los participantes
            usuario_en_rueda = False
            nuevos_participantes = []
            
            for participante in participantes:
                # Dependiendo de cómo estén almacenados los participantes
                if isinstance(participante, dict):
                    if (participante.get('id') == user_id or 
                        participante.get('usuarioId') == user_id or
                        participante.get('userId') == user_id):
                        usuario_en_rueda = True
                    else:
                        nuevos_participantes.append(participante)
                elif isinstance(participante, str):
                    if participante == user_id:
                        usuario_en_rueda = True
                    else:
                        nuevos_participantes.append(participante)
                else:
                    nuevos_participantes.append(participante)
            
            # Si el usuario estaba en la rueda, actualizar la lista de participantes
            if usuario_en_rueda:
                print(f"🔄 Eliminando usuario de la rueda {rueda_doc.id}")
                ruedas_ref.document(rueda_doc.id).update({
                    'participantes': nuevos_participantes
                })
                ruedas_actualizadas += 1
        
        print(f"✅ Usuario eliminado de {ruedas_actualizadas} ruedas de negocio como participante")
        
        # 5. ELIMINAR LIKES DEL USUARIO EN PUBLICACIONES
        print(f"📝 Eliminando likes del usuario en publicaciones")
        publicaciones_todas_ref = db_firestore.collection('Publicacion')
        publicaciones_todas_query = publicaciones_todas_ref.stream()
        
        publicaciones_actualizadas = 0
        for publicacion_doc in publicaciones_todas_query:
            publicacion_data = publicacion_doc.to_dict()
            likes = publicacion_data.get('likes', [])
            
            if user_id in likes:
                nuevos_likes = [like for like in likes if like != user_id]
                publicaciones_ref.document(publicacion_doc.id).update({
                    'likes': nuevos_likes
                })
                publicaciones_actualizadas += 1
        
        print(f"✅ Likes eliminados de {publicaciones_actualizadas} publicaciones")
        
        # 6. ELIMINAR LIKES DEL USUARIO EN COMENTARIOS
        print(f"📝 Eliminando likes del usuario en comentarios")
        comentarios_todos_ref = db_firestore.collection('Comentarios')
        comentarios_todos_query = comentarios_todos_ref.stream()
        
        comentarios_actualizados = 0
        for comentario_doc in comentarios_todos_query:
            comentario_data = comentario_doc.to_dict()
            likes_comentarios = comentario_data.get('likes_Comentarios', [])
            
            if user_id in likes_comentarios:
                nuevos_likes_comentarios = [like for like in likes_comentarios if like != user_id]
                comentarios_ref.document(comentario_doc.id).update({
                    'likes_Comentarios': nuevos_likes_comentarios
                })
                comentarios_actualizados += 1
        
        print(f"✅ Likes eliminados de {comentarios_actualizados} comentarios")
        
        # 7. FINALMENTE ELIMINAR EL USUARIO
        usuario_ref.delete()
        
        # Resumen de la operación
        resumen = f"""
        ✅ Usuario '{usuario_nombre}' eliminado completamente
        
        📊 Resumen de eliminación:
        • Publicaciones eliminadas: {publicaciones_eliminadas}
        • Comentarios eliminados: {comentarios_eliminados}
        • Ruedas de negocio eliminadas: {ruedas_eliminadas}
        • Ruedas actualizadas (como participante): {ruedas_actualizadas}
        • Likes en publicaciones eliminados: {publicaciones_actualizadas}
        • Likes en comentarios eliminados: {comentarios_actualizados}
        """
        
        flash(resumen, 'success')
        print(f"✅ Usuario {user_id} eliminado completamente con todos sus datos")
        
    except Exception as e:
        flash(f'❌ Error al eliminar el usuario: {str(e)}', 'error')
        print(f"❌ Error eliminando usuario {user_id}: {e}")
    
    return redirect(url_for('dashboard'))

@app.route('/eliminar_publicacion_dashboard/<pub_id>', methods=['POST'])
def eliminar_publicacion_dashboard(pub_id):
    if not db_firestore:
        flash('Error de conexión con Firebase', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        print(f"🗑️ Eliminando publicación {pub_id}")
        
        # Primero eliminar todos los comentarios de esta publicación
        comentarios_ref = db_firestore.collection('Comentarios')
        comentarios_query = comentarios_ref.where('publicacionId', '==', pub_id).stream()
        
        comentarios_eliminados = 0
        for comentario_doc in comentarios_query:
            comentario_id = comentario_doc.id
            print(f"🗑️ Eliminando comentario {comentario_id} de la publicación {pub_id}")
            comentarios_ref.document(comentario_id).delete()
            comentarios_eliminados += 1
        
        print(f"✅ Eliminados {comentarios_eliminados} comentarios de la publicación {pub_id}")
        
        # Luego eliminar la publicación
        db_firestore.collection('Publicacion').document(pub_id).delete()
        
        flash(f'✅ Publicación eliminada correctamente (junto con {comentarios_eliminados} comentarios)', 'success')
        print(f"✅ Publicación {pub_id} eliminada")
        
    except Exception as e:
        flash(f'❌ Error al eliminar la publicación: {str(e)}', 'error')
        print(f"❌ Error eliminando publicación {pub_id}: {e}")
    
    return redirect(url_for('dashboard'))

@app.route('/eliminar_comentario_dashboard/<comentario_id>', methods=['POST'])
def eliminar_comentario_dashboard(comentario_id):
    if not db_firestore:
        flash('Error de conexión con Firebase', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        print(f"🗑️ Eliminando comentario {comentario_id}")
        db_firestore.collection('Comentarios').document(comentario_id).delete()
        flash('✅ Comentario eliminado correctamente', 'success')
        print(f"✅ Comentario {comentario_id} eliminado")
        
    except Exception as e:
        flash(f'❌ Error al eliminar el comentario: {str(e)}', 'error')
        print(f"❌ Error eliminando comentario {comentario_id}: {e}")
    
    return redirect(url_for('dashboard'))

@app.route('/eliminar_rueda_dashboard/<rueda_id>', methods=['POST'])
def eliminar_rueda_dashboard(rueda_id):
    if not db_firestore:
        flash('Error de conexión con Firebase', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        print(f"🗑️ Eliminando rueda {rueda_id}")
        
        # Verificar que el documento existe antes de eliminar
        rueda_ref = db_firestore.collection('RuedaNegocio').document(rueda_id)
        rueda_doc = rueda_ref.get()
        
        if not rueda_doc.exists:
            flash('❌ La rueda de negocio no existe', 'error')
            print(f"❌ Rueda {rueda_id} no encontrada en Firebase")
            return redirect(url_for('dashboard'))
        
        rueda_ref.delete()
        flash('✅ Rueda de negocio eliminada correctamente', 'success')
        print(f"✅ Rueda {rueda_id} eliminada exitosamente")
        
    except Exception as e:
        flash(f'❌ Error al eliminar la rueda de negocio: {str(e)}', 'error')
        print(f"❌ Error eliminando rueda {rueda_id}: {e}")
    
    return redirect(url_for('dashboard'))

# ----------------- RUTAS PARA AGREGAR NUEVOS ELEMENTOS -----------------
@app.route('/agregar_usuario_dashboard', methods=['POST'])
def agregar_usuario_dashboard():
    if not db_firestore:
        flash('Error de conexión con Firebase', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        password = request.form.get('password', '').strip()
        numero = request.form.get('numero', '').strip()
        emprendimiento = request.form.get('emprendimiento', '').strip()
        
        print(f"➕ Agregando nuevo usuario:")
        print(f"  Nombre: {nombre}")
        print(f"  Correo: {correo}")

        # Validar campos requeridos
        if not nombre or not correo or not password:
            flash('Nombre, correo y contraseña son obligatorios', 'error')
            return redirect(url_for('dashboard'))

        nuevo_usuario = {
            'nombre': nombre,
            'correo': correo,
            'password': password,  # En producción, esto debería estar hasheado
            'numero': numero,
            'emprendimiento': emprendimiento,
            'fotoPerfil': '',
            'fecha_creacion': firestore.SERVER_TIMESTAMP
        }

        db_firestore.collection('Usuario').add(nuevo_usuario)
        flash('✅ Usuario agregado correctamente', 'success')
        print(f"✅ Nuevo usuario agregado: {nombre}")
        
    except Exception as e:
        flash(f'❌ Error al agregar el usuario: {str(e)}', 'error')
        print(f"❌ Error agregando usuario: {e}")
    
    return redirect(url_for('dashboard'))

@app.route('/agregar_rueda_dashboard', methods=['POST'])
def agregar_rueda_dashboard():
    if not db_firestore:
        flash('Error de conexión con Firebase', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        nombre = request.form.get('nombre', '').strip()
        fecha = request.form.get('fecha', '')
        descripcion = request.form.get('descripcion', '').strip()
        estado = request.form.get('estado', 'planificada')
        
        print(f"➕ Agregando nueva rueda de negocio:")
        print(f"  Nombre: {nombre}")
        print(f"  Fecha: {fecha}")
        print(f"  Estado: {estado}")

        # Validar campos requeridos
        if not nombre or not fecha or not descripcion:
            flash('Nombre, fecha y descripción son obligatorios', 'error')
            return redirect(url_for('dashboard'))

        nueva_rueda = {
            'nombre': nombre,
            'fecha': fecha,
            'descripcion': descripcion,
            'estado': estado,
            'participantes': [],
            'fecha_creacion': firestore.SERVER_TIMESTAMP,
            'creado_por': 'admin'
        }

        db_firestore.collection('RuedaNegocio').add(nueva_rueda)
        flash('✅ Rueda de negocio agregada correctamente', 'success')
        print(f"✅ Nueva rueda agregada: {nombre}")
        
    except Exception as e:
        flash(f'❌ Error al agregar la rueda de negocio: {str(e)}', 'error')
        print(f"❌ Error agregando rueda: {e}")
    
    return redirect(url_for('dashboard'))

# ----------------- LOGOUT -----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio'))

# ----------------- MAIN -----------------
if __name__ == '__main__':
    app.run(debug=True, port=8000)