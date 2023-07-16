from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from comunidadeimpressionadora.models import usuario
from flask_login import current_user
from wtforms import TextAreaField
from wtforms import HiddenField

#=========================================================================================================================
mensagens = {
    'required': 'Este campo é obrigatório.',
    'length': 'Este campo deve ter entre %(min)d e %(max)d caracteres.',
    'email': 'Digite um endereço de email válido.',
    'equal_to': 'Os campos devem ser iguais.'
}


#=========================================================================================================================
class CriarContaForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(mensagens['required']), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(mensagens['required']), Email(mensagens['email'])])
    password = PasswordField('Senha', validators=[DataRequired(mensagens['required']), Length(min=6, max=30)])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(mensagens['required']), EqualTo('password', message=mensagens['equal_to'])])
    submit_criar_conta = SubmitField('Criar Conta')

    def validate_email(self, email):
        Usuario = usuario.query.filter_by(email= email.data).first()
        if Usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail')
#=========================================================================================================================
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(mensagens['required']), Email(mensagens['email'])])
    password = PasswordField('Senha', validators=[DataRequired(mensagens['required']), Length(min=6, max=30)])      
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    submit_login = SubmitField('Entrar')

#=========================================================================================================================
class FormEditarPerfil(FlaskForm):
    username = StringField('Novo Usuário', validators=[DataRequired(mensagens['required']), Length(min=3, max=20)])
    email = StringField('Novo Email', validators=[DataRequired(mensagens['required']), Email(mensagens['email'])])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    
    linguagem_python = BooleanField('Python')
    linguagem_java = BooleanField('java')
    linguagem_javasrcipt = BooleanField('JavasCript')
    linguagem_c = BooleanField('C')
    linguagem_SQL = BooleanField('SQL')
    linguagem_PHP = BooleanField('PHP')
    linguagem_TypeScript = BooleanField('TypeScript')
    linguagem_ccc = BooleanField('C++')
    linguagem_cc = BooleanField('C#')

    desenvolvedor_Front = BooleanField('Dev Front-end')
    desenvolvedor_back = BooleanField('Dev Back-end')
    desenvolvedor_full = BooleanField('Dev Full-stack ')
    desenvolvedor_desk = BooleanField('Dev Desktop')
    desenvolvedor_web = BooleanField('Dev web')
    desenvolvedor_mobile = BooleanField('Dev Mobile')
    desenvolvedor_jogos = BooleanField('Dev de jogos')

    botao_submit_editarperfil = SubmitField('Confirmar Edição')


    def validate_email(self, email):
        if current_user.email != email.data:
            Usuario = usuario.query.filter_by(email= email.data).first()
            if Usuario:
                raise ValidationError('Já exite um usuário com este e-mail. Cadastre-se com outro e-mail')

#=========================================================================================================================

class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post Aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post') 
    botao_submit2 = SubmitField('Confirmar edição ')


class FormResponderPost(FlaskForm):
    resposta = TextAreaField('Resposta', validators=[DataRequired()])
    
    botao_submit = SubmitField('Responder')




