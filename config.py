
class Config:
    SECRET_KEY = '2fad37ea88d279117a11d079689e93e9'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # app.config['MAIL_USERNAME'] = #####os.environ.get()
    # app.config['MAIL_PASSWORD'] = #####os.environ.get()