from decouple import config



class Settings:
    mongo_uri = config("MONGO_URI")
    salt = config("SALT").encode()
    secret_key = config("SECRET_KEY")
    algorithm = "HS256"
    access_token_expire_minutes = 120
    db_name = "docto-db"


CONFIG = Settings()
