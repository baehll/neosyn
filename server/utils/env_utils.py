from decouple import config, UndefinedValueError

class EnvManager:
    def __init__(self) -> None:
        needed_vars = ["DATABASE_URL", "OPENAI_API_KEY", "FACEBOOK_OAUTH_CLIENT_ID", "FACEBOOK_OAUTH_CLIENT_ID", "EARLY_ACCESS_KEYS", "FLASK_SECRET_KEY", "IMPLEMENTED_PLATFORMS", "GPT_ASSISTANT_ID"]

        for var in needed_vars:
            val = config(var)
            if (val == ""):
                raise UndefinedValueError
            

