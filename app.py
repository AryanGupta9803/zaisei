from flask import Flask, render_template, redirect, request
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)
