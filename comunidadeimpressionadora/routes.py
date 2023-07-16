from flask import render_template, flash, url_for, redirect,request , abort, session
from comunidadeimpressionadora import app, database, bcrypt, socketio
from comunidadeimpressionadora.forms import LoginForm, CriarContaForm,FormEditarPerfil, FormCriarPost,FormResponderPost 
from comunidadeimpressionadora.models import usuario, Post, Comentario, Notificacao
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image
from flask_socketio import emit
from datetime import datetime


#====================================================================================================
#function de atalho para o inicio da pagina
@app.route("/")
def home():
    #mostra os postes que foram publicados por ultimo
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)
#=================================================================
#funtion para direcionar ate o numero para contato da pagina
@app.route("/numero")
def contato():
    return render_template('contato.html')

#===============================================================
#funtion para direcionar ate os usuarios da pagina
@app.route("/usuarios")
@login_required
def usuarios():
    lista_usuario = usuario.query.all()
    return render_template('usuarios.html' , lista_usuario = lista_usuario)
#==================================================================================================



#====================================================================================================

@app.route('/criar conta', methods=['GET', 'POST'])
def criar_conta():
    """
    Função de visualização para criar uma nova conta de usuário.
    """
    form_criar_conta = CriarContaForm()  # Cria uma instância do formulário para criar uma conta

    if form_criar_conta.validate_on_submit():  # Se for uma requisição POST e o formulário for válido
        senha_cript = bcrypt.generate_password_hash(form_criar_conta.password.data)  # Criptografa a senha fornecida pelo usuário
        Usuario = usuario(username=form_criar_conta.username.data, email=form_criar_conta.email.data, senha=senha_cript)  # Cria um novo objeto Usuario com os dados do formulário e a senha criptografada
        database.session.add(Usuario)  # Adiciona o novo usuário ao banco de dados
        database.session.commit()  # Salva as alterações no banco de dados
        login_user(Usuario)  # Faz o login do usuário recém-criado
        flash('Bem-vindo ao DevVerso! Sua conta foi criada com sucesso.', 'alert-success')  # Exibe uma mensagem de sucesso
        return redirect(url_for('home'))  # Redireciona o usuário para a página inicial

    return render_template('criar conta.html', form_criar_conta=form_criar_conta)

#====================================================================================================

@app.route('/sair', methods=['GET', 'POST'])
@login_required
def sair():
    """
    Função de visualização para sair da conta de usuário.
    """
    foto_perfil = url_for('static', filename='foto_perfil/{}'.format(current_user.foto_perfil))
    
    if request.method == 'POST':  # Se for uma requisição POST
        logout_user()  # Faz o logout do usuário
        flash(f'Você saiu da conta', 'alert-primary')  # Exibe uma mensagem de aviso
        return redirect(url_for('home'))  # Redireciona o usuário para a página inicial
    
    return render_template('confirm_logout.html', foto_perfil=foto_perfil)
#====================================================================================================


@app.route('/perfil')
@login_required
def perfil():
    """
    Função de visualização para exibir o perfil do usuário.
    """
    foto_perfil = url_for('static', filename='foto_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


#====================================================================================================
@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    """
    Função de visualização para criar um novo post.
    """
    form = FormCriarPost()  # Cria uma instância do formulário para criar um post
    
    if form.validate_on_submit():  # Se for uma requisição POST e o formulário for válido
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)  # Cria um novo objeto Post com os dados do formulário e o usuário atual como autor
        database.session.add(post)  # Adiciona o novo post ao banco de dados
        database.session.commit()  # Salva as alterações no banco de dados
        flash('Post Criado com Sucesso', 'alert-success')  # Exibe uma mensagem de sucesso
        return redirect(url_for('home'))  # Redireciona o usuário para a página inicial
    
    return render_template('criar_post.html', form=form)  # Renderiza o template 'criar_post.html', passando o formulário como argumento

#====================================================================================================
# functions que irei usar no site

# está é para salvar a imagem do usuario
def salvar_imagem(imagem):
    # Gera um código único de 8 caracteres para ser usado no nome do arquivo
    codigo = secrets.token_hex(8)
    # Separa o nome do arquivo e a extensão da imagem
    nome, extensao = os.path.splitext(imagem.filename)
    # Cria um novo nome para o arquivo, adicionando o código gerado anteriormente e a extensão
    nome_arquivo = nome + codigo + extensao
    # Define o caminho completo onde a imagem será salva no servidor
    caminho_completo = os.path.join(app.root_path, 'static/foto_perfil', nome_arquivo)
    # Define o tamanho desejado para a imagem (400x400 pixels)
    tamanho = (400, 400)
    # Abre a imagem original usando a biblioteca PIL
    imagem_reduzida = Image.open(imagem)
    # Redimensiona a imagem para o tamanho desejado
    imagem_reduzida.thumbnail(tamanho)
    # Salva a imagem redimensionada no caminho completo especificado
    imagem_reduzida.save(caminho_completo)
    # Retorna o nome do arquivo para ser armazenado no banco de dados ou usado em outras partes do código
    return nome_arquivo

# ----------------------------------------------------------------------------------------------------------------
#  está é de salvar alterações da parte de edtitar perfil

def atualizar_linguagen(form):
    # Cria uma lista vazia para armazenar as linguagens selecionadas
    lista_linguagens = []
    # Percorre todos os campos do formulário
    for campo in form:
        # Verifica se o campo está relacionado a uma linguagem
        if 'linguagem_' in campo.name:
            # Verifica se o campo está marcado (foi selecionado pelo usuário)
            if campo.data:
                # Adiciona o texto do rótulo do campo à lista de linguagens
                lista_linguagens.append(campo.label.text)
    # Retorna as linguagens selecionadas como uma única string, separadas por ponto e vírgula
    return ';'.join(lista_linguagens)

# ----------------------------------------------------------------------------------------------------------------

def atualizar_desenvolvedor(form):
    # Cria uma lista vazia para armazenar os tipos de desenvolvedor selecionados
    lista_desenvolvedor = []
    # Percorre todos os campos do formulário
    for campo in form:
        # Verifica se o campo está relacionado a um tipo de desenvolvedor
        if 'desenvolvedor_' in campo.name:
            # Verifica se o campo está marcado (foi selecionado pelo usuário)
            if campo.data:
                # Adiciona o texto do rótulo do campo à lista de tipos de desenvolvedor
                lista_desenvolvedor.append(campo.label.text)
    # Retorna os tipos de desenvolvedor selecionados como uma única string, separados por ponto e vírgula
    return ';'.join(lista_desenvolvedor)




#====================================================================================================

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    
    if form.validate_on_submit():
        # Atualiza o e-mail e o nome de usuário do usuário atual com os valores do formulário
        current_user.email = form.email.data
        current_user.username = form.username.data
        # Verifica se uma nova foto de perfil foi enviada pelo usuário
        if form.foto_perfil.data:
            # Salva a nova imagem de perfil e obtém o nome do arquivo retornado pela função salvar_imagem
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            # Atualiza o nome do arquivo da foto de perfil do usuário atual
            current_user.foto_perfil = nome_imagem
        # Atualiza as informações de linguagem e tipo de desenvolvedor do usuário atual
        if any([campo.data for campo in form if 'linguagem_' in campo.name]):
            current_user.linguagem = atualizar_linguagen(form)
        else:
            current_user.linguagem = 'Não informado'
            
        if any([campo.data for campo in form if 'desenvolvedor_' in campo.name]):
            current_user.tipo_dev = atualizar_desenvolvedor(form)
        else:
            current_user.tipo_dev = 'Não informado'
            
        # Confirma as alterações no banco de dados
        database.session.commit()
        # Exibe uma mensagem de sucesso ao usuário
        flash('Perfil atualizado com sucesso', 'alert-success')
        # Redireciona o usuário para a página de perfil
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    
    foto_perfil = url_for('static', filename='foto_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)
#====================================================================================================
@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    """
    Função de visualização para exibir e atualizar um post.
    """
    post = Post.query.get(post_id)  # Recupera o post com o ID fornecido do banco de dados
    tem_comentarios = Comentario.query.filter_by(id_post=post_id).first() is not None
    
    if post and current_user == post.autor:  # Verifica se o usuário atual é o autor do post
        form = FormCriarPost()  # Cria uma instância do formulário para criar um post
        
        if request.method == 'GET':  # Se for uma requisição GET, preencha os campos do formulário com os dados do post
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():  # Se for uma requisição POST e o formulário for válido, atualize os dados do post
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()  # Salva as alterações no banco de dados
            flash('Post atualizado com sucesso', 'alert-success')
            return redirect(url_for('home'))  # Redireciona o usuário para a página inicial após atualizar o post
    else:
        form = None  # Se o usuário atual não for o autor, não exiba o formulário
        
    return render_template('post.html', post=post, form=form, tem_comentarios=tem_comentarios)


#====================================================================================================
# Rota para excluir um post
@app.route('/post/<int:post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    """
    Função de visualização para excluir um post.
    """
    post = Post.query.get(post_id)  # Recupera o post com o ID fornecido do banco de dados
    
    if current_user == post.autor:  # Verifica se o usuário atual é o autor do post
        # Excluir todos os comentários associados ao post
        Comentario.query.filter_by(id_post=post_id).delete()
        
        database.session.delete(post)  # Remove o post do banco de dados
        database.session.commit()  # Salva as alterações no banco de dados
        flash('Seu Post foi excluído com sucesso', 'alert-danger')
        return redirect(url_for('home'))  # Redireciona o usuário para a página inicial
    else:
        abort(403)  # Retorna um erro 403 (Acesso Proibido) caso o usuário atual não seja o autor do post


#====================================================================================================


@app.route('/meus_posts', methods=['GET'])
@login_required
def meus_posts():
    # Recupera todos os posts do usuário atual
    posts = Post.query.filter_by(autor=current_user).all()
    return render_template('meus_posts.html', posts=posts)


#====================================================================================================

@app.route('/editar_post/<post_id>', methods=['GET', 'POST'])
@login_required
def editar_post(post_id):
    post = Post.query.get(post_id)  # Recupera o post com o ID fornecido do banco de dados
    
    if post.autor != current_user:  # Verifica se o usuário atual é o autor do post
        abort(403)  # Retorna um erro 403 (Acesso Proibido) caso o usuário atual não seja o autor do post

    form = FormCriarPost()  # Cria uma instância do formulário para editar o post

    if request.method == 'GET':  # Se for uma requisição GET, preencha os campos do formulário com os dados do post
        form.titulo.data = post.titulo
        form.corpo.data = post.corpo
    elif form.validate_on_submit():  # Se for uma requisição POST e o formulário for válido, atualize os dados do post
        post.titulo = form.titulo.data
        post.corpo = form.corpo.data
        database.session.commit()  # Salva as alterações no banco de dados
        flash('Post atualizado com sucesso', 'alert-success')
        return redirect(url_for('home'))  # Redireciona o usuário de volta para a página de "Meus Posts"

    return render_template('editar_post.html', form=form, post=post)






#====================================================================================================

@app.route('/comentario/<int:comentario_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_comentario(comentario_id):
    comentario = Comentario.query.get_or_404(comentario_id)
    # Verificar se o usuário atual é o autor do comentário
    if current_user != comentario.autor:
        abort(403)  # Código HTTP 403 Forbidden - Acesso Negado

    if request.method == 'POST':
        novo_conteudo = request.form['conteudo']
        comentario.conteudo = novo_conteudo
        database.session.commit()
        flash('Comentário atualizado com sucesso!', 'success')
        return redirect(url_for('exibir_respostas', post_id=comentario.id_post))

    return render_template('editar_comentario.html', comentario=comentario)


#====================================================================================================


@app.route('/comentario/<int:comentario_id>/excluir', methods=['POST'])
@login_required
def excluir_comentario(comentario_id):
    comentario = Comentario.query.get_or_404(comentario_id)

    # Verificar se o usuário atual é o autor do comentário
    if current_user != comentario.autor:
        abort(403)  # Código HTTP 403 Forbidden - Acesso Negado

    database.session.delete(comentario)
    database.session.commit()
    flash('Comentário excluído com sucesso!', 'success')
    return redirect(url_for('exibir_respostas', post_id=comentario.id_post))

#====================================================================================================
# Rota para adicionar notificações à lista da sessão
@socketio.on('adicionar_notificacao')
def adicionar_notificacao(data):
    mensagem_notificacao = data['voce tem uma nova notificação']
    id_usuario_respondeu = current_user.id

    # Buscar o objeto Usuario correspondente ao ID do usuário que respondeu
    usuario_respondeu = usuario.query.get_or_404(id_usuario_respondeu)
    
    # Obter o nome do usuário que respondeu
    nome_usuario_respondeu = usuario_respondeu.username

    # Crie uma nova instância de Notificacao com a mensagem, o ID do usuário que respondeu e o nome do usuário
    notificacao = Notificacao(mensagem=f'{nome_usuario_respondeu} fez um novo comentário em seu Post', usuario_id=id_usuario_respondeu)

    # Salve a notificação no banco de dados
    database.session.add(notificacao)
    database.session.commit()

    # Emitir uma notificação para o autor do post, se necessário (mantenha esta parte)
    autor_do_post = Post.query.get_or_404(Post.id).autor
    mensagem_notificacao = notificacao
    socketio.emit('nova_notificacao', {'mensagem': mensagem_notificacao}, room=autor_do_post.id)




# ... Seu código de rota de login existente ...
#====================================================================================================


@app.route('/login', methods=['GET', 'POST'])
def login():
    formlogin = LoginForm()

    if formlogin.validate_on_submit():
        Usuario = usuario.query.filter_by(email=formlogin.email.data).first()
        if Usuario and bcrypt.check_password_hash(Usuario.senha, formlogin.password.data):
            login_user(Usuario, remember=formlogin.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {formlogin.email.data}', 'alert-success')

            parametro_next = request.args.get('next')
            if parametro_next:
                return redirect(parametro_next)
            else:
                return redirect(url_for('home'))


    return render_template('login.html', formlogin=formlogin)

#====================================================================================================

@app.route('/responder_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def responder_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = FormResponderPost()

    if form.validate_on_submit():
        # Obtenha o ID do usuário que está fazendo o comentário (use a lógica adequada para isso)
        id_usuario = current_user.id  # Substitua isso pela lógica real para obter o ID do usuário atual

        # Buscar o objeto Usuario correspondente ao ID do usuário atual
        usuario_respondeu = usuario.query.get_or_404(id_usuario)
        
        # Obter o nome do usuário que respondeu
        nome_usuario_respondeu = usuario_respondeu.username

        # Crie uma nova instância de Comentario com os dados do formulário, o ID do usuário e o nome do usuário
        comentario = Comentario(
            conteudo=form.resposta.data,
            autor_id=id_usuario,
            id_post=post_id
        )
        
        # Salve o comentário no banco de dados
        database.session.add(comentario)
        database.session.commit()

        flash('Resposta enviada com sucesso!', 'success')

        # Criar e salvar a notificação associada ao post no banco de dados, incluindo o nome do usuário
        notificacao = Notificacao(
            mensagem=f'{nome_usuario_respondeu} fez um novo comentário no seu post!',
            data=datetime.utcnow(),
            usuario_id=post.autor.id,
            comentario_id=comentario.id
        )
        database.session.add(notificacao)
        database.session.commit()

        return redirect(url_for('home'))

    return render_template('responder_post.html', post=post, form=form)



#====================================================================================================


@app.route('/notificacoes')
@login_required
def notificacoes():
    # Obter as notificações mais recentes do usuário atual a partir do banco de dados
    notificacoes = Notificacao.query.filter_by(usuario_id=current_user.id).order_by(Notificacao.data.desc()).all()

    # Renderizar o arquivo HTML de notificações, passando a lista de notificações como contexto
    return render_template('notificacoes.html', notificacoes=notificacoes)



#====================================================================================================

@app.route('/post/<int:post_id>/respostas')
@login_required
def exibir_respostas(post_id):
    post = Post.query.get_or_404(post_id)
    respostas = Comentario.query.filter_by(id_post=post_id).order_by(Comentario.id.desc()).all()

    return render_template('exibir_respostas.html', post=post, respostas=respostas)


#====================================================================================================
@app.route('/notificacoes/excluir/<int:notificacao_id>', methods=['POST'])
@login_required
def excluir_notificacao(notificacao_id):
    # Buscar a notificação no banco de dados
    notificacao = Notificacao.query.get_or_404(notificacao_id)
    
    # Verificar se a notificação pertence ao usuário atual
    if notificacao.usuario_id == current_user.id:
        # Excluir a notificação do banco de dados
        database.session.delete(notificacao)
        database.session.commit()

        flash('Notificação excluída com sucesso!', 'success')

    return redirect(url_for('notificacoes'))
