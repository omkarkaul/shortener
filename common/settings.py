from os import environ


class Settings:
    ENV = environ.get('ENV', 'local')
