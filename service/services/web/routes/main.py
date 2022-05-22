import json
import requests

from flask import Blueprint, render_template, jsonify, request
from flask_executor import Executor
from sqlalchemy.exc import NoResultFound


from project import db
from project import app

executor = Executor(app)
main = Blueprint('main', __name__)


@main.route('/main', methods=['GET'])
def upload():
    return jsonify({'status': 'OK'})