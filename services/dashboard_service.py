from config.firebase_config import get_db, init_firebase
from google.cloud import firestore

def get_dashboard_data():
    """Obtiene todos los datos para el dashboard - VERSIÓN CON CAMPOS REALES"""
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

        # --- Ruedas de Negocio --- CON CAMPOS REALES
        ruedas = []
        try:
            print("🔍 Buscando colección 'RuedaNegocio'...")
            ruedas_ref = db_firestore.collection('RuedaNegocio')
            ruedas_docs = ruedas_ref.stream()
            
            doc_count = 0
            for doc in ruedas_docs:
                data = doc.to_dict()
                tema = data.get('tema', 'Sin tema')
                print(f"📄 Rueda {doc_count + 1}: {tema}")
                
                ruedas.append({
                    'id': doc.id,
                    'tema': tema,
                    'descripcion': data.get('descripcion', ''),
                    'fecha': data.get('fecha', ''),
                    'hora': data.get('hora', ''),
                    'link': data.get('link', ''),
                    'asistentes': data.get('asistentes', []),
                    'estado': data.get('estado', 'activa'),
                    'userName': data.get('userName', ''),
                    'userEmprendimiento': data.get('userEmprendimiento', ''),
                    'userId': data.get('userId', ''),
                    'userPhotoUrl': data.get('userPhotoUrl', ''),
                    'fechaCreacion': data.get('fechaCreacion', ''),
                    'fechaActualizacion': data.get('fechaActualizacion', ''),
                    'fechaCompleta': data.get('fechaCompleta', '')
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
    """Actualiza una rueda de negocio en Firebase - CON CAMPOS REALES"""
    db_firestore = get_db()
    if not db_firestore:
        print("❌ No hay conexión a Firebase")
        return False
    try:
        # Agregar fecha de actualización
        data['fechaActualizacion'] = firestore.SERVER_TIMESTAMP
        
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
    """Agrega una nueva rueda de negocio a Firebase - CON CAMPOS REALES"""
    db_firestore = get_db()
    if not db_firestore:
        print("❌ No hay conexión a Firebase")
        return False
    try:
        # Agregar timestamps
        data['fechaCreacion'] = firestore.SERVER_TIMESTAMP
        data['fechaActualizacion'] = firestore.SERVER_TIMESTAMP
        
        db_firestore.collection('RuedaNegocio').add(data)
        print("✅ Nueva rueda de negocio agregada")
        return True
    except Exception as e:
        print(f"❌ Error agregando rueda: {e}")
        return False

def eliminar_usuario_completamente(user_id):
    """Elimina completamente un usuario y todo su rastro en la base de datos"""
    db_firestore = get_db()
    if not db_firestore:
        print("❌ No hay conexión a Firebase")
        return False
    
    try:
        print(f"🗑️ INICIANDO ELIMINACIÓN COMPLETA del usuario: {user_id}")
        
        # 1. ELIMINAR PUBLICACIONES DEL USUARIO
        print("📝 Buscando publicaciones del usuario...")
        publicaciones_ref = db_firestore.collection('Publicacion')
        publicaciones_usuario = publicaciones_ref.where('userId', '==', user_id).stream()
        
        publicaciones_eliminadas = 0
        for pub in publicaciones_usuario:
            # Eliminar comentarios de esta publicación
            comentarios_ref = db_firestore.collection('Comentarios')
            comentarios_publicacion = comentarios_ref.where('publicacionId', '==', pub.id).stream()
            
            comentarios_eliminados = 0
            for comentario in comentarios_publicacion:
                comentario.reference.delete()
                comentarios_eliminados += 1
            
            # Eliminar la publicación
            pub.reference.delete()
            publicaciones_eliminadas += 1
            print(f"   🗑️ Publicación {pub.id} eliminada (+ {comentarios_eliminados} comentarios)")
        
        # 2. ELIMINAR COMENTARIOS DEL USUARIO
        print("💬 Buscando comentarios del usuario...")
        comentarios_ref = db_firestore.collection('Comentarios')
        comentarios_usuario = comentarios_ref.where('usuarioId', '==', user_id).stream()
        
        comentarios_eliminados = 0
        for comentario in comentarios_usuario:
            comentario.reference.delete()
            comentarios_eliminados += 1
        print(f"   🗑️ {comentarios_eliminados} comentarios eliminados")
        
        # 3. ELIMINAR RUEDAS DE NEGOCIO CREADAS POR EL USUARIO
        print("🤝 Buscando ruedas de negocio del usuario...")
        ruedas_ref = db_firestore.collection('RuedaNegocio')
        ruedas_usuario = ruedas_ref.where('userId', '==', user_id).stream()
        
        ruedas_eliminadas = 0
        for rueda in ruedas_usuario:
            rueda.reference.delete()
            ruedas_eliminadas += 1
        print(f"   🗑️ {ruedas_eliminadas} ruedas de negocio eliminadas")
        
        # 4. ELIMINAR AL USUARIO DE LISTAS DE ASISTENTES EN RUEDAS
        print("👥 Eliminando usuario de listas de asistentes...")
        todas_ruedas = ruedas_ref.stream()
        ruedas_actualizadas = 0
        
        for rueda in todas_ruedas:
            rueda_data = rueda.to_dict()
            asistentes = rueda_data.get('asistentes', [])
            
            if user_id in asistentes:
                nuevos_asistentes = [a for a in asistentes if a != user_id]
                rueda.reference.update({'asistentes': nuevos_asistentes})
                ruedas_actualizadas += 1
        
        print(f"   🔄 Usuario removido de {ruedas_actualizadas} ruedas como asistente")
        
        # 5. ELIMINAR LIKES DEL USUARIO EN PUBLICACIONES
        print("❤️ Eliminando likes del usuario en publicaciones...")
        todas_publicaciones = db_firestore.collection('Publicacion').stream()
        publicaciones_actualizadas = 0
        
        for pub in todas_publicaciones:
            pub_data = pub.to_dict()
            likes = pub_data.get('likes', [])
            
            if user_id in likes:
                nuevos_likes = [l for l in likes if l != user_id]
                pub.reference.update({'likes': nuevos_likes})
                publicaciones_actualizadas += 1
        
        print(f"   🔄 Likes eliminados de {publicaciones_actualizadas} publicaciones")
        
        # 6. ELIMINAR LIKES DEL USUARIO EN COMENTARIOS
        print("💖 Eliminando likes del usuario en comentarios...")
        todos_comentarios = db_firestore.collection('Comentarios').stream()
        comentarios_actualizados = 0
        
        for comentario in todos_comentarios:
            comentario_data = comentario.to_dict()
            likes_comentarios = comentario_data.get('likes_Comentarios', [])
            
            if user_id in likes_comentarios:
                nuevos_likes_comentarios = [l for l in likes_comentarios if l != user_id]
                comentario.reference.update({'likes_Comentarios': nuevos_likes_comentarios})
                comentarios_actualizados += 1
        
        print(f"   🔄 Likes eliminados de {comentarios_actualizados} comentarios")
        
        # 7. FINALMENTE ELIMINAR EL USUARIO
        print("👤 Eliminando usuario principal...")
        db_firestore.collection('Usuario').document(user_id).delete()
        
        # RESUMEN FINAL
        print(f"\n🎉 ELIMINACIÓN COMPLETA EXITOSA:")
        print(f"   📝 Publicaciones eliminadas: {publicaciones_eliminadas}")
        print(f"   💬 Comentarios eliminados: {comentarios_eliminados}")
        print(f"   🤝 Ruedas eliminadas: {ruedas_eliminadas}")
        print(f"   👥 Ruedas actualizadas (asistente): {ruedas_actualizadas}")
        print(f"   ❤️ Publicaciones con likes removidos: {publicaciones_actualizadas}")
        print(f"   💖 Comentarios con likes removidos: {comentarios_actualizados}")
        print(f"   👤 Usuario principal: ELIMINADO")
        
        return True
        
    except Exception as e:
        print(f"💥 ERROR en eliminación completa: {e}")
        return False