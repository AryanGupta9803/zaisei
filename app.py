from flask import Flask, render_template, redirect, request
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)

cred = credentials.Certificate('zaisei-kuhaku-firebase-adminsdk-534l6-98bbc60897.json')
firebase_admin.initialize_app(cred)


