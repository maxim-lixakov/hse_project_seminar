#!/bin/bash
# activate venv
. "/home/mvliksakov/project_seminar/hse_project_seminar/venv/bin/activate"
#go to spider directory
cd  "/home/mvliksakov/project_seminar/hse_project_seminar/wildberries/wildberries/spiders"
now=$(date +"%m_%d_%Y")
echo $now
#run scrapy spider
python "/home/mvliksakov/project_seminar/hse_project_seminar/test.py"
scrapy crawl goods --logfile log.log -o res_for_$now.jl

