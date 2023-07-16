#------IMPORTANDO AS BIBLIOTECAS ----------
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login  import LoginManager
from flask_socketio import SocketIO, emit

#abrindo o site Flask
app = Flask(__name__)

#deixando o site mais seguro
app.config['SECRET_KEY'] = '1dad613e1c42ae1b97cc863abc053ebf'
#direcionando o banco de dados para o arquivo principal da pasta
#para criar o banco de dados tem que ser um arquivo de fora da pasta junto com o main da pagina
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'comunidade.db')
socketio = SocketIO(app)


database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Faça login para continuar!'
login_manager.login_message_category = 'alert-warning'

from comunidadeimpressionadora import routes
