import sys
import os

import requests


for file in os.listdir('/root/hse_project_seminar/crawling/wildberries/wildberries/spiders/'):
    file_path = f'/root/hse_project_seminar/crawling/wildberries/wildberries/spiders/{file}'
    if file_path[-7:] == '2022.jl':
        files = {'file': open(file_path, 'rb')}

        url = 'http://localhost:1337/api/upload'
        r = requests.post(url, files=files)
        print(r.status_code, file)