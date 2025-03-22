# FLM-APP-BE
The place to storage the back-end system of FLM-APP

create db with name slm_app in PostgreSQL
change username and password of PostgreSQL in model.py
redirect terminal to folder models -> run file model.py: python model.py to create data table 
redirect terminal to flm_app_api 

-m venv my_env

my_env\Scripts\Activate

pip install -r requirement.txt    

uvicorn flm_app_api.main:app --host localhost --port 8080 --reload  



