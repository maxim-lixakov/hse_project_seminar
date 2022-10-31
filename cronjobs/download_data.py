import sys

import requests


file_path = sys.argv[1]
files = {'file': open(file_path, 'rb')}

url = 'http://localhost:1337/upload'
r = requests.post(url, files=files)
print(r.status_code)