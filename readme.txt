git clone https://github.com/thaivt1312/hrv_server.git
cd hrv_server

1. Run server
    This project is running with python 3.10, please upgrade or downgrade to 3.10 for best run
    a. Database
        This database will be run in mysql at localhost
        Import hrv_server/server/db.sql to your local database
        Open config/db_connect and replace with your host/port/user/password/database
    b. Server
        - Prepare the first running:
            cd server 
            python -m venv venv
            source venv/Scripts/activate
            pip install -r requirements.txt
        - Run server:
            source venv/Scripts/activate
            python manage.py runserver
            This server will be run at localhost:8000
        - Deploy for smart watch app to connect:
            Deploy server with any services (I'm using ngrok and deployed to "https://intent-alien-crisp.ngrok-free.app" at my server host machine)
            Add your deployed url to ALLOWED_HOSTS in file hrv_server/server/ServerSettings/settings.py, something like this:
                ALLOWED_HOSTS = ["localhost", "127.0.0.1", "https://intent-alien-crisp.ngrok-free.app"] 
                    -> ALLOWED_HOSTS = ["localhost", "127.0.0.1", "https://intent-alien-crisp.ngrok-free.app", "https:/your-url]

2. Run app
    App is tested with 'Samsung galaxy watch 6'
    Import hrv_server/app to Android Studio
    Replace all the "https://intent-alien-crisp.ngrok-free.app/" places to the url of your deployed server
    Connect to physical smart watch device
    Run project on physical device
    The app need to be always running
    On your first time, please click all four buttons to request permissions to record audio, measure heart rate and get your current location. Please choose allow this app to access to those permissions.

3. System:
    When you run app and done access to all permissions, the server will start sending messages through firebase to the device.
    Messages has 2 type: get_heart_rate (get heart rates and location) and get_audio_record.
    The get_heart_rate will be sent every 5 minutes from the start.
    When received, the app will start getting heart rates, locations or recording audio and send back to the server.
    Server will process the heart rate and predict stress level, if stress level is higher than 1, server will send messages to record 1 minute long audio.
    When received audio, the server will predict if anything dangerous happened in that audio.
    Finnally, the server will return stress level and dangerous if any in the audio file.