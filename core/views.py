from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect

from .forms import contatoForm, ProdutoModelForm
from .models import Produto

'''a definição (def) na 'views' é justamente para criar a requisição ou o pedido(request)
para o front da aplicação web, aqui conseguimos criar o contexto do que fazer com os dados 
requisitados ou enviados, aqui podemos definir o metodo POST (Função para enviar dados) ja que 
o metodo GET é a primeira função que definimos no projeto pois se trata do que vemos na aplicação  
'''
#retorna a pagina 'index'


def index(request):
    context = {
        'produtos': Produto.objects.all()
    }
    return render(request, 'index.html', context)

#retorna a pagina contato, existe um contexto definido como 'form' que é um formulario
def contato(request):
    form = contatoForm(request.POST or None)

    if str(request.method) =='POST':
        if form.is_valid():
            #instanciou o metodo da classe 'contatoForm' dentro da pagina 'forms.py' chamado de 'send_mail'
            #send-mail é um metodo de instacia porem os dados de instacia são coletados na propria classe dentro de forms.py
            form.send_mail()

            messages.success(request, 'E-mail enviado com sucesso')
            form = contatoForm()
        else:
            messages.error(request, 'Erro ao enviar e-mail')
# a variavel context esta carregando a variavel 'form' declarado logo a cima
    context = {
        'form': form
    }
    return render(request, 'contato.html', context)

def produto(request):
    if str(request.user) !='AnonymousUser': #Verificando se é um usuario autenticado( inscrito no /Admin)
        if str(request.method) == 'POST':
            form = ProdutoModelForm(request.POST, request.FILES)
            if form.is_valid():

                form.save()
                messages.success(request, 'Produto salvo com sucesso!')
                form = ProdutoModelForm()
            else:
                messages.error(request, 'Erro ao salvar o produto')
        else:
            form = ProdutoModelForm()

        context = {
            'form': form
        }
        return render(request, 'produto.html', context)
    else:
        return redirect('index')


