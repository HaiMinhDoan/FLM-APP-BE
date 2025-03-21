# FLM-APP-BE
The place to storage the back-end system of FLM-APP

-m venv my_env

my_env\Scripts\Activate

pip install -r requirement.txt    

uvicorn flm_app_api.main:app --host localhost --port 8080 --reload  
