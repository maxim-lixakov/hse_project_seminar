import json
from datetime import datetime, timedelta
import os

import requests
import psycopg2
import psycopg2.extras
import pandas as pd


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


conn = psycopg2.connect(
  host='db',
  user='hello_flask',
  password='hello_flask',
  database='hello_flask_prod',
  port=5432,
)


# Ежедневное количество проданных товаров по id товара
@main.route('/daily_qty/<prod_id>', methods=['GET'])
def daily_qty(prod_id):

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(f'''
          SELECT * FROM (
            SELECT
              product_id, name, qty, dt, LEAD(qty, -1) OVER (ORDER BY dt) - qty AS diff
              FROM products
              WHERE product_id = {prod_id}
              ) AS t1
          WHERE diff IS NOT NULL AND diff >= 0
        ''')
        fetched = cursor.fetchall()

    return jsonify({'result':[dict(row) for row in fetched]})


# print(daily_qty(connection, 18602386))


# Количество проданных товаров с выбранного дня по id товара
@main.route('/day_qty/<prod_id>', methods=['GET'])
def sold_prods_by_id(prod_id):

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(f'''
          SELECT SUM(CASE WHEN diff > 0 THEN diff ELSE 0 END) AS sold_prods
          FROM (
          SELECT LEAD(qty, -1) OVER (ORDER BY dt) - qty AS diff
            FROM products
            WHERE product_id = {prod_id}
        ) AS t1
        ''')
        fetched = cursor.fetchall()

    return jsonify({'result':[dict(row) for row in fetched]})


# print(sold_prods_by_id(connection, 18602386))


# В среднем (по дням) на маркетплейсе доступно столько-то товара с наименованием N. Посмотреть насколько большой рынок сейчас
@main.route('/avg_by_name/<prod_name>', methods=['GET'])
def avg_available_prods_amt_by_name(prod_name):

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(f'''
          SELECT name, CAST(SUM(qty) / (SELECT MAX(dt) - MIN(dt) FROM products) AS INT)
          FROM products
          WHERE name = '{prod_name}'
          GROUP BY name
        ''')
        fetched = cursor.fetchall()

    return jsonify({'result':[dict(row) for row in fetched]})


# print(avg_available_prods_amt_by_name(connection, 'Соль для ванн'))


# В среднем (по дням) на маркетплейсе каждый поставщик имеет по столько-то товара с наименованием N. Посмотреть кто сколько продает
@main.route('/goods_by_prod/<prod_name>', methods=['GET'])
def avg_seller_prods_amt_by_name(prod_name):

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(f'''
          SELECT product_id, CAST(SUM(qty) / (SELECT MAX(dt) - MIN(dt) FROM products) AS INT)
          FROM products
          WHERE name = '{prod_name}'
          GROUP BY product_id
        ''')
        fetched = cursor.fetchall()

    return jsonify({'result':[dict(row) for row in fetched]})


# print(avg_seller_prods_amt_by_name(connection, 'Соль для ванн'))


# Количество дней с нулевым остатком по id товара (есть дефицит получается ХА)
@main.route('/days_without_qty/<prod_id>', methods=['GET'])
def zero_qty_days_amt_by_id(prod_id):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(f'''
          SELECT COUNT(*)
          FROM (
            SELECT product_id, name, qty, dt
              FROM products
              WHERE product_id = {prod_id} and qty = 0
          ) as t1
        ''')
        fetched = cursor.fetchall()

    return jsonify({'result':[dict(row) for row in fetched]})


@main.route('/load_data', methods=['GET'])
def load_data():
    date_now = datetime.now().strftime("%m_%d_%Y %H:%M:%S").split()[0]
    df_temp = pd.read_json(f"f'/home/spiders/res_for_{date_now}.jl", lines=True)
    # dates = [(datetime.today() - timedelta(days=i)).strftime('%Y-%m-%d')[5:].replace('-', '_') + '_2022' for i in range(24, -1, -1)]

    df_temp['dt'] = datetime.strptime(date_now, '%m_%d_%Y').date().strftime('%m-%d-%Y')

    numeric_cols = ['pics', 'priceU', 'salePriceU', 'qty', 'supplierId', 'rating', 'inn']
    for col in numeric_cols:
        df_temp[col] = df_temp[col].fillna(0)

    # df_temp['comments'].fillna('0 Р С•РЎвЂљР В·РЎвЂ№Р Р†Р С•Р Р†')
    df_temp.fillna('', inplace=True)

    # df_temp['comments'] = df_temp['comments'].apply(lambda x: int(x.split()[0]))
    df_temp['priceU'] = df_temp['priceU'].apply(lambda x: int(x / 100))
    df_temp['salePriceU'] = df_temp['salePriceU'].apply(lambda x: int(x / 100))
    df_temp['colors'] = df_temp['colors'].apply(lambda x: ' '.join([el['name'] for el in x]))
    df_temp['supplierId'] = df_temp['supplierId'].apply(lambda x: int(x))
    df_temp['inn'] = df_temp['inn'].apply(lambda x: str(int(x)))
    df_temp['inn'].replace(to_replace={'0': ''}, inplace=True)

    danger_cols = ['name', 'brand', 'supplierName', 'legalAddress']
    for col in danger_cols:
        df_temp[col] = df_temp[col].apply(lambda x: x.translate({ord(c): None for c in '\'&'}))

    try:
        df_temp = df_temp.drop(columns=['questions', 'diffPrice', 'description', 'sizes', 'comments'])
    except:
        df_temp = df_temp.drop(columns=['questions', 'diffPrice', 'description', 'sizes'])

    # print(df_temp.columns)

    df_temp_0, df_temp_1 = df_temp[:20000], df_temp[:20000]
    values_0 = str([tuple(el) for el in df_temp_0.values])[1:-1]
    values_1 = str([tuple(el) for el in df_temp_1.values])[1:-1]

    conn = psycopg2.connect(
        host='db',
        user='hello_flask',
        password='hello_flask',
        database='hello_flask_prod',
        port=5432,
    )

    with conn.cursor() as cursor:
        cursor.execute(
            f'INSERT INTO products VALUES {values_0};'
        )
        conn.commit()
        cursor.execute(
            f'INSERT INTO products VALUES {values_1};'
        )
        print(f'SUCCESS on {date_now}')
