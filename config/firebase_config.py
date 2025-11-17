import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore, storage

db_firestore = None
bucket = None
firebase_initialized = False

def init_firebase():
    global db_firestore, bucket, firebase_initialized
    
    if firebase_initialized:
        return True

    load_dotenv()  # Carga variables del .env

    try:
        print("🚀 INICIANDO FIREBASE DESDE VARIABLES DE ENTORNO...")

        # Variables obligatorias
        required_vars = ["FIREBASE_PRIVATE_KEY", "FIREBASE_CLIENT_EMAIL", "FIREBASE_PROJECT_ID"]
        for var in required_vars:
            if not os.environ.get(var):
                raise Exception(f"❌ VARIABLE FALTANTE: {var}")

        # Reconstruir la clave privada con saltos de línea correctos
        private_key = os.environ["FIREBASE_PRIVATE_KEY"].replace("\\n", "\n")

        firebase_config = {
            "type": os.environ.get("FIREBASE_TYPE", "service_account"),
            "project_id": os.environ["FIREBASE_PROJECT_ID"],
            "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID", ""),
            "private_key": private_key,
            "client_email": os.environ["FIREBASE_CLIENT_EMAIL"],
            "client_id": os.environ.get("FIREBASE_CLIENT_ID", ""),
            "auth_uri": os.environ.get("FIREBASE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
            "token_uri": os.environ.get("FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
            "auth_provider_x509_cert_url": os.environ.get("FIREBASE_AUTH_PROVIDER_X509_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
            "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_X509_CERT_URL", "")
        }

        cred = credentials.Certificate(firebase_config)

        # Inicializar Firebase solo si no está inicializado
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {
                'storageBucket': f"{os.environ['FIREBASE_PROJECT_ID']}.appspot.com"
            })
            print("🎉 Firebase inicializado correctamente")
        else:
            print("⚠️ Firebase ya estaba inicializado")

        db_firestore = firestore.client()
        bucket = storage.bucket()
        firebase_initialized = True

        print("✅ Conexión a Firestore y Storage establecida")
        return True
        
    except Exception as e:
        print(f"💥 ERROR CRÍTICO CON FIREBASE: {e}")
        db_firestore = None
        bucket = None
        firebase_initialized = False
        return False

def get_db():
    """Obtiene la instancia de la base de datos, inicializando si es necesario"""
    global db_firestore
    if db_firestore is None:
        init_firebase()
    return db_firestore

def get_bucket():
    """Obtiene la instancia de storage, inicializando si es necesario"""
    global bucket
    if bucket is None:
        init_firebase()
    return bucket