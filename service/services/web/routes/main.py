import json
from datetime import datetime, timedelta
from collections import defaultdict
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


class Products(db.Model):
    __tablename__ = "products"

    info_id = db.Column(db.Integer, primary_key=True, index=True)
    product_id = db.Column(db.Integer)
    rating = db.Column(db.Numeric(3, 2))
    description = db.Column(db.String(50000))
    questions = db.Column(db.String(50000))
    name = db.Column(db.String(500))
    brand = db.Column(db.String(200))
    priceU = db.Column(db.Integer)
    salePriceU = db.Column(db.Integer)
    pics = db.Column(db.Integer)
    colors = db.Column(db.String(500))
    sizes = db.Column(db.String(500))
    qty = db.Column(db.Integer)
    diffPrice = db.Column(db.Boolean)
    supplierId = db.Column(db.Integer)
    supplierName = db.Column(db.String(200))
    inn = db.Column(db.String(20))
    price_history = db.Column(db.String(50000))
    dt = db.Column(db.Date)


db.create_all()
db.session.commit()



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


@main.route('/some_info/<prod_id>', methods=['GET'])
def some_info(prod_id):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(f'''
          SELECT *
          FROM products
          WHERE product_id = {prod_id} AND dt = now()::date - interval '3 days'
        ''')
        fetched = cursor.fetchall()

    return jsonify({'result':[dict(row) for row in fetched]})


#                                            id       
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




# print(sold_prods_by_id(connection, 18602386))


@main.route('/api/data_info', methods=['GET'])
def data_info():
    count = db.session.query(Products).count()
    return jsonify({'rows': count})



#           (       )                                 -                          N.                                          
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


# print(avg_available_prods_amt_by_name(connection, '             '))


#           (       )                                                  -                          N.                               
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


# print(avg_seller_prods_amt_by_name(connection, '             '))


@main.route('/viewpage', methods=['GET'])
def viewpage():
    a = """
    <html>
    <head>
    <title>My first chart using FusionCharts Suite XT</title>
    <!-- Include fusioncharts core library -->
    <script type="text/javascript" src="https://cdn.fusioncharts.com/fusioncharts/latest/fusioncharts.js"></script>
    <!-- Include fusion theme -->
    <script type="text/javascript" src="https://cdn.fusioncharts.com/fusioncharts/latest/themes/fusioncharts.theme.fusion.js"></script>
    <script type="text/javascript">
     
     FusionCharts.ready(function () {
     
     var revenueChart = new FusionCharts({
     "type":"line",
     "renderAt":"chartContainer",
     "width":'100%',
     "height":'100%',
     "dataFormat":"json",
     "dataSource": {
     "chart": {
     "caption":"Выручка по дням",
     "subCaption":"",
     "xAxisName":"Дата",
     "yAxisName":"Сумма",
     "theme":"zune",
     
     },
     "data": """ +request.args.get('body')+"""
          
          
          
        
     
     }
     });
     
     revenueChart.render();
     });
     
    </script>
    
    </script>
    </head>
    <body>
    <div id="chartContainer">FusionCharts XT will load here!</div>
    </body>
    </html>
    """

    return a
    #file1 = '/home/mvliksakov/project_seminar/hse_project_seminar/service/services/web/routes/index.html'

    #with open(file1, 'r') as f:
     #   return f.read()


#                                       id        (                          )
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


@main.route('/daily_qty_revenue/<prod_id>', methods=['GET'])
def daily_qty_revenue(prod_id):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(f'''
          SELECT product_id, name, dt, diff, diff * sale_price AS revenue FROM (
            SELECT
              product_id, name, qty, dt, LEAD(qty, -1) OVER (ORDER BY dt) - qty AS diff, sale_price
              FROM products
              WHERE product_id = {prod_id}
              ) AS t1
          WHERE diff IS NOT NULL AND diff >= 0
        ''')
        fetched = cursor.fetchall()
    return jsonify({'result':[dict(row) for row in fetched]})


@main.route('/sold_prods_by_id/<prod_id>', methods=['GET'])
def sold_prods_by_id(prod_id):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(f'''
      SELECT SUM(sale_price) / COUNT(*) * SUM(CASE WHEN diff > 0 THEN diff ELSE 0 END) AS total_revenue,
       SUM(CASE WHEN diff > 0 THEN diff ELSE 0 END) AS sold_prods_amt
      FROM (
      SELECT sale_price, LEAD(qty, -1) OVER (ORDER BY dt) - qty AS diff
        FROM products
        WHERE product_id = {prod_id}
    ) AS t1
    ''')
        fetched = cursor.fetchall()
    return jsonify({'result':[dict(row) for row in fetched]})


@main.route('/predict_revenue/<prod_id>', methods=['GET'])
def predict_revenue(prod_id, days_to_predict=7):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(f'''
          SELECT product_id, name, dt, diff, diff * sale_price AS revenue FROM (
            SELECT
              product_id, name, qty, dt, LEAD(qty, -1) OVER (ORDER BY dt) - qty AS diff, sale_price
              FROM products
              WHERE product_id = {prod_id}
              ) AS t1
          WHERE diff IS NOT NULL AND diff >= 0
        ''')
        fetched = cursor.fetchall()
    sql_dict = [dict(row) for row in fetched]

    df_req = pd.DataFrame(sql_dict)

    revenue = list(df_req['revenue'].values)

    X = [[i] for i in range(1, len(revenue) + 1)]
    y = revenue

    # regressor = LinearRegression().fit(X, y)
    #
    # return jsonify({'result':
    #                     [0 if el < 0 else int(el) for el in regressor.predict([[len(revenue)+i]
    #                                                                            for i in range(1, days_to_predict+1)])]})

@main.route("/api/upload", methods=['POST'])
def upload_data():

    date_now = datetime.now().strftime("%m_%d_%Y %H:%M:%S").split()[0]
    dt = datetime.strptime(date_now, '%m_%d_%Y').date().strftime('%m-%d-%Y')

    f = request.files.get('file')
    vals = []
    errors = 0

    for line in f.read().decode('ascii').split('\n'):
        try:
            vals.append(defaultdict(lambda: None, json.loads(line)))
        except:
            errors += 1

    print(f'{errors} broken jsons out of {len(vals)}', flush=True)  # 1 out of 141 000 as a rule

    obj_lines = ['questions', 'colors', 'sizes', 'price_history']

    for val in vals:

        for line in obj_lines:
            if val[line]:
                val[line] = str(val[line])

        db_model = Products(
            product_id=val['id'],
            rating=val['rating'],
            description=val['description'],
            questions=val['questions'],
            name=val['name'],
            brand=val['brand'],
            priceU=val['priceU'],
            salePriceU=val['salePriceU'],
            pics=val['pics'],
            colors=val['colors'],
            sizes=val['sizes'],
            qty=val['qty'],
            diffPrice=val['diffPrice'],
            supplierId=val['supplierId'],
            supplierName=val['supplierName'],
            inn=val['inn'],
            price_history=val['price_history'],
            dt=dt
        )
        db.session.add(db_model)

    db.session.commit()

    return {"Result": "OK"}


@main.route('/api/get_info/<prod_id>', methods=['GET'])
def get_info(prod_id):
    product = db.session.query(Products).filter(Products.product_id == prod_id).first()
    return jsonify(qty=product.qty)


@main.route('/load_data', methods=['GET'])
def load_data():
    date_now = datetime.now().strftime("%m_%d_%Y %H:%M:%S").split()[0]
    df_temp = pd.read_json(f"f'/home/spiders/res_for_{date_now}.jl", lines=True)
    # dates = [(datetime.today() - timedelta(days=i)).strftime('%Y-%m-%d')[5:].replace('-', '_') + '_2022' for i in range(24, -1, -1)]

    df_temp['dt'] = datetime.strptime(date_now, '%m_%d_%Y').date().strftime('%m-%d-%Y')

    numeric_cols = ['pics', 'priceU', 'salePriceU', 'qty', 'supplierId', 'rating', 'inn']
    for col in numeric_cols:
        df_temp[col] = df_temp[col].fillna(0)

    # df_temp['comments'].fillna('0 РѕС‚Р·С‹РІРѕРІ')
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

    df_temp_0, df_temp_1 = df_temp[:20000], df_temp[20000:]
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

    if values_1:
        cursor.execute(
          	  f'INSERT INTO products VALUES {values_1};'
        	)
        conn.commit()
        print(f'SUCCESS on {date_now}')

