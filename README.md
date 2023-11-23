# neosyn

## Setup Client

.env.local file in /client/

    ```
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
    python -m venv dks-venv
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
    DEFAULT_USERS=<username>:<password>//<username>:<password>//...
    JWT_SECRET_TOKEN=<KEY>
    FLASK_SECRET_KEY=<KEY>
    ```
