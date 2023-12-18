from decouple import config, UndefinedValueError

class EnvManager:
    def __init__(self) -> None:
        needed_vars = ["DATABASE_URL", "OPENAI_API_KEY", "DEFAULT_USERS", "JWT_SECRET_TOKEN", "FLASK_SECRET_KEY", "FB_CLIENT_SECRET"]
        self.DEFAULT_USERS = []

        for var in needed_vars:
            val = config(var)
            if (val == ""):
                raise UndefinedValueError
            
    # liest die default_users aus, sollte  
    def init_default_users(self):
        for creds in config("DEFAULT_USERS").split("//"):
            (name, pw) = creds.split(":")
            self.DEFAULT_USERS.append((name, pw))

