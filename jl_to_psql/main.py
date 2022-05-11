from datetime import datetime, timedelta

import psycopg2
import pandas as pd

date_now = datetime.now().strftime("%m_%d_%Y %H:%M:%S").split()[0]
print(date_now)
#df = pd.read_json(f'/home/mvliksakov/project_seminar/hse_project_seminar/crawling/wildberries/wildberries/spiders/res_for_{date_now}.jl', lines=True)
df = pd.read_json(f'/home/mvliksakov/project_seminar/hse_project_seminar/crawling/wildberries/wildberries/spiders/res_for_{date_now}.jl', lines=True)
df['dt'] = (datetime.today() - timedelta(days=11)).strftime('%Y-%m-%d')
df['name'] = df['name'].apply(lambda x: x.replace('&', 'and'))
df['name'] = df['name'].apply(lambda x: x.replace('\'', ''))

dff = df[['id', 'qty', 'dt', 'name', 'rating']]

values = str([tuple(el) for el in dff.values])[1:-1]

connection = psycopg2.connect(
  host = "localhost",
  user = "romashka",
  password = "romashka",
  database = "wildberries",
  port = 5432
)

with connection.cursor() as cursor:
  cursor.execute(
  f'INSERT INTO products (product_id, qty, dt, name, rating) VALUES {values};'
  )
  connection.commit()
print('SUCCESS')