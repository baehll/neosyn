from decouple import config, UndefinedValueError

class EnvManager:
    def __init__(self) -> None:
        needed_vars = ["DATABASE_URL", "OPENAI_API_KEY", "DEFAULT_USERS", "JWT_SECRET_TOKEN", "FACEBOOK_OAUTH_CLIENT_ID", "FACEBOOK_OAUTH_CLIENT_ID", "EARLY_ACCESS_KEYS"]
        self.DEFAULT_USERS = []

        for var in needed_vars:
            val = config(var)
            if (val == ""):
                raise UndefinedValueError
            

