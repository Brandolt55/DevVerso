from comunidadeimpressionadora import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return usuario.query.get(int(id_usuario))

class usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String , default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)
    tipo_dev = database.Column(database.String, nullable=False, default='Não informado')
    linguagem = database.Column(database.String, nullable=False, default='Não informado')

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

class Comentario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    conteudo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    autor_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    id_post = database.Column(database.Integer, database.ForeignKey('post.id'), nullable=False)
    autor = database.relationship('usuario', backref='comentarios')
    post = database.relationship('Post', backref='comentarios')

class Notificacao(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    mensagem = database.Column(database.String(200), nullable=False)
    data = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    usuario_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    comentario_id = database.Column(database.Integer, database.ForeignKey('comentario.id'), nullable=True)

    usuario = database.relationship('usuario', foreign_keys=[usuario_id], backref='notificacoes')
    comentario = database.relationship('Comentario', foreign_keys=[comentario_id])

    def __repr__(self):
        return f"Notificacao('{self.mensagem}', '{self.data}')"
