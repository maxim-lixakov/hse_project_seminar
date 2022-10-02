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
python /root/hse_project_seminar/jl_to_psql/main.py

