from pydantic_settings import BaseSettings


class Setting(BaseSettings):

    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


settings = Setting(_env_file='.env')