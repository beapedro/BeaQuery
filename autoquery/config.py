
from BeaQuery import app
import os 



SQLALCHEMY_DATABASE_URI =  \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha='!',
        servidor = 'localhost',
        database = ''
    )

