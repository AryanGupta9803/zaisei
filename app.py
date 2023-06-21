from flask import Flask, render_template, redirect, request
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore

app = Flask(__name__)

cred = credentials.Certificate('kuhaku-admin.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

users_ref = db.collection('users')

@app.route('/login/<string:users>/<string:passw>')
def login(users, passw) {
    doc_ref = users_ref.document(users)
    doc = doc_ref.get()
    if doc.exists:
        details = doc.to_dict()
        if details[user] = users and details[pass] = passw:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})
    else:
        return jsonify({"success": False})
}

@app.route('/signup/<string:users>/<string:passw>')
def signup(users, passw) {
    data = {"user": users, "pass": passw}
    users_ref.document(users).set(data)
    doc_ref = users_ref.document(users)
    doc = doc_ref.get()
    if doc.exists:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})
}