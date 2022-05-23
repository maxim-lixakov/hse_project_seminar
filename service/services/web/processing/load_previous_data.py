from datetime import datetime, timedelta
import os

import psycopg2
import pandas as pd

date_now = datetime.now().strftime("%m_%d_%Y %H:%M:%S").split()[0]
dates = [(datetime.today() - timedelta(days=i)).strftime('%Y-%m-%d')[5:].replace('-', '_') + '_2022' for i in range(24, -1, -1)]

connection = psycopg2.connect(
  host='db',
  user='hello_flask',
  password='hello_flask',
  database='hello_flask_prod',
  port=5432,
)

for date in dates:

  try:
    df_temp = pd.read_json(f'/home/spiders/res_for_{date}.jl', lines=True)
  except:
    print(date, 'does not exist')
    continue

  df_temp['dt'] = datetime.strptime(date, '%m_%d_%Y').date().strftime('%m-%d-%Y')

  numeric_cols = ['pics', 'priceU', 'salePriceU', 'qty', 'supplierId', 'rating', 'inn']
  for col in numeric_cols:
    df_temp[col] = df_temp[col].fillna(0)

  # df_temp['comments'].fillna('0 Р С•РЎвЂљР В·РЎвЂ№Р Р†Р С•Р Р†')
  df_temp.fillna('', inplace=True)

  # df_temp['comments'] = df_temp['comments'].apply(lambda x: int(x.split()[0]))
  df_temp['priceU'] = df_temp['priceU'].apply(lambda x: int(x/100))
  df_temp['salePriceU'] = df_temp['salePriceU'].apply(lambda x: int(x/100))
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

  with connection.cursor() as cursor:
    cursor.execute(
    f'INSERT INTO products VALUES {values_0};'
    )
    connection.commit()
    cursor.execute(
    f'INSERT INTO products VALUES {values_1};'
    )
    print(f'SUCCESS on {date}')
