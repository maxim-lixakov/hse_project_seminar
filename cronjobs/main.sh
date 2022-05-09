#!/bin/bash
# activate venv
. "/home/mvliksakov/project_seminar/hse_project_seminar/crawling/venv/bin/activate"
#go to spider directory
cd  "/home/mvliksakov/project_seminar/hse_project_seminar/crawling/wildberries/wildberries/spiders"
now=$(date +"%m_%d_%Y")
echo $now
#run scrapy spider
scrapy crawl goods -o res_for_$now.jl

