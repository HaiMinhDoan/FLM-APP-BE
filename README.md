# FLM-APP-BE
The place to storage the back-end system of FLM-APP

create db with name slm_app in PostgreSQL
change username and password of PostgreSQL in model.py
redirect Terminal to slm_api 

docker build -t slm_api .

docker run -d -p 8080:8080 slm_api

