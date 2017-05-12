import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = True
SECRET_KEY = "please_replace_me" #replace with a unique alphanumeric key
MAIL_SERVER='' #smtp.mailprovider.com, generally
MAIL_PORT=465 #might be a different port, depending on mailprovider
MAIL_USE_SSL=True
MAIL_USE_TLS=False
MAIL_USERNAME='' #username@mailprovider.com, generally
MAIL_PASSWORD='' #password to username@mailprovider.com's email
GOOGLE_API_KEY='' #insert your google API key
WEATHER_API_KEY='' #insert your openweathermap.org api key
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')