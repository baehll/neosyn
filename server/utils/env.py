from decouple import config, UndefinedValueError

# Überprüft, ob alle benötigten ENV_VARS da sind
needed_vars = ["DATABASE_URL", "OPENAI_API_KEY", "DEFAULT_USERS", "JWT_SECRET_TOKEN", "FLASK_SECRET_KEY"]
DEFAULT_USERS = []
ENV_VARS = {}

def check_env_vars():
    for var in needed_vars:
        try:
            val = config(var)
            ENV_VARS.update({var: val})
        except UndefinedValueError:
            print(f"ENV_VAR {var} nicht gefunden, ist aber benötigt")

def init_default_users():
    for creds in config("DEFAULT_USERS").split("//"):
        (name, pw) = creds.split(":")
        DEFAULT_USERS.append((name, pw))
        

check_env_vars()
init_default_users()