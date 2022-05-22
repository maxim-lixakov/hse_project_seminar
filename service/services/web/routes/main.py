import json
import requests
import psycopg2

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


@main.route('/select', methods=['GET'])
def select():
    connection = psycopg2.connect(
 	 host='db',
 	 user='hello_flask',
  	password='hello_flask',
  	database='hello_flask_prod',
  	port=5432,
	)
    with connection.cursor() as cursor:
    	a = cursor.execute('''
  	SELECT id, name, -1 * SUM(CASE WHEN diff < 0 THEN diff ELSE 0 END) as sold_prods
 	 FROM (SELECT id, name, qty, dt, neighbor(qty, -1) AS prev, qty-prev as diff FROM products WHERE id = 33182571 and dt > '2022-04-24') GROUP BY id, name ''')
    print(a)
    return jsonify({'status': 'OK'})
