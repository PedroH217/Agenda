from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato
# Create your views here.
def login(request):

    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    
    if not usuario or not senha:
        messages.error(request, "Campos não podem estar vazios!")
        return render(request, 'accounts/login.html')
    
    user = auth.authenticate(username=usuario, password=senha)
    
    if not user:
        messages.error(request, 'Usuário ou senha inválidos')
        return render(request, 'accounts/login.html')
    
    else:
        auth.login(request, user)
        return redirect('dashboard')
    
    

def logout(request):
    
    auth.logout(request)
    return render(request, 'accounts/login.html')


def cadastro(request):
    
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')
    
    # Puchando dados de cadastro inseridos pelo usuário
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')
    
    # Verificando se todos os campos estão preenchidos
    if not nome or not sobrenome or not email or not \
            usuario or not senha or not senha2:
        
        messages.error(request, 'Todos os campos devem estar preenchidos')
        
        return render(request, 'accounts/cadastro.html')
    
    # Verificando a validade do email
    try:
        validate_email(email)

    except:
        messages.error(request, 'E-mail inválido' )
        return render(request, 'accounts/cadastro.html')
    
    # Verificando tamanho minimo de usuario e senha
    if len(senha) < 6:
        messages.error(request, 'Senha precisa ter 6 ou mais caracteres.')
        return render(request, 'accounts/cadastro.html')
    
    
    if len(usuario) < 6:
        messages.error(request, 'usuário precisa ter 6 ou mais caracteres.')
        return render(request, 'accounts/cadastro.html')
    
    #verificando se senha e senha2 são iguais
    if senha != senha2:
        messages.error(request, 'Senhas não conferem em si')
        
        return render(request, 'accounts/cadastro.html')
    
    
    #Verificando se usuario já existe
    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário já existe')
        
        return render(request, 'accounts/cadastro.html')
    
    #Verificando se o email já existe
    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email já existe')
    
        return render(request, 'accounts/cadastro.html')
 
       
    user = User.objects.create_user(username=usuario, email=email, password=senha,
                                    first_name=nome, last_name=sobrenome)
    
    user.save()
    messages.success(request, 'Cadastro realizado com sucesso. Efetue login.')
    
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    
    if request.method != 'POST':
        form = FormContato()
        
        return render(request, 'accounts/dashboard.html', { 'form' : form })
    
    form = FormContato(request.POST, request.FILES)
    
    
    if not form.is_valid():
        messages.error('Erro ao enviar formulário.')
        form = FormContato(request.POST)
        
        return render(request, 'accounts/dashboard.html', {'form': form})

    
    descricao = request.POST.get('descricao')
    
    if len(descricao) < 5:
        messages.error(request, 'Descrição deve ter mais de 5 caracteres.')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form' : form})
    
    messages.success(request, 'Novo contato adicionado com sucesso.')
    form.save()
    return redirect('dashboard')
    
    