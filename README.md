# neosyn Dev Environment

## Setup Client
**SUBJECT TO CHANGE**
.env.local file in /client/

    ```bash
    VITE_FB_APP_ID=175537112285037
    VITE_BASE_URL=http://localhost:5000
    ```
### Commands

    npm install
    npm run dev

## Setup Server

### Python

1. Create a virtual environment with
    ```bash
    python -m venv neosyn-venv
    ```

2. Activate the virtual environment with
    ```bash
    source dks-venv/bin/activate
    ```

3. Install some requirements with
    ```bash
    pip install -r requirements.txt
    ```

4. .env.local file with 
    ```
    DATABASE_URL=sqlite:///database.db
    OPENAI_API_KEY=<KEY>
    EARLY_ACCESS_KEYS=<KEY>;<KEY>;...
    FLASK_SECRET_KEY=<KEY>
    FACEBOOK_OAUTH_CLIENT_ID=175537112285037
    FACEBOOK_OAUTH_CLIENT_SECRET=<KEY>
    COMPANY_FILE_UPLOAD_FOLDER=./UPLOADS/COMPANY_FOLDERS
    IMPLEMENTED_PLATFORMS=Instagram
    GPT_ASSISTANT_ID=asst_71TD5Qg6iTIy75t2k8hVWrwj
    ```

5. For local testing, run the following command to start flask as HTTPS and self signed cert in DEBUG mode
    ```
    flask run --cert=adhoc --debug
    ```
### DB Migration

1. migrations-folder initialisieren in ./
    ```bash
    flask --app app.py db init
    ```

2. migration scripts generieren
    ```bash
    flask --app app.py db migrate -m "WICHTIGE MESSAGE"
    ```

3. migration script **REVIEWEN**

4. apply migration changes
    ```bash
    flask --app app.py db upgrade
    ```