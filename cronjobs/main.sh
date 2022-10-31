#!/bin/bash
# activate venv
. "/root/hse_project_seminar/crawling/venv/bin/activate"
#go to spider directory
cd  "/root/hse_project_seminar/crawling/wildberries/wildberries/spiders"
now=$(date +"%m_%d_%Y")
echo $now
#run scrapy spider
scrapy crawl goods -o res_for_$now.jl
#insert to psql
python3 /root/hse_project_seminar/cronjobs/download_data.py /root/hse_project_seminar/crawling/wildberries/wildberries/spiders/res_for_$now.jl

