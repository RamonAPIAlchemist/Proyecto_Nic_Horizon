from config.firebase_config import get_db, init_firebase

def get_dashboard_data():
    """Obtiene todos los datos para el dashboard - VERSIÓN CORREGIDA"""
    # Asegurarnos de que Firebase esté inicializado
    if not init_firebase():
        print("❌ No se pudo inicializar Firebase")
        return None
    
    db_firestore = get_db()
    if not db_firestore:
        print("❌ No hay conexión a Firebase")
        return None

    try:
        print("📊 Iniciando carga de datos del dashboard...")
        
        # --- Usuarios ---
        usuarios = []
        try:
            print("🔍 Buscando colección 'Usuario'...")
            usuarios_ref = db_firestore.collection('Usuario')
            usuarios_docs = usuarios_ref.stream()
            
            doc_count = 0
            for doc in usuarios_docs:
                data = doc.to_dict()
                print(f"📄 Usuario {doc_count + 1}: {data.get('nombre', 'Sin nombre')}")
                usuarios.append({
                    'id': doc.id,
                    'nombre': data.get('nombre', 'Sin nombre'),
                    'correo': data.get('correo', 'Sin email'),
                    'fotoPerfil': data.get('fotoPerfil', ''),
                    'numero': data.get('numero', ''),
                    'emprendimiento': data.get('emprendimiento', ''),
                    'descripcionEmprendimiento': data.get('descripcionEmprendimiento', ''),
                    'productosServicios': data.get('productosServicios', []),
                    'ubicacion': data.get('ubicacion', '')
                })
                doc_count += 1
                
            total_usuarios = len(usuarios)
            print(f"✅ Usuarios cargados: {total_usuarios}")
            
        except Exception as e:
            print(f"❌ Error cargando usuarios: {e}")
            total_usuarios = 0

        # --- Publicaciones ---
        publicaciones = []
        try:
            print("🔍 Buscando colección 'Publicacion'...")
            publicaciones_ref = db_firestore.collection('Publicacion')
            publicaciones_docs = publicaciones_ref.stream()
            
            doc_count = 0
            for doc in publicaciones_docs:
                data = doc.to_dict()
                descripcion = data.get('descripcion', '')
                print(f"📄 Publicación {doc_count + 1}: {descripcion[:50] if descripcion else 'Sin descripción'}...")
                publicaciones.append({
                    'id': doc.id,
                    'descripcion': descripcion,
                    'url_Imagen': data.get('url_Imagen', ''),
                    'userName': data.get('userName', ''),
                    'userEmprendimiento': data.get('userEmprendimiento', ''),
                    'userId': data.get('userId', ''),
                    'userPhotoUrl': data.get('userPhotoUrl', ''),
                    'fechaCreacion': data.get('fechaCreacion', ''),
                    'likes': data.get('likes', []),
                    'comentarios': data.get('comentarios', 0)
                })
                doc_count += 1
                
            total_publicaciones = len(publicaciones)
            print(f"✅ Publicaciones cargadas: {total_publicaciones}")
        except Exception as e:
            print(f"❌ Error cargando publicaciones: {e}")
            total_publicaciones = 0

        # --- Comentarios ---
        comentarios = []
        try:
            print("🔍 Buscando colección 'Comentarios'...")
            comentarios_ref = db_firestore.collection('Comentarios')
            comentarios_docs = comentarios_ref.stream()
            
            doc_count = 0
            for doc in comentarios_docs:
                data = doc.to_dict()
                texto = data.get('texto', '')
                print(f"📄 Comentario {doc_count + 1}: {texto[:30] if texto else 'Sin texto'}...")
                comentarios.append({
                    'id': doc.id,
                    'texto': texto,
                    'userName': data.get('usuarioNombre', data.get('userName', '')),
                    'usuarioId': data.get('usuarioId', data.get('userId', '')),
                    'usuarioFotoUrl': data.get('usuarioFotoUrl', data.get('userPhotoUrl', '')),
                    'publicacionId': data.get('publicacionId', ''),
                    'fechaComentario': data.get('fechaComentario', ''),
                    'likes_Comentarios': data.get('likes_Comentarios', [])
                })
                doc_count += 1
                
            total_comentarios = len(comentarios)
            print(f"✅ Comentarios cargados: {total_comentarios}")
        except Exception as e:
            print(f"❌ Error cargando comentarios: {e}")
            total_comentarios = 0

        # --- Ruedas de Negocio ---
        ruedas = []
        try:
            print("🔍 Buscando colección 'RuedaNegocio'...")
            ruedas_ref = db_firestore.collection('RuedaNegocio')
            ruedas_docs = ruedas_ref.stream()
            
            doc_count = 0
            for doc in ruedas_docs:
                data = doc.to_dict()
                nombre = data.get('nombre', 'Sin nombre')
                print(f"📄 Rueda {doc_count + 1}: {nombre}")
                ruedas.append({
                    'id': doc.id,
                    'nombre': nombre,
                    'fecha': data.get('fecha', ''),
                    'descripcion': data.get('descripcion', ''),
                    'participantes': data.get('participantes', []),
                    'estado': data.get('estado', 'activa'),
                    'creado_por': data.get('creado_por', ''),
                    'fecha_creacion': data.get('fecha_creacion', '')
                })
                doc_count += 1
                
            total_ruedas = len(ruedas)
            print(f"✅ Ruedas de negocio cargadas: {total_ruedas}")
        except Exception as e:
            print(f"❌ Error cargando ruedas: {e}")
            total_ruedas = 0

        # --- Productos/Servicios ---
        try:
            total_productos = sum([len(u.get('productosServicios', [])) for u in usuarios])
            print(f"✅ Total productos/servicios: {total_productos}")
        except Exception as e:
            print(f"❌ Error calculando productos: {e}")
            total_productos = 0

        # Resumen final
        print("\n📊 RESUMEN DE DATOS CARGADOS:")
        print(f"   👥 Usuarios: {total_usuarios}")
        print(f"   📝 Publicaciones: {total_publicaciones}")
        print(f"   💬 Comentarios: {total_comentarios}")
        print(f"   🔄 Ruedas de negocio: {total_ruedas}")
        print(f"   🛍️ Productos/Servicios: {total_productos}")

        # Verificar que al menos tenemos algunos datos
        if total_usuarios == 0 and total_publicaciones == 0:
            print("⚠️ ADVERTENCIA: No se encontraron datos en Firebase")
            # Pero igual retornamos la estructura vacía para que el dashboard no falle
            return {
                "usuarios": usuarios,
                "publicaciones": publicaciones,
                "comentarios": comentarios,
                "ruedas": ruedas,
                "total_usuarios": total_usuarios,
                "total_publicaciones": total_publicaciones,
                "total_comentarios": total_comentarios,
                "total_productos": total_productos,
                "total_ruedas": total_ruedas
            }

        print("🎉 Dashboard cargado exitosamente!")
        return {
            "usuarios": usuarios,
            "publicaciones": publicaciones,
            "comentarios": comentarios,
            "ruedas": ruedas,
            "total_usuarios": total_usuarios,
            "total_publicaciones": total_publicaciones,
            "total_comentarios": total_comentarios,
            "total_productos": total_productos,
            "total_ruedas": total_ruedas
        }

    except Exception as e:
        print(f"💥 ERROR CRÍTICO en dashboard: {e}")
        return None

# Las demás funciones actualizadas para usar get_db()
def update_usuario(user_id, data):
    """Actualiza un usuario en Firebase"""
    db_firestore = get_db()
    if not db_firestore:
        print("❌ No hay conexión a Firebase")
        return False
    try:
        db_firestore.collection('Usuario').document(user_id).update(data)
        print(f"✅ Usuario {user_id} actualizado")
        return True
    except Exception as e:
        print(f"❌ Error actualizando usuario: {e}")
        return False

def update_publicacion(pub_id, data):
    """Actualiza una publicación en Firebase"""
    db_firestore = get_db()
    if not db_firestore:
        print("❌ No hay conexión a Firebase")
        return False
    try:
        db_firestore.collection('Publicacion').document(pub_id).update(data)
        print(f"✅ Publicación {pub_id} actualizada")
        return True
    except Exception as e:
        print(f"❌ Error actualizando publicación: {e}")
        return False

def update_rueda(rueda_id, data):
    """Actualiza una rueda de negocio en Firebase"""
    db_firestore = get_db()
    if not db_firestore:
        print("❌ No hay conexión a Firebase")
        return False
    try:
        db_firestore.collection('RuedaNegocio').document(rueda_id).update(data)
        print(f"✅ Rueda {rueda_id} actualizada")
        return True
    except Exception as e:
        print(f"❌ Error actualizando rueda: {e}")
        return False

def agregar_usuario(data):
    """Agrega un nuevo usuario a Firebase"""
    db_firestore = get_db()
    if not db_firestore:
        print("❌ No hay conexión a Firebase")
        return False
    try:
        db_firestore.collection('Usuario').add(data)
        print("✅ Nuevo usuario agregado")
        return True
    except Exception as e:
        print(f"❌ Error agregando usuario: {e}")
        return False

def agregar_rueda(data):
    """Agrega una nueva rueda de negocio a Firebase"""
    db_firestore = get_db()
    if not db_firestore:
        print("❌ No hay conexión a Firebase")
        return False
    try:
        db_firestore.collection('RuedaNegocio').add(data)
        print("✅ Nueva rueda de negocio agregada")
        return True
    except Exception as e:
        print(f"❌ Error agregando rueda: {e}")
        return False