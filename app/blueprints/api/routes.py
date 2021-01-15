from . import bp as api
from flask import render_template, redirect, url_for, jsonify
import requests
from app import db

@api.route('/', methods=['GET'])
def main():
    return render_template('api/main.html')