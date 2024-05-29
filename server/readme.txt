git clone https://github.com/thaivt1312/hrv_server.git
cd hrv_server
This project is running with python 3.10, please upgrade or downgrade to 3.10 for best run

1. Prepare
    a. Database
        This database will be run in mysql at localhost
        Import hrv_server/db.sql to your local database
        Open config/db_connect and replace with your host/port/user/password/database

2. Run server: 
    a. Prepare the first running:
        cd hrv_server 
        python -m venv venv
        source venv/Scripts/activate
        pip install -r requirements.txt
    b. Run server:
        source venv/Scripts/activate
        python manage.py runserver
        This server will be run at localhost:8000