from datetime import datetime, timedelta, date
import os

import psycopg2
import pandas as pd

delta = date.today() - date(2022, 4, 24)
dates = [str(date(2022, 4, 24) + timedelta(days=i))[5:].replace('-', '_') + '_2022' for i in range(delta.days + 1)]

connection = psycopg2.connect(
  host='db',
  user='hello_flask',
  password='hello_flask',
  database='hello_flask_prod',
  port=5432,
)

for cur_date in dates:

  try:
    df_temp = pd.read_json(f'/home/spiders/res_for_{cur_date}.jl', lines=True)
  except:
    print(date, 'does not exist')
    continue

  df_temp['dt'] = datetime.strptime(cur_date, '%m_%d_%Y').date().strftime('%m-%d-%Y')

  numeric_cols = ['priceU', 'salePriceU', 'qty', 'supplierId', 'rating', 'inn']
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
    df_temp = df_temp.drop(columns=['questions', 'diffPrice', 'description', 'sizes', 'comments', 'pics'])
  except:
    df_temp = df_temp.drop(columns=['questions', 'diffPrice', 'description', 'sizes'])

  # print(df_temp.columns)

  df_temp_0, df_temp_1 = df_temp[:20000], df_temp[20000:]
  values_0 = str([tuple(el) for el in df_temp_0.values])[1:-1]
  values_1 = str([tuple(el) for el in df_temp_1.values])[1:-1]

  with connection.cursor() as cursor:
    cursor.execute(
    f'INSERT INTO products VALUES {values_0};'
    )
    connection.commit()
    if values_1:
      cursor.execute(
      f'INSERT INTO products VALUES {values_1};'
      )
      connection.commit()
    print(f'SUCCESS on {cur_date}')
