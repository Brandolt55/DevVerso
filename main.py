from comunidadeimpressionadora import app, database, socketio
from comunidadeimpressionadora import models



#codigo de debug do site
if __name__ == '__main__':
    app.run(debug=True)




# ===========================================================

# este codigo é para a criação do banco de dados e ele deve sempre vir antes do "run" da pagina assim criado ele

# deve tmb importar o models que vai ser usado no database

# from comunidadeimpressionadora import models, database

# with app.app_context():
#     database.create_all()


# e no init da pagina deve haver o direcionamento do banco de dados para que ele fique abaixo do arquivo principal da pagina
# exemplo:  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'comunidade.db')

# ---------------------------------------------------------