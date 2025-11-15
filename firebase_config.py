# firebase_config.py
import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate("pay-nic-firebase-adminsdk-fbsvc-abd1cf1335.json")
firebase_app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'pay-nic.appspot.com'
})

db = firestore.client()
bucket = storage.bucket()
